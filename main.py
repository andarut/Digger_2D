import pygame
import sys
import random
from random import randint


# Разрешение экрана в пикселях
display_w = 1280
display_h = 720
game_exit = False


pygame.init()
game_display = pygame.display.set_mode((display_w, display_h), pygame.WINDOWMOVED)
pygame.display.set_caption('DIGGER 2D')
clock = pygame.time.Clock()

bg = pygame.image.load('bg.png')
menu = pygame.image.load('ui/menu.png')
sb = pygame.image.load('ui/sb.png')
camera_x = 0
camera_x_t = 0
camera_y = 1800
camera_y_t = 0
block_est = False

genImg = pygame.image.load('ui/gen.png')

gamestarted = False

gen = 0

chat = False

class block2:
    def __init__(self,x,y):
        self.img = pygame.image.load("photo2.png")
        self.x = 0
        self.y = 0
        self.bx = x
        self.by = y
        self.hp = 5
        self.fall = True
        self.fallSpeed = 0
        self.created = False
    def draw(self):
        if self.created:
            self.bx = int(float(self.x)/80.0)*80-camera_x
            self.by = int(float(self.y)/80.0)*80-camera_x
        else:
            self.x = self.bx * 80
            self.y = self.by * 80
            self.created = True
        game_display.blit(self.img, (self.x - camera_x, self.y-camera_y))


        self.fall = True
        for i in range(len(blocks)):
            if self.fall:
                if blocks[i] != self:
                    if self.x + 81 - camera_x > blocks[i].x - camera_x and self.x - camera_x < blocks[i].x - camera_x + 80 and self.y + 81 + self.fallSpeed + 5 > blocks[i].y and self.y < blocks[i].y + 20 + 81:
                        self.y = blocks[i].y - 80
                        self.fall = False
                        self.fallSpeed = 0

        #if self.y + self.fallSpeed+5 > 524:
        #    self.y = 524
        #    self.fall = False
        #    self.fallSpeed = 0

        if self.fall:
            self.y += self.fallSpeed
            self.fallSpeed += 5

        game_display.blit(self.img, (self.x-camera_x, self.y-camera_y))

class block:
    def __init__(self,x,y):
        self.img = pygame.image.load("photo.png")
        self.x = 0
        self.y = 0
        self.bx = x
        self.by = y
        self.hp = 5
    def draw(self):
        self.x = self.bx * 80
        self.y = self.by * 80
        game_display.blit(self.img, (self.x - camera_x, self.y-camera_y))

