import pyglet
from random import randrange
from pyglet.window.key import UP, DOWN, LEFT, RIGHT
from pathlib import Path
window = pyglet.window.Window(640, 640)
velikost_pole = 20
TILES_DIRECTORY = Path('snake-tiles')
snake_tiles = {}
for path in TILES_DIRECTORY.glob('*.png'):
    snake_tiles[path.stem] = pyglet.sprite.Sprite(pyglet.image.load(path))
    snake_tiles[path.stem].scale = 10/velikost_pole
print(snake_tiles)

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
    print(souradnice)

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

had = snake_tiles['tail-head']

obrazek2 = pyglet.image.load('apple.png')
jablko = pyglet.sprite.Sprite(obrazek2)
jablko.scale = 10/velikost_pole

def vykresli():
    window.clear()
    for x,y in souradnice[1:-1]:
        snake_tiles['right-right'].x = x*window.width/velikost_pole
        snake_tiles['right-right'].y = y*window.height/velikost_pole
        snake_tiles['right-right'].draw()

    x,y = souradnice[-1]
    snake_tiles['left-tongue'].x = x*window.width/velikost_pole
    snake_tiles['left-tongue'].y = y*window.height/velikost_pole
    snake_tiles['left-tongue'].draw()

    x,y = souradnice[0]
    snake_tiles['tail-right'].x = x*window.width/velikost_pole
    snake_tiles['tail-right'].y = y*window.height/velikost_pole
    snake_tiles['tail-right'].draw()
    
    for x,y in jidlo:
        jablko.x = x*window.width/velikost_pole
        jablko.y = y*window.height/velikost_pole
        jablko.draw()

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
