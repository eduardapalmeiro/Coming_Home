##############################################################
###               C O M I N G       H O M E                ###
##############################################################
### Objetivo: Levar o alien até sua casa e sobreviver      ###
### aos obstaculos.                                        ###
##############################################################
### Refatorado com OOP (Classes) para animação independente ###
##############################################################

import pygame
import random
import os
import cv2  # Biblioteca necessária para vídeo

# Inicializa o PyGame
pygame.init()
pygame.mixer.init()

# ----------------------------------------------------------
# 🔧 CONFIGURAÇÕES GERAIS
# ----------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("👽 Coming home 👽")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Cores
WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)
GREEN = (50, 239, 106)
DARK_GREEN = (13, 98, 70)

# ----------------------------------------------------------
# 🧩 SEÇÃO DE ASSETS (Gerenciamento de Recursos)
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
    "death_sound": "videogame-death-sound-43894.mp3",
    "menubg": "menubg.png",
    "winimg": "teladefinalbom.png",
    "loseimg": "teladefinalruim.png",
    "meteorolifeimg": "coracaometeoro.png",
    "transicaoFase1-2video": "1-2.mp4",
    "transicaoFase2-3video": "2-3.mp4",
    # Frames da animação do meteoro
    "anim_meteoro": ["meteoro001.png", "meteoro002.png", "meteoro003.png"]
}


def load_image(filename, fallback_color, size=None):
    """Carrega imagem com segurança. Cria um quadrado colorido se falhar."""
    if os.path.exists(filename):
        try:
            img = pygame.image.load(filename).convert_alpha()
            if size:
                img = pygame.transform.scale(img, size)
            return img
        except Exception as e:
            print(f"Erro ao ler imagem {filename}: {e}")
    else:
        print(f"Arquivo não encontrado: {filename}")

    # Fallback (quadrado colorido)
    surf = pygame.Surface(size or (50, 50))
    surf.fill(fallback_color)
    return surf


def load_sound(filename):
    if os.path.exists(filename):
        return pygame.mixer.Sound(filename)
    return None


# --- Carregamento ---
background = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
background2 = load_image(ASSETS["background2"], WHITE, (WIDTH, HEIGHT))
background3 = load_image(ASSETS["background3"], WHITE, (WIDTH, HEIGHT))
player_img = load_image(ASSETS["player"], BLUE, (64, 64))
player2_img = load_image(ASSETS["player2"], BLUE, (64, 64))
meteorosLife_img = load_image(ASSETS["meteorolifeimg"], RED, (40, 40))
menubg = load_image(ASSETS["menubg"], WHITE, (WIDTH, HEIGHT))
winimg = load_image(ASSETS["winimg"], WHITE, (WIDTH, HEIGHT))
loseimg = load_image(ASSETS["loseimg"], WHITE, (WIDTH, HEIGHT))

# Carrega Animação do Meteoro
meteor_frames = []
for frame_file in ASSETS["anim_meteoro"]:
    img = load_image(frame_file, (100, 100, 100), (40, 40))
    meteor_frames.append(img)

# Sons
sound_point = load_sound(ASSETS["sound_point"])
if sound_point: sound_point.set_volume(0.2)

sound_hit = load_sound(ASSETS["sound_hit"])
if sound_hit: sound_hit.set_volume(0.2)

if os.path.exists(ASSETS["music"]):
    pygame.mixer.music.load(ASSETS["music"])
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)


# ----------------------------------------------------------
# 🏛️ CLASSES (A SOLUÇÃO OOP)
# ----------------------------------------------------------

class Meteor(pygame.sprite.Sprite):
    def __init__(self, frames):
        super().__init__()
        self.frames = frames
        self.current_frame = 0  # Estado individual da animação
        self.anim_speed = 0.1  # Velocidade da animação

        self.image = self.frames[0]
        self.rect = self.image.get_rect()

        # Posição e velocidade iniciais
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(0, WIDTH - 40)
        self.rect.y = random.randint(-500, -50)
        self.speed_y = random.randint(4, 8)  # Velocidade variada

    def update(self):
        # 1. Movimento
        self.rect.y += self.speed_y

        # 2. Animação (Ciclo de frames)
        self.current_frame += self.anim_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

        # 3. Reset se sair da tela
        if self.rect.y > HEIGHT:
            self.reset_position()
            return True  # Retorna True se passou da tela (pontuação)
        return False


