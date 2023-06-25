import turtle
import random
import time


class SnakeGame:
    def __init__(self):
        self.flagStart = True
        self.__score = 0
        self.__speed = 5
        self.__screen = turtle.Screen()
        self.__screen.tracer(0)
        self.__screen.title('Snake')
        self.__screen.addshape("Snake_game/images/small_rocks.gif")
        self.__screen.addshape("Snake_game/images/food.gif")
        self.__screen.addshape("Snake_game/images/snake.gif")
        self.__screen.bgcolor("#2E9AFE")
        self.__screen.setup(width=1.0, height=1.0)

        self.__start_button = None
        self.__table = None
        self.__frame_turtle = None
        self.__snake = None
        self.__food = None
        self.__snakeImg = None
        self.__obstaclesList = []
        self.__bodyList = []

        self.__pen = turtle.Turtle()
        self.__pen.speed(0)
        self.__pen.color("green")
        self.__pen.pensize(1)
        self.__pen.penup()
        self.__pen.hideturtle()
        self.__pen.goto(0, self.__screen.window_height() / 2 - 80)

        # Snake movements
        self.__screen.listen()
        self.__screen.onkeypress(lambda: setattr(self.__snake, 'direction', 'up'), 'Up')
        self.__screen.onkeypress(lambda: setattr(self.__snake, 'direction', 'down'), "Down")
        self.__screen.onkeypress(lambda: setattr(self.__snake, 'direction', 'left'), "Left")
        self.__screen.onkeypress(lambda: setattr(self.__snake, 'direction', 'right'), "Right")
        self.__screen.onkeypress(lambda: setattr(self.__snake, 'direction', 'exit'), "x")

    def __randomLocation(self):
        x_min = int(-self.__screen.window_width() / 2 + 75)
        x_max = int(self.__screen.window_width() / 2 - 75)
        y_min = int(-self.__screen.window_height() / 2 + 140)
        y_max = int(self.__screen.window_height() / 2 - 130)
        x = 0
        y = 0
        while x == 0 and y == 0:
            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)
        return x, y

    # Increase snake speed
    def __increase_speed(self):
        self.__speed += 2
        self.__score += 10
        self.__pen.clear()
        self.__pen.write(f"Score: {self.__score}", align="center", font=("Courier", 34, "bold"))

    def __createFood(self):
        self.__food = turtle.Turtle()
        self.__food.speed(0)
        self.__food.shape("Snake_game/images/food.gif")
        self.__food.penup()
        self.__food.goto(0, 100)
        self.__screen.update()

    def __createButton(self, location: int, bColor: str, length: int, text: str) -> None:
        self.__frame_turtle.goto((self.__start_button.xcor()) - location,
                                 (self.__start_button.ycor() + 15) - 50 / 2)  # -65

        self.__frame_turtle.fillcolor(bColor)
        self.__frame_turtle.begin_fill()
        for _ in range(2):
            self.__frame_turtle.forward(length - 2 * 10)
            self.__frame_turtle.circle(10, 90)
            self.__frame_turtle.forward(50 - 2 * 10)
            self.__frame_turtle.circle(10, 90)
        self.__frame_turtle.end_fill()
        self.__start_button.write(text, align="center", font=("Arial", 20, "bold"))

    def __createBorder(self) -> None:
        self.__table = turtle.Turtle()
        self.__table.penup()
        self.__table.pensize(5)
        self.__table.goto(-650, -270)
        self.__table.pendown()
        self.__table.fillcolor("#585858")
        self.__table.begin_fill()
        for i in range(2):
            self.__table.forward(1290)
            self.__table.left(90)
            self.__table.forward(550)
            self.__table.left(90)
        self.__table.end_fill()

        self.__table.penup()
        self.__table.goto(-630, -250)
        self.__table.pendown()
        self.__table.fillcolor("#2E2E2E")
        self.__table.begin_fill()
        for i in range(2):
            self.__table.forward(1250)
            self.__table.left(90)
            self.__table.forward(510)
            self.__table.left(90)
        self.__table.end_fill()
        self.__table.hideturtle()

    # Add obstacles
    def __create_obstacles(self):
        for i in range(5):
            obstacle = turtle.Turtle()
            obstacle.speed(0)
            obstacle.shape("Snake_game/images/small_rocks.gif")
            obstacle.penup()
            obstacle.goto(self.__randomLocation()[0], self.__randomLocation()[1])
            self.__obstaclesList.append(obstacle)

    def __game_over(self):
        [self.__bodyList[body].hideturtle() for body in range(len(self.__bodyList))]
        [obstacle.hideturtle() for obstacle in self.__obstaclesList]

        self.__food.hideturtle()
        self.__table.clear()
        # self.__table = None
        self.__pen.clear()

        turtle.hideturtle()
        turtle.color("red")
        turtle.write("GAME OVER!", align="center", font=("Courier", 40, "bold"))
        self.__screen.update()
        time.sleep(3)  # Wait for 3 seconds
        turtle.clear()
        self.__screen.update()
        self.__start_button = turtle.Turtle()
        self.__start_button.penup()
        self.__start_button.hideturtle()
        self.__frame_turtle = turtle.Turtle()
        self.__frame_turtle.penup()
        self.__frame_turtle.hideturtle()

        self.__start_button.goto(-200, -200)
        self.__start_button.color("red")

        self.__createButton(65, "green", 150, "restart")

        self.__start_button.color("yellow")
        self.__start_button.goto(self.__start_button.xcor() + 200, self.__start_button.ycor())
        self.__createButton(40, "blue", 100, "exit")

        self.__start_button.color("#2E2E2E")
        self.__start_button.goto(self.__start_button.xcor() + 200, self.__start_button.ycor())
        self.__createButton(65, "#82FA58", 150, "continue")
        self.__screen.update()
        self.__screen.onscreenclick(self.__helperGameOver, btn=1, add=True)
        self.flagStart = False
        # self.__screen.mainloop()

    def __helperGameOver(self, x, y):
        print(x,y)
        self.flagStart = True
        self.__start_button.clear()
        self.__frame_turtle.clear()
        self.__start_button = None
        self.__frame_turtle = None
        if -274 <= x <= -127 and -209 <= y <= -160:
            self.__screen.onscreenclick(None)
            [self.__bodyList[body].clear() for body in range(len(self.__bodyList))]
            self.__snake = None
            self.__bodyList.clear()
            [obstacle.clear() for obstacle in self.__obstaclesList]
            self.__obstaclesList.clear()
            self.__food.clear()
            self.__food = None
            self.__score = 0  # Reset the score
            self.__speed = 5
            self.__screen.update()
            self.start()

        elif -50 <= x <= 48 and -209 <= y <= -160:
            self.__screen.bye()

        elif 125 <= x <= 273 and -209 <= y <= -160:
            self.__screen.onscreenclick(None)
            self.__createBorder()
            [self.__bodyList[body].showturtle() for body in range(len(self.__bodyList))]
            [obstacle.showturtle() for obstacle in self.__obstaclesList]
            self.__food.showturtle()
            self.__snake.goto(0, 0)

            if len(self.__bodyList) > 1:
                for i in range(1, len(self.__bodyList)):
                    self.__bodyList[i].goto(0, self.__bodyList[i-1].ycor()-7)

            self.__snake.direction = "stop"
            self.__pen.write(f"Score: {self.__score}", align="center", font=("Courier", 34, "bold"))
            self.__screen.update()
            self.__start_game()


    # Checks the collision of the snake with food
    def __check_collision(self):
        distance = self.__snake.distance(self.__food)
        if distance < 20:
            if self.__speed % 3 == 0:
                [i.goto(self.__randomLocation()[0], self.__randomLocation()[1]) for i in self.__obstaclesList]

            self.__food.goto(self.__randomLocation()[0], self.__randomLocation()[1])
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("green")
            new_segment.penup()
            self.__bodyList.append(new_segment)
            self.__increase_speed()

    def __move(self):
        if self.__snake.direction == "stop":
            pass
        else:
            [self.__bodyList[i].goto(self.__bodyList[i - 1].xcor(), self.__bodyList[i - 1].ycor()) for i in
         range(len(self.__bodyList) - 1, 0, -1)]
        # print(self.__snake.position(), "snake", [i.position() for i in self.__bodyList])
            if len(self.__bodyList) > 0:
                self.__bodyList[0].goto(self.__snake.xcor(), self.__snake.ycor())

        if self.__snake.direction == "up":
            self.__snake.sety(self.__snake.ycor() + self.__speed)
        if self.__snake.direction == "down":
            self.__snake.sety(self.__snake.ycor() - self.__speed)
        if self.__snake.direction == "left":
            self.__snake.setx(self.__snake.xcor() - self.__speed)
        if self.__snake.direction == "right":
            self.__snake.setx(self.__snake.xcor() + self.__speed)

    def start(self):
        self.__start_button = turtle.Turtle()
        self.__start_button.penup()
        self.__start_button.hideturtle()
        self.__start_button.goto(0, -200)

        self.__frame_turtle = turtle.Turtle()
        self.__frame_turtle.penup()
        self.__frame_turtle.hideturtle()

        self.__start_button.shapesize(2, 2)
        self.__createButton(89, "green", 200, "Start")

        self.__snakeImg = turtle.Turtle()
        self.__snakeImg.penup()
        self.__snakeImg.goto(0, 20)
        self.__snakeImg.pendown()
        self.__snakeImg.shape("Snake_game/images/snake.gif")
        self.__screen.update()
        self.__screen.onscreenclick(self.__helperStart_game, btn=1, add=True)
        self.__screen.mainloop()

    def __helperStart_game(self, x, y):
        if self.__start_button.distance(x, y) < 50:
            self.__screen.onscreenclick(None)
            self.__frame_turtle.clear()
            self.__start_button.clear()
            self.__snakeImg.hideturtle()
            self.__snakeImg = None

            self.__snake = turtle.Turtle()
            self.__snake.speed(0)
            self.__snake.shape("square")
            self.__snake.color("black")
            self.__snake.penup()
            self.__snake.goto(0, 0)
            self.__snake.direction = "stop"
            self.__bodyList.append(self.__snake)

            self.__createBorder()
            self.__createFood()
            self.__create_obstacles()
            self.__pen.write(f"Score: {self.__score}", align="center", font=("Courier", 34, "bold"))
            self.__start_game()

    def __start_game(self):
        while self.flagStart:

            self.__screen.update()

            if self.__snake is not None:
                if self.__snake.direction == "exit":
                    break

                self.__move()
                time.sleep(.1)

                if self.__check_collision():
                    pass

                for obstacle in self.__obstaclesList:
                    if self.__snake.distance(obstacle) < 20:
                        print("boom")
                        self.__game_over()

                if self.__snake is not None and self.__snake.xcor() > self.__screen.window_width() / 2 - 70 or self.__snake.xcor() < -self.__screen.window_width() / 2 + 60 or self.__snake.ycor() > self.__screen.window_height() / 2 - 120 or self.__snake.ycor() < -self.__screen.window_height() / 2 + 130:
                    print("over the screen")
                    self.__game_over()
                body_positions = [body.position() for body in self.__bodyList]
                if self.__snake.position() in body_positions[1:]:
                    print(body_positions)
                    self.__game_over()


game = SnakeGame()
game.start()
