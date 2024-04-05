import pygame
import os
import time
import random
from os import listdir
from os.path import isfile, join
#Importamos todas las librerias que necesitamos
pygame.font.init()
#Hacemos esto para poder usatr texto en pygame

WIDTH, HEIGHT = 800, 600
#Estas 2 variables representan la altura y la anchura (Las usaremos para la ventana, pero tambien podriamos utilizarlas para mas cosas)
#Las colocamos en mayusculas porque su valor no cambiara 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#Esta funcion de pygame se usa para crear una ventana
pygame.display.set_caption("Cookie Explode")
#Esta funcion de pygame se usa para darle un nombre a la ventana 

BG = pygame.transform.scale(pygame.image.load(join("Pygame","Cookie Explode","assets","Background","cocina.jpeg")), (WIDTH, HEIGHT))
#Define el fondo y lo escala para que cuadre con la ventana

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5
PROJECTILE_WIDTH = 10
PROJECTILE_HEIGHT = 20
PROJECTILE_VEL = 3
BULLET_WIDTH = 20
BULLET_HEIGHT = 20
BULLET_VEL = 4
#Definimos el tamaño y la velocidad de las estrellas, el jugador y las balas

FONT_1 = pygame.font.SysFont("arial", 30)
FONT_2 = pygame.font.SysFont("arial", 100)
FONT_3 = pygame.font.SysFont("arial", 35)
#Definimos como queremos que se vea el texto

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
#Definimos los colores que vamos a usar

def draw(player, elapsed_time, stars, healers, bullets, life, level_type, bullet_countdown):
    #Elegimos tods las variables que vamos a utilizar
    #Definimos todo lo que tenemos que dibujar en la ventana
    WIN.blit(BG, (0, 0)) 
    #Las coordenadas (0, 0) son la esquina superior izquierda

    time_text = FONT_1.render(f"Time: {round(elapsed_time)}s", 1, WHITE)
    WIN.blit(time_text, (10, 10))
    life_text = FONT_1.render(f"Lifes: {round(life)}", 1, WHITE)
    WIN.blit(life_text, (200, 10))
    if(level_type != 0):
        level_text = FONT_1.render(f"Level: {round(level_type)}", 1, WHITE)
        WIN.blit(level_text, (400, 10))
    if bullet_countdown > 0:
        countdown_text = FONT_1.render(f"Recharging bullet: {bullet_countdown}s", 1, WHITE)
        WIN.blit(countdown_text, (10, 50))

    pygame.draw.rect(WIN, RED, player)

    for star in stars:
        pygame.draw.rect(WIN, WHITE, star)
    for healer in healers:
        pygame.draw.rect(WIN, GREEN, healer)
    for bullet in bullets:
        pygame.draw.rect(WIN, BLACK, bullet)

    pygame.display.update()
    #Esto hace que los dibujes se limpien y no se acumulen
    
