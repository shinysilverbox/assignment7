# play.py
# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""

from datetime import time, datetime
import time
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):

        # initialize counter
        # TODO: Get this bigger, right color, etc., and get it to actually dynamically update
        self._seconds = ['3', '2', '1']
        self.seconds_count = 0

        # create bricks
        self._bricks = []
        # TODO: Why does the following line need 2x the offset?
        y = GAME_HEIGHT - 2 * BRICK_Y_OFFSET - BRICK_HEIGHT

        colors = [colormodel.RED, colormodel.ORANGE, colormodel.YELLOW,
                  colormodel.GREEN, colormodel.BLUE]
        current_color = 0
        row_counter = 0

        for i in range(BRICK_ROWS):

            # loop through the color array to change brick color every 2 rows
            if row_counter == 2:
                current_color += 1
                row_counter = 0
            if current_color == len(colors):
                current_color = 0

            # TODO: Fix left/right margins
            x = BRICK_SEP_H + (BRICK_WIDTH / 2.)
            for j in range(BRICKS_IN_ROW):
                # create a brick
                # GRectangle(x=0,y=0,width=10,height=10,fillcolor=colormodel.RED)
                brick = GRectangle()
                brick.x = x
                brick.y = y
                brick.width = BRICK_WIDTH
                brick.height = BRICK_HEIGHT
                brick.fillcolor = colors[current_color]
                self._bricks.append(brick)
                x += BRICK_WIDTH + BRICK_SEP_H

            y += BRICK_HEIGHT + BRICK_SEP_V
            row_counter += 1

        # create paddle
        paddle = GRectangle()
        paddle.x = GAME_WIDTH / 2.
        paddle.y = PADDLE_OFFSET + PADDLE_HEIGHT / 2.
        paddle.width = PADDLE_WIDTH
        paddle.height = PADDLE_HEIGHT
        paddle.fillcolor = colormodel.BLACK
        self._paddle = paddle

        # create ball
        x_pos = GAME_WIDTH / 2
        y_pos = GAME_HEIGHT / 2
        self._ball = Ball(x=x_pos, y=y_pos, width=BALL_DIAMETER, height=BALL_DIAMETER, fillcolor=colormodel.RED)

    def serve_ball(self):
        # alter velocity
        self._ball._vx = random.uniform(1.0, 5.0)
        self._ball._vx = self._ball._vx * random.choice([-1, 1])
        self._ball._vy = -5.0

    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL

    def move_paddle(self, dx):
        self._paddle.x += dx
        if self._paddle.left <= 0:
            self._paddle.x -= dx
        if self._paddle.right >= GAME_WIDTH:
            self._paddle.x -= dx

    def serve_ball(self):
        pass

    def move_ball(self):
        self._ball.x = self._ball.x + self._ball._vx
        self._ball.y = self.ball.y

    # DRAW METHOD TO DRAW THE PADDLE, BALL, AND BRICKS
    def draw_objects(self, view, state):
        # bricks
        for self.brk in self._bricks:
            self.brk.draw(view)

        # paddle
        self._paddle.draw(view)

        # countdown clock
        if self._counter is not None:
            number = GLabel(text=str(self._counter), x=GAME_WIDTH / 2., y=GAME_HEIGHT / 2., font_size=60)
            number.draw(view)

        # draw ball if in correct state
        if state == STATE_ACTIVE:
            self._ball.draw(view)

        # TODO delete this after figuring out how to draw things
        # create ball
        ball = GEllipse()
        ball.x = BALL_DIAMETER / 2
        ball.y = GAME_HEIGHT / 2
        ball.fillcolor = colormodel.RED
        ball._vx = 0
        ball._vy = 0
        ball.draw(view)


        # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION

        # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
