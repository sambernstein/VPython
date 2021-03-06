# (C) Sam Bernstein 9/28/2014
# group Ben, Sam and Daniel

from visual import *
from visual.graph import *
from visual.controls import * # for controls window
import csv
from types import *

##from sympy import * # this is for the calculus

def setvel(obj): # called on slider drag events
    if obj == Vx:
        ball.velocity.x = obj.value
        ball2.velocity.x = obj.value
    if obj == Vy:
        ball.velocity.y = obj.value
        ball2.velocity.y = obj.value
        
def startitnow(): # Called by controls when button clicked
    print "button clicked"
    if start.text == 'Start':
        global startit
        startit = True
        start.text = 'Running'
    else:
        start.text = 'Start'

def enditnow(): # Called by controls when button clicked
    print "Ended"
    if start.text == 'End':
        global finished
        finished = True
        start.text = 'Ended'

def change():
    if start.text == 'Start':
        start.text = 'Running'
    else:
        start.text = 'Start'

def tprint(string = "\n", *argv): # accepts as many arguments as specified, and prints them all if console = True
    global console
    string = str(string)
    if console:
        print string,
        for arg in argv:
             arg = str(arg)
             print arg
##        print "\n"
        
# used for inputting data from excel
def csv_print(string = "\n", *argv): # accepts as many arguments as specified, and prints them all if csv_input_console = True
    global csv_input_console
    string = str(string)
    if csv_input_console:
        print string,
        for arg in argv:
             arg = str(arg)
             print arg
##        print "\n"


def return_angle_list(filepath = "//Users/samebernstein/Desktop/Lab 3 - Rocket Launch Modeling/exp_data.csv"):
    global raw_data
    
    f = csv.reader(open(filepath, "rU"), dialect=csv.excel_tab)

    n = 0
    for row in f:
        if n != 0:   
            raw_data.append(row) # adds each row of data to list
        n +=1

    for row in raw_data:         
         raw_data[raw_data.index(row)] = str(row) # converts row lists to strings

    angle_found = []
    notch_found = []
    range_found = []

    tprint()
    for row in raw_data: # raw string of value

        first = False
        second = False # reset for new row, because new row not yet cleaned up
        comma_count = 0
        end_angle = 0
        
        for char in range(len(row)): # just the indices

    ##        raw_data[raw_data.index(row)][(raw_data.index(row)).index(char)] = str(raw_data[raw_data.index(row)][(raw_data.index(row)).index(char)])

    ##        csv_print type(char)
            if row[char] == ',': # if character is a comma
                comma_count +=1
                csv_print("Found comma")
                
            if comma_count == 1 and not first:
                 csv_print("Assigning first value.")
                 angle_found.append(int(row[2:char]))
                 end_angle = char + 1
                 first = True
                 
            if comma_count == 2 and not second:
                 csv_print("Assigning second value.")
                 notch_found.append(int(row[end_angle:char]))
                 second = True

                 if char+1 != len(row)-2:
                      range_found.append(float(row[char+1:len(row)-2]))
                 else:
                      range_found.append(float(-1))
                 break
        csv_print()
        csv_print(angle_found[raw_data.index(row)])
        csv_print(notch_found[raw_data.index(row)])
        csv_print(range_found[raw_data.index(row)])

    csv_print(angle_found)
    csv_print(notch_found)

    return sorted(list(set(angle_found)))

