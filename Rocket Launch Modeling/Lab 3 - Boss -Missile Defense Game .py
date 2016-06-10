# (C) Sam Bernstein 10/14/2014
# group Ben, Sam and Daniel
# Extra Credit Anti-Soviet Missile Defense Game
# Note: may induce epileptic seizures.


from visual import *
from visual.graph import *
from visual.controls import * # for controls window
from types import *
import random

##from sympy import * # this is for the calculus

def setvel(obj): # called on slider drag events
    if obj == Vx:
        ball.velocity.x = obj.value
        ball2.velocity.x = obj.value
    if obj == Vy:
        ball.velocity.y = obj.value
        ball2.velocity.y = obj.value

def set_ang(): # called on slider drag events
    global angle_launch
    angle_launch = 90 + angle_pick.value
##    print "Angle changed to ", angle_launch

def launch():
    global rocket
    global new_rocket
    if len(rocket) < 3:
        new_rocket = True

def delete(f): # deletes rocket with index f
    global rocket
    global less
    rocket[f].visible = False
##    rocket[f].trail.visible = False
##    del rocket[f].trail
    rocket.remove(rocket[f])
        
def delete_e(f): # deletes enemy with index f
    global enemy
    global less
    enemy[f].visible = False
##    enemy[f].trail.visible = False
##    del enemy[f].trail
    enemy.remove(enemy[f])
    
def delete_r(f): # deletes rescue pyramid with index f
    global rescue
    global less
    rescue[f].visible = False
    rescue.remove(rescue[f])
    
def delete_b(f): # deletes rescue pyramid with index f
    global boss
    global less
    boss[f].visible = False
    boss.remove(boss[f])

def reset(): # clears all arrays of game objects
    global rocket
    global enemy
    global boss
    global rescue
    global base
    global floor
    
    global game_over
    global init_e_t
    global init_r_t
    global hit_count
    global r_num

    for r in rocket:
        r.visible = False
        rocket.remove(r)
    for e in enemy:
        e.visible = False
        enemy.remove(e)
    for b in boss:
        b.visible = False
        boss.remove(b)
    for r in rescue:
        r.visible = False
        rescue.remove(r)
    for b in base:
        b.visible = True
    

    game_over.visible = False

    enemy_t = init_e_t
    rescue_t = init_r_t
    hit_count, r_num = 0,0
    
    print
        
    
def startitnow(): # Called by controls when button clicked
##    print "Pause/Continue clicked"
    global startit

    if start.text == 'Start':
        startit = True
        start.text = 'Pause'
        
    elif start.text == 'Pause':
        startit = False
        start.text = 'Continue'
    elif start.text == 'Continue':
        startit = True
        start.text = 'Pause'

def enditnow(): # Called by controls when button clicked
    if stop.text == 'End':
        global game_done
        global finished
        global override
        global startit
        game_done = True
        finished = True
        override = True
        startit = True
        stop.text = 'Ended'
        
def restart():
    global startit
    global game_done
    if game_done:
        startit = True

def change(string):
    start.text = str(string)

def tprint(string = "\n", *argv): # accepts as many arguments as specified, and prints them all if console = True
    global console
    string = str(string)
    if console:
        print string,
        for arg in argv:
             arg = str(arg)
             print arg,
        print "\n"


#-------------------------------------------------------------------



# Control flow variables
console = False # if False, console won't update with regular launch info

startit = False
finished = False
game_done = False

override = False

rocket_under = False

main_rate = 3000

# video screen
screen = display(x = 0, width = 600, height = 600, center = (0,2,0), title = "Air Resistance and Projectile Motion")

floor = box(length=5, width=1, height=0.5, color = color.white)

game_over = text(text="GAME OVER", pos = (-floor.length*.5 + .4, floor.height*.5 + 2, 0), height = .5, color = color.yellow)
game_over.visible = False



