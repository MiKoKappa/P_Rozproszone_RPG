import pygame
import math
from sockets import Sockets


class Player():
    width = height = 32

    def __init__(self, startx, starty, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.moving = 0
        self.stamina = 1
        self.health = 1
        self.direction = 3
        self.attack = -1
        self.attackimages = ((pygame.image.load('assets/character/a_right1.png'),pygame.image.load('assets/character/a_right2.png'), pygame.image.load('assets/character/a_right3.png'), pygame.image.load('assets/character/a_right4.png')),(pygame.image.load('assets/character/a_left1.png'), pygame.image.load('assets/character/a_left2.png'), pygame.image.load('assets/character/a_left3.png'), pygame.image.load('assets/character/a_left4.png')), (pygame.image.load('assets/character/a_up1.png'), pygame.image.load('assets/character/a_up2.png'), pygame.image.load('assets/character/a_up3.png'), pygame.image.load('assets/character/a_up4.png')), (pygame.image.load('assets/character/a_center1.png'), pygame.image.load('assets/character/a_center2.png'), pygame.image.load('assets/character/a_center3.png'), pygame.image.load('assets/character/a_center4.png')))
        self.images = ((pygame.image.load('assets/character/right.png'), pygame.image.load('assets/character/right1.png'), pygame.image.load('assets/character/right.png'), pygame.image.load('assets/character/right2.png')), (pygame.image.load('assets/character/left.png'), pygame.image.load('assets/character/left1.png'), pygame.image.load('assets/character/left.png'), pygame.image.load('assets/character/left2.png')), (pygame.image.load('assets/character/up.png'), pygame.image.load('assets/character/up1.png'), pygame.image.load('assets/character/up.png'), pygame.image.load('assets/character/up2.png')), (pygame.image.load('assets/character/center.png'), pygame.image.load('assets/character/center1.png'), pygame.image.load('assets/character/center.png'), pygame.image.load('assets/character/center2.png')))
        self.velocity = 2

    def draw(self, g):
        #pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)
        if(self.attack != -1):
        	g.blit(self.attackimages[self.direction][math.floor(self.attack/8)], (self.x, self.y))
        	self.attack += 2
        	if(self.attack == 32):
        		self.attack = -1
        else:
        	if(self.x != -1 and self.y != -1):
       			g.blit(self.images[self.direction][math.floor(self.moving/8)], (self.x+8, self.y))


    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """
        self.direction = dirn
        if(self.attack == -1):
	        self.moving = (self.moving + math.ceil(self.velocity)-1)%32
	        
	        if dirn == 0:
	            self.x += self.velocity
	        elif dirn == 1:
	            self.x -= self.velocity
	        elif dirn == 2:
	            self.y -= self.velocity
	        else:
	            self.y += self.velocity
class Game:

    def __init__(self, w, h):
        self.sock = Sockets()
        self.width = w
        self.height = h
        self.player = Player(50, 50)
        self.player2 = Player(100,100)
        self.canvas = Canvas(self.width, self.height, "Socket-RPG")

    def run(self):
        clock = pygame.time.Clock()
        objects = []
        objects.append(pygame.Rect(104,132,8,90))
        objects.append(pygame.Rect(104,228,32,1))
        objects.append(pygame.Rect(128, 66, 48, 50))
        objects.append(pygame.Rect(110, 160, 24, 22))
        objects.append(pygame.Rect(110,142,10,10))
        objects.append(pygame.Rect(215,176,30,2))
        objects.append(pygame.Rect(192,126,10,2))
        objects.append(pygame.Rect(192,96,85,10))
        objects.append(pygame.Rect(220,82,42,10))
        objects.append(pygame.Rect(300,120,10,80))
        objects.append(pygame.Rect(154,10,5,2))
        objects.append(pygame.Rect(220,30,5,2))
        objects.append(pygame.Rect(10,20,10,5))
        objects.append(pygame.Rect(0,250,25,50))
        objects.append(pygame.Rect(35,270,37,30))
        objects.append(pygame.Rect(80,290,10,10))
        objects.append(pygame.Rect(0,305,145,10))
        objects.append(pygame.Rect(190,305,145,10))
        objects.append(pygame.Rect(260,290,20,10))
        objects.append(pygame.Rect(295,270,20,10))
        run = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False
            keys = pygame.key.get_pressed()
            colide = [False,False,False,False]
            for obj in objects:
            	if(pygame.Rect(self.player.x+self.player.velocity,self.player.y,32,32).colliderect(obj)):
            		colide[0] = True
            	if(pygame.Rect(self.player.x-self.player.velocity,self.player.y,32,32).colliderect(obj)):
            		colide[1] = True
            	if(pygame.Rect(self.player.x, self.player.y-self.player.velocity,32,32).colliderect(obj)):
            		colide[2] = True
            	if(pygame.Rect(self.player.x, self.player.y+self.player.velocity,32,32).colliderect(obj)):
            		colide[3] = True
            self.player.velocity = 2

            if keys[pygame.K_SPACE]:
            	if(self.player.attack == -1):
            		self.player.attack = 0
            if keys[pygame.K_LSHIFT]:
            	if(self.player.stamina > 0):
          	        self.player.velocity = 3
          	        self.player.stamina -= 0.01
            else:
                if(self.player.stamina < 1):
                    self.player.stamina += 0.005
            if keys[pygame.K_RIGHT]:
                if self.player.x <= self.width - 32 - self.player.velocity and not colide[0]:
                    self.player.move(0)
            if keys[pygame.K_LEFT]:
                if self.player.x >= self.player.velocity and not colide[1]:
                    self.player.move(1)
            if keys[pygame.K_UP]:
                if self.player.y >= self.player.velocity and not colide[2]:
                   	self.player.move(2)
            if keys[pygame.K_DOWN]:
                if self.player.y <= self.height - 32 - self.player.velocity and not colide[3]:
                    self.player.move(3)
            # Send Network Stuff
            self.player2.x, self.player2.y, self.player2.direction, self.player2.moving, self.player2.attack = self.parse_data(self.send_data())

            # Update Canvas
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            pygame.draw.rect(self.canvas.get_canvas(), (255,255,0), (10, 5, 100*self.player.stamina, 5), 0)
            pygame.draw.rect(self.canvas.get_canvas(), (255,0,0), (10, 10, 100*self.player.health, 5), 0)

            #for obj in objects:
            	#pygame.draw.rect(self.canvas.get_canvas(), (255,0,0), (obj.x,obj.y,obj.width,obj.height), 0)
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.sock.id) + ":" + str(self.player.x) + "," + str(self.player.y) + "," + str(self.player.direction) + "," + str(self.player.moving) + "," + str(self.player.attack)
        reply = self.sock.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1]), int(d[2]), int(d[3]), int(d[4])
        except:
            return -1,-1,3,0,-1


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        flags = pygame.SCALED
        self.height = h
        self.bg = pygame.image.load('assets/bg.png')
        self.screen = pygame.display.set_mode((w,h), flags)
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        #self.screen.fill((255,255,255)
        self.screen.blit(self.bg, (0,0))

if __name__ == "__main__":
    g = Game(320,320)
    g.run()