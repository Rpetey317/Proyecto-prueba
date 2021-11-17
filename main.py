import pygame as pg
import numpy as np
import sys
import random
import math

'''
TODO:
- Implementar timer
- Implementar Highscore
- Implementar que se giren las fichas
- Hacer un menú principal
- Añadir gráficos y sonido
- Hacer que sólo se pueda dejar la ficha si va a destruir algo
- Reescribir el choclo de elif para cambiar las fichas de abajo unas por otras
- Arreglar que la ficha seleccionada aparece abajo de las que están más a la derecha
'''

filas = 6
columnas = 11
tam_cuadrado = 60
width = (columnas + 2) * tam_cuadrado
height = (filas + 5) * tam_cuadrado
score = 0

# colores
BLANCO = (255, 255, 255)
ROJO = (255, 100, 100)
VERDE = (100, 255, 100)
AZUL = (100, 100, 255)
AMARILLO = (255, 204, 100)
NINGUNO = (150, 150, 150)


# genera una matriz
def gen_matriz(f, c):
    mat = np.zeros((f, c), np.int8)   # hace falta aclarar el datatype, pygame suele dar problemas con los floats
    return mat


# dibuja el tablero
def gen_tablero_graf(ventana):
    global tam_cuadrado, filas, columnas, width, height

    # Tablero principal

    # horizontales
    for i in range(filas + 1):
        y = (i + 1) * tam_cuadrado
        inic = tam_cuadrado
        fin = width - tam_cuadrado
        pg.draw.line(ventana, BLANCO, (inic, y), (fin, y))

    # verticales
    for j in range(columnas + 1):
        x = (j + 1) * tam_cuadrado
        inic = tam_cuadrado
        fin = height - tam_cuadrado * 4
        pg.draw.line(ventana, BLANCO, (x, inic), (x, fin))

    # casillas de abajo

    # horizontales
    for k in range(0, 2):
        for n in range(1, 4):
            fl = 4 * n - 3  # calculé fx tal que f1 = 1, f2 =5 y f3 = 9, es esa recta
            x1 = tam_cuadrado * fl
            x2 = tam_cuadrado * (fl + 3)
            y = tam_cuadrado * (filas + 2 + k)
            pg.draw.line(ventana, BLANCO, (x1, y), (x2, y))

    # verticales
    for m in range(columnas + 1):
        x = (m + 1) * tam_cuadrado
        inic = (filas + 2) * tam_cuadrado
        fin = (filas + 3) * tam_cuadrado
        pg.draw.line(ventana, BLANCO, (x, inic), (x, fin))


# generar la ventana:
dimensiones = (width, height)
vent = pg.display.set_mode(dimensiones)
pg.display.set_caption("Demo")

vent.fill((150, 150, 150))
gen_tablero_graf(vent)
pg.display.update()


# la clase que define las 3 fichas en la parte de abajo de la pantalla
class Ficha(object):
    global ROJO, VERDE, AZUL, AMARILLO, tam_cuadrado, filas

    def __init__(self, color1, color2, color3, pos):
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.pos = pos
        self.orientacion = 0

    # dibuja la ficha en la pantalla
    def dibujar(self, ventana, pos):
        self.pos = pos
        col = [NINGUNO, ROJO, VERDE, AZUL, AMARILLO]
        r = int(tam_cuadrado / 2 - 5)
        x0 = pos[0]
        y0 = pos[1]

        pg.draw.circle(ventana, col[self.color1], (x0 - tam_cuadrado, y0), r)
        pg.draw.circle(ventana, col[self.color2], (x0, y0), r)
        pg.draw.circle(ventana, col[self.color3], (x0 + tam_cuadrado, y0), r)

    # genera nuevas fichas en las casillas de abajo
    def generar(self, ventana, pos):
        cx = int((4 * (pos + 1) - 2) * tam_cuadrado + tam_cuadrado / 2)
        cy = int((filas + 2) * tam_cuadrado + tam_cuadrado / 2)
        self.dibujar(ventana, (cx, cy))

    # chequea que se esté intentando poner la ficha en una posición válida
    def cambio_check(self, casilla):
        if 2 <= casilla[0] <= columnas - 1 and 1 <= casilla[1] <= filas:
            return True
        else:
            return False

    # cambia los colores de la ficha por los de la posicón clickeada en el tablero
    def cambio(self, tabl, casilla):
        x = casilla[0]
        y = casilla[1]
        col1 = tabl[y - 1][x - 2]
        col2 = tabl[y - 1][x - 1]
        col3 = tabl[y - 1][x]
        self.color1 = col1
        self.color2 = col2
        self.color3 = col3

    # girar las fichas (sin implementar)
    def girar(self):
        pass