# game controls screen
c = controls(x = screen.x, y = screen.height + 5, width = screen.width, height = 200, title = "Simulation Controls")

start = button(pos=(0,-10), height=10, width=20, text='Pause', action = lambda: startitnow())
stop =  button(pos=(start.pos.x+25,start.pos.y), height=10, width=20, text='End', action = lambda: enditnow())
again = button(pos=(start.pos.x-30,start.pos.y), height = 10, width = 20, text = 'Again', action = lambda: restart())
angle_pick = slider(text = 'Launch angle',min = -90, max = 90, pos=( (start.pos.x - 50),start.pos.y + 15), width=7, length=90, axis=(1,0,0), action = lambda: set_ang())
launch_new =  button(pos=(angle_pick.pos.x + angle_pick.length*.5,angle_pick.pos.y + 10), height=10, width=20, text='Launch', action = lambda: launch())

screen.select()
#------------------------------------------------------------------------#
# EDITABLE CONSTANT PARAMETERS #
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




W = 0 # work done by spring
rocket_max = 0 # maximum height of rocket trajectory
rocket_x_initial = 0

f = 0 # which human rocket
new_rocket = False
#------------------------------------------------------------------------#
# Objects

boss = []
boss_time = []
boss_sin = []
enemy = []
enemy_pos = []

size = .1
rocket_L = .5
real_L = .2
screen.select()

rocket = []
rescue = []

t_size = .25
line_set = .8
screen.select()
line = []

line.append(text(text="Defend your blue bases", pos = (-floor.length*.5 + line_set, floor.height*.5 + 1.5, 0), height = t_size, color = color.blue))
line.append(text(text="from the Soviet missiles", pos = (-floor.length*.5 + line_set, floor.height*.5 + 1, 0), height = t_size, color = color.red))
line.append(text(text="with the power of your", pos = (-floor.length*.5 + line_set, floor.height*.5 + .5, 0), height = t_size, color = color.yellow))
line.append(text(text="SAMs", pos = (-floor.length*.5+2.2*line_set, floor.height*.5 + 0, 0), height = t_size*1.5, color = color.green))

change("Start")

startit = False
while not startit:
    rate(100)

for l in line:
    l.visible = False


bar_r = .02
bar = cylinder(pos = (0, 1.3*(floor.height*.5), 0), axis = (-1*L_bar,0,0), radius = bar_r, color = color.white)
bar_L = cylinder(length = L_bar, radius = bar_r, color = bar.color)
bar_M = cylinder(length = L_bar*1.2, radius = bar_r*.2, color = bar.color)
bar_R = cylinder(length = L_bar, radius = bar_r, color = bar.color)


base = []
balls = 4
ball_r = .1
for n in range(0, balls):
    base.append(sphere(radius = ball_r, pos = (-floor.length*.5 + n*floor.length/balls + .5, .5*floor.height + ball_r,0), color = color.blue) )
    enemy_pos.append(base[-1].pos.x)
##    text(text=(str(n*floor.length/divisions)), pos = (mark[n].x - marker_font, mark[n].y - floor.height*1.5, mark[n].z), height = marker_font, color = mark[n].color)

#--------------------------------------------------------------#


##rocket[f].airresistance = b*mag2(rocket[f].v)*norm(rocket[f].v)
#----------------------------------

### add distance marks
##marker_font = floor.length/60
##mark = {}
##divisions = 5
##for n in range(0, divisions + 1):
##    mark[n] = box(length = floor.length/50, height = floor.height*1.1, width = floor.width, pos = (-floor.length*.5 + n*floor.length/divisions, -.5*floor.height, 1), color = color.red) 
##    text(text=(str(n*floor.length/divisions)), pos = (mark[n].x - marker_font, mark[n].y - floor.height*1.5, mark[n].z), height = marker_font, color = mark[n].color)


screen.select()



colors = [color.red, color.yellow, color.green, color.orange, color.white, color.blue, color.cyan, color.magenta]

