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
    global rex, cactus, bird, cloud, ground1, ground2, replay
    global btn_sound, gameover_sound, score_sound

    rex = []
    cactus = [[], []]
    bird = []

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
    mainScreen()
    pass

def mainScreen():
    global gamepad, ground1
    
    i = 1
    msgDisp = False
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    runGame()
                    pass
                pass
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                pass
            pass
        if i % 30 == 0:
            if msgDisp:
                i = 0
                msgDisp = False
                pass
            else:
                msgDisp = True
                pass
            pass
        i += 1

        gamepad.fill(color.white)
        drawObject(ground1, 0, pad_height - 80)
        drawText("T-Rex Runner", 100, color.dimgray, pad_width / 2, pad_height / 2 - 90, center)
        drawText("Extended | By Studio.Chem", 50, color.dimgray, pad_width / 2, pad_height / 2 - 45, center)
        drawText("Copyright: Studio.Chem, 2018-2019 | stdio.chem@gmail.com", 30, color.dimgray, pad_width / 2, pad_height - 20, center)
        if msgDisp:
            drawText("Press SPACE To Start", 50, color.dimgray, pad_width / 2, pad_height / 2 + 30, center)
            pass
        pygame.display.update()
        clock.tick(60)
        pass
    pass

def gameOver():
    global gamepad, replay
    global gameover_sound

    drawText("GAME OVER", 100, color.dimgray, pad_width / 2, pad_height / 2 - 90, center)
    drawObject(replay, pad_width / 2 - 40, pad_height / 2 - 50)
    drawText("Replay? (Y/N)", 50, color.dimgray, pad_width / 2, pad_height / 2 + 40, center)
    pygame.display.update()
    pygame.mixer.Sound.play(gameover_sound)
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    runGame()
                    pass
                elif event.key == pygame.K_n:
                    pygame.quit()
                    quit()
                    pass
                pass
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                pass
            pass
        pass
    pass

def runGame():
    global gamepad, clock
    global rex, cactus, bird, cloud, ground1, ground2
    global btn_sound, score_sound

    pygame.mixer.Sound.play(score_sound)

    score = 0
    score_filter = 100

    cactus_txy = []    
    bird_txy = []
    cloud_txy = []

    rex_x = 60
    rex_y = pad_height - 138
    rex_y_change = 0
    rex_canjump = True
    rex_t_cooltime = 5
    rex_t = 0

    ground1_x = 0
    ground2_x = 2400

    speed = 5

    score_cooltime = 0

    cactus_cooltime = 0
    cactus_spawntime = 10

    bird_cooltime = 0
    bird_spawntime = 10
    bird_shapetime = 0

    text_flag = False
    text_show = True
    text_cooltime = 0

    cloud_cooltime = 0
    cloud_spawntime = 10

    gameovered = False

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and rex_canjump:
                    pygame.mixer.Sound.play(btn_sound)
                    rex_y_change = -14
                    rex_canjump = False
                    pass
                elif event.key == pygame.K_a and rex_canjump:
                    pygame.mixer.Sound.play(btn_sound)
                    rex_y_change = -11.5
                    rex_canjump = False
                pass
            if event.type == pygame.QUIT:
                crashed = True
                pass
            pass

        if gameovered:
            gameOver()
            pass
        
        if text_flag:
            text_cooltime += 1
            if text_cooltime > 70:
                text_cooltime = 0
                score_cooltime = 9
                text_flag = False
                pass
            if text_cooltime % 10 == 0:
                if text_show:
                    text_show = False
                    pass
                else:
                    text_show = True
                    pass
                pass
            pass
        
        score_cooltime +=1
        if score_cooltime == 10 and not text_flag: 
            score_cooltime = 0
            score += 1
            pass
        elif text_flag:
            score_cooltime = 0
            pass

        if score % 100 == 0 and score != 0:
            text_flag = True
            pass
        
        if score >= score_filter:
            pygame.mixer.Sound.play(score_sound)
            speed += 1
            score_filter += 100
            pass

        if cactus_cooltime == cactus_spawntime:
            cactus_size = random.randrange(0,2)
            if cactus_size == 0:
                cactus_type = random.randrange(0, 4)
                cactus_txy.append([cactus[cactus_size][cactus_type], 2500, pad_height - 120])
                pass
            else:
                cactus_type = random.randrange(0, 6)
                cactus_txy.append([cactus[cactus_size][cactus_type], 2500, pad_height - 150])
                pass
            cactus_cooltime = 0
            cactus_spawntime = random.randrange(int(40-speed*0.7), int(210-speed*7))
            pass
        else:
            cactus_cooltime += 1
            pass

        if bird_cooltime == bird_spawntime:
            bird_txy.append([bird[0], 2500, random.randrange(20, 100), 0])
            bird_cooltime = 0
            bird_spawntime = random.randrange(int(200 - speed*0.5), int(400-speed*0.5))
            pass
        else:
            if score > 500:
                bird_cooltime += 1
                pass
            pass

        if cloud_cooltime == cloud_spawntime:
            cloud_txy.append([cloud, 2500, random.randrange(20, 80)])
            cloud_cooltime = 0
            cloud_spawntime = random.randrange(70, 400)
            pass
        else:
            cloud_cooltime += 1
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
        
        if rex_y > pad_height - 138:
            rex_y_change = 0
            rex_y = pad_height - 138
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
                if cts[1] < rex_x + 50 and cts[1] > rex_x and cts[2] > rex_y - 13  and cts[2] < rex_y + 70:
                    gameovered = True
                    pass
                pass

        if not len(bird_txy) == 0:
            for i, brd in enumerate(bird_txy):
                brd[1] -= speed * 1.5
                bird_txy[i][1] = brd[1]
                bird_txy[i][3] += 1
                if brd[1] < - 60:
                    try:
                        bird_txy.remove(brd)
                        pass
                    except:
                        pass
                    pass
                if brd[1] < rex_x + 80 and brd[1] > rex_x and brd[2] > rex_y and brd[2] < rex_y + 90:
                    gameovered = True
                    pass
                if not len(bird_txy) == 0:
                    if bird_txy[i][3] > 9:
                        if bird_txy[i][0] == bird[0]:
                            bird_txy[i][0] = bird[1]
                            pass
                        elif bird_txy[i][0] == bird[1]:
                            bird_txy[i][0] = bird[0]
                            pass
                        bird_txy[i][3] = 0
                        pass
                    pass
                pass
            pass

        if not len(cloud_txy) == 0:
            for i, cld in enumerate(cloud_txy):
                cld[1] -= speed * 0.8
                cloud_txy[i][1]  = cld[1]
                if cld[1] < -60:
                    try:
                        cloud_txy.remove(cld)
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

        if not len(bird_txy) == 0:
            for bt, bx, by, bk in bird_txy:
                drawObject(bt, bx, by)
                pass
            pass

        if not len(cloud_txy) == 0:
            for ct, cx, cy in cloud_txy:
                drawObject(ct, cx, cy)
                pass
            pass

        if gameovered:
            rex_t = 3
            pass
        
        drawObject(rex[rex_t], rex_x, rex_y)

        if text_show:
            drawText(str(score), 50, color.dimgray, pad_width - 10, 15, right)
            pass
        
        pygame.display.update()
        clock.tick(60)
        pass

    pygame.quit()
    quit()
    pass

if __name__ == '__main__':
    initGame()
    pass
