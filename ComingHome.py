##############################################################
###               C O M I N G       H O M E                ###
##############################################################
### Objetivo: Levar o alien até sua casa e sobreviver      ###
### aos obstaculos.                                        ###
##############################################################
### Prof. Filipo Novo Mor - github.com/ProfessorFilipo     ###
### M Eduarda Palmeiro - github.com/eduardapalmeiro        ###
##############################################################

import pygame
import random
import os
import time

# Inicializa o PyGame
pygame.init()

# ----------------------------------------------------------
# 🔧 CONFIGURAÇÕES GERAIS DO JOGO
# ----------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("👽 Coming home 👽")

# ----------------------------------------------------------
# 🧩 SEÇÃO DE ASSETS
# ----------------------------------------------------------
ASSETS = {
    "background": "fundo001.png",
    "background2": "fundo002.png",
    "background3": "fundo003.png",
    "player": "alien001.png",
    "player2": "alienamigo001.png",
    "sound_point": "collect-points-190037.mp3",
    "sound_hit": "hit-soundvideo-game-type-230510.mp3",
    "music": "emotional-futuristic-ambient-flying-over-the-universe-322221.mp3",
    "death_sound": "videogame-death-sound-43894",
    "menubg": "menubg.png",
    "winimg": "teladefinalbom.png",
    "loseimg": "teladefinalruim.png"
}

WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Função auxiliar para carregar imagens
def load_image(filename, fallback_color, size=None):
    if os.path.exists(filename):
        img = pygame.image.load(filename).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img

    surf = pygame.Surface(size or (50, 50))
    surf.fill(fallback_color)
    return surf


# Carregamento
background = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
background2 = load_image(ASSETS["background2"], WHITE, (WIDTH, HEIGHT))
background3 = load_image(ASSETS["background3"], WHITE, (WIDTH, HEIGHT))
player_img = load_image(ASSETS["player"], BLUE, (64, 64))
player2_img = load_image(ASSETS["player2"], BLUE, (64, 64))
menubg = load_image(ASSETS["menubg"], WHITE, (WIDTH, HEIGHT))
winimg = load_image(ASSETS["winimg"], WHITE, (WIDTH, HEIGHT))
loseimg = load_image(ASSETS["loseimg"], WHITE, (WIDTH, HEIGHT))

frames = [
    pygame.transform.scale(pygame.image.load("meteoro001.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load("meteoro002.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load("meteoro003.png"), (40, 40)),
]


# Sons
def load_sound(filename):
    if os.path.exists(filename):
        return pygame.mixer.Sound(filename)
    return None


sound_point = load_sound(ASSETS["sound_point"])
sound_hit = load_sound(ASSETS["sound_hit"])
death_sound = load_sound(ASSETS["death_sound"])

if os.path.exists(ASSETS["music"]):
    pygame.mixer.music.load(ASSETS["music"])
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

# ----------------------------------------------------------
# 🧠 VARIÁVEIS DE JOGO
# ----------------------------------------------------------
player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
player2_rect = player2_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))

player_speed = 7
player2_speed = 7

meteor_list = [pygame.Rect(random.randint(0, WIDTH - 40), random.randint(-500, -40), 40, 40) for _ in range(5)]
meteor_speed = 5

death = False
death2 = False

global score, score2

score = 0
lives = 3

score2 = 0
lives2 = 3

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
running = True
frame_index = 0


