from visual import *
import time
        
def keyInput(evt):
    global lander
    global thrust_time
    global no_fuel
    global tank_capacity
    global fuel_left
    global fuel_decrease
    global pause
    global try_over
    s = evt.key

    angle_change = 15
    
    if s == 'p':
        pause = not pause
        
    elif not try_over:
        if fuel_left > fuel_decrease*2:
            fuel_left -= fuel_decrease
            if s == 'a' or s == 'left':
                lander.angle += angle_change
            elif s == 'd' or s == 'right':
                lander.angle -= angle_change
            else:
               lander.v += 10*norm(lander.axis)*(tank_capacity/(.8*fuel_left + 2000)) #  make it go up
               fuel_left -= fuel_decrease
               thrust_time = 50 # shows thrust fire for 50 cycles

class Segment(object):
    def __init__(self, start=None, a=None, b=None, platform=None, flag=None):
        self.start = start
        self.a = a
        self.b = b
        self.platform = platform
        self.flag = flag

def surface(a, b, lander_x): # must plug in x-distance of lander from left side of segmeent
    return (a*lander_x + b)  # returns the y value of the lunar surface at the point where the lander is
    
def newLandscape(difficulty):
    global floor
    global landscape
    global start_landscape
    global divisions
    global top_height

    global sectionList


    floor.color = floor.reset_color
    moon.color = moon.reset_color
    
    divisions = 100*(difficulty//40) + 100

    y_upper_bound = 300
    
    scene.select()
    path = [(0,0,.5*floor.width),(0,0,-.5*floor.width)]

    is_platform = False
    platform_choice = 0
    
    old_x = start_landscape
    old_y = 0
    
    new_x = start_landscape
    new_y = 0

    length_choice = 1
    n_secs = 0
    interval = 0
    increment = (floor.length - start_landscape)/divisions
    
    hole = [(.5*floor.length + floor.pos.x, top_height), (start_landscape, top_height), (start_landscape, 0)]

    old_n = 0
    n = 0
    while n < divisions - 1: # create landscape shape to extrude

        length_choice = random.randint(-2, 40//difficulty)
        if length_choice < 2:
            n += 1
            n_secs = 1
        else:
            n += length_choice
            n_secs = length_choice
            
        new_x = old_x + n_secs*increment

        platform_choice = random.randint(0, difficulty + 3)  # determine whether next segment is a platform
        if platform_choice < difficulty:
            is_platform = False
            
            new_y = random.randint(0, y_upper_bound)
            while abs(new_y - old_y) < 15:             # makes sure non-platform segment isn't deceivingly flat
                new_y = random.randint(0, y_upper_bound)

            hole.append((new_x, new_y))
        else:
            is_platform = True
            
            hole.append((new_x, old_y))

        flag_l = 18
        flag_r = 2
        for k in range(n_secs): # for all the new sections added
            sectionList.append(Segment(old_x, (new_y - old_y)/(new_x - old_x), old_y, is_platform)) # add a new data object storing info for that section

            if is_platform:
                if len(sectionList) >= 2:
                    if sectionList[-2].platform: # previous section is a platform
                        if n_secs == 1:
                            flags[-1].visible = False
                            del flags[-1]
                            flags.append(cylinder(radius = flag_r, length = flag_l, pos = (new_x,new_y,0), color = color.red, axis = (0,1,0), opacity = 1))
                        elif k == n_secs - 1:
                            flags[-1].visible = False
                            del flags[-1]
                            flags.append(cylinder(radius = flag_r, length = flag_l, pos = (new_x,new_y,0), color = color.red, axis = (0,1,0), opacity = 1))
                        elif k == 0:
                            flags[-1].visible = False
                            del flags[-1]
                    else:
                        flags.append(cylinder(radius = flag_r, length = flag_l, pos = (old_x,old_y,0), color = color.red, axis = (0,1,0), opacity = 1))
                        flags.append(cylinder(radius = flag_r, length = flag_l, pos = (new_x,new_y,0), color = color.red, axis = (0,1,0), opacity = 1))
                else:
                    flags.append(cylinder(radius = flag_r, length = flag_l, pos = (old_x,old_y,0), color = color.red, axis = (0,1,0), opacity = 1))
                    flags.append(cylinder(radius = flag_r, length = flag_l, pos = (new_x,new_y,0), color = color.red, axis = (0,1,0), opacity = 1))
                
        old_x = new_x  # stores the previous points for calculations in next cycle
        old_y = new_y
        old_n += n_secs
        

    level_zone = shapes.pointlist(pos=[(.5*floor.length + floor.pos.x, top_height), (start_landscape, top_height), (start_landscape, 0), (.5*floor.length + floor.pos.x,0)])
    subtract = shapes.pointlist(pos = hole)
    
    landscape.append(extrusion(pos = path, shape= level_zone - subtract, color = color.gray(.5)))

def deleteLandscape():
    global sectionList
    global divisions
    global flags

    for f in flags:
        f.visible = False
        del f

    while len(sectionList) > 0:
        del sectionList[0]
        
    landscape[0].visible = False
    del landscape[0]

def newStars():
    global earth
    global floor
    global top_height
    global stars
    global level_number
    global num_stars

    crazy_level = 10
    star_colors = [color.blue, color.blue, color.blue, color.yellow, color.yellow]

    for n in range(25):
        star_colors.append(color.white)

    range_x = 2*floor.length
    range_y = 4*top_height
    
    star_x = 0
    star_y = 0
    star_z = 1.2*earth.pos.z
    star_radius = 2
    star_color = 0

    parallax = 800

    s = 0

    if level_number == crazy_level:
        num_stars = .3*num_stars

    if level_number >= crazy_level:
        while s < num_stars:
            
            star_x = random.randint(floor.pos.x - range_x, floor.pos.x + range_x)
            star_y = random.randint(-500, range_y)
            star_z = random.randint(-2*floor.width, 2*floor.width)
            
            star_radius = random.random()*2 + .5

            star_color = star_colors[random.randint(0,len(star_colors)-1)]

            stars.append(sphere(radius = star_radius, pos = (star_x, star_y, star_z), color = star_color,  material = materials.emissive))
            if abs(star_z) < 2*floor.width:
                stars.append(local_light(pos=(star_x, star_y, star_z), color=color.white))

            s+=1
    else:
        while s < num_stars:
            
            star_x = random.randint(floor.pos.x - range_x, floor.pos.x + range_x)
            star_y = random.randint(-500, range_y)
            star_z = 1.5*earth.pos.z + random.randint(-parallax, parallax)

            star_radius = random.random()*2 + .5

            star_color = star_colors[random.randint(0,len(star_colors)-1)]

            stars.append(sphere(radius = star_radius, pos = (star_x, star_y, star_z), color = star_color,  material = materials.emissive))
    ##        stars.append(local_light(pos=(star_x, star_y, star_z), color=color.white))

            s+=1
def deleteStars():
    global stars

    for s in stars:
        s.visible = False
        del s
                    
    
def crash(platform, at_an_angle = False):
    global lander
    global lander_length
    global upright_range
    global sectionList
    global segment_over
    global crash_count
    
    crash_count +=1
    for part in lander.objects:            
        part.color = color.red

    l_pos = lander.pos
    
    crash_time = 5
    turn_speed = 1
    vibration_speed = 5
    
    tip_angle = 35
    turn_to = 1000

    slope = 0
    slope_angle = 0
    
    size = 30
    below = 75
    front_d = 50

    print "lander.angle = ", lander.angle
    if platform:
        
        turn_to = 0
        if abs(90 - lander.angle) < upright_range:
            turn_to = 90
        elif 270 > lander.angle >= 90 + upright_range:
            turn_to = 180
        elif lander.angle <= upright_range:
            turn_to = 0
        else:
            turn_to = 360
        
        while not (turn_to - turn_speed < lander.angle < turn_to + turn_speed):
            rate(100)
            if lander.angle <= turn_to:
                lander.angle += turn_speed
            elif lander.angle > turn_to:
                lander.angle -= turn_speed
                
            lander.axis = (lander_length*math.cos(math.radians(lander.angle)), lander_length*math.sin(math.radians(lander.angle)), 0)

            lander.pos.y = l_pos.y + vibration_speed*math.cos(lander.angle) # for crash vibrations
            lander.pos.x = l_pos.x + vibration_speed*math.cos(1.3*lander.angle)

        if at_an_angle:
            you_crashed = text(text='You crashed into the platform!', align='center', pos = (lander.x, scene.center.y + 150, front_d), height = size, depth=-0.3, color=color.orange)
            advice = text(text='Land straight next time.', align='center', pos = (lander.x, you_crashed.y - below, front_d), height = size, depth=-0.3, color= color.orange)
        else:
            you_crashed = text(text='You crashed into the platform!', align='center', pos = (lander.x, scene.center.y + 150, front_d), height = size, depth=-0.3, color=color.orange)
            advice = text(text='Land slower next time.', align='center', pos = (lander.x, you_crashed.y - below, front_d), height = size, depth=-0.3, color= color.orange)

 
        crash_time *= 1.5
    else:
        slope = sectionList[segment_over].a
        slope_angle = math.degrees(math.atan(slope))

        print "slope_angle = ", slope_angle
        if slope_angle > 0:
            if abs(slope_angle) < tip_angle:
                if abs(90 + slope_angle - lander.angle) <= upright_range: # crash perpendicular to surface
                    turn_to = 90 + slope_angle
                elif lander.angle < 90 + slope_angle - upright_range:
                    turn_to = slope_angle
                elif slope_angle + 90 + upright_range < lander.angle < slope_angle + 90 + 180:
                    turn_to = slope_angle + 180
                else:
                    turn_to = slope_angle + 360 # if the shortest direction to the angle is through the 360 to 0 degree jump

            else: # if at a steeper angle
                if lander.angle <= 90 + slope_angle:
                    turn_to = slope_angle        # go to right side
                elif 90 + slope_angle < lander.angle < slope_angle + 90 + 180: 
                    turn_to = slope_angle + 180  # go to left side
                else:
                    turn_to = slope_angle + 360 # if the shortest direction to the angle is through the 360 to 0 degree jump
        else:
            if abs(slope_angle) < tip_angle:
                if abs(90 + slope_angle - lander.angle) <= upright_range: # crash perpendicular to surface
                    turn_to = 90 + slope_angle
                elif lander.angle < 90 + slope_angle - upright_range:
                    turn_to = slope_angle
                elif slope_angle + 90 + upright_range < lander.angle < slope_angle + 90 + 180:
                    turn_to = slope_angle + 180
                else:
                    turn_to = slope_angle + 360 # if the shortest direction to the angle is through the 360 to 0 degree jump

            else: # if at a steeper angle
                if lander.angle <= 90 + slope_angle:
                    turn_to = slope_angle        # go to right side
                elif 90 + slope_angle < lander.angle < slope_angle + 90 + 180: 
                    turn_to = slope_angle + 180  # go to left side
                else:
                    turn_to = slope_angle + 360 # if the shortest direction to the angle is through the 360 to 0 degree jump

        print "turn_to = ", turn_to
        while not (turn_to - turn_speed < lander.angle < turn_to + turn_speed):
            rate(100)
            if lander.angle <= turn_to:
                lander.angle += turn_speed
            elif lander.angle > turn_to:
                lander.angle -= turn_speed
                
            lander.axis = (lander_length*math.cos(math.radians(lander.angle)), lander_length*math.sin(math.radians(lander.angle)), 0)

            lander.pos.y = l_pos.y + vibration_speed*math.cos(lander.angle) # for crash vibrations
            lander.pos.x = l_pos.x + vibration_speed*math.cos(1.3*lander.angle)
            
        you_crashed = text(text='You crashed!', align='center', pos = (lander.x, scene.center.y + 150, front_d), height = size, depth=-0.3, color=color.red)
        advice = text(text="Don't do that!", align='center', pos = (lander.x, you_crashed.y - below, front_d), height = size, depth=-0.3, color=color.red)



    if lander.angle < 0:
        lander.angle = lander.angle + 360
    elif lander.angle > 360:
        lander.angle = lander.angle - 360

    wait(30*crash_time)

    print
    
##            
##    for c in range(10):
##        for part in lander.objects:            
##            part.color = color.red
##        wait(flicker)
##        for part in lander.objects:
##            part.color = color.orange
##        wait(flicker)
    
    advice.visible = False
    del advice
    
    you_crashed.visible = False
    del you_crashed
    
def land():
    global lander
    global fire
    global level_number
    global earth
    global crash_count

    crash_count = 0

    fire.visible = False

    turn_to = 90
    turn_speed = 1

    while not (turn_to - turn_speed < lander.angle < turn_to + turn_speed):
        rate(100)
        if lander.angle <= turn_to:
            lander.angle += turn_speed
        elif lander.angle > turn_to:
            lander.angle -= turn_speed
            
        lander.axis = (lander_length*math.cos(math.radians(lander.angle)), lander_length*math.sin(math.radians(lander.angle)), 0)
    
    won_size = 40
    front_d = 50
    you_won = text(text='You won!', align='center', pos = (lander.x, scene.center.y + 100, front_d), height = won_size, depth=-0.3, color=color.yellow)

    if level_number % 10 == 0:
        you_won.height += .5*you_won.height
        for n in range(6):
            for c in colors:
                rate(100)
                for part in lander.objects:
                    rate(100)
                    part.color = c
                moon.color = c
                floor.color = c
                landscape[0].color = c
                
                wait(4, True)
                
    elif level_number % 5 == 0:
        you_won.height += .5*you_won.height
        for n in range(6):
            for c in colors:
                for part in lander.objects:
                    part.color = c
                you_won.color = c
                wait(4)
    else:
        for n in range(6):
            for c in colors:
                for part in lander.objects:
                    part.color = c
                wait(4)
            
    you_won.visible = False
    del you_won
    
def resetLander():
    global lander
    global fuel_left
    global no_fuel
    global difficulty

    tank.visible = True

    fuel_factor = 50
    if fuel_factor*difficulty > .6*tank_capacity:
        fuel_left = .4*tank_capacity
    else:
        fuel_left = tank_capacity - fuel_factor*difficulty

    for part in lander.objects:
        part.color = part.reset_color

def newHeart():
    global dash
    dash.select()
    size = 20
    depth = 10
    h_color = color.red
    d_axis = (1,1,0)
    c_axis = (0,0,depth)
    
    heart = frame()

    diamond = box(frame = heart, length = size, height = size, width = depth, color = h_color, axis = d_axis)

    l_cyl = cylinder(frame = heart, radius = .5*size, height = depth, color = h_color, axis = c_axis, pos = (.5*size*math.cos(3*math.pi/4.), .5*size*math.sin(3*math.pi/4.), -.5*depth))
    r_cyl = cylinder(frame = heart, radius = .5*size, height = depth, color = h_color, axis = c_axis, pos = (.5*size*math.cos(math.pi/4.), .5*size*math.sin(math.pi/4.), -.5*depth))

    return heart
        
def updateLives():
    global death_number
    global crash_count
    global lives
    global dash
    dash.select()

    spacing = 45
    
    num_lives = death_number - crash_count

    while not(num_lives == len(lives)):
        if num_lives < len(lives):
            lives[-1].visible = False
            del lives[-1]

        elif num_lives > len(lives):
            lives.append(newHeart())
            lives[-1].pos = (-.5*dash.width + len(lives)*spacing + 15, 0, 0)
            
    scene.select()
    
def resetDashboard():
    global landing_signal
    landing_signal.visible = False

def wait(time, special = False):
    global earth

    rot_factor = .9
    rot_radius = 350
    t = 0
    if special:
        while t < time*2:
            rate(100)
            earth.time += 2
            earth.axis = (math.sin(math.radians(earth.time)), 0, math.cos(math.radians(earth.time)))

            earth.pos = (rot_radius*math.sin(math.radians(rot_factor*earth.time)) + lander.pos.x, rot_radius*math.cos(math.radians(rot_factor*earth.time)) + lander.pos.y, earth.default_pos.z)
            t += 1
    else:
        while t < time*2:
            rate(100)
            t += 1


 # END FUNCTIONS #
 
# game booleans
finished = False
try_over = False
level_won = False

pause = False

no_fuel = False

# game parameters

lander_radius = 10
lander_length = 20
lander_angle = 90

upright_range = 35
y_crash = 20

g = vector(0, -10, 0)
b = -.001

# landscape parameters
sectionList = []
segment_over = 0
divisions = 200
difficulty = 10

landscape = []
flags = []

moon_depth = 40
field_length = 5000

start_landscape = 400
top_height = 600
#----------------------#
# window parameters
zoom_factor = .55
zoom = .6
zoom_vector = vector(zoom,zoom,zoom)
default_center = 200
#----------------------#

dash_thickness = 100
dash_start = 0

# lives and landing signals #
dash = display(x = 0, y = dash_start, width = 1000, height = dash_thickness, center = (0,0,0), range = 500, title = "Dashboard")
dash.select()
lives = []

landing_signal = sphere(radius = 20, pos = (450,0,0), color = color.red, visible = True)
# Miscellaneous objects and things #
scene = display(x = 0, y = dash_start + dash_thickness - 10, width = dash.width, height = 700, center = (0,default_center,0), range = (350,350,350), title = "Lunar Lander")
scene.reset_range = scene.range

scene.select()
stars_filepath = "Hardrive/Users/samebernstein/Desktop/Google Drive/Lab 5 - Lunar Lander/star_background.jpg" # for star background


earth = sphere(radius = 100, pos = (0, 650, -900), axis = (0,1,0))
earth.material = materials.earth
earth.default_pos = earth.pos
earth.x_over = -300
earth.time = 0

stars = []
num_stars = 1000

floor = box(length=field_length, width=100, height= moon_depth, pos = (.5*field_length, -.5*moon_depth, 0), color = color.gray(0.5))
floor.reset_color = floor.color

moon_core = 2000
moon = box(length=field_length, width = floor.width, height = moon_core, pos = (floor.pos.x, -moon_depth - .5*moon_core, 0), color = floor.color)
moon.reset_color = moon.color

hi = text(text='Hi', align='center', pos = (-.3*floor.length, .5*top_height, 0), height = 20, depth=-0.3, color=color.yellow)

##light_1 = distant_light(direction=(-1, -0.22, 0), color=color.gray(0))
##light_2 = distant_light(direction= (-light_1.direction.x, light_1.direction.y, 0), color=color.gray(.8))
sun = local_light(pos=(earth.x - 500, earth.y, earth.z), color=color.white)
sun.x_over = 500
sun.side = [-1,1]
sun_shade = sphere(pos=sun.pos, radius = 50, color = color.yellow, material = materials.emissive)

# Level number and instructions text #
level_label = text(text='level 1', align='center', pos = (50, 350, 0), height = 40, depth=-0.3, color=color.yellow)
instructions_1 = text(text='arrow keys for movement', align='left', pos = (level_label.x - 80, level_label.y - 60, 0), height = .3*level_label.height, depth=-0.3, color=color.white)
instructions_2 = text(text='p for pause', align='left', pos = (level_label.x - 80, instructions_1.y - 20, 0), height = .3*level_label.height, depth=-0.3, color=color.white)
warning = text(text='* May cause epileptic seizures.', align='left', pos = (level_label.x - 80, instructions_2.y - 50, 0), height = .3*level_label.height, depth=-0.3, color=color.red)

##marker_font = 10
##mark = {}
##for n in range(0, divisions + 1):
##    mark[n] = box(length = 1, height = floor.height, width = floor.width + 1, pos = (start_landscape + (1./divisions)*(floor.length-start_landscape)*n, floor.y, 1), color = color.red) 
##    text(text=(str(100*n)), pos = (mark[n].x - 10, mark[n].y - 20, mark[n].z), height = marker_font, color = mark[n].color)


# lander and variables #
lander = frame()

colors = [color.magenta, color.orange, color.yellow, color.green, color.cyan, color.blue, color.white, color.gray(.8), color.white]
         
body = cylinder(frame = lander, radius = lander_radius, length = lander_length, pos = (0,0,0), color = color.white, axis = (1,0,0), opacity = .5)
body.reset_color = body.color

leg_h = 4
leg_width = 4
leg_length = 10

leg_l = box(frame = lander, axis = (-1.5,-1,0), pos = (-2,-body.radius,0), color = color.gray(.8), length = leg_length, width = leg_width, height = leg_h)
leg_l.reset_color = leg_l.color
leg_r = box(frame = lander, axis = (-1.5,1,0), pos = (-2,body.radius,0), color = color.gray(.8), length = leg_length, width = leg_width, height = leg_h)
leg_r.reset_color = leg_r.color

leg_height = abs(norm(leg_r.axis).x)*leg_r.length

cap = cone(frame = lander, radius = 10, length = 20, pos = (20,0,0), axis = (1,0,0), color = color.gray(.8), opacity = 1)
cap.reset_color = cap.color

tank = cylinder(frame = lander, radius = .8*body.radius, length = .8*body.length, pos = (2,0,0), color = (1, 0.7, 0.2), axis = body.axis)
tank.reset_color = tank.color
tank.fuel_height = tank.length
fuel_decrease = 40

fire = cone(frame = lander, radius = .7*lander_radius, color = color.orange, material = materials.shiny, pos=(0, 0, 0), axis = (-body.length, 0,0))
fire.reset_color = fire.color

tank_capacity = 10000
fuel_left = tank_capacity
thrust_time = 0

lander.pos = (0,80,0)
lander.v = vector(30, 0, 0)
lander.angle = lander_angle

landing_signal.visible = False

scene.bind('keydown', keyInput)

# meta game variables
level_number = 1
crash_count = 0
death_number = 5
dt = .01
t = 0
while not finished:

    if level_number <= 3:
        death_number = 5
    elif level_number <= 6:
        death_number = 4
    elif level_number <= 9:
        death_number = 3
    elif level_number <= 14:
        death_number = 2
    elif level_number == 15:
        death_number = 1
        
    if crash_count >= death_number and level_number > 1:
        level_number -=1
        crash_count = 0
        
    difficulty = 10 + 10*level_number

    newLandscape(difficulty)

    level_label.text = 'Level '+str(level_number)

    if level_number > 2:
        instructions_1.visible = False
        instructions_2.visible = False
        warning.visible = False
    
    increment = (floor.length - start_landscape)/divisions
    
    lander.pos = (100, 300, 0)
    lander.v = vector(30, 0, 0)
    lander.angle = 90
    
    earth.x_over = random.randint(-400, 700)
    while -150 < earth.x_over < 400:
        earth.x_over = random.randint(-600, 700)
    
    earth.pos.y = random.randint(earth.default_pos.y-100, earth.default_pos.y + 25)

    sun.x_over = sun.x_over*sun.side[random.randint(0,1)]

    newStars()
    
    updateLives()

    for obj in scene.objects: # for crazy earth-linked materials bug
        if not obj == earth:
            obj.material = None
    
    try_over = False
    level_won = False
    pause = False
    
    t = 0
    while not try_over:
        rate(200)

        air_r = b*mag2(lander.v)*norm(lander.v)
                       
        lander.pos = lander.pos + lander.v*dt
        lander.v = lander.v + g*dt
        lander.v = lander.v + (air_r)*dt 

        if lander.angle < 0:
            lander.angle = lander.angle + 360
        elif lander.angle > 360:
            lander.angle = lander.angle - 360

        if t%300 == 0:
            pass
##            print lander.angle
            
        lander.axis = (lander_length*math.cos(math.radians(lander.angle)), lander_length*math.sin(math.radians(lander.angle)), 0)
        tank.length = tank.fuel_height*(fuel_left* (1./tank_capacity) )

        earth.pos.x = lander.pos.x - earth.x_over
        earth.axis = (math.sin(math.radians(earth.time)), 0, math.cos(math.radians(earth.time)))
        earth.time += .03

        sun.pos.x = earth.pos.x + sun.x_over
        sun_shade.pos = sun.pos
        
        if thrust_time > 0:
            fire.visible = True
            thrust_time -= 1
        if thrust_time == 0:
            fire.visible = False


        while pause:
            rate(100)
            
        if lander.pos.x > start_landscape:

            segment_over = int((lander.pos.x - start_landscape)//increment)
            if segment_over > len(sectionList) - 1:
                segment_over = len(sectionList) - 1

            if lander.pos.x > floor.length - 10:
                try_over = True
                crash(False)
            
            elif sectionList[segment_over].platform:  # if over a platform
                landing_signal.visible = True
                
                if lander.pos.y < sectionList[segment_over].b + leg_height:
                    try_over = True
                    if abs(lander.v.y) < y_crash and abs(lander.v.x) < 15:
                        if abs(90 - lander.angle) <= upright_range:
                            lander.v = vector(0,0,0)
                            lander.color = color.green
            
                            level_won = True
                            land()
                        else:
                            crash(True, True)
                    else:
                        crash(True)
                else:
                    if abs(lander.v.y) < y_crash and abs(lander.v.x) < 15 and abs(90 - lander.angle) <= upright_range:
                        landing_signal.color = color.green
                    else:
                        landing_signal.color = color.red
                    
           
            else: # if not a platform
                landing_signal.visible = False
                if lander.pos.y <= surface(sectionList[segment_over].a, sectionList[segment_over].b, lander.pos.x - sectionList[segment_over].start) + leg_height:
                    try_over = True
                    crash(False)
                    
        elif (lander.pos.x < start_landscape and fuel_left < fuel_decrease*2) or lander.pos.x < hi.pos.x + 100:
                try_over = True
                
        if lander.pos.y < leg_height:
            lander.v = vector(0,0,0)

        if lander.pos.y > top_height:
            lander.pos -= (0,2,0)
            lander.v = vector(lander.v.x, -.5*lander.v.y, 0)

        scene.center = (lander.pos.x, (default_center + lander.pos.y)/2., 0)

        offset = ((lander.pos.y - zoom_factor*top_height)//50)
        if lander.pos.y > zoom_factor*top_height and scene.range.y < 1.7*scene.reset_range.y: # for zooming out and in
            scene.range += zoom_vector*offset
        elif lander.pos.y < zoom_factor*top_height + 350 and scene.range.y > scene.reset_range.y:
            offset = ((lander.pos.y - zoom_factor*top_height - 150)//50) - zoom_vector.x
            scene.range += zoom_vector*offset*.5

        if fuel_left < 2*fuel_decrease: # make tank disappear if out of fuel
            tank.visible = False
        
        t += 1
        
    wait(5)

    resetDashboard()
    deleteLandscape()
    deleteStars()
    resetLander()

    if level_won:
        level_number += 1
        

        
        