def menu():
    options = ["Jugar", "Niveles", "Salir"]
    selected_option = 0
    level_time = 0
    level_difficulty = 2
    level_type = 0
    
    menu_run = True
    while menu_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        main(level_time, level_difficulty, level_type)
                    elif selected_option == 1:
                        levels()
                    elif selected_option == 2:
                        menu_run = False

        WIN.fill(WHITE)
        for i, option in enumerate(options):
            if i == selected_option:
                color = BLACK
            else:
                color = GREY
            text = FONT_3.render(option, True, color)
            text_rect = text.get_rect()
            text_rect.center = (WIDTH // 2, HEIGHT // 2.5 + i * 60)
            WIN.blit(text, text_rect)
        pygame.display.flip()

    pygame.quit()
    
def levels():
    levels = ["Nivel 1", "Nivel 2", "Nivel 3", "Volver"]
    selected_level = 0
    level_time = 0
    level_difficulty = 2
    level_type = 0
    
    levels_run = True
    while levels_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                levels_run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_level = (selected_level - 1) % len(levels)
                elif event.key == pygame.K_DOWN:
                    selected_level = (selected_level + 1) % len(levels)
                elif event.key == pygame.K_RETURN:
                    if selected_level == 0:
                        level_time = 100
                        level_difficulty = level_difficulty - 1
                        level_type = 1
                        main(level_time, level_difficulty, level_type)
                    elif selected_level == 1:
                        level_time = 200
                        level_type = 2
                        main(level_time, level_difficulty, level_type)
                    elif selected_level == 2:
                        level_time = 300
                        level_type = 3
                        level_difficulty = level_difficulty + 1
                        main(level_time, level_difficulty, level_type)
                    elif selected_level == 3:
                        menu()

        WIN.fill(WHITE)
        for i, level in enumerate(levels):
            if i == selected_level:
                color = BLACK
            else:
                color = GREY
            text = FONT_3.render(level, True, color)
            text_rect = text.get_rect()
            text_rect.center = (WIDTH // 2, HEIGHT // 2.5 + i * 60)
            WIN.blit(text, text_rect)
        pygame.display.flip()

    pygame.quit()

def main(level_time, level_difficulty, level_type):
    #Aqui estamos definiendo la funcion main
    run = True 
    #Le decimos al codigo que la booliana run es verdadera 

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT) 
    #Definimos donde aparece el jugador
    
    clock = pygame.time.Clock() 
    #Necesitamos definir clock para ponerle un maximo a los fotogrmas por segundo (fps)
    start_time = time.time() 
    #Definims la variable start_time como time.time para que nos de el tiempo que a rascurrido desde que se abrio el juego
    elapsed_time = 0 
    #Numero desde donde se empiezan a contar los segundos
    
    projectile_add_increment = 2000
    projectile_count = 0
    
    stars = []
    hit = False
    
    healers = []
    heal = False
    life = 3
    
    bullets = []
    bullet_cooldown = 0
    bullet_countdown = 0
    num_bullets = 0
    
    game_times = []
    #Lista para almacenar los tiempos de cada partida
    
    while run:
        projectile_count += clock.tick(60)
        #Numero maximo de fotogramas por segundo
        elapsed_time = time.time() - start_time 
        #Start_time representa el tiempo en el que se empezo el juego y time.time el tiempo actual

        if projectile_count > projectile_add_increment:
        #Si el número de estrellas (projectile_count) es mayor que el incremento de estrellas (projectile_add_increment), entonces se ejecutará el siguiente bloque de código:
            for _ in range(level_difficulty):
                #Se ejecutará un bucle 3 veces:
                star_x = random.randint(0, WIDTH - PROJECTILE_WIDTH)
                #Se genera una posición aleatoria en el eje X para la estrella, dentro del ancho de la pantalla
                star = pygame.Rect(star_x, -PROJECTILE_HEIGHT,
                               PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
                #Se crea un objeto Rect (rectángulo) que representa la estrella, con la posición aleatoria en X y una posición inicial en Y fuera de la pantalla (-PROYECTILE_HEIGHT)
                stars.append(star)
                #Se agrega la estrella a la lista de estrellas (stars)
            if projectile_count % 10 == 0:
                #Agregar 1 sanador cada 10 estrellas
                for _ in range(1):
                    healer_x = random.randint(0, WIDTH - PROJECTILE_WIDTH)
                    healer = pygame.Rect(healer_x, -PROJECTILE_HEIGHT,
                                   PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
                    healers.append(healer)
            projectile_add_increment = max(200, projectile_add_increment - 50)
            #Se actualiza el valor de projectile_add_increment, tomando el máximo entre 200 y el valor actual menos 50.
            #Esto hace que el incremento de estrellas se reduzca con el tiempo.
            projectile_count = 0
            #Se reinicia el contador de estrellas (projectile_count) a 0.

        #Mientras run sea verdaera
        for event in pygame.event.get():
            #Para todos los evenetos desde que se llamo a esta funcion
            if event.type == pygame.QUIT:
                #Si el tipo de evento es un evento QUIT (ocurre cuando se ppica en la x de la pantalla)
                run = False
                break 
            #Usamos beak para salir del "for"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and bullet_cooldown <= 0 and num_bullets < 1:
                    bullet = pygame.Rect(player.x + player.width // 2 - BULLET_WIDTH // 2, player.y - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT)
                    bullets.append(bullet)
                    bullet_cooldown = 10000
                    num_bullets += 1

        #Obtener el estado actual de las teclas presionadas
        keys = pygame.key.get_pressed()
        #Mover al jugador hacia la izquierda si se presiona la tecla 'izquierda' o 'a'
        #Verificar que al moverse a la izquierda, la posición no sea menor que 0 (borde izquierdo)
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        #Mover al jugador hacia la derecha si se presiona la tecla 'derecha' o 'd'
        #Verificar que al moverse a la derecha, la posición no sea mayor que WIDTH - PLAYER_WIDTH (borde derecho)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL
        #Mover al jugador hacia arriba si se presiona la tecla 'arriba' o 'w'
        #Verificar que al moverse hacia arriba, la posición no sea menor que 0 (borde superior)
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL
        #Mover al jugador hacia abajo si se presiona la tecla 'abajo' o 's'
        #Verificar que al moverse hacia abajo, la posición no sea mayor que HEIGHT - PLAYER_HEIGHT (borde inferior)
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y + PLAYER_VEL + PLAYER_HEIGHT <= HEIGHT:
            player.y += PLAYER_VEL
        #Definimos el movimiento del personaje
        if (keys[pygame.K_ESCAPE]):
            menu()

        for star in stars[:]:
            star.y += PROJECTILE_VEL
            if star.y > HEIGHT:
                stars.remove(star)
                #Cuando la estrella esta por debajo de la pantalla se elimina
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                #Cuando la estrella le da al jugador desaparece
                break

        for healer in healers[:]:
            healer.y += PROJECTILE_VEL
            if healer.y > HEIGHT:
                healers.remove(healer)
            elif healer.y + healer.height >= player.y and healer.colliderect(player):
                healers.remove(healer)
                heal = True
                break

        for bullet in bullets[:]:
            bullet.y -= BULLET_VEL
            if bullet.y < 0:
                bullets.remove(bullet)
                num_bullets -= 1
            else:
                for star in stars[:]:
                    if bullet.colliderect(star):
                        stars.remove(star)
                        bullets.remove(bullet)
                        num_bullets -= 1
                        break

        if bullet_cooldown > 0:
            bullet_cooldown -= clock.get_time()  
            bullet_countdown = int(bullet_cooldown / 1000 + 1)  
            
        if hit:
            life = life - 1
            hit = False

        if heal:
            life = life + 1
            heal = False

        if life <= 0:
            lost_text = FONT_2.render("You Lost!", 1, BLACK)
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2)) 
            pygame.display.update()
            #Cuando te dan y mueres aparece este texto
            pygame.time.delay(3000)
            menu()
            #Esto hace que tarde un poco en llegar al menu

        if elapsed_time >= level_time and level_time != 0:
            win_text = FONT_2.render("You Win!", 1, BLACK)
            WIN.blit(win_text, (WIDTH/2 - win_text.get_width()/2, HEIGHT/2 - win_text.get_height()/2)) 
            pygame.display.update()
            pygame.time.delay(3000)
            game_times.append(elapsed_time) 
            #Agregar el tiempo de la partida a la lista
            menu()

        draw(player, elapsed_time, stars, healers, bullets, life, level_type, bullet_countdown)
        #Llamamos a la funcion draw

    pygame.quit()

if __name__ == "__main__":
    #Se asegura de que el archivo se esté ejecutando directamente en lugar de ser importado como un módulo
    menu()  
    #Llama a la función main
