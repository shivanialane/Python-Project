import pygame
import math
import copy
import time
import random
from pygame.time import Clock
from pygame.event import get as get_events
from pygame import QUIT, Color, MOUSEBUTTONUP, MOUSEBUTTONDOWN
from pygame.draw import circle as draw_circle

pygame.init()
# These two functions are used for check the route whether a ball can be moved
def check_valid(mg, x, y):
    if x >= 0 and x < len(mg) and y >= 0 and y < len(mg[0]) and mg[x][y] == 1:
        return True
    else:
        return False
def process(step):
    # Checking the next point that cannot reach.
    change_records = []
    for i in range(len(step) - 1):
        if (abs(step[i][0] - step[i + 1][0]) == 0 and 
            abs(step[i][1] - step[i + 1][1]) == 1) or \
                        (abs(step[i][0] - step[i + 1][0]) == 1 
                        and abs(step[i][1] - step[i + 1][1]) == 0):
            pass
        else:
            change_records.append(i + 1)
    clip_nums = []
    for i in change_records:
        for j in range(i):
            if (abs(step[j][0] - step[i][0]) == 0 and 
                abs(step[j][1] - step[i][1]) == 1) or \
                        (abs(step[j][0] - step[i][0]) == 1 and 
                        abs(step[j][1] - step[i][1]) == 0):
                break
        clip_nums.append((j, i))
    record = []
    for i in clip_nums[::-1]:
        if not (i[0] in record or i[1] in record):
            step = step[:i[0] + 1] + step[i[1]:]
        record += list(range(i[0], i[1]))
step = []
def walk(mp, x, y, a, b):
    global step
    if x == a and y == b:
        step.append((x, y))
        process(step)
        return 1
    if check_valid(mp, x, y):
        step.append((x, y))
        mp[x][y] = 2
        switch = walk(mp, x, y + 1, a, b)
        if switch == 1:
            return 1
        switch = walk(mp, x, y - 1, a, b)
        if switch == 1:
            return 1
        switch = walk(mp, x - 1, y, a, b) 
        if switch == 1:
            return 1
        switch = walk(mp, x + 1, y, a, b)
        if switch == 1:
            return 1
# The below  functions are used for check whether 5 or more same color balls
def rowcheck(matrix):
    # rowcheck() is used for check all the rows of our game map
    newcolumnlist = []
    for row in range(9):
        column = 0
        rowcount = 0
        columncount = 0
        columnlist = []
        zu = (row, column)
        columnlist.append(zu)
        for i in range(8):
            if matrix[row][column] == matrix[row][column + 1]:
                rowcount += 1
                zu = (row, column + 1)
                columnlist.append(zu)
            if matrix[row][column] != matrix[row][column + 1] and rowcount < 4:
                rowcount = 0
                columnlist = []
                zu = (row, column + 1)
                columnlist.append(zu)
            if matrix[row][column] != matrix[row][column + 1] and rowcount >= 4:
                break
            column += 1
        if rowcount >= 4:
            for i in columnlist:
                newcolumnlist.append(i)
        row += 1
    return(newcolumnlist)
def columncheck(matrix):
    # columncheck() using same way of rowcheck().
    newrowlist = []
    for column in range(9):
        row = 0
        columncount = 0
        rowlist = []
        zu = (row, column)
        rowlist.append(zu)
        for i in range(8):
            if matrix[row][column] == matrix[row + 1][column]:
                columncount += 1
                zu = (row+1, column)
                rowlist.append(zu)
            elif matrix[row][column] != matrix[row + 1][column] and columncount < 4:
                columncount = 0
                rowlist = []
                zu = (row + 1, column)
                rowlist.append(zu)
            elif matrix[row][column] != matrix[row + 1][column] and columncount >= 4:
                break
            row += 1
        if columncount >= 4:
            for i in rowlist:
                newrowlist.append(i)
        column += 1
    return(newrowlist)
