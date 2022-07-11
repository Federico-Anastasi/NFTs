import bpy, hashlib, pprint
import cmath, json, time, numpy
import random as r
import numpy as np
from math import sin, cos, sinh, cosh, pi
from mathutils import Vector

#BASE FUNCTIONS
def calcZ1(x, y, k, n):
    value = cmath.exp(1j*(2*cmath.pi*k/n)) * (cmath.cosh(x+y*1j))**(2/n)
    if ( abs(value.real) < 0.061171462611008 and abs(value.imag) < 0.061171462611008 ):
        value = 0 + 0j
    return value

def calcZ2(x, y, k, n):
    value = cmath.exp(1j*(2*cmath.pi*k/n)) * (1 / 1j) * (cmath.sinh(x+y*1j))**(2/n)
    if ( abs(value.real) < 0.061171462611008 and abs(value.imag) < 0.061171462611008 ):
        value = 0 + 0j
    return value

def calcZ1Real(x, y, k, n):
    return (calcZ1(x, y, k, n)).real

def calcZ2Real(x, y, k, n):
    return (calcZ2(x, y, k, n)).real

def calcZ(x, y, k1_, k2_, n1_, n2_, a_):
    scale_a = 1
    z1 = calcZ1(x, y, k1, n1_)
    z2 = calcZ2(x, y, k2, n2_)
    return z1.imag * cos(a_/scale_a) + z2.imag*sin(a_/scale_a)

#METADATA STANDARD
metadata = {
    "id": 0,
    "Name": "name",
    "DNA": "datahash",
    "n1": 2,
    "n2": 2,
    "Random angle": 0,
    "Random Texture": 0,
    "Random RGB": 0,
    "Random noise": 0,
    "Scarcity": 0,
    "dev": {
        "rend_mode": "Cycles 64 256 22",
        "res": "1920x1920",
        "dim": 0
    }
}

#INITIAL TIME
t0=time.time()
seed=0000

#QUALITY
dim = 101
video_mode = False
md_dev = metadata["dev"]
md_dev["dim"] = dim

#PARAMS
N_min = 3
N_max = 16
mat_max = 6
created=(N_max-N_min)*(N_max-N_min)*mat_max
color_index = 0
index_list = []
metadata_F_PATH = ""
images_F_PATH = ""


#TEX SELECTION
tmp_1 = 0
tmp_2 = 0 
tmp_3 = 0
tmp_4 = 0 
tmp_5 = 0
go = True
prob=[]
weigth = [1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5]
rgb = [1,2,3,4,5,6]
len_wei = len(weigth)
tot_wei = sum(weigth)

for i in range(0,len_wei):
    prob.append(weigth[i]/tot_wei)

for i in range(0,1014):
    index_list.append(i+1)
    

#TEX SELECTION
def tex_selection():
    global weigth, len_wei, prob, go, tmp_1, tmp_2,tmp_3,tmp_4,tmp_5
    scar_rate = 0
    partial=0
    to_find=True
    rand = r.random()  
    
    for i in range(0,len_wei):
        condition = tmp_1 != weigth[len_wei-1-i] and tmp_2 != weigth[len_wei-1-i] and tmp_3 != weigth[len_wei-1-i] and tmp_4 != weigth[len_wei-1-i] and tmp_5 != weigth[len_wei-1-i]
        if(rand < prob[i]+partial):
            if(to_find):
                if(condition):
                    scar_rate = weigth[len_wei-1-i]
                    to_find=False
                    go = False
                    if tmp_1==0:
                        tmp_1=scar_rate
                    else:
                        if tmp_2==0:
                            tmp_2=scar_rate
                        else:
                            if tmp_3==0:
                                tmp_3=scar_rate
                            else:
                                if tmp_4==0:
                                    tmp_4=scar_rate
                                else:
                                    tmp_5=scar_rate           
        else:
            partial+=prob[i]
    
    return scar_rate

