# (C) Sam Bernstein 9/28/2014
# group Ben, Sam and Daniel


from visual import *
from visual.graph import *



rocket_done = False
rocket2_done = False

finished = False

# simulations screen
screen = display(x = 0, width = 500, height = 500, center = (0,3,0), title = "Air Resistance and Projectile Motion")


###
floor = box(length=20, width=1, height=0.5)

r = 1
rocket = sphere(color=color.white, pos = (-floor.length/2,floor.height/2 + r,0), radius = r)
rocket2 = sphere(color=color.red, pos = (-floor.length/2,floor.height/2 + r ,0), radius = r)

rocket_init_pos = rocket.pos  # for resetting and calculating range
rocket2_init_pos = rocket2.pos # for resetting and calculating range

# EDITABLE PARAMETERS #
b = -3 # air resistance constant
g = vector (0,-9.8,0) # gravitational constant


rocket.v = vector(10,10,0)
rocket2.v = rocket.v
rocket.airresistance = b*rocket.v 
#----------------------------------


rocket.trail = curve (color = rocket.color)
rocket2.trail = curve (color = rocket2.color)




# add distance mark_xers
marker_font = .5
mark = {}
divisions = 10
for n in range(0, divisions + 1):
    mark[n] = box(length = floor.length/50, height = floor.height*1.1, width = floor.width, pos = (-floor.length*.5 + n*floor.length/divisions, -.5*floor.height, 1), color = color.red) 
    text(text=(str(n*floor.length/divisions)), pos = (mark[n].x - marker_font, mark[n].y - floor.height*1.5, mark[n].z), height = marker_font, color = mark[n].color)
    print "mark ", n

## simulation data objects
data_air = []
point_air = {}
data = []
point = {}

## set up graph window
point_r = .7

angle_list = [2*n for n in range(0,91)]
speed_list = [s*2 for s in range(0,32)]

graph = display(x = screen.width + 10, width = 800, height = 800, center = (40,30,20), title = "angle and V vs. range")

width = 1
## angle
x_axis = arrow(axis = (1,0,0), length = 90, shaftwidth = width, color = color.red)
# make angle tick marks
marker_font = 13
mark_x = {}
divisions = 6
for n in range(0, divisions + 1):
    mark_x[n] = box(length = floor.length/50, height = floor.height*1.1, width = floor.width, pos = (n*x_axis.length/divisions, -.5*floor.height, -4), color = color.green) 
    label(text=(str(n*90/divisions)), pos = (mark_x[n].x, mark_x[n].y - floor.height*1.5, mark_x[n].z), height = marker_font, color = mark_x[n].color)
    
# launch speed
z_axis = arrow(axis = (0,0,1), length = 90, shaftwidth = width, color = color.red)
# range
y_axis = arrow(axis = (0,1,0), length = 50, shaftwidth = width, color = color.red)


dt =.01
t = 0
n = 0

print 

for s in speed_list:

##    print 'Speed: ', s
    for a in angle_list:
        screen.select()
        rocket_done, rocket2_done = False, False

        rocket.pos = rocket_init_pos
        rocket2.pos = rocket2_init_pos
        
        rocket.v.x = s*math.cos(math.radians(a))
        rocket.v.y = s*math.sin(math.radians(a))
        rocket2.v.x = s*math.cos(math.radians(a))
        rocket2.v.y = s*math.sin(math.radians(a))
        t = 0
        while not(rocket_done and rocket2_done):
            rate(10000)

            rocket.airresistance = b*mag2(rocket.v)*norm(rocket.v)
            
            rocket.pos = rocket.pos + (rocket.v)*dt
            rocket.v = rocket.v + g*dt
            rocket.v = rocket.v + (rocket.airresistance)*dt
            if rocket.y - rocket.radius <= floor.height/2 - 1:
                rocket.v = 0*rocket.v
                rocket_done = True
                
                
            rocket2.pos = rocket2.pos + (rocket2.v)*dt
            rocket2.v = rocket2.v + g*dt
            if rocket2.y - rocket2.radius <= floor.height/2 - 1:
                rocket2.v = 0*rocket.v
                rocket2_done = True

            rocket.trail.append(pos=rocket.pos)
            rocket2.trail.append(pos=rocket2.pos)

            t = t + dt

        

        displacement_air = rocket.pos.x + floor.length/2
        displacement = rocket2.pos.x + floor.length/2
##        print displacement
        graph.select()
        
        # graph scaling factors for independent variables
        s_graph = 1*s
        a_graph = .5*a
        k = .1
        
        # graphing for rocket with air resistance
        data_air.append(vector(a_graph, k*displacement_air, s_graph) ) 
        point_air[n] = sphere(color=color.cyan, pos = data_air[n], radius = point_r)

        # graphing for rocket in vacuum 
        data.append(vector(a_graph, k*displacement, s_graph) ) 
##        point[n] = sphere(color=color.gray(1),opacity = .2, pos = data[n], radius = point_r)
        n +=1
            
    ##        print "running: ", t

    ##        graph1.plot (pos = (t, rocket.v.x, rocket.v.y))
    ##     #   graph2.plot (pos = (t, rocket.v.y))
    ##        graph3.plot (pos = (t, rocket2.v.x, rocket2.v.y))
    ##     #   graph4.plot (pos = (t, rocket2.v.y))

print "done with plotting"

n=1
while n < 1000000000:
    rate(1000)
    n+=1

print "out of viewing loop"


