# Sam Bernstein (C) 2014-2015

from visual import *

txt_size = 12
line_len = 40
txt_wid = .5*txt_size*line_len - 70

txt_spacing = 2*txt_size + 20

window = display(x = 0, width = 600, center = (0,0,0), range = .38*txt_size*line_len)

# These while loops break up the text into lines
words = 'Placeholder text. Type quickly. The consortium of sponge manufacturers work through the wall of time. Make a spaceship by reinventing the wheel. Have pity for the clueless. The nine dwarfs teamed up to jump over the yellow brick wall. Ten computers danced until the morning sun. I did not ask for cheese in this salad.'
test_lines = [] # these are fixed for each round

start = 0
end = 0

line = 0  # starts at first line
while start < len(words) - 1: # this loop takes one long string and breaks it up into individual lines
    
    while end < len(words) - 1:
        if end - start > line_len and words[end] == ' ':
            break
        end += 1
        
    test_lines.append(text(text = words[start:end+1], pos = (-txt_wid, -line*txt_spacing, 0), align = 'left', height = txt_size, color = color.white))
    
    start = end + 1
    line += 1

num_lines = len(test_lines)
print "number of lines", num_lines


user_lines = [] # what the user types
for new_line in range(num_lines): # initialize all the user's lines
    user_lines.append(text(text = '', pos = (-txt_wid, -(new_line + .5)*txt_spacing, 0), align = 'left', height = txt_size, color = color.green))
print "user_lines initiated"

line = 0

def keyInput(evt): # for handling user typing
    global line
    global user_lines
    global test_lines
    global matches

##    print "Line: ", line
    
    s = evt.key
    if len(s) == 1 and not (line == len(test_lines) and len(user_lines[line].text) >= len(test_lines[line].text)): # checks that user hasn't reached end
        if len(user_lines[line].text) >= len(test_lines[line].text): # if at end of line, add new line
            line += 1
            window.center.y = user_lines[line].pos.y
        user_lines[line].text += s # append new character to new line
        
        window.center.y += -txt_spacing/(len(test_lines[line].text)) # for continuous scrolling
    elif (s == 'backspace' or s == 'delete') and len(user_lines[0].text) > 0:
        if len(user_lines[line].text) == 0: # if at beginning of line, subtract one line
            line -= 1
            window.center.y = user_lines[line].pos.y
          
        if evt.shift:
            user_lines[line].text = '' # erase all text
        else:
            user_lines[line].text = user_lines[line].text[:-1] # erase letter
            window.center.y += txt_spacing/(len(test_lines[line].text))

    matches = True
    for f in range(line):
        if user_lines[f].text != test_lines[f].text:
            matches = False
    if user_lines[line].text != test_lines[line].text[:len(user_lines[line].text)]:
        matches = False
            
    

window.bind('keydown', keyInput)


round_over = False

matches = True
# this is the main game loop
while True:
    line = 0
    
    while not round_over:
        rate(100)

        if matches:
            for r in user_lines:
                r.color = color.green
        else:
            for r in user_lines:
                r.color = color.red
        


        



        
    

