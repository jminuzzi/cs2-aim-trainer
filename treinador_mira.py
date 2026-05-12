
import pygame
import random
import math
import sys

# Inicialização
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Treinador de Mira - CS2 Style")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 150, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)

# Fonte
font = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 28)

class Bot:
    def __init__(self):
        self.reset()

    def reset(self):
        # Posição aleatória na tela
        self.x = random.randint(100, SCREEN_WIDTH - 100)
        self.y = random.randint(100, SCREEN_HEIGHT - 100)

        # Tamanho do bot (corpo)
        self.width = 60
        self.height = 120

        # Cabeça (zona de acerto)
        self.head_radius = 25
        self.head_x = self.x
        self.head_y = self.y - self.height//2 - 10

        # Movimento
        self.speed_x = random.choice([-1, 1]) * random.uniform(1, 3)
        self.speed_y = random.choice([-1, 1]) * random.uniform(0.5, 2)

        # Tipo de movimento
        self.move_type = random.choice(['linear', 'strafe', 'jump'])
        self.jump_timer = 0
        self.base_y = self.y

    def update(self):
        if self.move_type == 'linear':
            self.x += self.speed_x
            self.y += self.speed_y

        elif self.move_type == 'strafe':
            self.x += self.speed_x * 2
            # Mantém na mesma altura

        elif self.move_type == 'jump':
            self.x += self.speed_x
            self.jump_timer += 0.1
            self.y = self.base_y - abs(math.sin(self.jump_timer)) * 80

        # Atualiza posição da cabeça
        self.head_x = self.x
        self.head_y = self.y - self.height//2 - 10

        # Bounce nas bordas
        if self.x < 50 or self.x > SCREEN_WIDTH - 50:
            self.speed_x *= -1
        if self.y < 100 or self.y > SCREEN_HEIGHT - 50:
            self.speed_y *= -1
            self.base_y = self.y

    def draw(self, surface):
        # Corpo (retângulo)
        body_rect = pygame.Rect(
            self.x - self.width//2,
            self.y - self.height//2,
            self.width,
            self.height
        )
        pygame.draw.rect(surface, BLUE, body_rect)
        pygame.draw.rect(surface, WHITE, body_rect, 2)

        # Cabeça (círculo)
        pygame.draw.circle(surface, GRAY, (int(self.head_x), int(self.head_y)), self.head_radius)
        pygame.draw.circle(surface, WHITE, (int(self.head_x), int(self.head_y)), self.head_radius, 2)

    def check_headshot(self, mouse_x, mouse_y):
        dist = math.sqrt((mouse_x - self.head_x)**2 + (mouse_y - self.head_y)**2)
        return dist <= self.head_radius

class Crosshair:
    def __init__(self):
        self.size = 20
        self.thickness = 2
        self.gap = 8

    def draw(self, surface, x, y, on_target):
        color = GREEN if on_target else RED

        # Linhas da crosshair (estilo CS2)
        # Esquerda
        pygame.draw.line(surface, color, (x - self.gap - self.size, y), (x - self.gap, y), self.thickness)
        # Direita
        pygame.draw.line(surface, color, (x + self.gap, y), (x + self.gap + self.size, y), self.thickness)
        # Cima
        pygame.draw.line(surface, color, (x, y - self.gap - self.size), (x, y - self.gap), self.thickness)
        # Baixo
        pygame.draw.line(surface, color, (x, y + self.gap), (x, y + self.gap + self.size), self.thickness)

        # Ponto central
        pygame.draw.circle(surface, color, (x, y), 2)

def main():
    clock = pygame.time.Clock()

    # Esconde o cursor padrão
    pygame.mouse.set_visible(False)

    # Cria bots
    num_bots = 3
    bots = [Bot() for _ in range(num_bots)]

    # Crosshair
    crosshair = Crosshair()

    # Estatísticas
    hits = 0
    shots = 0
    headshot_streak = 0
    best_streak = 0

    running = True
    on_target = False

    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    # Reseta bots
                    bots = [Bot() for _ in range(num_bots)]
                    hits = 0
                    shots = 0
                    headshot_streak = 0
                if event.key == pygame.K_UP:
                    num_bots = min(num_bots + 1, 10)
                    bots.append(Bot())
                if event.key == pygame.K_DOWN:
                    num_bots = max(num_bots - 1, 1)
                    bots = bots[:num_bots]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clique esquerdo
                    shots += 1
                    hit = False
                    for bot in bots:
                        if bot.check_headshot(mouse_x, mouse_y):
                            hits += 1
                            hit = True
                            bot.reset()  # Respawn

                    if hit:
                        headshot_streak += 1
                        best_streak = max(best_streak, headshot_streak)
                    else:
                        headshot_streak = 0

        # Atualiza
        for bot in bots:
            bot.update()

        # Verifica se mira está na cabeça
        on_target = any(bot.check_headshot(mouse_x, mouse_y) for bot in bots)

        # Desenha
        screen.fill(DARK_GRAY)

        # Desenha bots
        for bot in bots:
            bot.draw(screen)

        # Desenha crosshair
        crosshair.draw(screen, mouse_x, mouse_y, on_target)

        # HUD
        accuracy = (hits / shots * 100) if shots > 0 else 0

        texts = [
            f"Headshots: {hits}",
            f"Tiros: {shots}",
            f"Precisão: {accuracy:.1f}%",
            f"Sequência: {headshot_streak}",
            f"Recorde: {best_streak}",
            f"Bots: {num_bots}",
            "",
            "[R] Reset | [↑↓] Bots | [ESC] Sair"
        ]

        y_offset = 10
        for text in texts:
            if text:
                surface = font_small.render(text, True, WHITE)
                screen.blit(surface, (10, y_offset))
            y_offset += 25

        # Indicador de mira na cabeça
        if on_target:
            indicator = font.render("HEADSHOT!", True, GREEN)
            screen.blit(indicator, (SCREEN_WIDTH//2 - 60, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