def return_notch_list(filepath = "//Users/samebernstein/Desktop/Lab 3 -  Rocket Launch Modeling/exp_data.csv"):
    global raw_data
    
    f = csv.reader(open(filepath, "rU"), dialect=csv.excel_tab)

    n = 0
    for row in f:
        if n != 0:   
            raw_data.append(row) # adds each row of data to list
        n +=1

    for row in raw_data:         
         raw_data[raw_data.index(row)] = str(row) # converts row lists to strings

    angle_found = []
    notch_found = []
    range_found = []

    tprint()
    for row in raw_data: # raw string of value

        first = False
        second = False # reset for new row, because new row not yet cleaned up
        comma_count = 0
        end_angle = 0
        
        for char in range(len(row)): # just the indices

    ##        raw_data[raw_data.index(row)][(raw_data.index(row)).index(char)] = str(raw_data[raw_data.index(row)][(raw_data.index(row)).index(char)])

    ##        csv_print type(char)
            if row[char] == ',': # if character is a comma
                comma_count +=1
                csv_print("Found comma")
                
            if comma_count == 1 and not first:
                 csv_print("Assigning first value.")
                 angle_found.append(int(row[2:char]))
                 end_angle = char + 1
                 first = True
                 
            if comma_count == 2 and not second:
                 csv_print("Assigning second value.")
                 notch_found.append(int(row[end_angle:char]))
                 second = True

                 if char+1 != len(row)-2:
                      range_found.append(float(row[char+1:len(row)-2]))
                 else:
                      range_found.append(float(-1))
                 break
        csv_print()
        csv_print(angle_found[raw_data.index(row)])
        csv_print(notch_found[raw_data.index(row)])
        csv_print(range_found[raw_data.index(row)])

    csv_print(angle_found)
    csv_print(notch_found)

    
    return sorted(list(set(notch_found)))

def notch_to_height(notch_list): # returns notch heights in meters for use in calculations
    global start_h # in inches
    global console
    global height_of_first_mark # in inches
    global inches_to_meters
    
    final_notch_height = []
    n = 0
    for notch in notch_list:
        final_notch_height.append(inches_to_meters*float(notch - 1 + height_of_first_mark - start_h)) # this is the vertical height in meters of the notch above the horizontal launch bar
        n+=1
    print
    print "Raw notch height list: ", final_notch_height
    print
    final_notch_height = sorted(final_notch_height)
    print
    print "Sorted notch height list: ", final_notch_height
    print
    csv_print("\n"*2)
    csv_print(final_notch_height)
    csv_print("\n"*2)
    return  final_notch_height

    
def get_exp_data(filepath = "//Users/samebernstein/Desktop/Lab 3 -  Rocket Launch Modeling/exp_data.csv"):
    global raw_data
    global inches_to_meters
    csv_print("-"*30)
    
    angle_notch_pair = {}
    raw_data = []
    
    f = csv.reader(open(filepath, "rU"), dialect=csv.excel_tab)
    
    n = 0
    for row in f:
        if n != 0:   
            raw_data.append(row) # adds each row of data to list
        n +=1
     
    for row in raw_data:         
         raw_data[raw_data.index(row)] = str(row) # converts row lists to strings

    ind_pair = [] # final tuple receptacle for angle, notch pairs to be used as keys in final data dictionary

    angle_found = []
    notch_found = []
    range_found = []

    tprint()
    for row in raw_data: # raw string of value

        first = False
        second = False # reset for new row, because new row not yet cleaned up
        comma_count = 0
        end_angle = 0
        
        for char in range(len(row)): # just the indices

    ##        raw_data[raw_data.index(row)][(raw_data.index(row)).index(char)] = str(raw_data[raw_data.index(row)][(raw_data.index(row)).index(char)])

    ##        csv_print type(char)
            if row[char] == ',': # if character is a comma
                comma_count +=1
                csv_print("Found comma")
                
            if comma_count == 1 and not first:
                 csv_print("Assigning first value.")
                 angle_found.append(int(row[2:char]))
                 end_angle = char + 1
                 first = True
                 
            if comma_count == 2 and not second:
                 csv_print("Assigning second value.")
                 notch_found.append(int(row[end_angle:char]))
                 second = True

                 if char+1 != len(row)-2:
                      range_found.append(inches_to_meters*float(row[char+1:len(row)-2]))
                 else:
                      range_found.append(float(-1))
                 break
        csv_print()
        csv_print(angle_found[raw_data.index(row)])
        csv_print(notch_found[raw_data.index(row)])
        csv_print(range_found[raw_data.index(row)])

    csv_print(angle_found)
    csv_print(notch_found)

    angle_found = sorted(list(set(angle_found)))
    notch_found = sorted(list(set(notch_found)))

    csv_print()
    csv_print("Angle list found: \n", angle_found)
    csv_print("Notch list found: \n", notch_found)
    csv_print()

    t = 1
    for a in angle_found:
         for notch in notch_found:
              ind_pair.append( (a, notch) ) # combine notch list and angle list into pairs for final range keys
              t+=1
    csv_print(t)

    csv_print("\n"*6)

    
    data = {}
    csv_print("len of range: ", len(range_found))
    csv_print( "len of pair: ", len(ind_pair))
    for n in range(len(ind_pair)):
        data[ind_pair[n] ] =  range_found[n]

    csv_print("\n"*2)

    csv_print("Data dictionary length = ", len(data))
    print data # compare this with .csv data, must be the same
    
    csv_print("-"*30)

    return data

    