def left_sloping(matrix):
    # for checking the left diagnoals(from left top to right bottom)
    column = 0
    newleftslop = []
    for column in range(5):
        row = 0
        count = 0
        leftslop = []
        a = 0
        zu = ()
        if row == 0 and column == 0:
            a = 9
            zu = (0, 0)
        elif row == 0 and column == 1:
            a = 8
            zu = (0, 1)
        elif row == 0 and column == 2:
            a = 7
            zu = (0, 2)
        elif row == 0 and column == 3:
            a = 6
            zu = (0, 3)
        elif row == 0 and column == 4:
            a = 5
            zu = (0, 4)
        leftslop.append(zu)
        for i in range(a - 1):
                if matrix[row][column] == matrix[row + 1][column + 1]:
                    count += 1
                    zu = (row+1, column+1)
                    leftslop.append(zu)
                elif matrix[row][column] != matrix[row + 1][column + 1] and count < 4:
                    count = 0
                    leftslop = []
                    zu = (row + 1, column + 1)
                    leftslop.append(zu)
                elif matrix[row][column] != matrix[row + 1][column + 1] and count >= 4:
                    break
                row += 1
                column += 1
        if count >= 4:
            for i in leftslop:
                    newleftslop.append(i)
        column += 1
    column = 0
    row = 1
    a = 0
    leftslop = []
    for row in range(5):
        column = 0
        count = 0
        leftslop = []
        a = 0
        if row == 1 and column == 0:
            a = 8
            zu = (1, 0)
        elif row == 2 and column == 0:
            a = 7
            zu = (2, 0)
        elif row == 3 and column == 0:
            a = 6
            zu = (3, 0)
        elif row == 4 and column == 0:
            a = 5
            zu = (4, 0)
        leftslop.append(zu)
        for i in range(a - 1):
            if matrix[row][column] == matrix[row + 1][column + 1]:
                count += 1
                zu = (row + 1, column + 1)
                leftslop.append(zu)
            elif matrix[row][column] != matrix[row + 1][column + 1] and count < 4:
                count = 0
                leftslop = []
                zu = (row + 1, column + 1)
                leftslop.append(zu)
            elif matrix[row][column] != matrix[row + 1][column + 1] and count >= 4:
                break
            row += 1
            column += 1
        if count >= 4:
            for i in leftslop:
                newleftslop.append(i)
        row += 1
    return(newleftslop)


def right_sloping(matrix):
    # will check all the right diagonals (right top to left column).
    column = 8
    newrightslop = []
    columnlist = [8, 7, 6, 5, 4]
    for g in columnlist:
        row = 0
        count = 0
        rightslop = []
        a = 0
        zu = ()
        if row == 0 and g == 8:
            a = 9
            zu = (0, 8)
        elif row == 0 and g == 7:
            a = 8
            zu = (0, 7)
        elif row == 0 and g == 6:
            a = 7
            zu = (0, 6)
        elif row == 0 and g == 5:
            a = 6
            zu = (0, 5)
        elif row == 0 and g == 4:
            a = 5
            zu = (0, 4)
        rightslop.append(zu)
        column = g
        for i in range(a - 1):
            if matrix[row][column] == matrix[row + 1][column - 1]:
                count += 1
                zu = (row + 1, column - 1)
                rightslop.append(zu)
            elif matrix[row][column] != matrix[row + 1][column - 1] and count < 4:
                count = 0
                rightslop = []
                zu = (row + 1, column - 1)
                rightslop.append(zu)
            elif matrix[row][column] != matrix[row + 1][column - 1] and count >= 4:
                break
            row += 1
            column -= 1
        if count >= 4:
            for i in rightslop:
                newrightslop.append(i)
        column -= 1
    column = 8
    row = 1
    a = 0
    rightslop = []
    for row in range(5):
        column = 8
        count = 0
        rightslop = []
        a = 0
        if row == 1 and column == 8:
            a = 8
            zu = (1, 8)
        elif row == 2 and column == 8:
            a = 7
            zu = (2, 8)
        elif row == 3 and column == 8:
            a = 6
            zu = (3, 8)
        elif row == 4 and column == 8:
            a = 5
            zu = (4, 8)
        rightslop.append(zu)
        for i in range(a - 1):
            if matrix[row][column] == matrix[row + 1][column - 1]:
                count += 1
                zu = (row+1, column-1)
                rightslop.append(zu)
            elif matrix[row][column] != matrix[row + 1][column - 1] and count < 4:
                count = 0
                rightslop = []
                zu = (row + 1, column - 1)
                rightslop.append(zu)
            elif matrix[row][column] != matrix[row + 1][column - 1] and count >= 4:
                break
            row += 1
            column -= 1
        if count >= 4:
            for i in rightslop:
                newrightslop.append(i)
        row += 1
    return(newrightslop)