#MATERIAL IMAGE
material_I = bpy.data.materials.new(name='material_I')
material_I.use_nodes = True
mat_nodes_I = material_I.node_tree.nodes
mat_links_I = material_I.node_tree.links
princ_BSDF_I = mat_nodes_I['Principled BSDF']
princ_BSDF_I.inputs[4].default_value = 0.5
image_tex = mat_nodes_I.new('ShaderNodeTexImage')
image_tex.projection ='FLAT'
image_tex.interpolation ='Smart'
noise_tex_I = mat_nodes_I.new('ShaderNodeTexNoise')
combine_tex_I = mat_nodes_I.new('ShaderNodeCombineRGB')
separate_tex_I = mat_nodes_I.new('ShaderNodeSeparateRGB')
mat_links_I.new(noise_tex_I.outputs['Color'],image_tex.inputs['Vector'])
mat_links_I.new(image_tex.outputs['Color'],separate_tex_I.inputs['Image'])
mat_links_I.new(combine_tex_I.outputs['Image'],princ_BSDF_I.inputs['Base Color'])
s_red = separate_tex_I.outputs[0]
s_green = separate_tex_I.outputs[1]
s_blue = separate_tex_I.outputs[2]
c_red = combine_tex_I.inputs[0]
c_green = combine_tex_I.inputs[1]
c_blue = combine_tex_I.inputs[2]

#RANGE
x = np.linspace(0, pi/2, dim)
y = np.linspace(-pi/2, pi/2, dim)
x, y = np.meshgrid(x, y)

#INIT RANDOM
r.seed(a=seed)

for n1 in range(N_min,N_max):
    for n2 in range(N_min,N_max):
        tmp_1 = 0
        tmp_2 = 0 
        tmp_3 = 0
        tmp_4 = 0 
        tmp_5 = 0
        for mat in range(0,mat_max): 
            tp0=time.time()
            color_index +=1
            
            ### RANDOM ### ANGLE SELECTION
            angle_r = ( (pi/8) + r.random()*(pi/4) ) % (pi/4)
            a_radian = angle_r

################################# START #################################

            #INIT MESH DATA
            verts = [[]]
            edges = [[]]
            edge_set = []
            faces = [[]]
            face_set = []

            #BUILD
            for i in range(n1*n2):
                edge_set.append(set())
                face_set.append(set())

            count = 0
            for k1 in range(n1):
                for k2 in range(n2):
                    # calc X, Y, Z values
                    X = np.frompyfunc(calcZ1Real, 4, 1)(x, y, k1, n1).astype('float32')
                    Y = np.frompyfunc(calcZ2Real, 4, 1)(x, y, k2, n2).astype('float32')
                    Z = np.frompyfunc(calcZ, 7, 1)(x, y, k1, k2, n1, n2, a_radian).astype('float32')

                    X_ = X.flatten()
                    Y_ = Y.flatten()
                    Z_ = Z.flatten()
                    
                    v = []
                    for x1, y1, z1 in zip(X_, Y_, Z_):
                        v.append(((float(x1), float(y1), float(z1))))
                    verts[0].extend(v)
                        
                    for i in range(dim * dim):
                        y_index = i / dim
                        x_index = i % dim
                        j = i + count * dim * dim
                        if (y_index < dim - 1) and (x_index < dim - 1):
                            edge_set[count].add(tuple(sorted([j, j+dim])))
                            edge_set[count].add(tuple(sorted([j+dim, j+dim+1])))
                            edge_set[count].add(tuple(sorted([j+dim+1, j+1])))
                            edge_set[count].add(tuple(sorted([j+1, j])))
                            face_set[count].add(tuple(([j, j+dim, j+dim+1, j+1])))
                    
                    count += 1

            for i in range(n1*n2):
                edges[0].extend(list(edge_set[i]))
                faces[0].extend(list(face_set[i]))
            
