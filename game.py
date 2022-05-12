from email import generator
import pygame
from components import Screen
from card import *

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Cards")
    
    def _quit_game(self):
        pygame.quit()
        return None

    def run(self):
        m = MouseCard()
        d = Deck()
        d.fiftytwo_pickup()
        for i in range(len(d.deck)):
            m.add_sub(d.deck[i])

        func_dict = {
            pygame.MOUSEBUTTONUP: m.notify_up,
            pygame.MOUSEBUTTONDOWN: m.notify_down,
            pygame.QUIT : self._quit_game
        }
        
        while True:
            Screen.screen.fill(Screen.SCREENCOLOR)
            m.set_curr(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type in func_dict:
                    func_dict[event.type]()
            
            for stack in range(len(d.deck)):
                for c in range(stack):
                    d.deck[stack][c.z].show()
    
            #d.deck.function()

            pygame.display.flip()
            Screen.clock.tick(Screen.FPS)
            m.set_prev(m.curr)
