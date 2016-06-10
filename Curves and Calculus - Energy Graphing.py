# (C) Sam Bernstein 2014

from visual import *
from visual.controls import * # for controls window
from visual.graph import * # import graphing features

from subprocess import call



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


def f_range(start, stop, step): # makes generator for plotting track curve
    r = start
    while r < stop:
        yield r
        r += step

def tprint(string = "\n", *argv): # accepts as many arguments as specified, and prints them all if console = True
    global console
    string = str(string)
    if console:
        print string,
        for arg in argv:
             arg = str(arg)
             print arg,
##        print "\n"


def print_term(coeff, power, omit = False): # for outputting polynomials to terminal
    to_power = "x^"

    if coeff != 0:
        if power == 0:
            if coeff < 0:
                print " - ",abs(coeff)
            else:
                print " + ",coeff

        elif not omit:
            if abs(coeff) == 1:
                if coeff < 0:
                    print " - ",to_power,power,
                else:
                    print " + ",to_power,power,
            else:
                if coeff < 0:
                    print " - ",abs(coeff),to_power,power,
                else:
                    print " + ",coeff,to_power,power,
        else:            
            if abs(coeff) == 1:
                if coeff < 0:
                    print to_power,power,
                else:
                    print to_power,power,
            else:
                if coeff < 0:
                    print abs(coeff),to_power,power,
                else:
                    print coeff,to_power,power,


def setmu(obj):
    global mu
    mu = obj.value
    

def set_coeff(surface, power): # called for slider event
    tprint("Coeffs", surface.coeffs)
    print "power selected: ", power
    surface.delete_plot()
    surface.coeffs[0] = self.poly_controls[0].value
    surface.update()
    surface.draw(Curve.draw_start, Curve.draw_stop, Curve.step)
##    surface.print_polynomial()

            
class Curve(object):

    draw_start = -5
    draw_stop  =  5

    view_range = abs(draw_start - draw_stop)
    
    step =  view_range/200.

    
    
    def __init__(self, coeffs):
        self.coeffs = coeffs
        self.update()
        self.make_controls()

    def update(self):

        self.coeffs_enumerate = enumerate(self.coeffs)
        
        self.coeffs_prime = [c*self.coeffs[c] for c in range(1, len(self.coeffs))]
        self.prime_enumerate = enumerate(self.coeffs_prime)

        square = [0]*(2*len(self.coeffs_prime)-1)

        for power1,coeff1 in self.prime_enumerate:
            for power2,coeff2 in self.prime_enumerate:
                square[power1 + power2] += coeff1*coeff2

        self.prime_square = square

    def set_coeff(self, obj, power): # called for slider event

