import pygame
from pygame.locals import *
import time
import threading
from network import Network
import pickle
pygame.font.init()


played = False
width = 700
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

#Rock Image
r_right = pygame.transform.smoothscale(pygame.image.load('.\\assets\\rock_right.png'), (230, 210))
r_left = pygame.transform.smoothscale(pygame.image.load('.\\assets\\rock_left.png'), (230, 210))

#Paper Image
p_right = pygame.transform.smoothscale(pygame.image.load('.\\assets\\paper_right.png'), (230, 210))
p_left = pygame.transform.smoothscale(pygame.image.load('.\\assets\\paper_left.png'), (230, 210))

#Scissors Image
s_right = pygame.transform.smoothscale(pygame.image.load('.\\assets\\scissors_right.png'), (230, 210))
s_left = pygame.transform.smoothscale(pygame.image.load('.\\assets\\scissors_left.png'), (230, 210))

#mainmenu Image
r_p_s = pygame.transform.smoothscale(pygame.image.load('.\\assets\\r_p_s.png'), (380, 350))

icon = pygame.image.load('.\\assets\\icon.jpg')
pygame.display.set_icon(icon)


smallfont = pygame.font.Font('.\\assets\\AtariClassic-gry3.ttf',23)
sfont = pygame.font.Font('.\\assets\\AtariClassic-gry3.ttf',12)
bigfont = pygame.font.Font('.\\assets\\AtariClassic-gry3.ttf',40)
t_rock = smallfont.render('Rock' , True , (255,255,255))
t_paper = smallfont.render('Paper' , True , (255,255,255))
t_scissors = smallfont.render('Scissors' , True , (255,255,255))
winlose = bigfont.render('tie' , True , (255,255,255))
text_rect = winlose.get_rect(center=(width/2, 100))
t_comp = sfont.render('Computer' , True , (255,255,255)) 
t_user = sfont.render('You' , True , (255,255,255))
t_again = smallfont.render('Try Again' , True , (255,255,255))
t_quit = smallfont.render('Quit' , True , (255,255,255))
clock = pygame.time.Clock()


def start_animation(duration):
    start_time = pygame.time.get_ticks()
    end_time = start_time + duration * 1000  # Convert duration to milliseconds

    while pygame.time.get_ticks() < end_time:
        screen.fill((0, 0, 0))  # Clear the screen
        for hand in hands:
            hand.draw(screen)
        pygame.display.flip()


class Button:
    def __init__(self, text, x, y, color,w,hw):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.hover_color = hw
        self.width = w
        self.height = 50
        self.is_hovered = False

    def draw(self, win):
        current_color = self.hover_color if self.is_hovered else self.color
        
        pygame.draw.rect(win, current_color, (self.x, self.y, self.width, self.height),0,4)
        pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, self.width, self.height), 3, 4)

        text = smallfont.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2), self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
        
    def update_hover_state(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        # Check if the mouse cursor is over the button
        self.is_hovered = self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height
           
    
btns = [Button("Rock", 50,520, (0,0,255),180,(0,0,230)), Button("Paper", 260,520, (0,255,0),180,(0,230,0)),Button("Scissor",470,520, (255,0,0),180,(230,0,0))]

startmenubtns =[Button("Start", 205,440, (100,100,100),200,(0,230,0)), Button("Quit",205,510, (100,100,100),200,(230,0,0))]
mainmenubtns =[Button("Join/Create Room", 95,470, (100,100,100),420,(0,230,0)), Button("Back",205,530, (100,100,100),200,(230,0,0))]
# input_rect = pygame.Rect(95, 400, 420, 50)
# user_text = ''
# color_active = pygame.Color('lightskyblue3')
# color_passive = pygame.Color('chartreuse4')
# color = color_passive
# active = False

def timer_function():
    time.sleep(2)
    global played  # Use the global run variable
    played = False

class hand:
    def __init__(self, image , pos):
        self.image = image
        self.pos = pos
        self.initial_pos = pos  # Store the initial position
        self.move_direction = 1  # 1 for moving down, -1 for moving up
        self.move_speed = 4
        
    def draw(self,screen):
        screen.blit(self.image,self.pos)

    def changeHand(self,image):
        screen.fill((0,0,0))
        self.image=image
    
    def move(self):
        
        # Update the position to create the up and down animation
        self.pos = (self.pos[0], self.pos[1] + self.move_speed * self.move_direction)

        # Change direction when reaching the top or bottom
        if self.pos[1] <= self.initial_pos[1] - 40:
            self.move_direction = 1
        elif self.pos[1] >= self.initial_pos[1] + 40:
            self.move_direction = -1
        
  
hands=[hand(r_left,(0,150)),hand(r_right,(470,150))]      

def mainGame():
    
    
    screen.fill((0,0,0))
    run = True
    while run:
    
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        
        for hand in hands:
            global played
            if played:
                hand.move()
            hand.draw(screen)
            
        for btn in btns:
            btn.draw(screen)
            btn.update_hover_state(mouse)

        pygame.display.update()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    if btn.click(mouse):
                        if(btn.text.lower() == "rock"):
                            
                            timer_thread = threading.Thread(target=timer_function)
                            timer_thread.start()
                            
                            played = True   
                            hands[0].changeHand(r_left)
                            print("Rock")
                            
                        elif(btn.text.lower() == "paper"):  
                            hands[0].changeHand(p_left)
                            print("Paper")
                        else:
                            hands[0].changeHand(s_left)
                            print("Scissor")


def mainmenu():
    n = Network()
    print(n.getP())
    input_rect = pygame.Rect(95, 400, 420, 50)
    user_text = ''
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    active = False
    screen.fill((0,0,0))
    run = True
    while run:
    
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        screen.blit(r_p_s,r_p_s.get_rect(center=(width/2, height/2-100)) )
        for btn in mainmenubtns:
            btn.draw(screen)
            btn.update_hover_state(mouse)
        
        pygame.display.update()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                    
                for btn in mainmenubtns:
                    if btn.click(mouse):
                        if(btn.text.lower() == "join/create room"):
                            reply = n.send(user_text)
                            print(reply)
                            pass
                            
                        elif(btn.text.lower() == "back"): 
                            run = False
            if event.type == pygame.KEYDOWN:
                        # Check for backspace
                        if event.key == pygame.K_BACKSPACE:
                            # get text input from 0 to -1 i.e. end.
                            user_text = user_text[:-1]
                        # Unicode standard is used for string
                        # formation
                        else:
                            user_text += event.unicode
        
        pygame.draw.rect(screen, color, input_rect,0,4)
        text_surface = smallfont.render(user_text, True, (255, 255, 255))
      
        # render at position stated in arguments
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
        
        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(100, text_surface.get_width()+10)
        pygame.display.flip()
    screen.fill((0,0,0))
    

def startWindow():
    screen.fill((0,0,0))
    run = True
    while run:
    
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        screen.blit(r_p_s,r_p_s.get_rect(center=(width/2, height/2-100)) )
        for btn in startmenubtns:
            btn.draw(screen)
            btn.update_hover_state(mouse)
        
        pygame.display.update()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in startmenubtns:
                    if btn.click(mouse):
                        if(btn.text.lower() == "start"):
                            
                            mainmenu()
                            
                            
                        elif(btn.text.lower() == "quit"):
                            pygame.quit() 
                            run = False
    
                       
startWindow()