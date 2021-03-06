from tkinter import *
import random
import time
from tkinter import messagebox as mb
class Game:
    def __init__(self):
        self.t = Tk()
        self.t.title('Game - Stickman go out')
        self.t.resizable(0, 0)
        self.t.wm_attributes("-topmost", 1)
        self.c = Canvas(self.t, width = 500, height = 500, bd = 0, highlightthickness=0)
        self.c.pack()
        self.t.update()
        self.c_height = 500
        self.c_width = 500
        self.bg = PhotoImage(file="background.gif")
        width = self.bg.width()
        height = self.bg.width()
        for x in range (0, 5):
            for y in range (0, 5):
                self.c.create_image(y*height, x*width, image = self.bg, anchor = "nw")
        self.sprites = []
        self.running = True
    def mainloop(self):
        while 1:
            g.c.create_text(365,10, text = 'Двері закриються через ' +str(round(120 - (time.time() - time1),2)) + ' секунд', font = ('semibold', 11), tag = 'times')
            if self.running == True:
                for sprite in self.sprites:
                    sprite.move()
            self.t.update_idletasks()
            self.t.update()
            time.sleep(0.01)
            if time.time() - time1 > 120.00:
                g.c.delete('times')
                self.running = False
                mb.showinfo("You Lost","Game Over")
                break
            elif time.time() - time1 < 120.00 and self.running == True:
                g.c.delete('times')
                g.c.create_text(365,10, text = 'Двері закриються через ' +str(round(120 - (time.time() - time1),2)) + ' секунд', font = ('semibold', 11), tag = 'times')
            elif self.running == False:
                g.c.delete('times')
                break
                