##        print "power selected: ", self.poly_controls.index(obj)
        self.delete_plot()
        self.coeffs[power] = obj.value
        self.update()
        self.draw(Curve.draw_start, Curve.draw_stop, Curve.step)
    ##    surface.print_polynomial()

    def make_controls(self):
        global indent
        global begin_power_controls
        global apart
        global lbl_size
        global h_button
        global wid
        
        self.poly_controls = []
        self.control_labels = []


        for power, coeff in self.coeffs_enumerate:
            
            control_range = 10/(self.view_range**(.7*power) + 1)
            if power == 0:
                control_range =1.8*self.view_range
            elif power == 1:
                control_range = 2
            
            self.poly_controls.append(slider(text = 'Power ', min = coeff - control_range, max = coeff + control_range, pos= (begin_power_controls, abs(indent) - power*apart), width=wid, length=100, axis=(1,0,0)))

            if power == 0:
                self.poly_controls[-1].action = lambda: self.set_coeff(self.poly_controls[0], 0)
            elif power == 1:
                self.poly_controls[-1].action = lambda: self.set_coeff(self.poly_controls[1], 1)
            elif power == 2:
                self.poly_controls[-1].action = lambda: self.set_coeff(self.poly_controls[2], 2)
            elif power == 3:
                self.poly_controls[-1].action = lambda: self.set_coeff(self.poly_controls[3], 3)
            elif power == 4:
                self.poly_controls[-1].action = lambda: self.set_coeff(self.poly_controls[4], 4)
            elif power == 5:
                self.poly_controls[-1].action = lambda: self.set_coeff(self.poly_controls[5], 5)
            elif power == 6:
                self.poly_controls[-1].action = lambda: self.set_coeff(self.poly_controls[6], 6)
            elif power == 7:
                self.poly_controls[-1].action = lambda: self.set_coeff(self.poly_controls[7], 7)
            elif power == 8:
                self.poly_controls[-1].action = lambda: self.set_coeff(self.poly_controls[8], 8)
            elif power == 9:
                self.poly_controls[-1].action = lambda: self.set_coeff(self.poly_controls[9], 9)
            elif power == 10:
                self.poly_controls[-1].action = lambda: self.set_coeff(self.poly_controls[10], 10)
            elif power == 11:
                self.poly_controls[-1].action = lambda: self.set_coeff(self.poly_controls[11], 11)

            print "power: ", power
            print "control_range: ", control_range
            print
            self.control_labels.append(button(text = str(power), pos = (self.poly_controls[-1].pos.x - .2*self.poly_controls[-1].length, self.poly_controls[-1].pos.y), height=.5*h_button, width= h_button))


    def print_polynomial(self):
        print self.coeffs
        print_term(self.coeffs[-1], len(self.coeffs), True)
        
        for power, coeff in reversed(list(enumerate(self.coeffs[:len(self.coeffs)]))):

            print_term(coeff, power)

        print "Value at left end:  ",self.value(Curve.draw_start)
        print "Value at right end: ",self.value(Curve.draw_stop)

    def value(self, x):
        y = 0
        for c in range(len(self.coeffs)):
            y += self.coeffs[c]*(x**c)
        return y

    def derivative(self, x): # instantaneous derivative at x
        y_prime = 0
        for c in range(len(self.coeffs_prime)):
            y_prime += self.coeffs_prime[c]*(x**c)
        return y_prime
    
    def arc_length(self, old_x, new_x): # calculates arc length of segment traveled using calculus arc length formula

        total = 0
        a = 0
        for power, coeff in enumerate(self.coeffs_prime):
            total += coeff*(old_x**power)

        a = math.sqrt(1 + total**2)


        square_total = 0
        b = 0
        for power, coeff in enumerate(self.coeffs_prime):
            total += coeff*(new_x**power)
            
        b = math.sqrt(1 + total**2)

        return abs(b - a)

    
    def draw(self, start_x, stop_x, resolution):
        global path
        
        points = [(stop_x, 0), (start_x, 0)]

        for x in f_range(start_x, stop_x, resolution):
            points.append( (x, self.value(x)))
            
        pl = shapes.pointlist(pos= points)
        self.plot = extrusion(pos= path, shape = pl, color=color.gray(.8))

    def delete_plot(self):
        self.plot.visible =  False
        del self.plot

    
pause = False
falling = False


console = True

g = vector(0,-5,0)
s_g = 40*g
m = 1 # mass of ball
mu = .1 # coefficeint of friction

# controls window
h_win = 600
spacing = 8
c = controls(x = 0, width = 400, height = h_win, title = "Simulation Controls")


##control_2 = slider(text = 'Power 2',min = -3, max = 2, pos=(-apart*9,.5*apart), width=7, length=60, axis=(1,0,0), action = lambda:set_coeff(control_2))

indent = -40
begin_power_controls = indent
apart = 14
lbl_size = 10
h_button = 10
wid = 10

start =  button(pos=(0,80), height=h_button, width= 2*h_button, text='Pause', action= lambda: pausenow())
restart = button(pos=(start.pos.x, start.pos.y - 9), height = h_button, width = 2*h_button, text = 'Restart', action = lambda: restartnow())

mu_control =  slider(text = 'mu', min = 0, max = 1, pos=(indent, restart.pos.y - 15), width= wid, length=60, axis=(1,0,0), action = lambda:setmu(mu_control))
mu_lbl = button(text = 'mu', pos = (mu_control.pos.x - .2*mu_control.length, mu_control.pos.y), height=.5*h_button, width= h_button)

## sets up main window
scene = display(x = c.x + c.width + spacing, width = 600, height = h_win, center = (0,200,0), title = "Simulation")


# energy graph setup
bar_width = 150
energy = display(x = scene.x + scene.width + spacing, width = 250, center = (1.5*bar_width, 850, 0), height = scene.height, range = 1500, title = "Energy Graph")

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

# give graph bars colors
potential.color = color.blue
kinetic.color = color.orange
friction.color = color.yellow

