import turtle
import time
import sys

size = 20
tower_width = 100
tower_height = 200
tower_radius = 10
tower_distance = 250
tower_altitude = -100

SPEED = 5

tower_loc = {
    "A": -1,
    "B": 0,
    "C": 1
}

tower_poles = {
    "A": [],
    "B": [],
    "C": []
}

FillColors = [
    "#d25b6a",
    "#d2835b",
    "#e5e234",
    "#83d05d",
    "#2862d2",
    "#35b1c0",
    "#5835c0"
]

 # iterative algorithm stack class method 
class Stack:
    def __init__(self, capacity):
        self.capacity = capacity
        self.top = -1
        self.array = [0]*capacity
        
def createStack(capacity):
    stack = Stack(capacity)
    return stack

def isFull(stack):
    return (stack.top == (stack.capacity - 1))

def isEmpty(stack):
    return (stack.top == -1 )

def push(stack, disk):
    if(isFull(stack)):
        return
    stack.top+=1
    stack.array[stack.top] = disk
    
def Pop(stack):
    if(isEmpty(stack)):
        return -sys.maxsize
    Top = stack.top
    stack.top-=1
    return stack.array[Top]




# Add a global variable to keep track of the steps
steps = 0


def set_plate(i):
    l = size * (i + 2)

    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    t.speed(0)

    t.left(90)
    t.begin_poly()
    t.forward(l)
    t.circle(size, 180)
    t.forward(l * 2)
    t.circle(size, 180)
    t.forward(l)
    t.end_poly()
    p = t.get_poly()

    turtle.register_shape("plate_%s" % i, p)




def set_tower():
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    t.speed(0)

    t.left(90)
    t.begin_poly()
    t.forward(tower_width)
    t.circle(tower_radius, 180)
    t.forward(tower_width - tower_radius)
    t.right(90)
    t.forward(tower_height)
    t.circle(tower_radius, 180)
    t.forward(tower_height)
    t.right(90)
    t.forward(tower_width - tower_radius)
    t.circle(tower_radius, 180)
    t.forward(tower_width)
    t.end_poly()
    p = t.get_poly()
    turtle.register_shape("tower", p)


def draw_towers():
    set_tower()
    tower = turtle.Turtle("tower")
    tower.speed(0)
    tower.penup()
    tower.goto(-tower_distance, tower_altitude)
    tower.stamp()
    tower.goto(0, tower_altitude)
    tower.stamp()
    tower.goto(tower_distance, tower_altitude)


def draw_plates(pn):
    plates = []
    for i in range(pn):
        set_plate(i)
        _p = turtle.Turtle('plate_%s' % i)
        _p.penup()
        _p.speed(SPEED)
        _colorIdx = i % len(FillColors)
        _color = FillColors[_colorIdx]
        _p.color(_color, _color)
        plates.append(_p)

    return plates

def draw_disks(pn):
    disks = []
    for i in range(pn):
        set_plate(i)
        _p = turtle.Turtle('plate_%s' % i)
        _p.penup()
        _p.speed(SPEED)
        _colorIdx = i % len(FillColors)
        _color = FillColors[_colorIdx]
        _p.color(_color, _color)
        disks.append(_p)

    return disks

def draw_move(plate, fromPole, toPole):
    global steps
    steps += 1

    to_x = tower_loc[toPole] * tower_distance
    toPole_count = len(tower_poles[toPole])
    to_y = tower_altitude + 2 * tower_radius + toPole_count * size * 2

    if fromPole:
        tower_poles[fromPole].remove(plate)
        from_x = tower_loc[fromPole] * tower_distance
        plate.goto(from_x, tower_height)
        plate.goto(to_x, tower_height)

    plate.goto(to_x, to_y)
    tower_poles[toPole].append(plate)


