# (C) Sam Bernstein 2014

"""
REAMDE:

Simulates an object sliding down an incline. User can select incline angle
and coefficient of friction. Plots distribution of different types of energy
in real time.

"""
from visual import *
from visual.controls import * # for controls window
from visual.graph import * # import graphing features 

def restartnow():
    global done_ball
    done_ball = True

def pausenow(): # Called by controls when button clicked
    if start.text == 'Continue':
        global pause
        pause = False
        start.text = 'Pause'
    else:
        pause = True
        start.text = 'Continue'

def change():
    if start.text == 'Start':
        start.text = 'Running'
    else:
        start.text = 'Start'

def surface(x):
    global incline
    return incline[0].m*x + incline[0].b

def setmu(obj):
    global mu
    mu = obj.value
    
def setangle(obj): # called on slider drag events
    global incline
    global incline_angle
    incline_angle = obj.value
    
    newIncline()
    
def newIncline():
    global earth
    global incline
    global incline_angle
    global path

    while len(incline)>0:
        incline[0].visible = False
        del incline[0]
    
    h = earth.length*math.tan(math.radians(incline_angle))
    tri_face = Polygon( [(earth.pos.x - .5*earth.length, 0), (earth.pos.x + .5*earth.length,0), (earth.pos.x - .5*earth.length, h)] )

    incline.append(extrusion(pos= path, shape=tri_face, color=color.gray(.8)))
    incline[0].m = -h/earth.length
    incline[0].b = .5*h

    
pause = False
falling = False
g = vector(0,-9.8,0)
m = 1 # mass of ball
mu = .1 # coefficeint of friction

## sets up main window
scene = display(x = 0, width = 600, height = 650, center = (0, 200,0), title = "Ball")

# energy graph setup
bar_width = 150
energy = display(x = scene.x + scene.width + 10, width = 350, center = (1.5*bar_width, 850, 0), height = scene.height, range = 1500, title = "Energy Graph")

size = 6
below = 100
potential = box(width = bar_width, length = bar_width, height = 100, pos = (bar_width*.5, 0, 0))
potential_label = label(text = 'U', pos = potential.pos - (0,below,0), size = size)

kinetic = box(width = bar_width, length = bar_width, height = 100, pos = (bar_width + bar_width*.5, 0, 0))
kinetic_label = label(text = 'K', pos = kinetic.pos - (0,below,0), size = size)

friction = box(width = bar_width, length = bar_width, height = 100, pos = (2*bar_width + bar_width*.5, 0, 0))
friction.magnit = 0
friction_label = label(text = 'W of f', pos = friction.pos - (0,below,0), size = size)
component_f = vector(0,0,0)
##
## scene objects and stuff
scene.select()
earth_length = 150
earth_height = 5
earth = box(length = earth_length, height = earth_height, width = 10, pos = (0,-.5*earth_height,0), color = color.white)

scene.range = earth.length*.7
scene.center.y = scene.range.y*.85

incline = []
path = [(0,0,earth.pos.z + .5*earth.width),(0,0,earth.pos.z - .5*earth.width)]

ball = sphere(radius = 5, color = color.orange)

ball.pos = (earth.pos.x - .45*earth.length, earth.pos.y + .5*earth.height + ball.radius + 500/9.8, 0)
ball.reset_x = ball.x
ball.v = vector(0,0,0)
ball.reset_v = ball.v


done_ball = False
breakout = False

# controls window
c = controls(x = scene.x, y = scene.height + 5, width = energy.x + energy.width, height = 150, title = "Simulation Controls")

apart = 8
lbl_size = 10
h_button = 10
angle_control = slider(text = 'angle',min = 0, max = 70, pos=(-apart*9,.5*apart), width=7, length=60, axis=(1,0,0), action = lambda:setangle(angle_control))
angle_lbl = button(text = 'angle', pos = (angle_control.pos.x - .2*angle_control.length, angle_control.pos.y), height=.5*h_button, width= h_button)

mu_control =  slider(text = 'mu', min = 0, max = 1, pos=(-apart*9,-.5*apart), width=7, length=60, axis=(1,0,0), action = lambda:setmu(mu_control))
mu_lbl = button(text = 'mu', pos = (mu_control.pos.x - .2*mu_control.length, mu_control.pos.y), height=.5*h_button, width= h_button)

start =  button(pos=(20,5), height=h_button, width= 2*h_button, text='Pause', action= lambda: pausenow())
restart = button(pos=(start.pos.x, start.pos.y - 9), height = h_button, width = 2*h_button, text = 'Restart', action = lambda: restartnow())

# give graph bars colors
potential.color = color.blue
kinetic.color = ball.color
friction.color = color.yellow

incline_angle = random.randint(5,60) #randomly generate starting incline
newIncline()

dt = 0.01
t = 0
cycle = 0
while not breakout:
    t = 0
    count = 0
    cycle += 1

    ball.x = ball.reset_x

    if incline_angle != 0:
        ball.y = surface(ball.x - ball.radius*math.sin(math.radians(incline_angle))) + ball.radius*math.cos(math.radians(incline_angle))
    else:
        ball.y = 100
    ball.v = ball.reset_v

    friction.height = 0

    done_ball = False
    while not(done_ball):
        rate(300)
        t = t + dt
        count += 1

        old_x = ball.x
        
        rad_a = math.radians(incline_angle)
        
        if ball.y - ball.radius*math.cos(rad_a) > 1 + surface(ball.x - ball.radius*math.sin(rad_a)): # if ball is not above incline plane
            falling = True
            ball.a = g
            
        else:
            if falling:
                ball.v = vector(0,0,0)
            falling = False
            ball.y = surface(ball.x - ball.radius*math.sin(rad_a)) + ball.radius*math.cos(rad_a)
            
            component_g = vector(abs(g.y)*math.sin(rad_a)*math.cos(rad_a), g.y*(math.sin(rad_a)**2),0) # gravity
            if ball.v.y < 0 and ball.v.x > 0:
                component_f = vector(-mu*abs(g.y)*math.cos(rad_a)*math.cos(rad_a), mu*abs(g.y)*math.cos(rad_a)*math.sin(rad_a)) # friction
            else:
                component_f = vector(0,0,0)
            ball.a = component_g + component_f
        
        ball.v = ball.v + ball.a*dt
        ball.pos = ball.pos + ball.v*dt

        
        if ball.pos.y <= earth.pos.y + .5*earth.height + ball.radius:
            done_ball = True


        if not(abs(g.y)*m*(ball.pos.y - ball.radius) < 0):            
            potential.height = abs(g.y)*m*(ball.y - ball.radius)
        else:
            potential.height = 0
        potential.pos.y = .5*potential.height
        
        kinetic.height = .5*m*mag2(ball.v)
        kinetic.pos.y = .5*kinetic.height

        if not falling:
            F = mag(component_f)*m
            dist = math.sqrt(1 + incline[0].m**2)*abs(ball.x - old_x) # this is the arclength formula from calculus
            friction.height += F*dist
            
        friction.pos.y = .5*friction.height

        while pause:
            rate(100)