def riemann_sum(a, b, divisions = 10000): # all ints, defaults at ten thousand divisions
    global L_band
    global k
    global console

    if a == 0: # handle divide by zero error
        a = 0.0001
        
##    print "Riemann started"
    rect = {}
    total = 0

    d_dist = (b-a)/divisions

    dist = a
    
    for n in range(0,divisions):
        rect[n] = (k*(math.sqrt(L_band**2 + dist**2) - L_band)*math.cos(math.atan(L_band/dist)) ) * d_dist # calculate area of slice
        dist += d_dist # move over one interval

##        if console and dist > b:
##            print
##            print "OVER BOUND B by ", dist - b

    for n in range(0,len(rect)): # add up slices
        total += rect[n]

    return total

    

##init_printing(use_unicode=False, wrap_line=False, no_global=True) # sets up sympy stuff
##dist = Symbol('dist') #dist will be used as the variable for integrating the work (W)


# Control flow variables
console = False # if False, console won't update with regular launch info
csv_input_console = False

startit = False
finished = False

rocket_done = False
rocket_under = False

main_rate = 3000
exp_file = "//Users/samebernstein/Desktop/Lab 3 -  Rocket Launch Modeling/exp_data.csv"

# simulations screen
screen = display(x = 0, width = 500, height = 500, center = (0,2,0), title = "Air Resistance and Projectile Motion")

floor = box(length=5, width=1, height=0.5)

##(414.25, -1.15625)
#------------------------------------------------------------------------#
# EDITABLE CONSTANT PARAMETERS #
b = -0.29375 # air resistance constant # THIS WAS FOUND USING MACHINE LEARNING
g = vector (0,-9.8,0) # gravitational constant
k = 214.0 # spring constant of launch setup # THIS WAS FOUND USING MACHINE LEARNING

L = .25 # distance of launcher pad from hinge, in meters - MEASURED

L_bar = .50 # length of bottom launch bar # in meters
L_band = 0.0254*9 # length of each rubber band when unstretched # in meters
L_to_back = 0.56515 #distance to back of bottom bar from which Simon will be measuring to angle changing hinge

m = .05 # mass of the rocket, in kg MEASURE MEASURE MEASURE MEASURE
height_of_first_mark = 6.65 # in inches
start_h = 1 # height between bottom horizontal launch bar and bottom of rubber bands in loaded position ------------MEASURED # in inches
inches_to_meters = 0.0254


# SIMULATION VARIABLES THAT MAY CHANGE #
n = 0
angle_list = [5*a for a in range(1,17)] # 5 degrees to 85 degrees
notch_list = [s for s in range(6,11)]

angle_list = [10*a for a in range(1,8)] # Define list of angles and notch levels for calculating ranges
notch_list = [2*s for s in range(3,5)]


W = 0 # work done by spring
rocket_max = 0 # maximum height of rocket trajectory
rocket_x_initial = 0

v = 0 # this is the the starting speed of rocket (scalar)

h = 0 # height of landing, in meters, used for range prediction
#------------------------------------------------------------------------#



