from collections import deque
import pygame as pg
import random
import numpy as np
import sys
from pygame.sprite import Sprite

pg.init()

def split_points(points):
    """Divide a lista de pontos em duas partes aproximadamente iguais."""
    p = deque(points)
    left = [p.popleft() for _ in range(len(p)//2)]
    right = [p.popleft() for _ in range(len(p))]
    return left, right

def brute_force_pair(circles):
    """Encontra o par mais próximo usando o método de força bruta."""
    if len(circles) <= 1:
        return []
    if len(circles) == 2:
        return circles

    pair = [circles[0], circles[1]]
    shortest_dist = distance(pair[0], pair[1])
    for i in range(len(circles)):
        for j in range(len(circles)):
            if i == j: continue
            new_dist = distance(circles[i], circles[j])
            if new_dist < shortest_dist:
                pair = [circles[i], circles[j]]
                shortest_dist = new_dist

    return pair

def closest_within_band(circles):
    """Encontra o par mais próximo dentro de uma faixa de largura fixa."""
    if len(circles) < 2:
        return None
    pair = [circles[0], circles[1]]
    shortest_dist = distance(pair[0], pair[1])
    circles = sorted(circles, key=lambda s: s.pos.y)
    for i in range(len(circles)):
        for j in range(i+1, min(len(circles), i+7)):
            new_dist = distance(circles[i], circles[j])
            if new_dist < shortest_dist:
                pair = [circles[i], circles[j]]
                shortest_dist = new_dist

    return pair

def divide_and_conquer(circles):
    """Encontra o par mais próximo usando o algoritmo de divisão e conquista."""
    if len(circles) <= 3:
        return brute_force_pair(circles)

    left, right = split_points(circles)
    closest_left_pair = divide_and_conquer(left)
    closest_right_pair = divide_and_conquer(right)

    distance_left = distance(closest_left_pair[0], closest_left_pair[1])
    distance_right = distance(closest_right_pair[0], closest_right_pair[1])
    delta = min(distance_left, distance_right)

    middle = left[len(left)-1].pos.x
    circles_within_band = [a for a in circles if abs(a.pos.x - middle) < delta]
    closest_pair_band = closest_within_band(circles_within_band)

    if closest_pair_band:
        if distance(closest_pair_band[0], closest_pair_band[1]) < delta:
            return closest_pair_band

    return closest_left_pair if distance_left < distance_right else closest_right_pair

def adjust_direction_randomly() -> float:
    """Ajusta a direção aleatoriamente."""
    return (random.random() - 0.5) * 0.2

def wall_collision_check(pos, direction) -> float:
    """Verifica e ajusta a direção em caso de colisão com as bordas da tela."""
    x, y = pos
    if x > 750: direction = np.pi
    if x < 0: direction = 0
    if y > 750: direction = np.pi/2
    if y < 0: direction = np.pi*1.5

    return direction

def distance(circle1, circle2) -> float:
    """Calcula a distância entre dois círculos."""
    return np.sqrt(
        (np.abs(circle1.pos.x - circle2.pos.x)**2) + 
        (np.abs(circle1.pos.y - circle2.pos.y)**2)
    )

class Point:
    """Representa um ponto no plano 2D."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Circle(Sprite):
    """Representa um círculo no jogo."""
    def __init__(self, game, x, y):
        Sprite.__init__(self, game.circles)
        self.game = game
        self.radius = 5  # Tamanho do círculo
        self.image = pg.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)
        pg.draw.circle(self.image, (0, 0, 0), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = Point(x, y)
        self.direction = random.random() * 2 * np.pi
        self.speed = 3

    def random_walk(self):
        """Move o círculo aleatoriamente, ajustando a direção se necessário."""
        self.direction = wall_collision_check(self.rect.center, self.direction)
        self.direction += adjust_direction_randomly()

        move_x = np.cos(self.direction) * self.speed
        move_y = np.sin(self.direction) * -self.speed
        self.pos.x += move_x
        self.pos.y += move_y
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

    def update(self):
        """Atualiza o estado do círculo."""
        self.random_walk()

class Game:
    """Representa o jogo de comparação de algoritmos de pares mais próximos."""
    def __init__(self):
        pg.display.set_caption('Closest Pair - Compare Algorithms')
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((1500, 750))  # Tela dividida
        self.font = pg.font.Font(None, 36)
        self.add_circle_interval = 1000  # Intervalo em milissegundos
        self.last_circle_add_time = pg.time.get_ticks()
        self.circles = pg.sprite.Group()
        self.algorithm = divide_and_conquer  # Algoritmo padrão
        self.algorithm_name = "Divide e Conquista"

    def new(self):
        """Inicializa o jogo com círculos novos."""
        self.circles.empty()
        for _ in range(50):  # define o número de círculos iniciais
            self.add_circle()

    def run(self):
        """Inicia o loop principal do jogo."""
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def draw(self):
        """Desenha os círculos e a interface gráfica do jogo."""
        # Limpa a tela principal
        self.screen.fill((255, 255, 255))

        # Cria superfícies para cada lado da tela
        left_surface = pg.Surface((750, 750), pg.SRCALPHA)
        right_surface = pg.Surface((750, 750), pg.SRCALPHA)

        # Limpa as superfícies
        left_surface.fill((255, 255, 255))
        right_surface.fill((255, 255, 255))

        # Algoritmo Divide e Conquista
        if self.algorithm_name == "Divide e Conquista":
            pair_dc = divide_and_conquer(list(self.circles))
            if pair_dc:
                for circle in self.circles:
                    if circle in pair_dc:
                        pg.draw.circle(circle.image, (200, 0, 0), (circle.radius, circle.radius), circle.radius)
                    else:
                        pg.draw.circle(circle.image, (0, 0, 0), (circle.radius, circle.radius), circle.radius)
            self.circles.draw(left_surface)
            self.display_info(left_surface, len(self.circles), "Divide e Conquista")

        # Algoritmo Força Bruta
        elif self.algorithm_name == "Força Bruta":
            pair_bf = brute_force_pair(list(self.circles))
            if pair_bf:
                for circle in self.circles:
                    if circle in pair_bf:
                        pg.draw.circle(circle.image, (200, 0, 0), (circle.radius, circle.radius), circle.radius)
                    else:
                        pg.draw.circle(circle.image, (0, 0, 0), (circle.radius, circle.radius), circle.radius)
            self.circles.draw(right_surface)
            self.display_info(right_surface, len(self.circles), "Força Bruta")

        # Atualiza a tela principal com as superfícies divididas
        self.screen.blit(left_surface, (0, 0))
        self.screen.blit(right_surface, (750, 0))
        pg.display.update()

    def update(self):
        """Atualiza o estado do jogo e adiciona novos círculos conforme necessário."""
        self.circles.update()

        # Verifica se é hora de adicionar um novo círculo
        current_time = pg.time.get_ticks()
        if current_time - self.last_circle_add_time > self.add_circle_interval:
            self.add_circle()
            self.last_circle_add_time = current_time

    def events(self):
        """Processa eventos de entrada do usuário."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.toggle_algorithm()

    def display_info(self, sub_screen, n_points, algorithm_name):
        """Exibe informações sobre o algoritmo e o FPS."""
        # Calcular o FPS
        fps = self.clock.get_fps()
        # Texto para exibir o número de pontos e FPS
        text = f'{algorithm_name}: Pontos: {n_points} - FPS: {fps:.2f}'
        # Renderizar o texto
        text_surface = self.font.render(text, True, (0, 0, 0))
        # Desenhar o texto na tela
        sub_screen.blit(text_surface, (10, 10))

    def add_circle(self):
        """Adiciona um novo círculo na tela."""
        x = random.randint(10, 740)
        y = random.randint(10, 740)
        Circle(self, x, y)

    def toggle_algorithm(self):
        """Alterna entre os algoritmos de comparação de pares mais próximos."""
        if self.algorithm_name == "Divide e Conquista":
            self.algorithm_name = "Força Bruta"
            self.algorithm = brute_force_pair
        else:
            self.algorithm_name = "Divide e Conquista"
            self.algorithm = divide_and_conquer

    def quit(self):
        """Encerra o jogo e fecha o pygame."""
        pg.quit()
        sys.exit()

g = Game()
g.new()
g.run()