# ----------------------------------------------------------
# Funções
# ----------------------------------------------------------
def menu():
    button_width = 220
    button_height = 60

    # posição do botão
    button_rect = pygame.Rect(
        (WIDTH // 2 - button_width // 2, HEIGHT // 2 + 100),
        (button_width, button_height)
    )

    title_font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 50)

    while True:
        screen.blit(menubg, (0, 0))

        # Detectar mouse
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        # Verificar hover no botão
        if button_rect.collidepoint(mouse_pos):
            button_color = (50, 239, 106)
            if mouse_click:
                return
        else:
            button_color = (16, 209, 74)

        # Desenhar botão
        pygame.draw.rect(screen, button_color, button_rect, border_radius=12)

        # Texto do botão
        play_text = button_font.render("JOGAR", True, (13, 98, 70))
        screen.blit(play_text, (
            button_rect.x + button_rect.width // 2 - play_text.get_width() // 2,
            button_rect.y + button_rect.height // 2 - play_text.get_height() // 2
        ))

        pygame.display.flip()

        # Eventos gerais (sair)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def lose():
    global score, score2
    global death, death2
    death = True
    death2 = True
    scorefinal = max(score, score2)
    pygame.mixer.music.stop()
    screen.blit(loseimg, (0, 0))
    end_text = font.render("Você perdeu!", True, WHITE)
    final_score = font.render(f"Maior pontuação: {scorefinal}", True, WHITE)
    screen.blit(end_text, (320, 500))
    screen.blit(final_score, (290, 450))
    pygame.display.flip()

def win():
    global death, death2
    death = True
    death2 = True
    scorefinal = max(score, score2)
    pygame.mixer.music.stop()
    screen.blit(winimg, (0, 0))
    end_text = font.render("Você venceu!", True, WHITE)
    final_score = font.render(f"Maior pontuação: {scorefinal}", True, WHITE)
    screen.blit(end_text, (320, 500))
    screen.blit(final_score, (290, 450))
    pygame.display.flip()


# Desenha players
def vida():
    global death, death2

    if lives <= 0:
        death = True
    if lives2 <= 0:
        death2 = True

    if not death:
        screen.blit(player_img, player_rect)
    if not death2:
        screen.blit(player2_img, player2_rect)

    for meteor in meteor_list:
        screen.blit(frame_atual, meteor)


def fase1():
    screen.blit(background, (0, 0))
    vida()
    draw_hud()
    pygame.display.flip()


def fase2():
    screen.blit(background2, (0, 0))
    vida()
    draw_hud()
    pygame.display.flip()


def fase3():
    screen.blit(background3, (0, 0))
    vida()
    draw_hud()
    pygame.display.flip()


def draw_hud():
    text = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
    screen.blit(text, (10, 10))
    text2 = font.render(f"Pontos2: {score2}   Vidas2: {lives2}", True, WHITE)
    screen.blit(text2, (10, 40))


# ----------------------------------------------------------
# 🕹️ LOOP PRINCIPAL
# ----------------------------------------------------------
menu()
while running:

    clock.tick(FPS)
    frame_index = (frame_index + 0.2) % len(frames)
    frame_atual = frames[int(frame_index)]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimento jogador 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0: player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH: player_rect.x += player_speed
    if keys[pygame.K_UP] and player_rect.top > 0: player_rect.y -= player_speed
    if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT: player_rect.y += player_speed

    # Movimento jogador 2
    if keys[pygame.K_a] and player2_rect.left > 0: player2_rect.x -= player2_speed
    if keys[pygame.K_d] and player2_rect.right < WIDTH: player2_rect.x += player2_speed
    if keys[pygame.K_w] and player2_rect.top > 0: player2_rect.y -= player2_speed
    if keys[pygame.K_s] and player2_rect.bottom < HEIGHT: player2_rect.y += player2_speed

    # Movimento meteoros
    for meteor in meteor_list:
        meteor.y += meteor_speed

        if meteor.y > HEIGHT:
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)

            if not death:
                score += 1
            if not death2:
                score2 += 1

            if sound_point:
                sound_point.play()

        if meteor.colliderect(player_rect) and not death:
            lives -= 1
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)
            if sound_hit:
                sound_hit.play()

        if meteor.colliderect(player2_rect) and not death2:
            lives2 -= 1
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)
            if sound_hit:
                sound_hit.play()

    # Se os dois morrerem → fim do jogo
    if lives <= 0 and lives2 <= 0:
        running = False

    # Fases
    if score >= 30 or score2 >= 30:
        win()
    elif score >= 20 or score2 >= 20:
        fase3()
    elif score >= 10 or score2 >= 10:
        fase2()
    else:
        fase1()

lose()

# Tela final
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            waiting = False

pygame.quit()
