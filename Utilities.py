import pygame

class TextWriter():
    def __init__(self, font, font_size, color= (255, 255, 255)):
        self.typer = pygame.font.Font(font, font_size)
        self.color = color
        self.t = 1
        self._color = [int(255/20 * c) for c in range(0, 21)]
        self._color = self._color + [self._color[i] for i in range(19, 0, -1)]
        
    def reset(self):
        self.t = 1
        
    def just_write(self, msg, pos, win, align= 0):
        ''' align: 0-left, 1-center, 2-right'''
        info = self.typer.render(msg, 1, self.color)
        if align == 0:
            win.blit(info, (pos[0], pos[1]))
        elif align == 1:
            win.blit(info, (pos[0] - info.get_width()/2, pos[1]))
        else:
            win.blit(info, (pos[0] - info.get_width(), pos[1]))        
        
    def write(self, msg, pos, win, c_frame, T= 60):
        ln = len(msg)
        freq = T // ln
        
        info = self.typer.render(msg[:self.t], 1, self.color)
        win.blit(info, (pos[0], pos[1]))
        
        self.t = self.t + 1 if ln > self.t and c_frame % freq == 0 else self.t
        
    def write_pulsing(self, msg, pos, win, c_frame, freq= 5):
        '''pos is from the center'''
        txt_color = [self._color[int(c_frame/freq) % len(self._color)] for _ in range(3)]
        info = self.typer.render(msg, 1, txt_color)
        win.blit(info, (pos[0] - info.get_width()/2, pos[1]))