################################# END #################################

            #MESH & SMOOTH
            mymesh = bpy.data.meshes.new("Fermat-Surface")
            myobject = bpy.data.objects.new("Fermat-Surface",mymesh)
            bpy.context.collection.objects.link(myobject)
            mymesh.from_pydata(verts[0],edges[0],faces[0])
            n_poly = len(myobject.data.polygons)
            for i in range(n_poly):
                myobject.data.polygons[i].use_smooth = True
         
            #DEL
            del(edge_set)
            del(face_set)
            del(verts)
            del(edges)
            del(faces)
            print("Memory cleaned")

            #ROTATION
            frame_number = 0
            for i in range(0,360):
                angle = i*(2*pi/360)
                
                bpy.context.scene.frame_set(frame_number)
                myobject.rotation_euler[2] = angle
                myobject.keyframe_insert(data_path="rotation_euler",index = -1)
                frame_number += 1
                
            ########################   MATERIAL   ########################              
            
            #TEX SELECTION
            go = True
            while(go):
                scar_rate = tex_selection()

            #SEPARATE AND COMBINE RGB
            rand = r.choice(rgb)
            if ( rand == 1 ):
                mat_links_I.new(s_red,c_red)
                mat_links_I.new(s_green,c_green)
                mat_links_I.new(s_blue,c_blue)

            if ( rand == 2 ):
                mat_links_I.new(s_red,c_green)
                mat_links_I.new(s_green,c_red)
                mat_links_I.new(s_blue,c_blue)

            if ( rand == 3 ):
                mat_links_I.new(s_red,c_blue)
                mat_links_I.new(s_green,c_green)
                mat_links_I.new(s_blue,c_red)

            if ( rand == 4 ):
                mat_links_I.new(s_red,c_red)
                mat_links_I.new(s_green,c_blue)
                mat_links_I.new(s_blue,c_green)
            
            if ( rand == 5 ):
                mat_links_I.new(s_red,c_blue)
                mat_links_I.new(s_green,c_red)
                mat_links_I.new(s_blue,c_green)
            
            if ( rand == 6 ):
                mat_links_I.new(s_red,c_green)
                mat_links_I.new(s_green,c_blue)
                mat_links_I.new(s_blue,c_red)
            

            #TEX CORR
            for i in range(0,len_wei):
                if scar_rate == weigth[i]:
                    tex_name = i+1
                
            
            #APPLY TEXTURE & RANDOM NOISE
            myobject.data.materials.append(material_I)
            random_noise = 0.5 + 3.5*r.random()
            noise_tex_I.inputs[2].default_value = random_noise
            image_tex.image = bpy.data.images.load("...{}.jpg".format(tex_name))

            
            #SCARCITY RATING
            scarcity = scar_rate + 1 
            if(n1==n2):
                scarcity+=12               

            #ID CHOICE
            id = r.choice(index_list)
            for i in range(0,len(index_list)):
                if (id == index_list[i]):
                    to_del=i
            del index_list[to_del]

            #DNA
            string_name =  str(id) + str(n1) + str(n2) + str(scar_rate) + str(rand) + "secret key word"
            data_hash = hashlib.sha256(string_name.encode('ascii')).hexdigest()
            
            #SAVE METADATA 
            metadata["id"] = id            
            metadata["Name"] = "Fermat-Surface {}{}{}{}".format(n1,n2,tex_name,rand)
            metadata["DNA"] = str(data_hash)
            metadata["n1"] = n1
            metadata["n2"] = n2
            metadata["Random angle"] = angle_r
            metadata["Random Texture"] = tex_name
            metadata["Random RGB"] = rand
            metadata["Random noise"] = random_noise
            metadata["Scarcity"] = scarcity
            file_name = str(n1) + str(n2) +str(tex_name) + str(rand)
            string = metadata_F_PATH + "{}_{}_metadata.json".format(id,file_name)
            f = open(string,'w')
            json.dump(metadata,f,indent=4)
            f.close()
            
            #CONSOLE LOG
            print("Number: {}/{}".format(color_index,created))
            pprint.pprint(metadata)
            
            #RENDER
            scene = bpy.context.scene
            string = images_F_PATH + "{}_{}_Fermat".format(id,file_name)
            scene.render.filepath = string                
            bpy.ops.render.render(animation=video_mode,write_still=True)

            #CONSOLE LOG
            print("Completed!")
            tp1=time.time()
            dt=(tp1-tp0)/60
            print("Partial time: {}".format(dt))
                
            #DEL RENDERED SPACE
            bpy.data.objects.remove(scene.objects['Fermat-Surface'],do_unlink=True)
            

#CONSOLE LOG
t1=time.time()
dt=(t1-t0)/60
print("Created {} with dim {} in: {} min".format(created,dim,dt))