##test = display()
# Variables for setting up rocket #
##rocket_size = 1
#rocket dimensions
##r = 1
##r_h = 1*rocket_size #rocket length
##r_len = 10*rocket_size # rocket radius
##r_thickness = .7*r_h
##
##base_h = rocket_size*1
##base_l = base_h*1.6
##
##disp_x = -.5*r_len
##disp = .5*r_len
##
##
### SETTING UP ROCKET #
##base = Polygon( [(0,disp_x), (0,base_l + disp_x), (base_h,disp_x)] )
##
##shell = shapes.rectangle(pos=(0,0), width= r_h, height=r_len, roundness = 0.2) # height is length
##inside= shapes.rectangle(pos=(0,0), width= r_thickness, height= r_len + 2*base_l) # width is radius
##
####tip = Polygon( [(0,disp), (0,base_l + disp), (base_h,disp)] )
##
##tip = shapes.circle(pos = (0, .5*r_len),radius= .5*r_h, np=64)
##
##p = paths.circle( pos=(0,0,0), radius=.01, up = (1,0,0) )
##rocket = extrusion(pos=p, shape = base + shell + tip - inside, color=color.red)
##
##rocket.pos = (-floor.length/2, floor.height/2 + rocket_size,0)
##print "rocket made"
##
size = .1
rocket_L = .3
real_L = .2
screen.select()

rocket = arrow(length = rocket_L, axis = (1,0,0), pos = (-floor.length/2, floor.height/2,0), color=color.red)

screen.select()
bar_r = .02
bar = cylinder(pos = (-floor.length/2, floor.height/2, 0), axis = (-1*L_bar,0,0), radius = bar_r, color = color.white)
bar_L = cylinder(length = L_bar, radius = bar_r, color = bar.color)
bar_M = cylinder(length = L_bar*1.2, radius = bar_r*.2, color = bar.color)
bar_R = cylinder(length = L_bar, radius = bar_r, color = bar.color)
#--------------------------------------------------------------#

rocket_init_pos = rocket.pos  # for resetting and calculating range

rocket.v = vector(10,10,0)
rocket.airresistance = b*mag2(rocket.v)*norm(rocket.v)
#----------------------------------

# add distance marks
marker_font = floor.length/30
mark = {}
divisions = 5
for n in range(0, divisions + 1):
    mark[n] = box(length = floor.length/50, height = floor.height*1.1, width = floor.width, pos = (-floor.length*.5 + n*floor.length/divisions, -.5*floor.height, 1), color = color.red) 
    text(text=(str(n*floor.length/divisions)), pos = (mark[n].x - marker_font, mark[n].y - floor.height*1.5, mark[n].z), height = marker_font, color = mark[n].color)



## set up graph window----------------------------------------------
point_r = 1 # size of graphing sphere points

graph = display(x = screen.width + 10, width = 800, height = 800, center = (40,30,40), title = "angle and V vs. range")
c = controls(x = screen.x, y = screen.height + 5, width = screen.width, height = 200, title = "Simulation Controls")

graph.select()
width = 1
## angle
x_axis = arrow(axis = (1,0,0), length = 90, shaftwidth = width, color = color.red)
# make angle tick marks
marker_font = 13
mark_x = {}
divisions = 6
for n in range(0, divisions + 1):
    mark_x[n] = box(length = floor.length/50, height = floor.height*1.1, width = floor.width, pos = (n*x_axis.length/divisions, -.3*floor.height, .4*floor.width), color = color.green) 
    label(text=(str(n*90/divisions)), pos = (mark_x[n].x, mark_x[n].y - floor.height*1.5, mark_x[n].z), height = marker_font, color = mark_x[n].color)
    
# launch speed axis
z_axis = arrow(axis = (0,0,1), length = 90, shaftwidth = width, color = color.red)
# range axis
y_axis = arrow(axis = (0,1,0), length = 50, shaftwidth = width, color = color.red)
#-------------------------------------------------------------------


start =  button(pos=(20,0), height=10, width=20, text='Start', action = lambda: startitnow())
stop =  button(pos=(start.pos.x+25,0), height=10, width=20, text='Stop', action = lambda: enditnow())


