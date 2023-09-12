import sys, time
import random

import pygame 
#from pygame.locals import *
#from boombox import BoomBox



WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
WHITE = (226, 182, 116)
IMAGEWIDTH = 200
IMAGEHEIGHT = 200
FPS = 10

newcursor = "slipper.png"

def get_random_position(widow_width, window_height, image_width, image_height):
    random_x = random.randint(image_width/2, widow_width - image_width)
    random_y = random.randint(image_height/2, window_height - image_height)

    return random_x, random_y


# init mosquito random position
class Mosquito(pygame.sprite.Sprite):
    def __init__(self, width, height, random_x, random_y, widow_width, window_height):
        super().__init__()
        self.raw_image = pygame.image.load('ck.png').convert_alpha()
        self.image = pygame.transform.scale(self.raw_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (random_x, random_y)
        self.width = width
        self.height = height
        self.widow_width = widow_width
        self.window_height = window_height

class dead(pygame.sprite.Sprite):
    def __init__(self, width, height, random_x, random_y, widow_width, window_height):
        super().__init__()
        self.raw_image = pygame.image.load('dead.png').convert_alpha()
        self.image = pygame.transform.scale(self.raw_image, (width*1.4, height*1.4))
        self.rect = self.image.get_rect()
        self.rect.topleft = (random_x, random_y)
        self.width = width
        self.height = height
        self.widow_width = widow_width
        self.window_height = window_height

def main():
    pygame.init()
    #pygame.mixer.init()
    pygame.mouse.set_visible(False) #
    # load window surface
    window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    glovecursor = pygame.image.load(newcursor).convert_alpha() #

    pygame.display.set_caption('Hit the cockroach!')
    random_x, random_y = get_random_position(WINDOW_WIDTH, WINDOW_HEIGHT, IMAGEWIDTH, IMAGEHEIGHT)
    mosquito = Mosquito(IMAGEWIDTH, IMAGEHEIGHT, random_x, random_y, WINDOW_WIDTH, WINDOW_HEIGHT)
    reload_mosquito_event = pygame.USEREVENT + 1
    pygame.time.set_timer(reload_mosquito_event, 1000)
    points = 0
    my_font = pygame.font.Font("ArdleysHand-Regular.ttf", 40)
    my_hit_font = pygame.font.Font("ZombieA.ttf", 80)
    #download font: http://fontvip.com/A-fonts/50953.html
    #my_hit_font = pygame.font.SysFont("Arial.ttf", 80)  #可以吃系統字體
    hit_text_surface = None
    main_clock = pygame.time.Clock()
    sound = pygame.mixer.Sound('punch-140236.wav')
    sound.play()
    #boombox = boombox("punch-140236.wav")

    while True:
        
        # 偵測事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == reload_mosquito_event:
                # 偵測到重新整理事件，固定時間移除蚊子，換新位置
                mosquito.kill()
                # 蚊子新位置
                random_x, random_y = get_random_position(WINDOW_WIDTH, WINDOW_HEIGHT, IMAGEWIDTH, IMAGEHEIGHT)
                mosquito = Mosquito(IMAGEWIDTH, IMAGEHEIGHT, random_x, random_y, WINDOW_WIDTH, WINDOW_HEIGHT)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 當使用者點擊滑鼠時，檢查是否滑鼠位置 x, y 有在蚊子圖片上
                if random_x < pygame.mouse.get_pos()[0]+5 < random_x + IMAGEWIDTH and random_y < pygame.mouse.get_pos()[1]+5 < random_y + IMAGEHEIGHT:
                    #mosquito.kill()
                    
                    #random_x, random_y = get_random_position(WINDOW_WIDTH, WINDOW_HEIGHT, IMAGEWIDTH, IMAGEHEIGHT)
                    mosquito = dead(IMAGEWIDTH, IMAGEHEIGHT, random_x, random_y, WINDOW_WIDTH, WINDOW_HEIGHT)
                    #msg=random.choice(["Got you", "R.I.P.", "Good job"])
                    hit_text_surface = my_hit_font.render("R.I.P.", True, (250, 15, 15))
                    #sound = pygame.mixer.Sound('punch-140236.wav')
                    sound.play()
                    #boombox.play()
                    points += 5

        # 背景顏色，清除畫面
        window_surface.fill(WHITE)

        # 遊戲分數儀表板
        text_surface = my_font.render('Points: {}'.format(points), True, (0, 0, 0))
        # 渲染物件
        window_surface.blit(mosquito.image, mosquito.rect)
        window_surface.blit(text_surface, (30, 10))

        # 顯示打中提示文字
        
        if hit_text_surface:
            window_surface.blit(hit_text_surface, (random_x-50, random_y-30))
            hit_text_surface = None

        x,y = pygame.mouse.get_pos()
        x -= glovecursor.get_width()/15
        y -= glovecursor.get_height()/25
        window_surface.blit(glovecursor,(x,y))


        pygame.display.update()
        # 控制遊戲迴圈迭代速率
        main_clock.tick(FPS)

if __name__ == '__main__':    
    main()