class player:
    def __init__(self):
        self.x = 10
        self.y = 10
        self.hp = 100
        self.img = pygame.image.load('player.png')
        self.img_left = pygame.image.load('playerl.png')
        self.img_right = pygame.image.load('player.png')

        self.bs = pygame.image.load('ui/bs.png')

        self.moveLeft = False
        self.moveRight = False
        self.allowLeft = True
        self.allowRight = True

        self.max_speed = 6
        self.speed = 0

        self.jump = False
        self.jumpTic = 0
        self.jumpSpeed = 0
        self.fall = True
        self.fallTic = 0

        self.seedown = False
        self.seeup = False

        self.seeright = True

        self.fallSpeed = 0

        self.name = "Шкальник"
    def draw(self):
        if self.moveLeft:
            if self.speed > self.max_speed*-1:
                self.speed -= 5
            self.img = self.img_left
        if self.moveRight:
            if self.speed < self.max_speed:
                self.speed += 5
            self.img = self.img_right
        if not self.moveLeft and not self.moveRight:
            if self.speed > 0:
                self.speed -= 5
            if self.speed < 0:
                self.speed += 5
            if self.speed == 0:
                self.speed = 0



        if self.jump:
            self.jumpTic += 1
            self.jumpSpeed -= 1
            self.y -= self.jumpSpeed
            if self.jumpTic > 10:
                self.jumpTic = 0
                self.jump = False
                self.jumpSpeed = 0
                self.fall = True
        else:
            self.jumpSpeed = 0

        self.x += self.speed


        if self.seeright:
            if self.seedown:
                game_display.blit(self.bs, (int(float(player1.x + 140)/80.0)*80-camera_x, (int(float(player1.y + 100)/80.0))*80-camera_y))
            elif self.seeup:
                game_display.blit(self.bs, (int(float(player1.x + 140) / 80.0) * 80 - camera_x, (int(float(player1.y + 100) / 80.0)-2) * 80-camera_y))
            else:
                game_display.blit(self.bs, (int(float(player1.x + 140) / 80.0) * 80 - camera_x, (int(float(player1.y + 100) / 80.0)-1) * 80-camera_y))
        else:
            if self.seedown:
                game_display.blit(self.bs, (int(float(player1.x - 80)/80.0)*80-camera_x, (int(float(player1.y + 100)/80.0))*80-camera_y))
            elif self.seeup:
                game_display.blit(self.bs, (int(float(player1.x - 80) / 80.0) * 80 - camera_x, (int(float(player1.y + 100) / 80.0)-2) * 80-camera_y))
            else:
                game_display.blit(self.bs, (int(float(player1.x - 80) / 80.0) * 80 - camera_x, (int(float(player1.y + 100) / 80.0)-1) * 80-camera_y))

        # colision
        self.fall = True
        for i in range(len(blocks)):
            if self.fall:
                if player1.x + 60 - camera_x > blocks[i].x - camera_x and player1.x - camera_x < blocks[i].x - camera_x + 80 and player1.y + 80 + self.fallSpeed + 5 > blocks[i].y and player1.y < blocks[i].y + 20 + 60:
                    if self.fall and not self.jump:
                        self.y = blocks[i].y - 79
                        self.fall = False
                        self.fallSpeed = 0
                    elif self.jump:
                        self.jump = False
                        self.y += self.jumpSpeed+5
                        self.fall = True
            if player1.x + 60 - camera_x > blocks[i].x - camera_x-10 and player1.x - camera_x < blocks[i].x+1 - camera_x + 80 and player1.y + 80 + self.fallSpeed + 5 > blocks[i].y+10 and player1.y < blocks[i].y + 80-10:
                self.x -= self.speed
        #if self.y + self.fallSpeed+5 > 924:
        #    self.y = 924
        #    self.fall = False
        #    self.fallSpeed = 0

        if self.fall:
            self.y += self.fallSpeed
            self.fallSpeed += 5

        game_display.blit(self.img, (self.x-camera_x, self.y-camera_y))

class block3:
    def __init__(self,x,y):
        self.img = pygame.image.load("photo3.png")
        self.x = 0
        self.y = 0
        self.bx = x
        self.by = y
        self.hp = 5
        self.fall = True
        self.fallSpeed = 0
    def draw(self):
        self.x = self.bx * 80
        self.y = self.by * 80


        game_display.blit(self.img, (self.x-camera_x, self.y-camera_y))
class block4:
    def __init__(self,x,y):
        self.img = pygame.image.load("photo4.png")
        self.x = 0
        self.y = 0
        self.bx = x
        self.by = y
        self.hp = 5
        self.fall = True
        self.fallSpeed = 0
    def draw(self):
        self.x = self.bx * 80
        self.y = self.by * 80


        game_display.blit(self.img, (self.x-camera_x, self.y-camera_y))
class block5:
    def __init__(self,x,y):
        self.img = pygame.image.load("photo5.png")
        self.x = 0
        self.y = 0
        self.bx = x
        self.by = y
        self.hp = 5
        self.fall = True
        self.fallSpeed = 0
    def draw(self):
        self.x = self.bx * 80
        self.y = self.by * 80



        game_display.blit(self.img, (self.x-camera_x, self.y-camera_y))
class block6:
    def __init__(self,x,y):
        self.img = pygame.image.load("photo6.png")
        self.x = 0
        self.y = 0
        self.bx = x
        self.by = y
        self.hp = 5
        self.fall = True
        self.fallSpeed = 0
    def draw(self):
        self.x = self.bx * 80
        self.y = self.by * 80


        game_display.blit(self.img, (self.x-camera_x, self.y-camera_y))