v = 20 # this is the the starting speed of rocket (scalar)
angle_launch = 90 

b = 1.4 # air resistance constant # FIND BY EXPERIMENT
g = vector (0,-20,0) # gravitational constant

coll_d = .3
r_num = 0
hit_count = 0
round_count = 0

dt =.001
time = 1
t = -time
enemy_t = 200
boss_t = 3*enemy_t
extra_death_speed_cutoff_time = 10000

rescue_t = 4*enemy_t


init_e_t = enemy_t
init_r_t = rescue_t
#--------------------------------------------------START SIMULATION AND CALCULATIONS-------------------------------------------------------#
count = 1

print "GAME STARTED"

while not finished:

    # reset things for each round
    screen.select()

    round_count +=1
    print "-------------- Round ", round_count," --------------"

    floor.color = (1,1,1)
    n = 0
    c = 0
    
    startit = True
 
    
    tprint()
    
    game_done = False # reset variables for breaking out of simulation loop
    override = False
    
##            W = integrate(k*(sqrt(L_band**2 + dist**2) - L_band)*cos(atan(L_band/dist)), (dist, 0, 1))# find work done by spring on rocket

    rocket_under = False

    for ball in base:
        enemy_pos.append(ball.pos.x)
        
    t = 0
    max_reached = False
    while not(game_done):
        rate(80)
##        print t
        bar.axis = (-L_bar*math.cos(math.radians(90-angle_launch)), L_bar*math.sin(math.radians(90-angle_launch)), 0 )
        bar_L.axis = (L_bar*math.cos(math.radians(angle_launch)), L_bar*math.sin(math.radians(angle_launch)), 0 )
        bar_L.pos = (bar.pos.x - L_bar*math.cos(math.radians(90-angle_launch)), bar.pos.y + L_bar*math.sin(math.radians(90-angle_launch)), 0)

        bar_M.axis = 1.1*bar_L.axis
        bar_M.pos = (bar.pos.x - L_bar*.5*math.cos(math.radians(90-angle_launch)), bar.pos.y + L_bar*.5*math.sin(math.radians(90-angle_launch)), 0)
        
        bar_R.axis = bar_L.axis
        bar_R.pos = bar.pos

        t += time

##        if t% 10 == 0:
##            print "t = ", t

        if t%1000 == 0 and enemy_t > 30:
            enemy_t -=4

        if t%1000 == 0 and rescue_t >30:
            rescue_t -=2

        if t%rescue_t == 0:
            empty_bases = False
            for b in base:  # check to see if there are any empty bases for a rescue
                if b.visible == False:
                    empty_bases = True
                    
            if empty_bases:
                # assign dead base to rescue object
                wrong_base = True
                while wrong_base:
                    dead_base = random.randrange(0,4)
                    if base[dead_base].visible == False:
                        wrong_base = False

                rescue.append(pyramid(size = (.25,.25,.25), pos = (5*(random.random()-.5), 4+1.5*random.random(), 0), axis = (0,1,0), up = (1,0,0), opacity = .3, color= color.magenta))
                rescue[-1].base = dead_base
                rescue[-1].v = vector(0, -v*.1 , 0)
                tprint( "made rescue ", t/rescue_t)


        if t%boss_t == 0: # for super bosses
            extra_death_speed = t/400.0
            if t > extra_death_speed_cutoff_time:
                extra_death_speed = t/extra_death_speed_cutoff_time

            boss.append(cone(length = .03, radius = .2, pos = (3*(random.random()-.5), 5.5, 0), axis = (0,1,0), up = (1,0,0), opacity = .5, color= color.orange))
            boss[-1].axis = (0,-1,0)
            boss[-1].v = vector(0, -v*.05*(1.0 + extra_death_speed) , 0)
            # for boss motion effects
            boss_time.append(0)
            boss_sin.append(0)
            tprint("made boss ", t/boss_t)

        if t%enemy_t == 0:
        
            no_bases = True
            for b in base:  # check to see if there are any empty bases for a rescue
                if b.visible == True:
                    no_bases = False

            new_pos = 2.5
            
            if not no_bases:
                wrong_pos = True
                while wrong_pos: # make sure new enemy attacks existing base
                    new_pos = enemy_pos[int(4*random.random())]
                    for b in base:
                        if b.visible == True and b.pos.x == new_pos:
                            wrong_pos = False
                            break
            else: # if there are no bases, put anywhere
                new_pos = enemy_pos[int(4*random.random())]
                    
            enemy.append(arrow(length = rocket_L, pos = (new_pos, 4+1.5*random.random(), 0), color=color.red))
            enemy[-1].v = vector(0, 0 , 0)
    ##            enemy[-1].trail = curve(color = colors[c%8])
    ##            enemy[-1].v.y = v*math.sin(math.radians(angle_launch))
    ##            enemy[-1].v.x = v*math.cos(math.radians(angle_launch))
            enemy[-1].axis = (rocket_L*norm(enemy[-1].v))
            enemy[-1].airresistance = vector(0,0,0)
            tprint( "Enemy made", int(t/enemy_t))

        
        if new_rocket:
            
            rocket.append(arrow(length = rocket_L, pos = (bar.pos.x - L*math.cos(math.radians(90 - angle_launch)), bar.pos.y + L*math.sin(math.radians(90 - angle_launch)),0), color=color.green))
            rocket[-1].v = vector(math.cos(math.radians(angle_launch))*v, math.sin(math.radians(angle_launch))*v , 0)
