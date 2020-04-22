import pygame, random
from pygame import *
from time import sleep

imagem_de_fundo = pygame.image.load('Background_do_jogo_800x600.jpg')


def musica_jogatina():
    # Música de fundo do jogo durante a jogatina
    pygame.mixer.music.load('musica_jogo.wav')
    pygame.mixer.music.play()


def comer_a_comida(colisao_cobra, colisao_comida):
    """nessa parte, quando a cabeça da cobra ficar na mesma posição da comida ela come,
    aumenta de tamanho e a comida aparce em outro lugar."""
    return colisao_cobra[0] == colisao_comida[0] and colisao_cobra[1] == colisao_comida[1]

#isso é necessário para aparecer a pontuação, game over e os níveis
pygame.font.init()

pygame.init()

#texto que vai aparecer quando der game over
texto_gameover = 'Game Over'

tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Python em Python')

pontuacao = 0
contador = 0
cont = 10
level_v = 1 # level verdadeiro
level = 0

# chama a função que inicia a música do jogo
musica_jogatina()

# valores das direções que a cobra vai andar
para_cima = 0
para_direita = 1
para_baixo = 2
para_esquerda = 3

# Corpo da cobra
cobra = [(200, 200), (210, 200), (220, 200)]
pele_da_cobra = pygame.Surface((10, 10))
pele_da_cobra.fill((255, 255, 0))
cabeca_da_cobra = pygame.Surface((10, 10))
cabeca_da_cobra.fill((0, 0, 255))

# Nessa função a comida vai aparecer em algum lugar randômico sem está fora da linha, isto é, "10 por 10"
def comida_do_rato():
    x = random.randint(20, 10)
    y = random.randint(0, 590)
    l = (x // 10 * 10, y // 10 * 10)
    if l not in cobra:
        return l
    else:
        return comida_do_rato()

# criando a comida
rato_comer = comida_do_rato()
rato = pygame.Surface((10, 10))
rato.fill((255, 70, 30))

# direção inicial da cobra(A cabeça está do lado esquedo, logo o corpo cresce para o lado direito)
direção = para_esquerda



movimentação_da_cobra = pygame.time.Clock()
inicio_do_jogo = True

while inicio_do_jogo:
    if pontuacao >= 0:
        movimentação_da_cobra.tick(cont)  # aqui é a velocidade que a cobra vai andar

    for event in pygame.event.get():  # Faz tem a opção de fechar o jogo
        if event.type == QUIT:
            pygame.quit()

    if level == 4:
        cont = cont + 5
        level = 0
        level_v = level_v + 1

    tela.blit(imagem_de_fundo, (0, 0))

    #tela cheia
    if event.type == KEYUP:
        if event.key == K_F10:
            pygame.display.toggle_fullscreen()

    #AQUI FAZ COM QUE O MAUSE NÃO APARECE NA TELA DO JOGO
    pygame.mouse.set_visible(False)

    #Nessa parte determina as direções em que a cobra anda, nesse aqui são as setas
    if event.type == KEYDOWN:
        if event.key == K_UP:
            if direção != para_baixo:
                direção = para_cima
        if event.key == K_DOWN:
            if direção != para_cima:
                direção = para_baixo
        if event.key == K_LEFT:
            if direção != para_direita:
                direção = para_esquerda
        if event.key == K_RIGHT:
            if direção != para_esquerda:
                direção = para_direita

    # Nessa parte determina as direções em que a cobra anda, nesse aqui são W,A,S,D
    if event.type == KEYDOWN:
        if event.key == K_w:
            if direção != para_baixo:
                direção = para_cima
        if event.key == K_s:
            if direção != para_cima:
                direção = para_baixo
        if event.key == K_a:
            if direção != para_direita:
                direção = para_esquerda
        if event.key == K_d:
            if direção != para_esquerda:
                direção = para_direita

    # Nessa parte a cobra come a maçã e em seguida cresce
    if comer_a_comida(cobra[0], rato_comer):
        rato_comer = comida_do_rato()
        pontuacao = pontuacao + 25
        cobra.append((0, 0))
        level = level + 1

    # Aqui faz o corpo andar junto com a cabeça
    for k in range(len(cobra) - 1, 0, -1):
        cobra[k] = (cobra[k - 1][0], cobra[k - 1][1])

    if direção == para_cima:
        cobra[0] = (cobra[0][0], cobra[0][1] - 10)
    if direção == para_baixo:
        cobra[0] = (cobra[0][0], cobra[0][1] + 10)
    if direção == para_direita:
        cobra[0] = (cobra[0][0] + 10, cobra[0][1])
    if direção == para_esquerda:
        cobra[0] = [cobra[0][0] - 10, cobra[0][1]]

    #Aqui da Game Over se a cobra tentar sair da tela do jogo
    if cobra[0][0] == 800 or cobra[0][1] == 600 or cobra[0][0] < 0 or cobra[0][1] < 0:
        mostrar_pont = pygame.font.SysFont(font, 80)
        texto_over = mostrar_pont.render('%s' % (texto_gameover), True, (200, 30, 50))
        pygame.mixer_music.stop()
        pygame.mixer.music.load('game_over1.wav')
        pygame.mixer.music.play()
        sleep(5)
        tela.blit(texto_over, (250, 250))
        pygame.display.update()
        inicio_do_jogo = False
        break

    #aqui da Game Over se a cobra tentar comer a si mesma
    for i in range(1, len(cobra) - 1):
        if cobra[0][0] == cobra[i][0] and cobra[0][1] == cobra[i][1]:
            mostrar_pont = pygame.font.SysFont(font, 80)
            texto_over = mostrar_pont.render('%s' % (texto_gameover), True, (200, 30, 50))
            pygame.mixer_music.stop()
            pygame.mixer.music.load('game_over1.wav')
            pygame.mixer.music.play()
            sleep(5)
            tela.blit(texto_over, (250, 250))
            pygame.display.update()
            inicio_do_jogo = False

    #tela.fill((255, 255, 255))
    tela.blit(rato, rato_comer)
    tela.blit(cabeca_da_cobra, cobra[0])
    for i in range(1, len(cobra)):
        tela.blit(pele_da_cobra, cobra[i])

    #for pos in cobra:
    #tela.blit(pele_da_cobra, pos)

    #Nessa parte faz aparecer a pontuação do jogador
    font = pygame.font.get_default_font()  # Fonte padrão
    mostrar_pont = pygame.font.SysFont(font, 40)  # tamanho 40
    texto_pontuacao = mostrar_pont.render('Pontuação: %s' % (pontuacao), True, (255, 200, 70))
    tela.blit(texto_pontuacao, (550, 10))

    #NESSA PARTE AQUI É ONDE APARECE OS NÍVELS NO JOGO
    font = pygame.font.get_default_font()  # Fonte padrão
    mostrar_pont = pygame.font.SysFont(font, 40)  # tamanho 40
    texto_pontuacao = mostrar_pont.render('level: %s' % (level_v), True, (255, 200, 70))
    tela.blit(texto_pontuacao, (50, 10))

    pygame.display.update()

pygame.quit()