# dibuja las fichas en la pantalla
def dibujar_ficha_tablero(ventana, colorid, f, c):
    global ROJO, VERDE, AZUL, AMARILLO, NINGUNO, tam_cuadrado
    col = [NINGUNO, ROJO, VERDE, AZUL, AMARILLO]
    r = int(tam_cuadrado / 2 - 5)
    c = (int(tam_cuadrado * (c + 1) + tam_cuadrado / 2), int(tam_cuadrado * (f + 1) + tam_cuadrado / 2))
    pg.draw.circle(ventana, col[colorid], c, r)


# genera la matriz de un tablero aleatorio
def gen_tablero_fichas(mat):
    for f in range(filas):
        for c in range(columnas):
            mat[f][c] = random.randrange(1, 5)


def dibujar_tablero(ventana, mat):
    global filas, columnas, score
    for f in range(filas):
        for c in range(columnas):
            cid = mat[f][c]
            dibujar_ficha_tablero(ventana, cid, f, c)

    # score pq ni ganas de ponerlo en una funcion aparte
    pg.font.init()
    font = pg.font.SysFont('monospace', 60)
    label = font.render(('SCORE: ' + str(score)), True, (255, 255, 255))
    vent.blit(label, (tam_cuadrado, 0))


# devuelve la casilla que se clickeó
def casilla_clickeada(click):
    clickx = click[0]
    clicky = click[1]
    col = int(math.floor(clickx / tam_cuadrado))
    fil = int(math.floor(clicky / tam_cuadrado))
    return col, fil


# rompe las fichas y trae las nuevas a lo candy crush
def destruccion_fichas(mat, fae):
    global score
    # poner 0s en las fichas a destruir
    for i in fae:
        mat[i[0]][i[1]] = 0
    # actualizar score
    puntos = 0
    for c in range(columnas):
        for f in range(filas):
            if mat[f][c] == 0:
                puntos += 1
    score += math.floor((155 * (puntos - 4) ** 2) + 400)  # una cuadrática calculada a ojo, felt good enough

    # esto lo vi en youtube, idk: https://youtu.be/p4jExm5Zf6Q?t=1327
    # es la "gravedad", baja las fichas no 0
    for c in range(columnas):
        ind = filas - 1
        for f in range(filas - 1, -1, -1):
            if mat[f][c] > 0:
                mat[ind][c] = mat[f][c]
                ind -= 1

        for f in range(ind, -1, -1):
            mat[f][c] = 0

    # genera las nuevas fichas
    for c in range(columnas):
        for f in range(filas):
            if mat[f][c] == 0:
                mat[f][c] = random.randrange(1, 5)