class Game:
    def __init__(self):
        # set for screen size
        self._height_ = 500
        self._width_ = 600
        # create window
        self._window_ = pygame.display.set_mode((self._width_, self._height_))
        self.create_window()
        self._ballmap_ = [[1 for i in range(9)] for j in range(9)]
        self._colormap_ = [[[] for i in range(9)] for j in range(9)]
        self._close_ = False
        self._clock_ = pygame.time.Clock()
        self._color_ = ['yellow', 'green', 'red', 'purple', 'brown', 'orange']
        self._mouse_pos_ = [0, 0]
        self._mouse_cond_ = 0
        self._last_ball_ = [0, 0]
        self._score_ = 0
    def create_window(self):
        pygame.display.set_caption("game")
        self.draw_grid()
        pygame.display.flip()
    def play_game(self):
        self.generate_ball()
        # update screen
        pygame.display.flip()
        while not self._close_:
            self._clock_.tick(30)
            self.events()
            # check for end game condition
            if self.end_game():
                # clear the screen and print 'Game over' in the screen
                self._window_.fill((0, 0, 0))
                self.message_display("Game over", self._width_/2, self._height_/2, 50)
                time.sleep(2)
                break
    def events(self):
        event_list = get_events()
        for event in event_list:
            self.single_event(event)
    def single_event(self, event):
        if event.type == QUIT:
            self._close_ = True
        elif event.type == MOUSEBUTTONUP:
            self._mouse_pos_[0], self._mouse_pos_[1] = event.pos
            self.move_ball()
            self.check_ball()
    def draw_grid(self):
        height = self._height_
        width = self._width_
        grid_h = height/11
        lines = [((grid_h, grid_h), (grid_h, height-grid_h)),
                 ((grid_h, grid_h), (height-grid_h, grid_h)),
                 ((grid_h, height-grid_h), (height-grid_h, height-grid_h)),
                 ((height-grid_h, grid_h), (height-grid_h, height-grid_h))]
        color = Color('white')
        for i in lines:
            pygame.draw.line(self._window_, color, i[0], i[1], 2)
        for i in range(8):
            pygame.draw.line(self._window_, color, 
                (grid_h*(i+2), grid_h), (grid_h*(i+2), height-grid_h))
            pygame.draw.line(self._window_, color, 
                (grid_h, grid_h*(i+2)), (height-grid_h, grid_h*(i+2)))
    def generate_ball(self):
        # generate_ball() generates 3 balls with random location
        array = [i for i in range(81)]
        for i in range(9):
            for j in range(9):
                if self._ballmap_[i][j] == 0:
                    array.remove(i * 9 + j)
        random_ball = [0, 0, 0]
        for i in range(3):
            random_ball[i] = random.choice(array)
            array.remove(random_ball[i])
            self._ballmap_[int(random_ball[i] / 9)][int(random_ball[i] % 9)] = 0
        for i in range(3):
            c = random.choice(self._color_)
            self._colormap_[int(random_ball[i] / 9)][int(random_ball[i] % 9)] = c
        self.draw_ball()
    def draw_ball(self):
        self._window_.fill((0, 0, 0))
        self.draw_grid()
        grid_h = self._height_/11
        for i in range(9):
            for j in range(9):
                if self._ballmap_[i][j] == 0:
                    draw_circle(self._window_, Color(self._colormap_[i][j]),
                                    (int((i+1.5) * grid_h), int((j+1.5) * grid_h)),
                                    int(grid_h/5 * 2))
        # draw score
        string = "Score: "+str(self._score_)
        width = self._height_ + (self._width_-self._height_) / 3
        self.message_display(string, width, grid_h, 25)
        # update the screen
        pygame.display.flip()
    def move_ball(self):
        grid_h = self._height_ / 11
        x_pos = self._mouse_pos_[0] - grid_h
        y_pos = self._mouse_pos_[1] - grid_h
        mou_pos = [int(x_pos / grid_h), int(y_pos / grid_h)]
        if mou_pos[0] > 8 or mou_pos[1] > 8:
            return
        if self._ballmap_[mou_pos[0]][mou_pos[1]] == 0:
            self._mouse_cond_ = 1
            self._last_ball_ = mou_pos
        elif self._ballmap_[mou_pos[0]][mou_pos[1]] == 1:
            if self._mouse_cond_ == 1:
                m = copy.deepcopy(self._ballmap_)
                m[self._last_ball_[0]][self._last_ball_[1]] = 1
                s = walk(m, self._last_ball_[0], self._last_ball_[1], 
                    mou_pos[0], mou_pos[1])
                if(s != 1):
                    return
                self._ballmap_[mou_pos[0]][mou_pos[1]] = 0
                self._ballmap_[self._last_ball_[0]][self._last_ball_[1]] = 1
                self._colormap_[mou_pos[0]][mou_pos[1]] = self._colormap_[self._last_ball_[0]][self._last_ball_[1]]
                self._colormap_[self._last_ball_[0]][self._last_ball_[1]] = []
                self._mouse_cond_ = 0
                self.draw_ball()
                time.sleep(0.2)
                if self.check_ball():
                    time.sleep(0.2)
                    self.generate_ball()
            else:
                pass

    def check_ball(self):
        s = 0
        c = columncheck(self._colormap_)
        for i in c:
            if(self._ballmap_[i[0]][i[1]] == 0):
                s = 1
                self._score_ += 2
            self._ballmap_[i[0]][i[1]] = 1
        c = rowcheck(self._colormap_)
        for i in c:
            if(self._ballmap_[i[0]][i[1]] == 0):
                s = 1
                self._score_ += 2
            self._ballmap_[i[0]][i[1]] = 1
        c = left_sloping(self._colormap_)
        for i in c:
            if(self._ballmap_[i[0]][i[1]] == 0):
                s = 1
                self._score_ += 2
            self._ballmap_[i[0]][i[1]] = 1
        c = right_sloping(self._colormap_)
        for i in c:
            if(self._ballmap_[i[0]][i[1]] == 0):
                s = 1
                self._score_ += 2
            self._ballmap_[i[0]][i[1]] = 1
        self.draw_ball()
        if s == 0:
            return True
    def end_game(self):
        s = 0
        for i in range(9):
            for j in range(9):
                if self._ballmap_[i][j] == 1:
                    s += 1
        if s > 3:
            return False
        else:
            return True
    def text_objects(self, text, font):
        textSurface = font.render(text, True, (255, 255, 255))
        return textSurface, textSurface.get_rect()

    def message_display(self, text, width, height, size):
        largeText = pygame.font.Font('freesansbold.ttf', size)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = ((width), (height))
        self._window_.blit(TextSurf, TextRect)
        pygame.display.update()
def main():
    game = Game()
    game.play_game()
    pygame.display.quit()
main()

