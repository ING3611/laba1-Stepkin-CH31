import turtle
import time
import random


WIDTH, HEIGHT = 600, 600
INITIAL_DELAY = 0.1
score = 0
high_score = 0
game_paused = False
game_over = False


BG_COLOR = "#FFFDD0"  
BORDER_COLOR = "#800020"  
SNAKE_COLOR = "#800020"  
FOOD_COLOR = "#800020"  
TEXT_COLOR = "#800020"  
GAME_OVER_COLOR = "#800020"  


window = turtle.Screen()
window.title("змейка")
window.bgcolor(BG_COLOR)
window.setup(width=WIDTH, height=HEIGHT)
window.tracer(0)


border = turtle.Turtle()
border.speed(0)
border.color(BORDER_COLOR)
border.penup()
border.goto(-WIDTH/2 + 10, -HEIGHT/2 + 10)
border.pendown()
border.pensize(3)
for _ in range(4):
    border.forward(WIDTH - 20)
    border.left(90)
border.hideturtle()


head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color(SNAKE_COLOR)
head.penup()
head.goto(0, 0)
head.direction = "stop"


food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color(FOOD_COLOR)
food.penup()
food.goto(0, 100)


segments = []


score_display = turtle.Turtle()
score_display.speed(0)
score_display.color(TEXT_COLOR)
score_display.penup()
score_display.hideturtle()
score_display.goto(0, HEIGHT/2 - 40)
score_display.write("Счет: 0  Рекорд: 0", align="center", font=("Arial", 20, "bold"))


msg_display = turtle.Turtle()
msg_display.speed(0)
msg_display.color(TEXT_COLOR)
msg_display.penup()
msg_display.hideturtle()
msg_display.goto(0, 0)


def set_direction(direction):
    if not game_paused and not game_over:
        opposite_directions = {"up": "down", "down": "up", "left": "right", "right": "left"}
        if head.direction != opposite_directions[direction]:
            head.direction = direction

def toggle_pause():
    global game_paused
    if not game_over:
        game_paused = not game_paused
        msg_display.clear()
        if game_paused:
            msg_display.color(GAME_OVER_COLOR)
            msg_display.write("ПАУЗА", align="center", font=("Arial", 36, "bold"))

def restart_game():
    global score, high_score, delay, game_over, game_paused, segments
    
    head.goto(0, 0)
    head.direction = "stop"
    
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    
    score = 0
    delay = INITIAL_DELAY
    game_over = False
    game_paused = False
    
    msg_display.clear()
    score_display.clear()
    score_display.write(f"Счет: {score}  Рекорд: {high_score}", 
                       align="center", font=("Arial", 20, "bold"))
    
    food.goto(random.randint(-WIDTH//2 + 30, WIDTH//2 - 30),
              random.randint(-HEIGHT//2 + 30, HEIGHT//2 - 30))

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)


window.listen()
window.onkeypress(lambda: set_direction("up"), "Up")      
window.onkeypress(lambda: set_direction("up"), "w")       
window.onkeypress(lambda: set_direction("down"), "Down")  
window.onkeypress(lambda: set_direction("down"), "s")     
window.onkeypress(lambda: set_direction("left"), "Left")  
window.onkeypress(lambda: set_direction("right"), "Right") 
window.onkeypress(toggle_pause, "p")  
window.onkeypress(restart_game, "r")  


delay = INITIAL_DELAY

while True:
    window.update()
    
    if game_paused or game_over:
        continue
    
    if (abs(head.xcor()) > WIDTH/2 - 20 or abs(head.ycor()) > HEIGHT/2 - 20):
        game_over = True
        msg_display.color(GAME_OVER_COLOR)
        msg_display.write("ИГРА ОКОНЧЕНА", align="center", font=("Arial", 36, "bold"))
        msg_display.goto(0, -50)
        msg_display.write("Нажмите R для рестарта", align="center", font=("Arial", 20, "normal"))
    

    if head.distance(food) < 20:
        food.goto(random.randint(-WIDTH//2 + 30, WIDTH//2 - 30),
                 random.randint(-HEIGHT//2 + 30, HEIGHT//2 - 30))
        
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color(SNAKE_COLOR)
        new_segment.penup()
        segments.append(new_segment)
        
        delay = max(0.05, delay - 0.001)
        score += 10
        high_score = max(score, high_score)
        score_display.clear()
        score_display.write(f"Счет: {score}  Рекорд: {high_score}", 
                          align="center", font=("Arial", 20, "bold"))
    

    for i in range(len(segments)-1, 0, -1):
        segments[i].goto(segments[i-1].pos())
    
    if segments:
        segments[0].goto(head.pos())
    
    move()
    

    for segment in segments:
        if segment.distance(head) < 15:
            game_over = True
            msg_display.color(GAME_OVER_COLOR)
            msg_display.write("ИГРА ОКОНЧЕНА", align="center", font=("Arial", 36, "bold"))
            msg_display.goto(0, -50)
            msg_display.write("Нажмите R для рестарта", align="center", font=("Arial", 20, "normal"))
    
    time.sleep(delay)

window.mainloop()