##screen.waitfor('keydown') # wait for keyboard key press
##scene.waitfor('keyup')   # wait for keyboard key release



##    c.waitfor('click')     # wait for a click    # wait for a click

print "SIM STARTED"


rocket.trail = {}
colors = [color.red, color.yellow, color.green, color.orange, color.white, color.blue, color.cyan, color.magenta]


notch_list = [s for s in range(4,10)]
notch_h = []
angle_list = [5*a for a in range(5,18)] # 5 degrees to 85 degrees

raw_data = []
## simulation data structures
ind_pair = [] # tuple of keys for dictionary
data_sim = {} # dictionary for storing ((angle, notch) : range) data points made by simulation
data_exp = {} # dictionary for experiment data

point_sim = {}
point_exp = {}

diff = {} # for storing differences between experiment points and simulation points


#### Finding best variables 
target_range = 0
target_min = 0
target_max = 0
precision = .1 # what is the tolerance for predicted range

launch_options = {}
option = 0


dt =.0001
t = 0
#--------------------------------------------------START SIMULATION AND CALCULATIONS-------------------------------------------------------#
count = 1
while not finished:
    n = 0
    c = -1

    h = input("Vertical height of castle landing (in meters): ")
    target_range = input("Range to the base of the castle (in meters):")
    meters_to_it = input("Distance from origin to launcher (in meters):")

    target_range += meters_to_it
    
    target_min = (1.0 - .5*precision)*target_range
    target_max = (1.0 + .5*precision)*target_range
    print

    print "k = ", k
    print "b = ", b
    
    print "\n"*2
    tprint("Notch list: " + str(notch_list))
    tprint("Angle list: "+ str(angle_list))


    notch_h = notch_to_height(notch_list)

    tprint("Notch list: " + str(notch_list))
    tprint("Angle list: "+ str(angle_list))
    
    data_exp = get_exp_data(exp_file)


##    angle_list = input("Enter angles: ")
##    notch_list = input("Enter notches: ")
##    notch_h = [s - 1 + 6 - start_h for s in notch_list] # this is the vertical height in meters of the notch above the horizontal launch bar


    print "\n"*3
    print "Notch list: ", notch_list
    print "Notches: ", notch_h
    print "Angles:  ", angle_list
    print
    print "Data points sim:         Data points exp:           Difference (sim - exp):"



    for height in notch_h:
        if finished: break
        
        tprint("Notch height: "+ str(height))
        
        c +=1 # for cycling through trail colors
        if c == 8:
            c = 0

        W = riemann_sum(0, height, 10000)
##        print "W: ", W
        tprint()
        for a in angle_list:
            if finished: break
            screen.select()
            
            tprint()
            
            rocket_done = False # reset variables for breaking out of simulation loop
            
##            W = integrate(k*(sqrt(L_band**2 + dist**2) - L_band)*cos(atan(L_band/dist)), (dist, 0, 1))# find work done by spring on rocket

            
            displacement_air = -1 #if displacement = -1, we know it didn't launch / there was an error
            
            tprint("")
            if W < 0:
                tprint ("Launch "+ str(count)+ " failed. Not enough spring force to launch rocket.")
                rocket_done = True
                v = 0
            else:
                tprint ("Launch "+ str(count) + ":")
                v = math.sqrt((2*W)/m)

            if not rocket_done:
                if finished: break
                beta = 104.9 - a # angle of launch radius to the horizontal
                rocket.x = -floor.length/2 - L*math.cos(math.radians(beta)) # adjust start position backwards depending on angle
                rocket.y = L*math.sin(math.radians(beta)) + floor.height/2

