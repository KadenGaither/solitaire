import pygame
from components import Screen
import random


class MouseCard():
    def __init__(self):
        self.subs = []
        self.hold = False
        self.prev = (0,0)
        self.curr = (0,0)
    def add_sub(self, value):
        self.subs.append(value)
    def notify_up(self):
        self.hold = False
        for sub in self.subs:
            sub.get_notified_up(self.prev,self.curr)
    def notify_down(self):
        self.hold = True
        for sub in self.subs:
            sub.get_notified_down(self.prev)
    def set_prev(self,value):
        self.prev = value
    def set_curr(self,value):
        self.curr = value

class Card():
    def __init__(self, value, z_axis=0):
        self.value = value
        self.color = (240,240,200)
        self.x = 50
        self.y = 50
        self.z = z_axis
        self.width = 34
        self.height = 50
        self.fixed = False
        self.face_up = True
        self.able_to_drag = False
        self._curr_down = None
        self._if_mouse_moved = True
        self._font = pygame.font.Font("freesansbold.ttf",20)
        self._facedown_color = (40,40,190)
        self._accent_color = (40,40,40) if self.value[1]=="clubs"or self.value[1]=="spades"else (190,40,40)
        self._text = self._font.render(self.value[0]+self.value[1][0],True,self._accent_color)
        self._textrect = self._text.get_rect()
    
    def set_z(self, value:int):
        self.z = value

    def get_notified_up(self, prev, curr):
        if self.check_mouse(prev):
            if self._curr_down == prev == curr:
                self.face_up = not self.face_up if not self.fixed else self.face_up

    def get_notified_down(self, prev):
        self._curr_down = prev
        if self.fixed:
            self.able_to_drag = False
            return
        if self.check_mouse(prev):
            self.able_to_drag = True
        else:
            self.able_to_drag = False

    def check_mouse(self, prev_mouse):
        return (prev_mouse[0] > self.x and prev_mouse[0] < (self.width+self.x) and prev_mouse[1] > self.y and prev_mouse[1] < (self.height+self.y))

    def drag(self, prev_mouse, mouse_pos, hold):
        if self.check_mouse(prev_mouse):
            if hold: 
                if self.able_to_drag:
                    mp = (mouse_pos[0]-prev_mouse[0],mouse_pos[1]-prev_mouse[1])
                    self.x += mp[0]
                    self.y += mp[1]

    def show(self):
        pygame.draw.rect(Screen.screen, self.color, [self.x,self.y,self.width,self.height])
        if self.face_up:
            pygame.draw.rect(Screen.screen, self._accent_color, [self.x,self.y,self.width,self.height], 2)
            self._textrect.center = ((self.x+self.width/2),self.y+self.height/2)
            Screen.screen.blit(self._text, self._textrect)
        else:
            pygame.draw.rect(Screen.screen, self._facedown_color, [self.x,self.y,self.width,self.height], 2)



class MagnetStack():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.radius = 5
    
    def check_card(self, card):
        if (card.x+card.width)//2 > self.x-self.radius and (card.x+card.width)//2 < self.x+self.radius:
            if (card.y+card.height)//2 > self.y-self.radius and (card.y+card.height)//2 < self.y+self.radius:
                card.x = self.x
                card.y = self.y


class Deck():
    def __init__(self):
        self.suits = ("hearts","clubs","diamonds","spades")
        self.numbers = ("a","2","3","4","5","6","7","8","9","10","j","q","k")
        self.deck = [Card((self.numbers[i],self.suits[j])) for j in range(len(self.suits)) for i in range(len(self.numbers))]
        for i in range(52):
            self.deck[i].set_z(i+1)
        self.ordered_deck = tuple(self.deck)

    def fiftytwo_pickup(self):
        for c in self.deck:
            print(c.z)
            c.x = random.randint(0,Screen.SCREENWIDTH-c.width)
            c.y = random.randint(0,Screen.SCREENHEIGHT-c.height)
    
    def grid_display(self):
        places = [(i,j) for j in range(4) for i in range(13)]
        for i in range(len(self.deck)):
            self.deck[i].x *= places[i][0]
            self.deck[i].y *= places[i][1]