##            rocket[-1].trail = curve(color = colors[c%8])
            rocket[-1].v.y = v*math.sin(math.radians(angle_launch))
            rocket[-1].v.x = v*math.cos(math.radians(angle_launch))
            rocket[-1].axis = (rocket_L*norm(rocket[-1].v))
            rocket[-1].airresistance = vector(0,0,0)
            r_num +=1
            new_rocket = False


        for e in enemy: # update enemy kinematics
            e.axis = rocket_L*norm(e.v)

##            e.airresistance = b*mag(e.v)*norm(e.v) # b*mag2([f]v)*norm(f.v)
            e.pos = e.pos + (e.v)*dt
            e.v = e.v + g*dt
##            e.v = e.v + (e.airresistance)*dt # rocket with air resistance
            
        for f in rocket: # update kinematics rocket
            f.axis = rocket_L*norm(f.v)

##            f.airresistance = b*mag(f.v)*norm(f.v) # b*mag2([f]v)*norm(f.v)
            f.pos = f.pos + (f.v)*dt
            f.v = f.v + g*dt
##            f.v = f.v + (f.airresistance)*dt # rocket with air resistance
            
        spin_angle = (4*t)%360
        spin = time*.2
        
        for r in rescue:          
            r.up += vector(math.sin(math.radians(spin_angle)), 0, math.cos(math.radians(spin_angle)))
##            f.airresistance = b*mag(f.v)*norm(f.v) # b*mag2([f]v)*norm(f.v)
            r.pos = r.pos + (r.v)*dt
            r.v = r.v + g*dt
