from contextlib import redirect_stderr
from svg_turtle import SvgTurtle
import random, json, hashlib, matplotlib, math, colorsys
import matplotlib.pyplot as plt

"""
Dev LOVET ADDRESS = ""
NFT_ADDRESS: ""
METADATA STANDARD CID=""
IMG CID = ""
RANDOM SEED: 
"""

SCALE = 500
SIZE = 1000
MAX_SUPPLY = 1024
DOT_SIZE_MIN = 2
DOT_SIZE_MAX = 75
LINE_SIZE_MIN = 2
LINE_SIZE_MAX = 10
SIDE_SIZE_MIN = 10
SIDE_SIZE_MAX = 150
CID = ""
DEV_ADDRESS = ""
SELLER_FEE = 750 #Indicates a 7,5% seller fee.
set_1 = True
set_2 = True
set_3 = True
index_list = []
type = ""
area = 0
area_data =[]
random.seed(0000)

#color type
def color_folder(rgb_color):
    h = colorsys.rgb_to_hsv(rgb_color[0],rgb_color[1],rgb_color[2])[0]*360
    s = colorsys.rgb_to_hsv(rgb_color[0],rgb_color[1],rgb_color[2])[1]
    v = colorsys.rgb_to_hsv(rgb_color[0],rgb_color[1],rgb_color[2])[2]

    #black or gray
    if(v<0.1 or (s<0.15 and 0.1<v<0.65 )):
        return "black"
    #white
    if( s<0.15 and v>0.65 ):
        return "white"
    #red
    if( (h<11 or h>351) and s>0.7 and v>0.1):
        return "red"
    #pink
    if( ((h<11 or h>351) and s<0.7 and v>0.1) or 310<h<351 and s>0.15 and v>0.1):
        return "pink"
    #orange
    if(11<h<45 and s>0.15 and v>0.75):
        return "orange"
    #brown
    if(11<h<45 and s>0.15 and 0.1<v<0.75):
        return "brown"
    #yellow
    if(45<h<64 and s>0.15 and v>0.1):
        return "yellow"
    #green
    if(64<h<150 and s>0.15 and v>0.1):
        return "green"
    #blue_green
    if(150<h<180 and s>0.15 and v>0.1):
        return "blue_green"
    #purple
    if(255<h<310 and s>0.5 and v>0.1):
        return "purple"
    #blue
    if( 180<h<255 and s>0.15 and v>0.1 ):
        return "blue"
    return "other"


metadata = {
    "id": 1,
    "name": "#1",
    "description": "The DNA of this $LOVET is: ",
    "image": "ipfs://{}/1.svg".format(CID),
    "external_url": "https://0xlovet.com", 
    "seller_fee_basis_points": SELLER_FEE,
    "fee_recipient": "{}".format(DEV_ADDRESS), # Where seller fees will be paid to.
    "attributes":
                [
                    {
                        "trait_type": "Type",
                        "value": "Dot+Line"
                    },
                    {
                        "trait_type": "Background",
                        "value": "#ffffff"
                    },
                    {
                        "trait_type": "Area",
                        "value": 4
                    }
                ]
}


def random_xy():
    a = SCALE*(-1 + 2*random.random())
    b = SCALE*(-1 + 2*random.random())
    return a,b

def rgb():
    r = random.random()
    b = random.random()
    g = random.random()
    return r, b, g

def rgb_to_hex(color):
  return matplotlib.colors.to_hex(color)

def background(bob):
    color = rgb()
    bob.fillcolor(color)
    bob.goto(-SIZE/2 - 10,SIZE/2 + 10)
    bob.begin_fill()
    for j in range(4):
        bob.forward(SIZE + 10)
        bob.right(90)
    bob.end_fill()

    return color

def draw_dot(bob):
    size = random.randint(DOT_SIZE_MIN, DOT_SIZE_MAX)
    bob.dot(size,rgb())
    area = math.pi*(size/2)**2
    return area