blocktype = block
def createBlock():
    global blocktype
    okplace = True
    for i in range(len(blocks)):
        if player1.seeright:
            if player1.seedown:
                if blocks[i].bx == int(float(player1.x + 140) / 80.0) and blocks[i].by == int(float(player1.y + 100) / 80.0):
                    okplace = False
            elif player1.seeup:
                if blocks[i].bx == int(float(player1.x + 140) / 80.0) and blocks[i].by == int(float(player1.y + 100) / 80.0 - 2):
                    okplace = False
            else:
                if blocks[i].bx == int(float(player1.x + 140) / 80.0) and blocks[i].by == int(float(player1.y + 100) / 80.0 - 1):
                    okplace = False
        else:
            if player1.seedown:
                if blocks[i].bx == int(float(player1.x - 80) / 80.0) and blocks[i].by == int(float(player1.y + 100) / 80.0):
                    okplace = False
            elif player1.seeup:
                if blocks[i].bx == int(float(player1.x - 80) / 80.0) and blocks[i].by == int(float(player1.y + 100) / 80.0 - 2):
                    okplace = False
            else:
                if blocks[i].bx == int(float(player1.x - 80) / 80.0) and blocks[i].by == int(float(player1.y + 100) / 80.0 - 1):
                    okplace = False

    if okplace:
        if player1.seeright:
            if player1.seedown:
                blocks.append(blocktype(int(float(player1.x + 140) / 80.0), int(float(player1.y + 100) / 80.0)))
            elif player1.seeup:
                blocks.append(blocktype(int(float(player1.x + 140) / 80.0), int(float(player1.y + 100) / 80.0) - 2))
            else:
                blocks.append(blocktype(int(float(player1.x + 140) / 80.0), int(float(player1.y + 100) / 80.0) - 1))
        else:
            if player1.seedown:
                blocks.append(blocktype(int(float(player1.x - 80) / 80.0), int(float(player1.y + 100) / 80.0)))
            elif player1.seeup:
                blocks.append(blocktype(int(float(player1.x - 80) / 80.0), int(float(player1.y + 100) / 80.0) - 2))
            else:
                blocks.append(blocktype(int(float(player1.x - 80) / 80.0), int(float(player1.y + 100) / 80.0) - 1))

player1 = player()



blocks = [block3(-2,6)]
def process_keyboard(event):
    global block_est, blocktype, gamestarted, gen, chat, cf
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
            blocktype = block
        if event.key == pygame.K_2:
            blocktype = block2
        if event.key == pygame.K_3:
            blocktype = block3
        if event.key == pygame.K_4:
            blocktype = block4
        if event.key == pygame.K_5:
            blocktype = block5
        if event.key == pygame.K_6:
            blocktype = block6
        if event.key == pygame.K_k:
            createBlock()
        if event.key == pygame.K_l:
            for i in range(len(blocks)):
                if player1.seeright:
                    if player1.seedown:
                        if blocks[i].bx == int(float(player1.x + 140) / 80.0) and blocks[i].by == int(float(player1.y + 100) / 80.0):
                            blocks.remove(blocks[i])
                            return True
                    elif player1.seeup:
                        if blocks[i].bx == int(float(player1.x + 140) / 80.0) and blocks[i].by == int(float(player1.y + 100) / 80.0 - 2):
                            blocks.remove(blocks[i])
                            return True
                    else:
                        if blocks[i].bx == int(float(player1.x + 140) / 80.0) and blocks[i].by == int(float(player1.y + 100) / 80.0 - 1):
                            blocks.remove(blocks[i])
                            return True
                else:
                    if player1.seedown:
                        if blocks[i].bx == int(float(player1.x - 80) / 80.0) and blocks[i].by == int(float(player1.y + 100) / 80.0):
                            blocks.remove(blocks[i])
                            return True
                    elif player1.seeup:
                        if blocks[i].bx == int(float(player1.x - 80) / 80.0) and blocks[i].by == int(float(player1.y + 100) / 80.0 - 2):
                            blocks.remove(blocks[i])
                            return True
                    else:
                        if blocks[i].bx == int(float(player1.x - 80) / 80.0) and blocks[i].by == int(float(player1.y + 100) / 80.0 - 1):
                            blocks.remove(blocks[i])
                            return True
            return False
        if event.key == pygame.K_a:
            player1.moveLeft = True
            player1.seeright = False
        if event.key == pygame.K_d:
            player1.moveRight = True
            player1.seeright = True
        if event.key == pygame.K_r:
            if gamestarted:
                player1.y = 0
                player1.fallSpeed = 0
                blocks.clear()
                generateWorld(80)
        if event.key == pygame.K_SPACE:
            if gamestarted:
                if chat:
                    cf.send()
                elif player1.jumpSpeed <= 0:
                    player1.jump = True
                    player1.jumpSpeed = 40
            else:
                gamestarted = True
        if event.key == pygame.K_w:
            player1.seeup = True
        if event.key == pygame.K_s:
            player1.seedown = True
        if event.key == pygame.K_t:
            if chat:
                chat = False
            else:
                chat = True
        if event.key == pygame.K_LEFT:
            if chat:
                cf.sm -= 1
        if event.key == pygame.K_RIGHT:
            if chat:
                cf.sm += 1
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            player1.moveLeft = False
        if event.key == pygame.K_d:
            player1.moveRight = False
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        if event.key == pygame.K_w:
            player1.seeup = False
        if event.key == pygame.K_s:
            player1.seedown = False