##            f.v = f.v + (f.airresistance)*dt # rocket with air resistance            
         
        for b in boss:
            ##            r.axis = r.axis + vector(dt, dt, dt)

            boss_sin[boss.index(b)] = (2*boss_time[boss.index(b)])%360
            b.up += vector(math.cos(math.radians(spin_angle)), math.sin(math.radians(spin_angle)), 0)
            b.pos = b.pos + (b.v)*dt
            b.v = b.v + vector(math.cos(math.radians(boss_sin[boss.index(b)]))*.3, 0, 0)

            boss_time[boss.index(b)] +=1
            
        #--------------------------------------------------------------------------------------------------------------
        # for rockets
        less = 0
        f = 0
        while f < len(rocket): # for each rocket check if out of range
            # check if bottom of rocket is below landing height and that rocket is on the way down
            if rocket[f].v.x == 0: # divide by zero error catching
                rocket[f].v.x = 0.01
            if rocket[f].y - real_L*math.sin(math.atan(abs(rocket[f].v.y)/rocket[f].v.x)) <= floor.height/2 and rocket[f].v.y < 0:
                delete(f)
                f-=1
            f +=1

        less = 0
        f = 0
        while f < len(rocket): # delete if out of screen bounds
            if abs(rocket[f].pos.x) > .5*floor.length or rocket[f].pos.y > 4.5:
                delete(f)
                f-=1
            f +=1
        #---------------------------------------------
            
        # for enemies                 
        less = 0
        f = 0
        while f < len(enemy): # delete if below
            # check if bottom of rocket is below landing height and that rocket is on the way down
            if enemy[f].v.x == 0: # divide by zero error catch
                enemy[f].v.x = 0.01
            if enemy[f].y - real_L*math.sin(math.atan(abs(enemy[f].v.y)/enemy[f].v.x)) <= floor.height/2:
                delete_e(f)
                f-=1
            f +=1

        less = 0
        f = 0
        while f < len(enemy): # delete if out of screen bounds
            if abs(enemy[f].pos.x) > .5*floor.length or enemy[f].pos.y > 5:
                delete_e(f)
                f-=1
            f +=1


        #---------------------------------------------
        # for rescues                
        less = 0
        f = 0
        while f < len(rescue): # delete if below
            # check if bottom of lifesaver is below landing height
            if rescue[f].v.x == 0: # divide by zero error catch
                rescue[f].v.x = 0.01
            if rescue[f].y - real_L*math.sin(math.atan(abs(rescue[f].v.y)/rescue[f].v.x)) <= floor.height/2:
                delete_r(f)
                f-=1
            f +=1

        less = 0
        f = 0
        while f < len(rescue): # delete if out of screen bounds
            if abs(rescue[f].pos.x) > .5*floor.length or rescue[f].pos.y > 5:
                delete_r(f)
                f-=1
            f +=1

        #---------------------------------------------
        # for bosses               
        less = 0
        f = 0
        while f < len(boss): # END GAME IF BELOW
            # check if bottom of lifesaver is below landing height
            if boss[f].v.x == 0: # divide by zero error catch
                boss[f].v.x = 0.01
            if boss[f].y - boss[f].length <= floor.height/2:
                delete_b(f)
                game_done = True # break out
                f-=1
            f +=1

        less = 0
        f = 0
        while f < len(boss): # delete if out of screen bounds
            if abs(boss[f].pos.x) > .5*floor.length or boss[f].pos.y > 5.5:
                delete_b(f)
                f-=1
            f +=1
        #--------------------------------------------------------------------------------------------------------------

##        # if two rockets hit each other
##        less = 0
##        f = 0
##        while f < len(rocket):
##            p = 0
##            while p < len(rocket):
##                if math.hypot(rocket[f].pos.x - rocket[p].pos.x, rocket[f].pos.y - rocket[p].pos.y) < coll_d and not(p == f):
##                    delete(f) # delete first rocket
##                    if f < p: # if first rocket deletion moves indices down 1,
##                        delete(p-1) # move next rocket index down 1.
##                    else:
##                        delete(p)
##                    p-=1
##                    if len(rocket) == 0:
##                        break
##                    if not f == 0:
##                        f-=1
##                p +=1
##            f+=1
        # if rocket hits enemy rocket
        less = 0
        f = 0
        while f < len(rocket):
            p = 0
            while p < len(enemy):
                if math.hypot(rocket[f].pos.x - enemy[p].pos.x, rocket[f].pos.y - enemy[p].pos.y) < coll_d:
                    delete(f)
                    delete_e(p)
                    hit_count += 1
                    if len(rocket) == 0:
                        break
                    if not f == 0:
                        f-=1
                    p-=1
                p +=1
            f+=1

        less = 0
        f = 0
        while f < len(rocket): # rockets hit bosses
            p = 0
            while p < len(boss):
                if math.hypot(rocket[f].pos.x - boss[p].pos.x, rocket[f].pos.y - (boss[p].pos.y - boss[p].length) ) < coll_d:
                    delete(f)
                    delete_b(p)
                    hit_count += 1
                    if len(rocket) == 0:
                        break
                    if not f == 0:
                        f-=1
                    p-=1
                p +=1
            f+=1