# esta función sirve para chequear si se deben destruir fichas, y llama la la funcion para destruirlas si hace falta
def combo_check(mat):
    fichas_a_eliminar = []   # Array vacía para incluír las posiciones de las fichas q se deberían borrar
    estable = False   # Dice si ya no quedan fichas para eliminar en el tablero

    # check horizontal
    for c in range(columnas - 3):
        for f in range(filas):
            cas1 = mat[f][c]
            cas2 = mat[f][c + 1]
            cas3 = mat[f][c + 2]
            cas4 = mat[f][c + 3]
            if cas1 == cas2 == cas3 == cas4:
                fichas_a_eliminar.append((f, c))
                fichas_a_eliminar.append((f, c + 1))
                fichas_a_eliminar.append((f, c + 2))
                fichas_a_eliminar.append((f, c + 3))

    # check vertical
    for c in range(columnas):
        for f in range(filas-3):
            cas1 = mat[f][c]
            cas2 = mat[f + 1][c]
            cas3 = mat[f + 2][c]
            cas4 = mat[f + 3][c]
            if cas1 == cas2 == cas3 == cas4:
                fichas_a_eliminar.append((f, c))
                fichas_a_eliminar.append((f + 1, c))
                fichas_a_eliminar.append((f + 2, c))
                fichas_a_eliminar.append((f + 3, c))

    # Actualiza la flag de estable si el tablero está en una pos estable
    # Si no, llama a la función de destruir las fichas
    if len(fichas_a_eliminar) == 0:
        estable = True
    else:
        destruccion_fichas(mat, fichas_a_eliminar)

    return estable


# chequea si se clickeó en una casilla de abajo
def bounds(click, pos):
    flag = False
    coef = 4 * pos - 3
    if tam_cuadrado * coef < click[0] < tam_cuadrado * (coef + 3):
        if tam_cuadrado * (filas + 2) < click[1] < tam_cuadrado * (filas + 3):
            flag = True
    return flag


# devuelve la posicion(1,2,3) de la casilla seleccionada, y 0 si no se clickeo en una casilla
def ficha_seleccionada(click):
    x = 0
    for i in range(0, 3):
        if bounds(click, i + 1):
            x = i + 1
    return x


# resetea el tablero
def reset():
    tabl = gen_matriz(filas, columnas)
    gen_tablero_fichas(tabl)

    f1 = Ficha(random.randrange(1, 5), random.randrange(1, 5), random.randrange(1, 5), 0)
    f1.generar(vent, 0)

    f2 = Ficha(random.randrange(1, 5), random.randrange(1, 5), random.randrange(1, 5), 0)
    f2.generar(vent, 1)

    f3 = Ficha(random.randrange(1, 5), random.randrange(1, 5), random.randrange(1, 5), 0)
    f3.generar(vent, 2)

    return tabl, f1, f2, f3