def generateWorld(x_size: int):
    current_h = 90
    world_y = 100
    stone_y = 0
    current_x = 0
    for i in range(x_size):
        stone_y = 3 + randint(0, 2)
        for ii in range(current_h):
            if ii == current_h-1:
                blocks.append(block(current_x, world_y-ii))
            elif ii > current_h-1-stone_y:
                blocks.append(block4(current_x, world_y - ii))
            else:
                blocks.append(block3(current_x, world_y - ii))
        current_x+=1
        current_h += randint(-1, 1)

generateWorld(80)

class chatFrame:
    def __init__(self):
        self.img = pygame.image.load("ui/chat.png")
        self.sm = 0
        self.messages = [player1.name+" присоединился к игре"]
    def update(self):
        global chat
        if self.sm == -1:
            self.sm = 0
        if self.sm == 5:
            self.sm = 4
        if chat:
            game_display.blit(self.img, (0, 0))
            if self.sm == 0:
                game_display.blit(pygame.image.load("ui/m1.png"), (44, 576))
            if self.sm == 1:
                game_display.blit(pygame.image.load("ui/m2.png"), (161, 576))
            if self.sm == 2:
                game_display.blit(pygame.image.load("ui/m3.png"), (299, 576))
            if self.sm == 3:
                game_display.blit(pygame.image.load("ui/m4.png"), (44, 623))
            if self.sm == 4:
                game_display.blit(pygame.image.load("ui/m5.png"), (476, 623))
            for i in range(len(self.messages)):
                if i < 20:
                    myfont = pygame.font.SysFont('Arial', 30)
                    text = myfont.render(self.messages[i], False, (255, 255, 255))
                    game_display.blit(text, (50, 480-(i*20)))
    def send(self):
        if chat:
            if self.sm == 0:
                self.messages.insert(0, player1.name+":  УХАДИ")
            if self.sm == 1:
                self.messages.insert(0, player1.name+":  АТАШОЛ")
            if self.sm == 2:
                self.messages.insert(0, player1.name+":  ВЕЩЬ ИЛИ БАН")
            if self.sm == 3:
                self.messages.insert(0, player1.name+":  Я ТВОЮ МАМКУ В КИНО ВОДИЛ")
            if self.sm == 4:
                self.messages.insert(0, player1.name+":  АЗАЗАЗА")

cf = chatFrame()

def game_loop(update_time):
    global game_exit, block_est, gen
    global camera_x, camera_y, camera_x_t
    while not game_exit:
        for event in pygame.event.get():
            # print(event)
            process_keyboard(event)
            if event.type == pygame.QUIT:
                game_exit = True
                quit()

        game_display.fill((0, 0, 0))
        #camera
        camera_x_t = player1.x - display_w / 2
        camera_y_t = player1.y - display_h / 2
        if gamestarted:
            if player1.x > display_w/2 and player1.x < 9460:
                #camera_x = player1.x - display_w / 2
                camera_x += (camera_x_t-camera_x)/8

            if player1.y > display_h/2:
                #camera_x = player1.x - display_w / 2
                camera_y += (camera_y_t-camera_y)/8


        game_display.blit(bg, (0-camera_x/5, 0-camera_y/5))
        #game_display.blit(gr, (0-camera_x, 573))

        for i in range(len(blocks)):
            blocks[i].draw()

        player1.draw()


        if gamestarted:
            bv = blocktype(1,1).img
            game_display.blit(sb, (956, 20))
            game_display.blit(bv, (1167, 33))
        else:
            game_display.blit(menu, (0, 0))
            myfont = pygame.font.SysFont('Arial', 25)
            text = myfont.render("Разбаботка: Арутюнян Андрей, Белов Даниил. Для Школы Программистов", False, (255, 255, 255))
            game_display.blit(text, (320, 680))

        cf.update()

        if player1.x < 0:
            player1.x = 0
        elif player1.x > 4620:
            player1.x = 4620

        if camera_x > 3280:
            camera_x = 3280

        #myfont = pygame.font.SysFont('Arial', 30)
        #text = myfont.render("PlayerX: "+str(player1.x), False, (255, 255, 255))
        #game_display.blit(text, (50, 50))

        pygame.display.update()
        clock.tick(update_time)

game_loop(1000000000000)
pygame.quit()
quit()