##        # if rockets kill bases
##        less = 0
##        f = 0
##        while f < len(rocket):
##            p = 0
##
##            x_d = rocket[f].pos.x - base[p].pos.x
##            y_d = rocket[f].pos.y - base[p].pos.y
##            while p < len(base):
##                if math.hypot(x_d, y_d) < coll_d and base[p].visible == True:
##                    tprint( "base ", p, " hit.")
##                    base[p].visible = False
##                    delete(f)
##                    if len(rocket) == 0:
##                        break
##                    if not f == 0:
##                        f-=1
##                p +=1
##            f+=1

            
        # enemies kill bases
        less = 0
        f = 0
        while f < len(enemy):
##            print "   len enemy = ", len(enemy)
##            print "enemy index = ", f
            p = 0
            while p < len(base):
##                print "base index = ", p
                x_d = enemy[f].pos.x - base[p].pos.x
                y_d = enemy[f].pos.y - base[p].pos.y
                
                if math.hypot(x_d, y_d) < coll_d and base[p].visible == True:
                    tprint( "base ", p, " hit.")
                    base[p].visible = False
                    delete_e(f)
                    if len(enemy) == 0:
                        break
                    if not f == 0:
                        f-=1
                p +=1
            f+=1

        #-------------Resurrect base
        less = 0
        f = 0
        while f < len(rocket):
            p = 0
            while p < len(rescue):
                if math.hypot(rocket[f].pos.x - rescue[p].pos.x, rocket[f].pos.y - rescue[p].pos.y) < coll_d:
                    delete(f)
                    base[rescue[p].base].visible = True
                    delete_r(p)
                    if len(rocket) == 0:
                        break
                    if not f == 0:
                        f-=1
                    p-=1
                p +=1
            f+=1

        if not game_done:
            game_done = True
            if len(rescue) > 0: # check if still a chance of resurrecting base
                game_done = False
            else:
                for b in base:
                    if b.visible == True: # if at least one base still exists, game not over
                        game_done = False 
                        break
                    
        while not startit and not finished and not game_done: # for pausing
            rate(100)
            
                
##        for f in range(len(rocket)):
##            pass
##            rocket[f].trail.append(pos=rocket[f].pos)

    game_over.visible = True
    
    score_time = t
    print "You lasted ", score_time, " time units, intercepted ", hit_count, " Russian missiles,"
    print "and had a total hit percentage of ", round(100.0*(hit_count/float(r_num)), 2), "%."
    print "\n", "Hooray."

    # initiate death procedure
    
    for r in rocket:
        r.color = color.white
        r.v = vector(0,0,0)
        
        
    t = 0
    while t < 9:
        for c in colors:
            floor.color = c
            for e in enemy:
                rate(50)
                e.color = c
                for f in rocket: # update rockets kinematics
                    if not f.pos.y < floor.height*.5 + real_L:                        
                        f.axis = rocket_L*norm(f.v)
                        f.pos = f.pos + (f.v)*dt
                        f.v = f.v + 10*g*dt
            for r in rescue:
                rate(50)
                r.color = c

            for b in boss:
                rate(50)
                b.color = c
        t+=1
        
    tprint("Cycles: " + str(t/dt))
                              
    n +=1

    if not override:
        startit = False
        while not startit:
            rate(100)
        startit = False
        reset()

print
print "Game over."

exit()


