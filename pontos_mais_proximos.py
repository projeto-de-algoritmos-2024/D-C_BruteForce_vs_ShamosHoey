from collections import deque
import pygame as pg
import random
import numpy as np
import sys
from pygame.sprite import Sprite

pg.init()

def dividir_pontos(pontos):
    p = deque(pontos)
    esquerda = [p.popleft() for _ in range(len(p)//2)]
    direita = [p.popleft() for _ in range(len(p))]
    return esquerda, direita

def forca_bruta(circulos):
    if len(circulos) <= 1:
        return []
    if len(circulos) == 2:
        return circulos

    par = [circulos[0], circulos[1]]
    menor_distancia = distancia(par[0], par[1])
    for i in range(len(circulos)):
        for j in range(i + 1, len(circulos)):
            nova_distancia = distancia(circulos[i], circulos[j])
            if nova_distancia < menor_distancia:
                par = [circulos[i], circulos[j]]
                menor_distancia = nova_distancia

    return par

def mais_proximo_na_faixa(circulos):
    if len(circulos) < 2:
        return None
    par = [circulos[0], circulos[1]]
    menor_distancia = distancia(par[0], par[1])
    circulos = sorted(circulos, key=lambda s: s.pos.y)
    for i in range(len(circulos)):
        for j in range(i+1, min(len(circulos), i+7)):
            nova_distancia = distancia(circulos[i], circulos[j])
            if nova_distancia < menor_distancia:
                par = [circulos[i], circulos[j]]
                menor_distancia = nova_distancia

    return par

def dividir_e_conquistar(circulos):
    if len(circulos) <= 3:
        return forca_bruta(circulos)

    esquerda, direita = dividir_pontos(circulos)
    par_esquerda_mais_proximo = dividir_e_conquistar(esquerda)
    par_direita_mais_proximo = dividir_e_conquistar(direita)

    distancia_esquerda = distancia(par_esquerda_mais_proximo[0], par_esquerda_mais_proximo[1])
    distancia_direita = distancia(par_direita_mais_proximo[0], par_direita_mais_proximo[1])
    delta = min(distancia_esquerda, distancia_direita)

    meio = esquerda[len(esquerda)-1].pos.x
    circulos_na_faixa = [a for a in circulos if abs(a.pos.x - meio) < delta]
    par_mais_proximo_na_faixa = mais_proximo_na_faixa(circulos_na_faixa)

    if par_mais_proximo_na_faixa:
        if distancia(par_mais_proximo_na_faixa[0], par_mais_proximo_na_faixa[1]) < delta:
            return par_mais_proximo_na_faixa

    return par_esquerda_mais_proximo if distancia_esquerda < distancia_direita else par_direita_mais_proximo

def ajustar_direcao_aleatoriamente() -> float:
    return (random.random() - 0.5) * 0.2

def verificar_colisao_com_parede(posicao, direcao) -> float:
    x, y = posicao
    if x > 750: direcao = np.pi
    if x < 0: direcao = 0
    if y > 750: direcao = np.pi/2
    if y < 0: direcao = np.pi*1.5

    return direcao

def distancia(circulo1, circulo2) -> float:
    return np.sqrt(
        (np.abs(circulo1.pos.x - circulo2.pos.x)**2) +
        (np.abs(circulo1.pos.y - circulo2.pos.y)**2)
    )

class Ponto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Circulo(Sprite):
    def __init__(self, jogo, x, y):
        Sprite.__init__(self, jogo.circulos)
        self.jogo = jogo
        self.raio = 5
        self.image = pg.Surface((self.raio * 2, self.raio * 2), pg.SRCALPHA)
        pg.draw.circle(self.image, (0, 0, 0), (self.raio, self.raio), self.raio)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = Ponto(x, y)
        self.direcao = random.random() * 2 * np.pi
        self.velocidade = 3

    def caminhada_aleatoria(self):
        self.direcao = verificar_colisao_com_parede(self.rect.center, self.direcao)
        self.direcao += ajustar_direcao_aleatoriamente()

        mover_x = np.cos(self.direcao) * self.velocidade
        mover_y = np.sin(self.direcao) * -self.velocidade
        self.pos.x += mover_x
        self.pos.y += mover_y
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

    def update(self):
        self.caminhada_aleatoria()

class Jogo:
    def __init__(self):
        pg.display.set_caption('Par Mais Próximo - Comparar Algoritmos')
        self.relogio = pg.time.Clock()
        self.tela = pg.display.set_mode((1500, 750))
        self.fonte = pg.font.Font(None, 36)
        self.intervalo_adicionar_circulo = 1000
        self.ultimo_tempo_adicionar_circulo = pg.time.get_ticks()
        self.circulos = pg.sprite.Group()
        self.algoritmo = dividir_e_conquistar
        self.nome_algoritmo = "Dividir e Conquistar"

    def novo(self):
        self.circulos.empty()
        for _ in range(50):
            self.adicionar_circulo()

    def rodar(self):
        self.jogando = True
        while self.jogando:
            self.relogio.tick(60)
            self.eventos()
            self.atualizar()
            self.desenhar()

    def desenhar(self):
        self.tela.fill((255, 255, 255))

        superficie_esquerda = pg.Surface((750, 750), pg.SRCALPHA)
        superficie_direita = pg.Surface((750, 750), pg.SRCALPHA)

        superficie_esquerda.fill((255, 255, 255))
        superficie_direita.fill((255, 255, 255))

        if self.nome_algoritmo == "Dividir e Conquistar":
            par_dc = dividir_e_conquistar(list(self.circulos))
            if par_dc:
                for circulo in self.circulos:
                    if circulo in par_dc:
                        pg.draw.circle(circulo.image, (200, 0, 0), (circulo.raio, circulo.raio), circulo.raio)
                    else:
                        pg.draw.circle(circulo.image, (0, 0, 0), (circulo.raio, circulo.raio), circulo.raio)
            self.circulos.draw(superficie_esquerda)
            self.exibir_informacoes(superficie_esquerda, len(self.circulos), "Dividir e Conquistar")

        elif self.nome_algoritmo == "Força Bruta":
            par_fb = forca_bruta(list(self.circulos))
            if par_fb:
                for circulo in self.circulos:
                    if circulo in par_fb:
                        pg.draw.circle(circulo.image, (200, 0, 0), (circulo.raio, circulo.raio), circulo.raio)
                    else:
                        pg.draw.circle(circulo.image, (0, 0, 0), (circulo.raio, circulo.raio), circulo.raio)
            self.circulos.draw(superficie_direita)
            self.exibir_informacoes(superficie_direita, len(self.circulos), "Força Bruta")

        self.tela.blit(superficie_esquerda, (0, 0))
        self.tela.blit(superficie_direita, (750, 0))
        pg.display.flip()

    def exibir_informacoes(self, superficie, num_circulos, algoritmo):
        texto = self.fonte.render(f'Algoritmo: {algoritmo}', True, (0, 0, 0))
        superficie.blit(texto, (10, 10))
        texto = self.fonte.render(f'Círculos: {num_circulos}', True, (0, 0, 0))
        superficie.blit(texto, (10, 50))

    def adicionar_circulo(self):
        x = random.randint(0, 750)
        y = random.randint(0, 750)
        Circulo(self, x, y)

    def atualizar(self):
        self.circulos.update()

        tempo_atual = pg.time.get_ticks()
        if tempo_atual - self.ultimo_tempo_adicionar_circulo > self.intervalo_adicionar_circulo:
            self.adicionar_circulo()
            self.ultimo_tempo_adicionar_circulo = tempo_atual

    def eventos(self):
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                self.jogando = False
                pg.quit()
                sys.exit()

            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_q:
                    self.jogando = False
                    pg.quit()
                    sys.exit()

                if evento.key == pg.K_SPACE:
                    if self.nome_algoritmo == "Dividir e Conquistar":
                        self.nome_algoritmo = "Força Bruta"
                        self.algoritmo = forca_bruta
                    else:
                        self.nome_algoritmo = "Dividir e Conquistar"
                        self.algoritmo = dividir_e_conquistar

if __name__ == '__main__':
    jogo = Jogo()
    jogo.novo()
    jogo.rodar()