class LifeBonus(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.reset_position()
        self.speed_y = 5

    def reset_position(self):
        self.rect.x = random.randint(0, WIDTH - 40)
        self.rect.y = random.randint(-1500, -100)  # Aparecem menos frequentemente

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > HEIGHT:
            self.reset_position()


# ----------------------------------------------------------
# 🧠 VARIÁVEIS DE JOGO E GRUPOS
# ----------------------------------------------------------
player_rect = player_img.get_rect(center=(WIDTH // 2 - 50, HEIGHT - 60))
player2_rect = player2_img.get_rect(center=(WIDTH // 2 + 50, HEIGHT - 60))
player_speed = 7
player2_speed = 7

# Grupos de Sprites (Melhor gerenciamento)
meteor_group = pygame.sprite.Group()
life_group = pygame.sprite.Group()

# Criação dos Objetos
for _ in range(6):
    meteor_group.add(Meteor(meteor_frames))

for _ in range(2):
    life_group.add(LifeBonus(meteorosLife_img))

# Variáveis globais de estado
death = False
death2 = False
video_fase1_2_rodou = False
video_fase2_3_rodou = False
score = 0
lives = 3
score2 = 0
lives2 = 3

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
running = True


# ----------------------------------------------------------
# FUNÇÕES AUXILIARES
# ----------------------------------------------------------
def reproduzir_video(caminho_video):
    if not os.path.exists(caminho_video):
        return

    cap = cv2.VideoCapture(caminho_video)
    video_rodando = True

    while video_rodando:
        ret, frame = cap.read()
        if not ret:
            break

        # Rotação e correção de cor para Pygame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)
        frame = cv2.flip(frame, 0)  # Flip horizontal necessário após transpose

        frame_surface = pygame.surfarray.make_surface(frame)
        frame_surface = pygame.transform.scale(frame_surface, (WIDTH, HEIGHT))

        screen.blit(frame_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)  # ~30fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                video_rodando = False
    cap.release()


def menu():
    button_rect = pygame.Rect((WIDTH // 2 - 110, HEIGHT // 2 + 100), (220, 60))
    button_font = pygame.font.Font(None, 50)

    while True:
        screen.blit(menubg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]

        color = GREEN if button_rect.collidepoint(mouse_pos) else (16, 209, 74)
        if button_rect.collidepoint(mouse_pos) and clicked:
            pygame.time.delay(200)
            return

        pygame.draw.rect(screen, color, button_rect, border_radius=12)
        text = button_font.render("JOGAR", True, DARK_GREEN)
        screen.blit(text, text.get_rect(center=button_rect.center))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def game_over_screen(venceu=False):
    global score, score2
    screen.blit(winimg if venceu else loseimg, (0, 0))
    msg = "Você venceu!" if venceu else "Você perdeu!"

    txt_main = font.render(msg, True, WHITE)
    txt_score = font.render(f"Maior pontuação: {max(score, score2)}", True, WHITE)

    screen.blit(txt_main, txt_main.get_rect(center=(WIDTH // 2, 500)))
    screen.blit(txt_score, txt_score.get_rect(center=(WIDTH // 2, 450)))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        clock.tick(15)


def draw_hud():
    t1 = font.render(f"P1 Pontos: {score}   Vidas: {lives}", True, WHITE)
    t2 = font.render(f"P2 Pontos: {score2}   Vidas: {lives2}", True, WHITE)
    screen.blit(t1, (10, 10))
    screen.blit(t2, (WIDTH - t2.get_width() - 10, 10))


# ----------------------------------------------------------
# 🕹️ LOOP PRINCIPAL
# ----------------------------------------------------------
menu()

while running:
    clock.tick(FPS)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Verifica derrota global
    if death and death2:
        game_over_screen(venceu=False)
        break

    # --- Controles ---
    keys = pygame.key.get_pressed()

    # Player 1
    if not death:
        if keys[pygame.K_LEFT] and player_rect.left > 0: player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH: player_rect.x += player_speed
        if keys[pygame.K_UP] and player_rect.top > 0: player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT: player_rect.y += player_speed

    # Player 2
    if not death2:
        if keys[pygame.K_a] and player2_rect.left > 0: player2_rect.x -= player2_speed
        if keys[pygame.K_d] and player2_rect.right < WIDTH: player2_rect.x += player2_speed
        if keys[pygame.K_w] and player2_rect.top > 0: player2_rect.y -= player2_speed
        if keys[pygame.K_s] and player2_rect.bottom < HEIGHT: player2_rect.y += player2_speed

    # --- Update dos Objetos (Meteoros e Vidas) ---
    # Ao chamar update() no grupo, ele chama o update() de CADA objeto individualmente
    # Isso resolve a animação estática!

    # Lógica de Pontuação por desvio (baseada no retorno do update)
    for meteor in meteor_group:
        passou_tela = meteor.update()  # Chama update e verifica se retornou True
        if passou_tela:
            if not death: score += 1
            if not death2: score2 += 1
            if sound_point: sound_point.play()

    life_group.update()

    # --- Colisões ---
    # Meteoros (Dano)
    # collide_rect verifica sobreposição entre sprite e rect simples
    for meteor in meteor_group:
        if not death and meteor.rect.colliderect(player_rect):
            lives -= 1
            meteor.reset_position()
            if sound_hit: sound_hit.play()
            if lives <= 0: death = True

        if not death2 and meteor.rect.colliderect(player2_rect):
            lives2 -= 1
            meteor.reset_position()
            if sound_hit: sound_hit.play()
            if lives2 <= 0: death2 = True

    # Vidas (Bônus)
    for bonus in life_group:
        if not death and bonus.rect.colliderect(player_rect):
            lives += 1
            score += 5
            bonus.reset_position()
            if sound_point: sound_point.play()

        if not death2 and bonus.rect.colliderect(player2_rect):
            lives2 += 1
            score2 += 5
            bonus.reset_position()
            if sound_point: sound_point.play()

    # --- Gerenciamento de Fase ---
    current_max = max(score, score2)
    current_bg = background

    if current_max >= 150:
        game_over_screen(venceu=True)
        break
    elif current_max >= 100:
        if not video_fase2_3_rodou:
            reproduzir_video(ASSETS["transicaoFase2-3video"])
            video_fase2_3_rodou = True
        current_bg = background3
    elif current_max >= 50:
        if not video_fase1_2_rodou:
            reproduzir_video(ASSETS["transicaoFase1-2video"])
            video_fase1_2_rodou = True
        current_bg = background2

    # --- Desenho ---
    screen.blit(current_bg, (0, 0))

    if not death: screen.blit(player_img, player_rect)
    if not death2: screen.blit(player2_img, player2_rect)

    meteor_group.draw(screen)  # Desenha todos os meteoros
    life_group.draw(screen)  # Desenha todas as vidas

    draw_hud()
    pygame.display.flip()

pygame.quit()