import math

import pygame


def lerp(a:float, b:float, t:float) -> float:
    return a + (b - a) * t

def clamp(a:float, l:float, r:float) -> float:
    return min(max(a, l), r)

def easeOutQuint(x: float) -> float:
    return 1 - math.pow(1 - x, 5)

def easeOutSine(x:float) -> float:
    return math.sin(((x - 0.5) * math.pi / 2) / 2) + 0.5

def collideLineLine(l1_p1, l1_p2, l2_p1, l2_p2):

    # normalized direction of the lines and start of the lines
    P  = pygame.math.Vector2(*l1_p1)
    line1_vec = pygame.math.Vector2(*l1_p2) - P
    R = line1_vec.normalize()
    Q  = pygame.math.Vector2(*l2_p1)
    line2_vec = pygame.math.Vector2(*l2_p2) - Q
    S = line2_vec.normalize()

    # normal vectors to the lines
    RNV = pygame.math.Vector2(R[1], -R[0])
    SNV = pygame.math.Vector2(S[1], -S[0])
    RdotSVN = R.dot(SNV)
    if RdotSVN == 0:
        return False

    # distance to the intersection point
    QP  = Q - P
    t = QP.dot(SNV) / RdotSVN
    u = QP.dot(RNV) / RdotSVN

    return t > 0 and u > 0 and t*t < line1_vec.magnitude_squared() and u*u < line2_vec.magnitude_squared()

def colideRectLine(rect, p1, p2):
    return (collideLineLine(p1, p2, rect.topleft, rect.bottomleft) or
            collideLineLine(p1, p2, rect.bottomleft, rect.bottomright) or
            collideLineLine(p1, p2, rect.bottomright, rect.topright) or
            collideLineLine(p1, p2, rect.topright, rect.topleft))

def collideRectPolygon(rect, polygon):
    for i in range(len(polygon)-1):
        if colideRectLine(rect, polygon[i], polygon[i+1]):
            return True
    return False

def collideLinePolygon(p1, p2, polygon):
    for i in range(len(polygon)-1):
        if collideLineLine(p1, p2, polygon[i], polygon[i+1]):
            return True
    return False

def collidePolygonPolygon(polygon1, polygon2):
    for j in range(len(polygon1)-1):
        for i in range(len(polygon2)-1):
            if collideLineLine(polygon1[j], polygon1[j+1], polygon2[i], polygon2[i+1]):
                return True
    return False