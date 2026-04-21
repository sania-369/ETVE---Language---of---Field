import asyncio
import pygame
import random
import math
import sys

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🌀 Полевой Симулятор (ЕТВП) — Нажми ПРОБЕЛ для когерентности")
clock = pygame.time.Clock()

# Класс Солитона
class Soliton:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.mass = random.uniform(5, 15)
        self.radius = int(self.mass)
        self.color = (255, 255, 200)

    def update(self, solitons, coherence):
        for other in solitons:
            if other is self:
                continue
            dx = other.x - self.x
            dy = other.y - self.y
            dist = math.hypot(dx, dy)
            if dist == 0:
                dist = 1

            force = 0.005 * self.mass * other.mass / (dist * dist)
            if dist < self.radius + other.radius:
                force = -0.1 * force

            self.vx += (dx / dist) * force
            self.vy += (dy / dist) * force

        if coherence > 0.5:
            self.vx *= 0.995
            self.vy *= 0.995

        self.x += self.vx
        self.y += self.vy

        if self.x < 0 or self.x > WIDTH:
            self.vx *= -1
        if self.y < 0 or self.y > HEIGHT:
            self.vy *= -1
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def draw(self, screen, coherence):
        r = min(255, int(self.color[0] * (1 + coherence)))
        g = min(255, int(self.color[1] * (1 + coherence)))
        b = min(255, int(self.color[2] * (1 + coherence)))
        pygame.draw.circle(screen, (r, g, b), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius, 1)

async def main():
    running = True
    solitons = []
    coherence = 0.0

    while running:
        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if keys[pygame.K_SPACE]:
            coherence = min(1.0, coherence + 0.01)
        else:
            coherence = max(0.0, coherence - 0.005)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    solitons.append(Soliton(mouse_x, mouse_y))

        bg_color = (int(10 * coherence), int(10 * coherence), int(20 * coherence))
        screen.fill(bg_color)

        for s in solitons:
            s.update(solitons, coherence)
            s.draw(screen, coherence)

        font = pygame.font.SysFont(None, 24)
        text1 = font.render(f'Когерентность (C): {coherence:.2f} (Нажми ПРОБЕЛ для повышения)', True, (255, 255, 255))
        text2 = font.render(f'Солитонов: {len(solitons)} (Клик для создания)', True, (255, 255, 255))
        screen.blit(text1, (10, 10))
        screen.blit(text2, (10, 40))

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

asyncio.run(main())