class Coords:
    def __init__(self, x1 = 0, y1 = 0, x2 = 0, y2 = 0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class Sprite:
    def __init__(self, game):
        self.game =  game
        self.end = False
        self.coordinates = None
    def move(self):
        pass
    def coords(self):
        return self.coordinates

class Platform(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.c.create_image(x, y, image=self.photo_image, anchor='nw')
        self.coordinates = Coords(x, y, x + width, y + height)

class BotPlatform(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Platform.__init__(self, game, photo_image, x, y, width, height)
        self.time = time.time()
        speed = [-10, 10]
        random.shuffle(speed)
        self.x = speed[0]
        self.width = width
        self.height = height
        self.canvas_width = self.game.c.winfo_width()
    def coords(self):
        pos = self.game.c.coords(self.image)
        self.coordinates.x1 = pos[0]
        self.coordinates.y1 = pos[1]
        self.coordinates.x2 = pos[0] + self.width
        self.coordinates.y2 = pos[1] + self.height
        return self.coordinates
    def move(self):
        if time.time() - self.time > 0.3:
            pos = self.game.c.coords(self.image)
            self.game.c.move(self.image, self.x, 0)
            if pos [0] <= 0:
                self.x = random.randint(1, 3)
            elif pos[0] + self.width >= self.canvas_width:
                self.x = random.randint(-3, -1)
    
    

class Door(Sprite):
    def __init__(self, game, x, y, width, height):
        Sprite.__init__(self, game)
        self.c_door = PhotoImage(file="d_close.gif")
        self.o_door = PhotoImage(file="d_open.gif")
        self.image = game.c.create_image(x, y, image=self.o_door, anchor='nw')
        self.coordinates = Coords(x, y, x + (width / 3), y + height)
        self.end = True
        
    def cdoor(self):
        self.game.c.itemconfig(self.image, image=self.c_door)
        self.game.t.update_idletasks()
            
            

class Stickman(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.images_left = [
            PhotoImage(file="figure_L1.gif"),
            PhotoImage(file="figure_L2.gif"),
            PhotoImage(file="figure_L3.gif")
        ]
        self.images_right = [
            PhotoImage(file="figure_R1.gif"),
            PhotoImage(file="figure_R2.gif"),
            PhotoImage(file="figure_R3.gif")
        ]
        self.image_stand = PhotoImage(file="st_stand.gif")
        self.image = game.c.create_image(200, 470, image=self.image_stand, anchor='nw')
        self.x = 0
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()
        game.c.bind_all('<KeyPress-Left>',self.turn_left)
        game.c.bind_all('<KeyPress-Right>',self.turn_right)
        game.c.bind_all('<space>',self.jump)
        game.c.bind_all('<KeyPress-Down>',self.turn_down)
        
    def turn_down(self, evt):
        if self.y == 0:
            self.x = 0
    def turn_left(self, evt):
        if self.y == 0:
            self.x = -2
    def turn_right(self, evt):
        if self.y == 0:
            self.x = 2
    def jump(self, evt):
        if self.y == 0:
            self.y = -4
            self.jump_count = 0

    def animate(self):
        if self.y == 0 and self.x !=0:
            if time.time() - self.last_time > 0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
        if self.x == 0:
            if self.y == 0:
                self.game.c.itemconfig(self.image, \
                        image=self.image_stand)
            elif self.y != 0:
                self.game.c.itemconfig(self.image, \
                        image=self.images_left[2])
                
        if self.x < 0:
            if self.y != 0:
                self.game.c.itemconfig(self.image, \
                        image=self.images_left[2])
            else:
                self.game.c.itemconfig(self.image, \
                        image=self.images_left[self.current_image])
        elif self.x > 0:
            if self.y != 0:
                self.game.c.itemconfig(self.image, \
                        image=self.images_right[2])
            else:
                self.game.c.itemconfig(self.image, \
                        image=self.images_right[self.current_image])

    def coords(self):
        pos = self.game.c.coords(self.image)
        self.coordinates.x1 = pos[0]
        self.coordinates.y1 = pos[1]
        self.coordinates.x2 = pos[0] + 27
        self.coordinates.y2 = pos[1] + 30
        return self.coordinates
    
    def move(self):
        self.animate()
        if self.y < 0:
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = 4
        if self.y > 0:
            self.jump_count -= 1
        cord = self.coords()
        self.id = 0
        left = True
        right = True
        top = True
        bottom =True
        falling = True
        if self.y > 0 and cord.y2 >= self.game.c_height:
            self.y = 0
            bottom = False
        elif self.y < 0 and cord.y1 <= 0:
            self.y = 0
            top = False
        if self.x > 0 and cord.x2 >= self.game.c_width:
            self.x = 0
            right = False
        elif self.x < 0 and cord.x1 <= 0:
            self.x = 0
            left = False
        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_cord = sprite.coords()
            if top and self.y < 0 and collided_top(cord, sprite_cord):
                self.y = -self.y
                top = False
            if bottom and self.y > 0 and collided_bottom(self.y, cord, sprite_cord):
                self.y = sprite_cord.y1 - cord.y2
                if self.y < 0:
                    self.y = 0
                bottom = False
                top = False
            if bottom and falling and self.y == 0 and cord.y2 < self.game.c_height and collided_bottom(1, cord, sprite_cord):
                falling = False
            if left and self.x < 0 and collided_left(cord, sprite_cord):
                self.x = 0
                left = False
                if sprite.end:
                    self.game.running = False
                    time.sleep(0.2)
                    self.game.c.itemconfig(self.image, state='hidden')
                    time.sleep(0.2)
                    sprite.cdoor()
                    mb.showinfo("Congratulations","You won")
            if right and self.x > 0 and collided_right(cord, sprite_cord):
                self.x = 0
                right = False
                if sprite.end:
                    self.game.running = False
                    self.game.c.itemconfig(self.image, state='hidden')
                    time.sleep(0.3)
                    sprite.cdoor()
                    mb.showinfo("Congratulations","You won")
        if falling and bottom and self.y == 0 and cord.y2 < self.game.c_height:
            self.y = 4
        self.game.c.move(self.image, self.x, self.y)

def  within_x(c1, c2):
    if (c1.x1 > c2.x1 and c1.x1 < c2.x2) \
       or (c1.x2 > c2.x1 and c1.x2 < c2.x2)\
       or (c2.x1 > c1.x1 and c2.x1 < c1.x2)\
       or (c2.x2 > c1.x1 and c2.x2 < c1.x2):
        return True
    else:
        return False

def  within_y(c1, c2):
    if (c1.y1 > c2.y1 and c1.y1 < c2.y2) \
       or (c1.y2 > c2.y1 and c1.y2 < c2.y2)\
       or (c2.y1 > c1.y1 and c2.y1 < c1.y2)\
       or (c2.y2 > c1.y1 and c2.y2 < c1.y2):
        return True
    else:
        return False

def collided_left(c1, c2):
    if within_y(c1, c2):
        if c1.x1 <= c2.x2 and c1.x1 >= c2.x1:
            return True
    return False

def collided_right(c1, c2):
    if within_y(c1, c2):
       if c1.x2 >= c2.x1 and c1.x2 <= c2.x2:
            return True
    return False

def collided_top(c1, c2):
    if within_x(c1, c2):
        if c1.y1 <= c2.y2 and c1.y1 >= c2.y1:
            return True
    return False

def collided_bottom(y, c1, c2):
    if within_x(c1, c2):
        y_calc = c1.y2 + y
        if y_calc >= c2.y1 and y_calc <= c2.y2:
            return True
    return False


    
g = Game()
time1 = time.time()
g.c.create_text(250, 250, text='Нажміть пробіл щоб почати гру', font= ('Candara', 25, 'bold'), tag = 'txt_start')
def startgame(event):
    if event.keysym == 'space':
        g.c.delete('txt_start')
        plat1 = Platform(g, PhotoImage(file='platform2.gif'),\
            40, 480, 66, 10)
        plat2 = BotPlatform(g, PhotoImage(file='platform.gif'),\
            150, 440, 100, 10)
        plat3 = Platform(g, PhotoImage(file='platform.gif'),\
            300, 400, 100, 10)
        plat4 = Platform(g, PhotoImage(file='platform.gif'),\
            300, 160, 100, 10)
        plat5 = Platform(g, PhotoImage(file='platform2.gif'),\
            175, 350, 66, 10)
        plat6 = Platform(g, PhotoImage(file='platform2.gif'),\
            50, 300, 66, 10)
        plat7 = BotPlatform(g, PhotoImage(file='platform2.gif'),\
            170, 120, 66, 10)
        plat8 = Platform(g, PhotoImage(file='platform2.gif'),\
            45, 60, 66, 10)
        plat9 = Platform(g, PhotoImage(file='platform3.gif'),\
            170, 250, 33, 10)
        plat10 = Platform(g, PhotoImage(file='platform3.gif'),\
            230, 200, 33, 10)
        stickman = Stickman(g)
        door = Door(g, 50, 30, 45, 35)
        g.sprites.append(plat1)
        g.sprites.append(plat2)
        g.sprites.append(plat3)
        g.sprites.append(plat4)
        g.sprites.append(plat5)
        g.sprites.append(plat6)
        g.sprites.append(plat7)
        g.sprites.append(plat8)
        g.sprites.append(plat9)
        g.sprites.append(plat10)
        g.sprites.append(stickman)
        g.sprites.append(door)
        g.mainloop()
        
g.c.bind_all('<KeyPress-space>', startgame)

   