def draw_move2(src, dest, s, d, plates):
    pole1TopDisk = Pop(src)
    pole2TopDisk = Pop(dest)
 
    # When pole 1 is empty

    if (pole1TopDisk == -sys.maxsize):
        push(src, pole2TopDisk)
        moveTower2(d, s, plates[pole2TopDisk-1], src, dest)       
    
    # When pole2 pole is empty   
    elif (pole2TopDisk == -sys.maxsize):
        push(dest, pole1TopDisk)
        moveTower2(s, d, plates[pole1TopDisk-1], src, dest)
        
    # When top disk of pole1 > top disk of pole2
    elif (pole1TopDisk > pole2TopDisk):
        push(src, pole1TopDisk)
        push(src, pole2TopDisk)
        moveTower2(d, s, plates[pole2TopDisk-1], src, dest)
       
    # When top disk of pole1 < top disk of pole2
    else:
        push(dest, pole2TopDisk)
        push(dest, pole1TopDisk)
        moveTower2(s, d, plates[pole1TopDisk-1], src, dest)

def moveTower(height, fromPole, withPole, toPole, plates):
    if height == 1:
        draw_move(plates[0], fromPole, toPole)
    else:
        moveTower(height - 1, fromPole, toPole, withPole, plates)
        draw_move(plates[height - 1], fromPole, toPole)
        moveTower(height - 1, withPole, fromPole, toPole, plates)


def moveTower2(fromPeg, toPeg, plate, src, dest):
    global steps
    steps += 1

    to_x = tower_loc[toPeg] * tower_distance
    toPole_count = len(tower_poles[toPeg])
    to_y = tower_altitude + 2 * tower_radius + toPole_count * size * 2

    
    tower_poles[fromPeg].remove(plate)
    from_x = tower_loc[fromPeg] * tower_distance
    plate.goto(from_x, tower_height)
    plate.goto(to_x, tower_height)

    plate.goto(to_x, to_y)
    tower_poles[toPeg].append(plate)

    
        

def get_user_input():
    while True:
        num_plates = turtle.textinput("Number of Plates", "Enter the number of plates:")
        try:
            num_plates = int(num_plates)
            if num_plates == 1:
                turtle.textinput("Attention!!!", "Please enter a number other than 1.")
            else:
                return num_plates
        except ValueError:
            turtle.textinput("Please Enter a Valid Number", "Please enter a valid number.")
                    
def select_user_algorithm():
    while True:
        select_algorithm = turtle.textinput("select algorithm", "Enter the 0 for Recursive algorithm or enter 1 for Iterative algoritm")
        try:
            select_algorithm = int(select_algorithm)
            if  select_algorithm >= 2 or select_algorithm <= -1:
                turtle.textinput("Attention!!!", "Please enter number 1 or 0.")
            else:
                return select_algorithm
        except ValueError:
            turtle.textinput("Please Enter a Valid Number", "Please enter a valid number.")

def tohIterative(num_of_disks, src, aux, dest):
    s, d, a = 'A', 'B', 'C'
   
    # If number of disks is even, then interchange
    # destination pole and auxiliary pole
    if (num_of_disks % 2 == 0):
        temp = d
        d = a
        a = temp
    total_num_of_moves = int(pow(2, num_of_disks) - 1)
   
    # Larger disks will be pushed first
    for i in range(num_of_disks, 0, -1):
        push(src, i)
   
    for i in range(1, total_num_of_moves + 1):
        if (i % 3 == 1):
            draw_move2(src, dest, s, d, plates)
   
        elif (i % 3 == 2):
            draw_move2(src, aux, s, a, plates)
   
        elif (i % 3 == 0):
            draw_move2(aux, dest, a, d, plates)

if __name__ == '__main__':
    draw_towers()

    # Get user input for the number of plates
    n = get_user_input()
    f = select_user_algorithm()
    plates = draw_plates(n)
    
    src = createStack(n)
    dest = createStack(n)
    aux = createStack(n)

    # Measure the execution time
    start_time = time.time()

    for i in range(n):
        draw_move(plates[n - 1 - i], '', 'A')
    
    if f == 0:
        moveTower(n, 'A', 'B', 'C', plates)
    else:
        tohIterative(n, src, aux, dest)

    # Display the number of steps taken
    turtle.penup()
    turtle.goto(0, -150)
    turtle.write(f"Number of steps: {steps}", align="center", font="16")

    # Display the execution time
    end_time = time.time()
    execution_time = end_time - start_time
    turtle.penup()
    turtle.goto(0, -180)
    turtle.write(f"Execution time: {execution_time:.6f} seconds", align="center", font="16")

    turtle.done()
