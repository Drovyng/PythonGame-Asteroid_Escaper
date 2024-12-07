import random
import time

from pygame import draw
from geometry import *

pygame.display.init()
pygame.font.init()
SCREEN = pygame.display.set_mode((800, 800))
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Asteroid Escaper")

px = 400
py = 400
pxa = 0
pya = 0
pa = 0
fullRun = True

particles = []
r_bullets = []
timer = 3

time_last = time.perf_counter()
health = 1
running = True

font = pygame.font.SysFont("Cascadia Mono", 80)
fontSmall = pygame.font.SysFont("Cascadia Mono", 40)

class Input:
    B_LEFT = [pygame.K_LEFT, pygame.K_a]
    LEFT = False
    B_RIGHT = [pygame.K_RIGHT, pygame.K_d]
    RIGHT = False
    B_UP = [pygame.K_UP, pygame.K_w]
    UP = False
    B_DOWN = [pygame.K_DOWN, pygame.K_s]
    DOWN = False

    @classmethod
    def press(cls, key):
        global health, running, fullRun
        if key in cls.B_LEFT: cls.LEFT = True
        elif key in cls.B_RIGHT: cls.RIGHT = True
        elif key in cls.B_UP: cls.UP = True
        elif key in cls.B_DOWN: cls.DOWN = True
        elif key == pygame.K_ESCAPE: fullRun = False
        elif health <= 0 and key == pygame.K_SPACE: running = False

    @classmethod
    def release(cls, key):
        if key in cls.B_LEFT: cls.LEFT = False
        elif key in cls.B_RIGHT: cls.RIGHT = False
        elif key in cls.B_UP: cls.UP = False
        elif key in cls.B_DOWN: cls.DOWN = False


def kill():
    global particles, px, py
    if health <= 0:
        particles.append((px, py, 0, 125))
        px = 100000
        py = 100000

def spawn_rock(x:float, y:float, da:float):
    rock = []
    points = random.randint(6, 9)
    angle = math.pi * 2 / points
    radius = random.random() * 30 + 15
    mini = random.randint(1, 13) > 1
    for i in range(points):
        a = angle * i + random.random() * 0.3 - 0.15
        d = radius * (random.random() * 1.25 + 0.25)
        rock.append((a, d * 0.25 if mini else d))
    r_bullets.append((mini, rock, x, y, da, random.random() * 15 - 7.5, random.random() * math.pi * 2))

while fullRun:
    health = 1
    running = True
    px = 400
    py = 400
    pxa = 0
    pya = 0
    pa = 0
    particles = []
    e_bullets = []
    timer = 1.5
    time_last = time.perf_counter()
    gameTime = 0
    while running and fullRun:
        time_cur = time.perf_counter()
        elapsed = time_cur - time_last
        time_last = time_cur

        for event in pygame.event.get():
            if event.type == pygame.QUIT: fullRun = False
            elif event.type == pygame.KEYDOWN: Input.press(event.key)
            elif event.type == pygame.KEYUP: Input.release(event.key)

        if health > 0:
            if Input.LEFT:
                pa -= elapsed * 6
            if Input.RIGHT:
                pa += elapsed * 6
            if Input.UP:
                pxa += math.sin(pa) * elapsed * 1000
                pya -= math.cos(pa) * elapsed * 1000
            if Input.DOWN:
                pxa -= math.sin(pa) * elapsed * 500
                pya += math.cos(pa) * elapsed * 500
            px += pxa * elapsed
            py += pya * elapsed
            pxa = lerp(pxa, 0, elapsed * 2.5)
            pya = lerp(pya, 0, elapsed * 2.5)
            timer -= elapsed
            gameTime += elapsed

        if timer <= 0:
            timer = 0.25 + random.random() * 0.2 - 0.125
            rn = random.random() * 800
            nx, ny = random.choice([(0, rn), (rn, 0), (800, rn), (rn, 800)])
            na = math.atan2(px - nx, ny - py) + random.random() - 0.5
            spawn_rock(nx, ny, na)


        SCREEN.fill((0,0,0))

        m_p = [
            (px + math.sin(pa) * 25, py - math.cos(pa) * 25),
            (px - math.sin(pa + 0.5) * 25, py + math.cos(pa + 0.5) * 25),
            (px - math.sin(pa) * 5, py + math.cos(pa) * 5),
            (px - math.sin(pa - 0.5) * 25, py + math.cos(pa - 0.5) * 25),
            (px + math.sin(pa) * 25, py - math.cos(pa) * 25),
        ]
        i = 0
        while i < len(r_bullets):
            mini, rock, x, y, ra, fa, a = r_bullets[i]
            x += math.sin(ra) * 300 * elapsed
            y -= math.cos(ra) * 300 * elapsed
            a += fa * elapsed
            r_bullets[i] = mini, rock, x, y, ra, fa, a
            poly = []
            for p in rock:
                poly.append((x + p[1] * math.sin(a + p[0]), y - p[1] * math.cos(a + p[0])))
            if x > 850 or x < -50 or y > 850 or y < -50:
                r_bullets.remove(r_bullets[i])
                continue
            if collidePolygonPolygon(poly, m_p):
                health -= (0.05 + random.random() * 0.025) * (0.5 if mini else 1.0)
                kill()
                particles.append((x, y, 0, 15))
                r_bullets.remove(r_bullets[i])
                continue
            draw.lines(SCREEN, (240, 120, 120) if mini else (120, 240, 240), True, poly, 2 if mini else 4)
            i+=1
        i = 0
        while i < len(particles):
            x, y, a, m = particles[i]
            a += m * 2 * elapsed
            particles[i] = x, y, a, m
            if a > m:
                particles.remove(particles[i])
                continue
            draw.circle(SCREEN, (240, 40, 40), (x, y), a)
            i+=1

        if collideLinePolygon((0, 0), (0, 800), m_p):
            health -= 0.125
            kill()
            pxa = 800
        elif collideLinePolygon((800, 0), (800, 800), m_p):
            health -= 0.125
            kill()
            pxa = -800
        if collideLinePolygon((0, 15), (800, 15), m_p):
            health -= 0.125
            kill()
            pya = 800
        elif collideLinePolygon((0, 800), (800, 800), m_p):
            health -= 0.125
            kill()
            pya = -800




        draw.lines(SCREEN, (255, 255, 255), False, m_p, 2)



        draw.rect(SCREEN, (40, 40, 40), (0, 0, 800, 15))
        draw.rect(SCREEN, (250, 100, 100), (0, 0, 800 * health, 15))


        if health <= 0:
            sur1 = font.render("You Died!", True, (255, 255, 255))
            SCREEN.blit(sur1, (400 - sur1.get_width() * 0.5, 260))
            sur2 = font.render(f"Survived {int(gameTime)}.{int(gameTime * 100 % 100)} Seconds", True, (255, 255, 255))
            SCREEN.blit(sur2, (400 - sur2.get_width() * 0.5, 360))
            sur3 = font.render("Press [SPACE] to Restart", True, (255, 255, 255))
            SCREEN.blit(sur3, (400 - sur3.get_width() * 0.5, 460))
            sur4 = font.render("Press [ESC] to Quit", True, (255, 255, 255))
            SCREEN.blit(sur4, (400 - sur4.get_width() * 0.5, 560))
        else:
            SCREEN.blit(fontSmall.render(f"{int(gameTime)}.{int(gameTime * 100 % 100)}", True, (255, 255, 255)), (5, 765))

        pygame.display.flip()
        CLOCK.tick(60)