def main():
    global score
    # generar fichas
    f0 = Ficha(0, 0, 0, 0)  # placeholder

    f1 = Ficha(random.randrange(1, 5), random.randrange(1, 5), random.randrange(1, 5), 0)
    f1.generar(vent, 0)

    f2 = Ficha(random.randrange(1, 5), random.randrange(1, 5), random.randrange(1, 5), 0)
    f2.generar(vent, 1)

    f3 = Ficha(random.randrange(1, 5), random.randrange(1, 5), random.randrange(1, 5), 0)
    f3.generar(vent, 2)

    # dibujar tablero
    tablero = gen_matriz(filas, columnas)
    gen_tablero_fichas(tablero)
    dibujar_tablero(vent, tablero)

    # variables
    # genero una ficha random porsiaca el data type, es un placeholder en verdad
    selec = f0   # la ficha seleccionada
    flag = 0   # 1 si hay una ficha seleccionada actualmente, 0 si no

    # destruye todas las fichas destruibles antes de empezar y reinicia el score
    while not combo_check(tablero):
        combo_check(tablero)
    score = 0

    while True:
        for event in pg.event.get():

            # Cerrar la ventana
            if event.type == pg.QUIT:
                sys.exit()

            # clicks
            # si no hay nada agarrado, agarrar lo que se clickee
            if event.type == pg.MOUSEBUTTONDOWN:
                if flag == 0 and ficha_seleccionada(event.pos) != 0:
                    fichas = [f0, f1, f2, f3]
                    selec = fichas[ficha_seleccionada(event.pos)]
                    if selec != 0:
                        flag = 1

                # si hay algo agarrado
                elif flag == 1:  # el elif es necesario, con un else se buguea
                    if selec.cambio_check(casilla_clickeada(event.pos)):
                        # si tocas el tablero
                        # guardar los colores de la ficha antes de cambiarlos
                        tempcol1, tempcol2, tempcol3 = selec.color1, selec.color2, selec.color3
                        click = casilla_clickeada(event.pos)

                        # ahora se cambian los colores
                        selec.cambio(tablero, casilla_clickeada(event.pos))
                        tablero[click[1] - 1][click[0] - 2] = tempcol1
                        tablero[click[1] - 1][click[0] - 1] = tempcol2
                        tablero[click[1] - 1][click[0]] = tempcol3

                        while not combo_check(tablero):
                            combo_check(tablero)

                    # si tocas en las casillas de abajo
                    # sé que es terriblemente redundante e ineficiente, pero estaba apurado y era el modo fácil
                    elif bounds(event.pos, 1):
                        # caso de que tocas la casilla vacía, la vuelve a dejar en su lugar
                        if selec == f1:
                            f1.generar(vent, 0)
                            selec = f0
                            flag = 0
                        # caso en que tocas casillas con otras fichas, las intercambia del mismo modo que en el tablero
                        elif selec == f2:
                            tempcol1, tempcol2, tempcol3 = selec.color1, selec.color2, selec.color3
                            selec.color1, selec.color2, selec.color3 = f1.color1, f1.color2, f1.color3
                            f1.color1, f1.color2, f1.color3 = tempcol1, tempcol2, tempcol3
                        # idem
                        elif selec == f3:
                            tempcol1, tempcol2, tempcol3 = selec.color1, selec.color2, selec.color3
                            selec.color1, selec.color2, selec.color3 = f1.color1, f1.color2, f1.color3
                            f1.color1, f1.color2, f1.color3 = tempcol1, tempcol2, tempcol3
                    # Igual que el uno pero con los casos permutados
                    elif bounds(event.pos, 2):
                        if selec == f2:
                            f2.generar(vent, 1)
                            selec = f0
                            flag = 0
                        elif selec == f1:
                            tempcol1, tempcol2, tempcol3 = selec.color1, selec.color2, selec.color3
                            selec.color1, selec.color2, selec.color3 = f2.color1, f2.color2, f2.color3
                            f1.color1, f1.color2, f1.color3 = tempcol1, tempcol2, tempcol3
                        elif selec == f3:
                            tempcol1, tempcol2, tempcol3 = selec.color1, selec.color2, selec.color3
                            selec.color1, selec.color2, selec.color3 = f2.color1, f2.color2, f2.color3
                            f2.color1, f2.color2, f2.color3 = tempcol1, tempcol2, tempcol3
                    # Idem a casos 1 y 2
                    elif bounds(event.pos, 3):
                        if selec == f3:
                            f3.generar(vent, 2)
                            selec = f0
                            flag = 0
                        elif selec == f2:
                            tempcol1, tempcol2, tempcol3 = selec.color1, selec.color2, selec.color3
                            selec.color1, selec.color2, selec.color3 = f3.color1, f3.color2, f3.color3
                            f3.color1, f3.color2, f3.color3 = tempcol1, tempcol2, tempcol3
                        elif selec == f1:
                            tempcol1, tempcol2, tempcol3 = selec.color1, selec.color2, selec.color3
                            selec.color1, selec.color2, selec.color3 = f3.color1, f3.color2, f3.color3
                            f3.color1, f3.color2, f3.color3 = tempcol1, tempcol2, tempcol3
                    else:
                        pass

            # para que la ficha siga al mouse si está "levantada"
            if event.type == pg.MOUSEMOTION:
                if flag == 1:
                    selec.dibujar(vent, event.pos)

            # girar las fichas (sin implementar)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    pass
                if event.key == pg.K_x:
                    pass

            # resetear el juego
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    tablero, f1, f2, f3 = reset()
                    while not combo_check(tablero):
                        combo_check(tablero)
                    flag = 0
                    score = 0

        # actualiza la ventana, can't be bothered to write it in a function
        vent.fill((150, 150, 150))
        gen_tablero_graf(vent)
        dibujar_tablero(vent, tablero)
        f1.dibujar(vent, f1.pos)
        f2.dibujar(vent, f2.pos)
        f3.dibujar(vent, f3.pos)
        pg.display.update()


if __name__ == '__main__':
    main()