##
## scene objects and stuff
scene.select()
earth_length = 4
earth_height = 5
earth = box(length = earth_length, height = earth_height, width = 10, pos = (0,-.5*earth_height,0), color = color.gray(.8))
earth.visible = False

class Ball(object):
    global earth
    
    reset_x = 0

    d_ball = sphere(radius = .8, color = color.orange)

    d_ball.pos = (earth.pos.x - .45*earth.length, earth.pos.y + .5*earth.height + d_ball.radius + 10, 0)
    d_ball.reset_x = reset_x
    d_ball.v = vector(0,0,0)
    d_ball.reset_v = d_ball.v

    d_ball.old_x = d_ball.pos.x

    d_ball.falling = False

    def __init__(self, ball = None):
        if ball is None:
            self.ball = Ball.d_ball
        else:
            self.ball = ball
            self.ball.reset_x = Ball.d_ball.reset_x
            self.ball.v = Ball.d_ball.v
            self.ball.reset_v = Ball.d_ball.reset_v
            self.ball.old_x = Ball.d_ball.old_x
            self.ball.falling = Ball.d_ball.falling

    def update(self):
        global balls
        self.old_x = self.ball.pos.x
        
        if self.ball is balls[0]:
            self.ball.color = color.green
        
    def calculate_height(self, surface):
        pass
    


scene.range = 1.2*Curve.view_range
scene.center.y = .5*scene.range.y

incline = []
path = [(0,0,earth.pos.z + .5*earth.width),(0,0,earth.pos.z - .5*earth.width)]

balls = []
rad_a = 0

done_ball = False
breakout = False


zeroed = [0]*6

surface = Curve(zeroed)#randomly generate starting incline
surface.draw(Curve.draw_start, Curve.draw_stop, Curve.step)

balls.append(Ball())



dt = 0.01
t = 0
cycle = 0
while not breakout:
    t = 0
    count = 0
    cycle += 1


    for b in balls:
        b.ball.x = b.reset_x
        b.ball.y = surface.value(b.ball.x) + b.ball.radius
        
        b.ball.v = b.ball.reset_v

    friction.height = 0

    done_ball = False
    while not(done_ball):
        rate(300)
        t = t + dt
        count += 1

        if t%10000 == 0:
            surface.print_polynomial()
            tprint()

        for b in balls:

            b.update() # sets b.old_x
            
            rad_a = math.atan(surface.derivative(b.ball.x))
            
            if b.ball.y - b.ball.radius > surface.value(b.ball.x): # if ball is not above incline plane
                b.ball.falling = True
                b.ball.a = g
                
            else:
                if b.ball.falling:
                    b.ball.v = vector(0,0,0)
                b.ball.falling = False
                b.ball.y = surface.value(b.ball.x) + b.ball.radius
                
                component_g = -1*vector(abs(s_g.y)*math.sin(rad_a)*math.cos(rad_a), s_g.y*(math.sin(rad_a)**2),0) # s_g is a stronger gravity vector
                if b.ball.v.y < 0 and b.ball.v.x > 0:
                    component_f = vector(-mu*abs(s_g.y)*math.cos(rad_a)*math.cos(rad_a), mu*abs(s_g.y)*math.cos(rad_a)*math.sin(rad_a)) # friction
                else:
                    component_f = vector(0,0,0)
                b.ball.a = component_g + component_f
            
            b.ball.v = b.ball.v + b.ball.a*dt
            b.ball.pos = b.ball.pos + b.ball.v*dt

            
            if b.ball.pos.y <= earth.pos.y + .5*earth.height + b.ball.radius or not (Curve.draw_start < b.ball.pos.x < Curve.draw_stop):
                done_ball = True # for now


            if not(abs(g.y)*m*(b.ball.pos.y - b.ball.radius) < 0):            
                potential.height = abs(g.y)*m*(b.ball.y - b.ball.radius)
            else:
                potential.height = 0
            potential.pos.y = .5*potential.height
        

        
        if not balls[0].ball.falling:
            F = mag(component_f)*m
            dist = surface.arc_length(balls[0].ball.old_x, balls[0].ball.x) # arc length formula from calculus
            friction.height += F*dist

        if len(balls) > 0:
            kinetic.height = .5*m*mag2(balls[0].ball.v)
            kinetic.pos.y = .5*kinetic.height

            friction.pos.y = .5*friction.height

        while pause: # for pause button
            rate(100)