def draw_line(bob):
    a = random_xy()
    b = random_xy()
    bob.goto(a)
    size = random.randint(LINE_SIZE_MIN, LINE_SIZE_MAX)
    bob.pendown()
    bob.pensize(size)
    bob.color(rgb())
    bob.goto(b)

    area = size*math.sqrt( (a[0] - b[0])**2 + (a[1] - b[1])**2 )
    return area

def draw_triangle(bob):
    size = random.randint(SIDE_SIZE_MIN, SIDE_SIZE_MAX)
    bob.fillcolor(rgb())
    bob.begin_fill()
    phase = random.randint(0,359)
    bob.right(phase)
    for k in range(3):
        bob.forward(size)
        bob.right(120)
    bob.end_fill()

    area = (math.sqrt(3)/4)*size**2
    return area

#init index_list
for i in range(0,MAX_SUPPLY):
    index_list.append(i+1)


for i in range(MAX_SUPPLY):

    bob = SvgTurtle(SIZE,SIZE)
    bob.speed(0)
    bob.hideturtle()
    bob.setpos(0, 0)
    area=0

    #Draw background
    color = background(bob)

    #number of figures
    n = random.randint(1,100)

    if i > MAX_SUPPLY/4 - 1:
        set_1 = False
    if i > MAX_SUPPLY/2 - 1:
        set_2 = False
    if i > MAX_SUPPLY*(3/4) - 1:
        set_3 = False

    for j in range(n):

        if set_1:
            #Random move
            bob.penup()
            bob.goto(random_xy())
            #Dot
            area += draw_dot(bob)

            #Random move (inside)
            bob.penup()
            #Line
            area += draw_line(bob)
            
            #metadata
            type = "Dot+Line"
        else:
            if set_2:
                #Random move
                bob.penup()
                bob.goto(random_xy())
                #Dot
                area += draw_dot(bob)

                #Random move
                bob.penup()
                bob.goto(random_xy())
                #Triangle
                area += draw_triangle(bob)

                #metadata
                type = "Dot+Triangle"
            else:
                if set_3:
                    #Random move (inside)
                    bob.penup()
                    #Line
                    area += draw_line(bob)

                    #Random move
                    bob.penup()
                    bob.goto(random_xy())
                    #Triangle
                    area += draw_triangle(bob)

                    #metadata
                    type = "Line+Triangle"
                else:
                    #Random move
                    bob.penup()
                    bob.goto(random_xy())
                    #Dot
                    area += draw_dot(bob)

                    #Random move (inside)
                    bob.penup()
                    #Line
                    area += draw_line(bob)

                    #Random move
                    bob.penup()
                    bob.goto(random_xy())
                    #Triangle
                    area += draw_triangle(bob)

                    #metadata
                    type = "Dot+Line+Triangle"
   
                    

    #Random Id
    id = random.choice(index_list)
    for i in range(0,len(index_list)):
        if (id == index_list[i]):
            to_del=i
    del index_list[to_del]

    #Save as svg in color folders
    color_type = color_folder(color)
    filename_svg = ".../{}/{}.svg".format(color_type,id)
    bob.save_as(filename_svg)

    #Save as svg 
    bob.save_as(".../{}.svg".format(id))


    #hash256
    file = open(filename_svg,"rb")
    bytes = file.read()
    hash = hashlib.sha256(bytes).hexdigest()

    #metadata save
    metadata["id"] = str(id)
    metadata["name"] = "#{}".format(id)
    metadata["description"] = "The DNA of this $LOVET is: {}".format(hash)
    metadata["image"] = "ipfs://"+ CID +"/{}.svg".format(id)
    metadata["attributes"][0]["value"] = "{}".format(type) #Type
    metadata["attributes"][1]["value"] = "{}".format(rgb_to_hex(color)) #Background
    metadata["attributes"][2]["value"] = round(area)  #Area
    string =  ".../{}.json".format(id)
    f = open(string,'w')
    json.dump(metadata,f,indent=4)
    f.close()

    #data
    data = open("data.txt",'a')
    data.write(str(round(area)) + ", ")
    data.close
        






