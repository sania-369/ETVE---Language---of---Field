import pygame
import random
import math

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
        self.color = (255, 255, 200) # Базовый цвет — жёлтый

    def update(self, solitons, coherence):
        # Взаимодействие с другими солитонами (упрощённая гравитация + отталкивание)
        for other in solitons:
            if other is self:
                continue
            dx = other.x - self.x
            dy = other.y - self.y
            dist = math.hypot(dx, dy)
            if dist == 0: dist = 1

            # Гравитация (притяжение)
            force = 0.005 * self.mass * other.mass / (dist * dist)
            # Полевое отталкивание на близких дистанциях
            if dist < self.radius + other.radius:
                force = -0.1 * force
            
            self.vx += (dx / dist) * force
            self.vy += (dy / dist) * force

        # Влияние общей когерентности поля (замедление хаоса)
        if coherence > 0.5:
            self.vx *= 0.995
            self.vy *= 0.995

        # Обновление позиции
        self.x += self.vx
        self.y += self.vy

        # Границы (упругое отражение)
        if self.x < 0 or self.x > WIDTH: self.vx *= -1
        if self.y < 0 or self.y > HEIGHT: self.vy *= -1
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def draw(self, screen, coherence):
        # Цвет зависит от когерентности: чем выше C, тем ярче и "горячее" цвет
        r = min(255, int(self.color[0] * (1 + coherence)))
        g = min(255, int(self.color[1] * (1 + coherence)))
        b = min(255, int(self.color[2] * (1 + coherence)))
        pygame.draw.circle(screen, (r, g, b), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius, 1)

# Основная функция игры
def main():
    running = True
    solitons = []
    coherence = 0.0 # Глобальная когерентность поля (0.0 - 1.0)

    while running:
        # Обработка ввода
        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Z-принцип: ПРОБЕЛ повышает когерентность "Наблюдателя"
        if keys[pygame.K_SPACE]:
            coherence = min(1.0, coherence + 0.01)
        else:
            coherence = max(0.0, coherence - 0.005)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Клик — рождение нового солитона
                if event.button == 1: # Левая кнопка мыши
                    solitons.append(Soliton(mouse_x, mouse_y))

        # Фон поля зависит от когерентности
        bg_color = (int(10 * coherence), int(10 * coherence), int(20 * coherence))
        screen.fill(bg_color)

        # Обновление и отрисовка солитонов
        for s in solitons:
            s.update(solitons, coherence)
            s.draw(screen, coherence)

        # Отображение интерфейса
        font = pygame.font.SysFont(None, 24)
        text1 = font.render(f'Когерентность (C): {coherence:.2f} (Нажми ПРОБЕЛ для повышения)', True, (255, 255, 255))
        text2 = font.render(f'Солитонов: {len(solitons)} (Клик для создания)', True, (255, 255, 255))
        screen.blit(text1, (10, 10))
        screen.blit(text2, (10, 40))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
