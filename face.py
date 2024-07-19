import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Definição das cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Configurações da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Desenho de Olhos e Boca")

# Função para desenhar a boca
def draw_mouth():
    mouth_top_start = (screen_width // 2 - 50, screen_height // 2 + 100)
    mouth_top_end = (screen_width // 2 + 50, screen_height // 2 + 100)
    pygame.draw.line(screen, WHITE, mouth_top_start, mouth_top_end, 5)

    mouth_bottom_start = (screen_width // 2 - 50, screen_height // 2 + 110)
    mouth_bottom_end = (screen_width // 2 + 50, screen_height // 2 + 110)
    pygame.draw.line(screen, RED, mouth_bottom_start, mouth_bottom_end, 10)

# Função para desenhar os olhos abertos
def draw_eyes():
    eye_radius = 50
    eye_color = WHITE
    left_eye_center = (screen_width // 3, screen_height // 3)
    right_eye_center = (2 * screen_width // 3, screen_height // 3)
    pygame.draw.circle(screen, eye_color, left_eye_center, eye_radius)
    pygame.draw.circle(screen, eye_color, right_eye_center, eye_radius)

# Função para desenhar os olhos fechados
def draw_closed_eyes():
    left_eye_start = (screen_width // 3 - 50, screen_height // 3)
    left_eye_end = (screen_width // 3 + 50, screen_height // 3)
    right_eye_start = (2 * screen_width // 3 - 50, screen_height // 3)
    right_eye_end = (2 * screen_width // 3 + 50, screen_height // 3)
    pygame.draw.line(screen, WHITE, left_eye_start, left_eye_end, 5)
    pygame.draw.line(screen, WHITE, right_eye_start, right_eye_end, 5)

# Configurações para o piscar dos olhos
blink_start_time = pygame.time.get_ticks()
blink_interval = random.randint(2000, 5000)  # Piscar entre 2 e 5 segundos
blink_duration = 200  # Duração do piscar (200 ms)

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Limpar a tela
    screen.fill(BLACK)

    # Verificar se está na hora de piscar
    current_time = pygame.time.get_ticks()
    if current_time - blink_start_time < blink_duration:
        draw_closed_eyes()
    else:
        draw_eyes()
        if current_time - blink_start_time >= blink_interval:
            blink_start_time = pygame.time.get_ticks()
            blink_interval = random.randint(2000, 5000)  # Recalcular o intervalo de piscar

    # Desenhar a boca
    draw_mouth()

    # Atualizar a tela
    pygame.display.flip()
