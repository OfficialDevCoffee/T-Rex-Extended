#t-rex-extended.py
__author__ = 'stdio.chem@gmail.com'

import pygame, random
import color

pad_width = 1000
pad_height = 300
caption = "T-Rex Extended"
left = 0
center = 1
right = 2
score = 0

def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj,(x, y))
    pass

def textObject(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def drawText(text, size, color, x, y, align):
    global gamepad
    textFont = pygame.font.Font('font/pixel.ttf', size)
    TextSurf, TextRect = textObject(text, textFont, color)
    if align == left:
        TextRect.midleft = (x, y)
        pass
    elif align == center:
        TextRect.center = (x, y)
        pass
    elif align == right:
        TextRect.midright = (x, y)
        pass
    gamepad.blit(TextSurf, TextRect)
    pass

def initGame():
    global gamepad, clock
    global rex, cactus, bird, item, cloud, ground1, ground2, replay
    global btn_sound, gameover_sound, score_sound

    rex = []
    cactus = [[], []]
    bird = []
    item = []

    pygame.init()

    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption(caption)

    ground1 = pygame.image.load('image/ground.png')
    ground2 = ground1.copy()

    rex.append(pygame.image.load('image/rex_default.png'))
    rex.append(pygame.image.load('image/rex_run1.png'))
    rex.append(pygame.image.load('image/rex_run2.png'))
    rex.append(pygame.image.load('image/rex_gameover.png'))

    cactus[0].append(pygame.image.load('image/cactus_1.png'))
    cactus[0].append(pygame.image.load('image/cactus_2.png'))
    cactus[0].append(pygame.image.load('image/cactus_3.png'))
    cactus[0].append(pygame.image.load('image/cactus_4.png'))

    cactus[1].append(pygame.image.load('image/cactus_big_1.png'))
    cactus[1].append(pygame.image.load('image/cactus_big_2.png'))
    cactus[1].append(pygame.image.load('image/cactus_big_3.png'))
    cactus[1].append(pygame.image.load('image/cactus_big_4.png'))
    cactus[1].append(pygame.image.load('image/cactus_big_5.png'))
    cactus[1].append(pygame.image.load('image/cactus_big_6.png'))

    bird.append(pygame.image.load('image/bird_1.png'))
    bird.append(pygame.image.load('image/bird_2.png'))

    cloud = pygame.image.load('image/cloud.png')
    replay = pygame.image.load('image/replay.png')

    btn_sound = pygame.mixer.Sound('sound/button-press.wav')
    gameover_sound = pygame.mixer.Sound('sound/hit.wav')
    score_sound = pygame.mixer.Sound('sound/score-reached.wav')

    clock = pygame.time.Clock()
    runGame()
    pass

def runGame():
    global gamepad, clock
    global rex, cactus, bird, item, cloud, ground1, ground2, replay
    global btn_sound, score_sound

    score = 0

    cactus_txy = []    
    bird_txy = []
    cloud_txy = []

    rex_x = 60
    rex_y = pad_height - 130
    rex_y_change = 0
    rex_canjump = True
    rex_t_cooltime = 5
    rex_t = 0

    ground1_x = 0
    ground2_x = 2400

    speed = 5

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and rex_canjump:
                    rex_y_change = -14
                    rex_canjump = False
                    pass
                elif event.key == pygame.K_a and rex_canjump:
                    rex_y_change = -11.5
                    rex_canjump = False
                pass
            if event.type == pygame.QUIT:
                crashed = True
                pass
            pass

        score += 0.2

        if int(score) % 100 == 0 and score >= 100:
            speed += 0.2
            pass

        print((score, speed))

        cactus_spawn = random.randrange(0, int(1000 - speed * 5))
        cactus_type = random.randrange(0, 6)
        cactus_size = random.randrange(0,2)
        if cactus_spawn % 120 == 0:
            if cactus_type >= 0 and cactus_type <= 3 and cactus_size == 0:
                cactus_txy.append([cactus[cactus_size][cactus_type], 2500, pad_height - 120])
                pass
            elif cactus_type >= 0 and cactus_type <= 5 and cactus_size == 1:
                cactus_txy.append([cactus[cactus_size][cactus_type], 2500, pad_height - 140])
                pass
            pass
        
        ground1_x -= speed
        ground2_x -= speed

        if ground1_x < -2400:
            ground1_x = 2400
            pass

        if ground2_x < -2400:
            ground2_x = 2400
            pass

        rex_t_cooltime -= 1
        
        if rex_t_cooltime == 0:
            if rex_t == 0:
                rex_t = 1
                pass
            elif rex_t == 1:
                rex_t = 2
                pass
            else:
                rex_t = 1
                pass
            rex_t_cooltime = 5
            pass

        rex_y += rex_y_change

        if not rex_canjump:
            rex_y_change += 0.7
            pass
        
        if rex_y > pad_height - 130:
            rex_y_change = 0
            rex_y = pad_height - 130
            rex_canjump = True
            pass

        if not len(cactus_txy) == 0:
            for i, cts in enumerate(cactus_txy):
                cts[1] -= speed
                cactus_txy[i][1] = cts[1]
                if cts[1] < -60:
                    try:
                        cactus_txy.remove(cts)
                        pass
                    except:
                        pass
                    pass
                pass
            pass

        gamepad.fill(color.white)

        drawObject(ground1, ground1_x, pad_height - 80)
        drawObject(ground2, ground2_x, pad_height - 80)

        if not len(cactus_txy) == 0:
            for ct, cx, cy in cactus_txy:
                drawObject(ct, cx, cy)
                pass
            pass
        
        drawObject(rex[rex_t], rex_x, rex_y)
        pygame.display.update()
        clock.tick(60)
        pass

    pygame.quit()
    quit()
    pass

if __name__ == '__main__':
    initGame()
    pass