##                sphere(radius=.03, color = color.green, pos = rocket.pos)
                rocket_x_initial = -floor.length/2
                
                
                bar.axis = (-L_bar*math.cos(math.radians(90-a)), L_bar*math.sin(math.radians(90-a)), 0 )
                
                bar_L.axis = (L_bar*math.cos(math.radians(a)), L_bar*math.sin(math.radians(a)), 0 )
                bar_L.pos = (bar.pos.x - L_bar*math.cos(math.radians(90-a)), bar.pos.y + L_bar*math.sin(math.radians(90-a)), 0)

                bar_M.axis = 1.1*bar_L.axis
                bar_M.pos = (bar.pos.x - L_bar*.5*math.cos(math.radians(90-a)), bar.pos.y + L_bar*.5*math.sin(math.radians(90-a)), 0)
                
                bar_R.axis = bar_L.axis
                bar_R.pos = bar.pos
                
                rocket.v.x = v*math.cos(math.radians(a))
                rocket.v.y = v*math.sin(math.radians(a))

                rocket.trail[n] = curve(color = colors[c])
                rocket_under = False
                t = 0
    ##            print "loop STARTED"
                max_reached = False
                while not(rocket_done):
                    rate(10000)

                    rocket.axis = rocket_L*norm(rocket.v)

                    rocket.airresistance = b*mag(rocket.v)*norm(rocket.v) # b*mag2(rocket.v)*norm(rocket.v)
                    
                    rocket.pos = rocket.pos + (rocket.v)*dt
                    rocket.v = rocket.v + g*dt
                    rocket.v = rocket.v + (rocket.airresistance)*dt # rocket with air resistance

                    if rocket.v.y <= 0 and not max_reached:
                        rocket_max = rocket.y
                        max_reached = True
                        
                    # check if bottom of rocket is below landing height and that rocket is on the way down
                    if rocket.y - real_L*math.sin(math.atan(abs(rocket.v.y)/rocket.v.x)) <= floor.height/2 + h and rocket.v.y < 0:
                        rocket.v = 0*rocket.v
                        rocket_done = True
                        if rocket_max < floor.height/2 + h: # if rocket never reached necessary height
                            rocket_under = True

    ##                ball.pos = rocket.pos[0] + vector(0,1,0)
                    
                    rocket.trail[n].append(pos=rocket.pos)
                    t = t + dt
                    
                tprint ("Cycles: " + str(t/dt))

            if rocket_under:
                displacement_air = -1
            else:
                displacement_air = rocket.x - rocket_x_initial

            tprint("Range: " + str(displacement_air))
            graph.select()
            
            # graph scaling factors for independent variables
            h_graph = 4
            a_graph = a
            f = 3

            # this is where all the final interesting and important things happen with the data points
            ind_pair.append( (a, notch_list[notch_h.index(height)]) )

##            print "Ind_pair latest: ", ind_pair[-1]
            
            data_sim[ind_pair[-1]] = displacement_air
            
                           
            print ind_pair[n], data_sim[ind_pair[n]]

            
            point_sim[n] = sphere(color=color.cyan, pos = (a_graph, f*displacement_air, h_graph*notch_list[notch_h.index(height)]), radius = point_r)

            if target_min < data_sim[ind_pair[n]] < target_max:
                launch_options[ind_pair[n]] = data_sim[ind_pair[n]]
                option += 1
                                      
            n +=1
           
            count +=1

    
    print "Done with generating ranges."

    print "\n", "Options:"
    print launch_options

    startit = False
    while not startit:
        rate(100)
    startit = False                         
##    print "Data points sim:         Data points exp:"
##    for key in ind_pair:
##        print key, data_sim[key], "      -      ", key, data_exp[key]
##    print





                # for cycling through data point array
    ##            change()
    ##            while not startit:
    ##                rate(100)
    ##            startit = False
                
        ##        print "running: ", t

        ##        graph1.plot (pos = (t, rocket.v.x, rocket.v.y))
        ##     #   graph2.plot (pos = (t, rocket.v.y))
        ##        graph3.plot (pos = (t, rocket2.v.x, rocket2.v.y))
        ##     #   graph4.plot (pos = (t, rocket2.v.y))

while not startit:
    rate(100)
startit = False

print "-DONE-"


n=1
while n < 1000000:
    rate(100)
    n+=1
    if n%50000 == 0:
        print n


