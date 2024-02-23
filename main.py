import pygame
import os

# import random
# pygame.font.init()
pygame.init()
# print("Hello World")

#                                   variables begin
# Admin = "G"
# Login_attempt = 3
winWidth, winHeight = 1100, 700
DisplayName = "First Game"
White = (255, 255, 255)
BLACK = (0, 100, 0)
BackgroundRGB = White

RED_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2
HEATH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 70, 70
SHIP_WIDTH, SHIP_HEIGHT = 70, 70
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 3
BORDER_WIDTH = 10
BORDER = pygame.Rect((winWidth / 2) - (BORDER_WIDTH / 2), 0, BORDER_WIDTH, winHeight)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Gun+Silencer.mp3'))

# images
GUN_SHIP_BASE_IMAGE = pygame.image.load(
    os.path.join('Assets', 'gun_ship_base_0.1.png'))
GUN_SHIP_BASE = pygame.transform.rotate(
    pygame.transform.scale(GUN_SHIP_BASE_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 270)

GUN_SHIP_TURRET_IMAGE = pygame.image.load(
    os.path.join('Assets', 'gun_ship_turret_0.1.png'))
GUN_SHIP_TURRET = pygame.transform.rotate(
    pygame.transform.scale(GUN_SHIP_TURRET_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 270)

BLUE_JEDI_FIGHTER_IMAGE = pygame.image.load(
    os.path.join('Assets', 'jedi_Fighter_Blue.png'))
BLUE_JEDI_FIGHTER = pygame.transform.rotate(
    pygame.transform.scale(BLUE_JEDI_FIGHTER_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

JEDI_FIGHTER_PROJECTILE_IMAGE = pygame.image.load(
    os.path.join('Assets', 'jedi_Fighter_Projectile.png'))
JEDI_FIGHTER_PROJECTILE_L = pygame.transform.rotate(
    pygame.transform.scale(JEDI_FIGHTER_PROJECTILE_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

JEDI_FIGHTER_PROJECTILE_IMAGE = pygame.image.load(
    os.path.join('Assets', 'jedi_Fighter_Projectile.png'))
JEDI_FIGHTER_PROJECTILE_R = pygame.transform.rotate(
    pygame.transform.scale(JEDI_FIGHTER_PROJECTILE_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

BACKGROUND_IMAGE = pygame.image.load(
    os.path.join('Assets', 'stars_in_space 2023-03-03 111904.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (winWidth, winHeight))

WIN = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption(DisplayName)
# variables end
#                                                       functions


def draw_window(red, blue, red_bullet, blue_bullet, red_health, blue_health):
    WIN.blit(BACKGROUND, (0, 0))

    red_health_text = HEATH_FONT.render("Health: " + str(red_health), True, White)
    blue_health_text = HEATH_FONT.render("Health: " + str(blue_health), True, White)
    WIN.blit(red_health_text, (10, 10))
    WIN.blit(blue_health_text, (winWidth - red_health_text.get_width() - 10, 10))

    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(GUN_SHIP_BASE, (red.x, red.y))
    WIN.blit(BLUE_JEDI_FIGHTER, (blue.x, blue.y))

    for bullet in red_bullet:
        WIN.blit(JEDI_FIGHTER_PROJECTILE_R, bullet)
    for bullet in blue_bullet:
        WIN.blit(JEDI_FIGHTER_PROJECTILE_L, bullet)

    pygame.display.update()


def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0:  # (red) left ship moves <--
        red.x -= VEL  # (red) left ship moves -->
    if keys_pressed[pygame.K_d] and red.x + VEL + SPACESHIP_WIDTH < BORDER.x:
        red.x += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 0:  # (red) left ship moves ^
        red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y + VEL < winHeight - SPACESHIP_HEIGHT:  # (red) left ship moves down
        red.y += VEL


def handle_blue_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - VEL > BORDER.x + BORDER_WIDTH:  # (blue) right ship moves <--
        blue.x -= VEL  # (blue) right ship moves -->
    if keys_pressed[pygame.K_RIGHT] and blue.x + VEL < winWidth - SPACESHIP_WIDTH:
        blue.x += VEL
    if keys_pressed[pygame.K_UP] and blue.y - VEL > 0:  # (blue) right ship moves ^
        blue.y -= VEL
    if keys_pressed[pygame.K_DOWN] and blue.y + VEL < winHeight - SPACESHIP_HEIGHT:  # (blue) right ship moves down
        blue.y += VEL


def handle_bullets(red_bullet, blue_bullet, red, blue):
    for bullet in red_bullet:
        bullet.x += BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullet.remove(bullet)
        elif bullet.x > winWidth + SPACESHIP_WIDTH:
            red_bullet.remove(bullet)

    for bullet in blue_bullet:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullet.remove(bullet)
        elif bullet.x < 0 - SPACESHIP_WIDTH:
            blue_bullet.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, White)
    WIN.blit(draw_text, (winWidth / 2 - draw_text.get_width() / 2, winHeight / 2 - draw_text.get_height()))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(0, winHeight/2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    blue = pygame.Rect(1030, winHeight/2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_health = 10
    blue_health = 10
    red_bullet = []
    blue_bullet = []
    clock = pygame.time.Clock()
    mouse_pos = pygame.mouse.get_pos()
    # Important Quit Button
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullet) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x + SPACESHIP_WIDTH, red.y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
                    red_bullet.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(blue_bullet) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        blue.x - SPACESHIP_WIDTH, blue.y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
                    blue_bullet.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == BLUE_HIT:
                blue_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Blue Wins!"
        if blue_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break
        keys_pressed = pygame.key.get_pressed()
        handle_red_movement(keys_pressed, red)
        handle_blue_movement(keys_pressed, blue)
        handle_bullets(red_bullet, blue_bullet, red, blue)
        draw_window(red, blue, red_bullet, blue_bullet, red_health, blue_health)

    main()


if __name__ == "__main__":
    main()
