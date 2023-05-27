from pickle import FALSE
import pygame
from random import *
import math
from pygame import mixer

#Inicializar pygame
pygame.init()

#Crear la pantalla
pantalla=pygame.display.set_mode((800,600)) 

#Titulo e Icono
pygame.display.set_caption("Invasion espacial")
icono=pygame.image.load("ovni.png")
pygame.display.set_icon(icono)

#Fondo
fondo=pygame.image.load("Fondo.jpg")

#Variables de la Bala
img_bala= pygame.image.load("bala.png")
bala_x=0
bala_y=500
bala_x_cambio=0
bala_y_cambio=0.7
bala_visible=False

#Variable para el puntaje
puntaje=0
fuente=pygame.font.Font('freesansbold.ttf', 32)
#pide primero el nombre de la fuente y luego el tamaño, si quisiera otra fuente la tengo que descargar
texto_x=10
texto_y=10

#Variable vidas
vidas = 3
fuente_vidas=pygame.font.Font('freesansbold.ttf', 32)
vidas_x=648
vidas_y=10

#texto final de juego
fuente_final=pygame.font.Font('freesansbold.ttf',50)

def texto_final():
    mi_fuente_final= fuente_final.render('JUEGO TERMINADO',True,(255,255,255))
    pantalla.blit(mi_fuente_final,(150,100)) #(x,y)(150,100)

#Musica de fondo
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.3)#Regula el volumen
mixer.music.play(-1)

#Funcion mostrar vidas
def mostrar_vidas(x,y):
    texto=fuente_vidas.render(f"Vidas: {vidas}",True,(255,255,255))
    pantalla.blit(texto,(x,y))

#Funcion mostrar puntaje
def mostrar_puntaje(x ,y):
    texto=fuente.render(f'Puntaje: {puntaje}',True,(255,255,255))
    pantalla.blit(texto,(x,y))

# Variables Jugador
img_jugador=pygame.image.load("cohete.png")
jugador_x=368#mitad de la pantalla menos la mitad de los pixeles del png
jugador_y=500
jugador_x_cambio=0

#Variables Enemigos
img_enemigo=[]
enemigo_x=[]
enemigo_y=[]
enemigo_x_cambio=[]
enemigo_y_cambio=[]

cantidad_enemigos=5

#Loop para agregar la cantidad de enemigos
for enemigo in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(randint(0,736))
    enemigo_y.append(randint(50,200))
    enemigo_x_cambio.append(0.35)
    enemigo_y_cambio.append(50)


#Funcion jugador
def jugador(x,y):
    pantalla.blit(img_jugador,(x,y))


#Funcion bala
def disparar_bala(x,y):
    global bala_visible
    bala_visible=True
    pantalla.blit(img_bala , (x + 16,y + 10) )

#Funcion enemigo
def enemigo(x,y,ene):
    pantalla.blit(img_enemigo[ene],(x,y))

#Funcion detectar colisiiones
def hay_colision(x_1 , y_1, x_2, y_2):
    distancia=math.sqrt(math.pow(x_2 - x_1,2) + math.pow(y_2 - y_1,2)) #D= raiz uadradad de (x_2 - x_1) al cuadrado + (Y_2 - Y_1) al cuadrado
    if distancia < 27:
        return True
    else:
        return False

#Loop del juego
se_ejecuta= True
while se_ejecuta:
    #imagen del fondo
    pantalla.blit(fondo,(0,0))
   
    #Evento cerrar
    for evento in pygame.event.get():
        if evento.type==pygame.QUIT:#cuando apretas la x de arriba a la derecha
            se_ejecuta=False

    #Evento presionar teclas
        if evento.type==pygame.KEYDOWN:
            if evento.key==pygame.K_LEFT:
                jugador_x_cambio = -0.3
            if evento.key==pygame.K_RIGHT:
                jugador_x_cambio = 0.3
            if evento.key==pygame.K_SPACE:
                sonido_bala=mixer.Sound('disparo.mp3')
                sonido_bala.play()
                if bala_visible==False:
                    bala_x=jugador_x
                    disparar_bala(bala_x,bala_y)
                
        if evento.type==pygame.KEYUP:
            if evento.key==pygame.K_LEFT  or evento.key==pygame.K_RIGHT:
                 jugador_x_cambio = 0

    #Incrementa o decrementa segun la tecla que pulse
    jugador_x +=jugador_x_cambio

    #Mantener dentro de los limites al jugador
    if jugador_x <=0:
        jugador_x=0

    elif jugador_x >= 736:#800 pixeles de la pantalla menos los pixeles del "jugador"
        jugador_x= 736

    #Modifica ubicacion del enemigo
    for e in range(cantidad_enemigos):
        #fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

    #Mantener dentro de los limites al enemigo
        if enemigo_x[e] <=0:
            enemigo_x_cambio[e]=0.35
            enemigo_y[e]+=enemigo_y_cambio[e]

        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e]= -0.35
            enemigo_y[e]+=enemigo_y_cambio[e]

        #La colision
        colision=hay_colision(enemigo_x[e],enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision=mixer.Sound('Golpe.mp3')
            sonido_colision.play()
            bala_y=500
            bala_visible=False
            puntaje+=1
            enemigo_x[e]=randint(0,736)
            enemigo_y[e]=randint(50,200)
        #aparece el enemigo    
        enemigo(enemigo_x[e],enemigo_y[e],e)

    #Movimiento bala
    if bala_y <= -64:
        bala_y=500
        bala_visible=False

    if bala_visible:
        disparar_bala(bala_x,bala_y)
        bala_y -=bala_y_cambio       

    #Aparece el jugador
    jugador(jugador_x,jugador_y)

    #Mostar puntaje
    mostrar_puntaje(texto_x,texto_y)

    #Mostrar vidas
    mostrar_vidas(vidas_x,vidas_y)
   

    #Actualizar
    pygame.display.update()




