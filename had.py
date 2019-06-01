import pyglet
from random import randrange
from pyglet.window.key import UP, DOWN, LEFT, RIGHT
from pathlib import Path
window = pyglet.window.Window(640, 640)
window.set_location(20, 30)
velikost_pole = 20
TILES_DIRECTORY = Path('snake-tiles')
snake_tiles = {}
for path in TILES_DIRECTORY.glob('*.png'):
    snake_tiles[path.stem] = pyglet.sprite.Sprite(pyglet.image.load(path))
    snake_tiles[path.stem].scale = 10/velikost_pole

def pohyb(souradnice, jidlo):
    posledni = souradnice[-1]
    if strana == 'v':
        novy = (posledni[0] + 1, posledni[1])
    if strana == 'z':
        novy = (posledni[0] - 1, posledni[1])
    if strana == 'j':
        novy = (posledni[0], posledni[1] + 1)
    if strana == 's':
        novy = (posledni[0], posledni[1] - 1)
    if novy[0] >= velikost_pole or novy[1] >= velikost_pole or novy[0] < 0 or novy[1] < 0:
        raise ValueError('Game over')
    if novy in souradnice:
        raise ValueError('Game over')
    souradnice.append(novy)
    if novy in jidlo:
        jidlo.remove(novy)
        potrava(souradnice, jidlo)
    else:
        souradnice.pop(0)

def potrava(souradnice, jidlo):
    while True:
        x = randrange(0, velikost_pole)
        y = randrange(0, velikost_pole)
        nove_jidlo = x, y
        if nove_jidlo not in jidlo and nove_jidlo not in souradnice:
            jidlo.append(nove_jidlo)
            break

souradnice = [(0, 0), (1, 0), (2, 0)]
jidlo = []
potrava(souradnice, jidlo)
strana = 'v'

obrazek2 = pyglet.image.load('apple.png')
jablko = pyglet.sprite.Sprite(obrazek2)
jablko.scale = 10/velikost_pole

def vykresli():
    window.clear()
    for i in range(1, len(souradnice)-1):
        x, y = souradnice[i]
        x1, y1 = souradnice[i+1]
        x2, y2 = souradnice[i-1]
        orientace = (x-x1, y-y1)
        orientace2 = (x-x2, y-y2)
        nazev = 'body-'+ telo[orientace]
        nazev = ocas[orientace2] + '-' + ocas[orientace]
        snake_tiles[nazev].x = x*window.width/velikost_pole
        snake_tiles[nazev].y = y*window.height/velikost_pole
        snake_tiles[nazev].draw()

    x, y = souradnice[-1]
    x1, y1 = souradnice[-2]
    orientace = (x-x1, y-y1)
    nazev = ocas[orientace] + '-tongue'
    snake_tiles[nazev].x = x*window.width/velikost_pole
    snake_tiles[nazev].y = y*window.height/velikost_pole
    snake_tiles[nazev].draw()

    x, y = souradnice[0]
    x1, y1 = souradnice[1]
    orientace = (x-x1, y-y1)
    nazev = 'tail-'+ ocas[orientace]
    snake_tiles[nazev].x = x*window.width/velikost_pole
    snake_tiles[nazev].y = y*window.height/velikost_pole
    snake_tiles[nazev].draw()


    for x,y in jidlo:
        jablko.x = x*window.width/velikost_pole
        jablko.y = y*window.height/velikost_pole
        jablko.draw()

ocas = {(-1, 0): 'right', (1, 0): 'left', (0, 1): 'bottom', (0, -1): 'top'}
telo = {(-1, 0): 'right', (1, 0): 'right', (0, 1): 'top', (0, -1): 'top'}

def klavesnice(sym, mod):
    global strana
    if sym == UP:
        strana = 'j'
    if sym == DOWN:
        strana = 's'
    if sym == LEFT:
        strana = 'z'
    if sym == RIGHT:
        strana = 'v'

def tik(t):
    pohyb(souradnice, jidlo)
pyglet.clock.schedule_interval(tik, 1/4)

window.push_handlers(
    on_draw=vykresli,
    on_key_press=klavesnice,
)

pyglet.app.run()
