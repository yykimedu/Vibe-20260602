"""
Pygame 기반 테트리스 포팅 (단일 파일)

실행:
  pip install pygame
  python tetris.py

조작:
  ← → : 좌/우 이동
  ↑    : 회전
  ↓    : 소프트 드롭
  Space: 하드 드롭
  P    : 일시정지
"""

import sys
import random
import pygame

# 설정
COLS = 10
ROWS = 20
BLOCK = 30
WIDTH = COLS * BLOCK
HEIGHT = ROWS * BLOCK

COLORS = [
    (0,0,0),
    (255,107,107),
    (247,178,103),
    (125,206,130),
    (77,150,255),
    (199,125,255),
    (34,193,195),
    (255,209,102),
]

PIECES = ['I','J','L','O','S','T','Z']

def create_bag():
    bag = PIECES[:]
    random.shuffle(bag)
    return bag

def create_matrix(w,h):
    return [[0]*w for _ in range(h)]

def create_piece(t):
    if t == 'T':
        return [[0,1,0],[1,1,1],[0,0,0]]
    if t == 'O':
        return [[2,2],[2,2]]
    if t == 'L':
        return [[0,0,3],[3,3,3],[0,0,0]]
    if t == 'J':
        return [[4,0,0],[4,4,4],[0,0,0]]
    if t == 'S':
        return [[0,5,5],[5,5,0],[0,0,0]]
    if t == 'Z':
        return [[6,6,0],[0,6,6],[0,0,0]]
    if t == 'I':
        return [[0,0,0,0],[7,7,7,7],[0,0,0,0],[0,0,0,0]]

def piece_value(t):
    mapping = {'T':1,'O':2,'L':3,'J':4,'S':5,'Z':6,'I':7}
    return mapping[t]

def rotate(matrix, dir):
    # transpose
    for y in range(len(matrix)):
        for x in range(y):
            matrix[x][y], matrix[y][x] = matrix[y][x], matrix[x][y]
    if dir > 0:
        for row in matrix:
            row.reverse()
    else:
        matrix.reverse()

def collide(arena, player):
    m = player['matrix']
    o = player['pos']
    for y in range(len(m)):
        for x in range(len(m[y])):
            if m[y][x] != 0:
                ay = y + o['y']
                ax = x + o['x']
                if ay < 0 or ay >= ROWS or ax < 0 or ax >= COLS:
                    return True
                if arena[ay][ax] != 0:
                    return True
    return False

def merge(arena, player):
    m = player['matrix']
    o = player['pos']
    for y in range(len(m)):
        for x in range(len(m[y])):
            v = m[y][x]
            if v != 0:
                arena[y+o['y']][x+o['x']] = v

def arena_sweep(arena, state):
    row_count = 0
    y = ROWS-1
    while y >= 0:
        if 0 in arena[y]:
            y -= 1
            continue
        arena.pop(y)
        arena.insert(0, [0]*COLS)
        row_count += 1
    if row_count > 0:
        scores = [0,40,100,300,1200]
        state['score'] += scores[row_count] * state['level']
        state['lines'] += row_count
        state['level'] = state['lines'] // 10 + 1
        state['drop_interval'] = max(100, int(1000 * (0.9 ** (state['level']-1))))

def spawn(arena, player, bag):
    if not bag:
        bag.extend(create_bag())
    t = bag.pop()
    val = piece_value(t)
    base = create_piece(t)
    matrix = [[(cell and val) for cell in row] for row in base]
    player['matrix'] = matrix
    player['pos']['y'] = 0
    player['pos']['x'] = COLS//2 - len(matrix[0])//2
    # prepare next in bag[-1]
    return bag

def hard_drop(arena, player, state, bag):
    while not collide(arena, player):
        player['pos']['y'] += 1
    player['pos']['y'] -= 1
    merge(arena, player)
    arena_sweep(arena, state)
    spawn(arena, player, bag)

def draw_grid(surface, arena):
    for y in range(ROWS):
        for x in range(COLS):
            v = arena[y][x]
            color = COLORS[v]
            rect = pygame.Rect(x*BLOCK, y*BLOCK, BLOCK-1, BLOCK-1)
            pygame.draw.rect(surface, color, rect)

def draw_piece(surface, player):
    m = player['matrix']
    o = player['pos']
    for y in range(len(m)):
        for x in range(len(m[y])):
            v = m[y][x]
            if v:
                rect = pygame.Rect((o['x']+x)*BLOCK, (o['y']+y)*BLOCK, BLOCK-1, BLOCK-1)
                pygame.draw.rect(surface, COLORS[v], rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH+220, HEIGHT))
    pygame.display.set_caption('테트리스 - Pygame')
    clock = pygame.time.Clock()

    arena = create_matrix(COLS, ROWS)
    state = {
        'score': 0,
        'level': 1,
        'lines': 0,
        'drop_interval': 1000
    }

    bag = create_bag()
    player = {'pos': {'x':0,'y':0}, 'matrix': None}
    bag = spawn(arena, player, bag) or bag

    # 한글 표시를 우선하는 시스템 폰트를 찾습니다.
    def get_korean_font(size):
        candidates = [
            'malgungothic', 'malgun gothic', '맑은 고딕',
            'nanumgothic', 'nanum gothic', 'noto sans kr',
            'noto', 'arial unicode ms', 'gulim', 'batang', 'arial'
        ]
        for name in candidates:
            path = pygame.font.match_font(name)
            if path:
                try:
                    return pygame.font.Font(path, size)
                except Exception:
                    continue
        return pygame.font.SysFont(None, size)

    font = get_korean_font(24)
    last_drop = pygame.time.get_ticks()
    running = True
    paused = False

    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player['pos']['x'] -= 1
                    if collide(arena, player):
                        player['pos']['x'] += 1
                elif event.key == pygame.K_RIGHT:
                    player['pos']['x'] += 1
                    if collide(arena, player):
                        player['pos']['x'] -= 1
                elif event.key == pygame.K_DOWN:
                    player['pos']['y'] += 1
                    if collide(arena, player):
                        player['pos']['y'] -= 1
                        merge(arena, player)
                        arena_sweep(arena, state)
                        bag = spawn(arena, player, bag) or bag
                    state['score'] += 1
                elif event.key == pygame.K_UP:
                    rotate(player['matrix'], 1)
                    if collide(arena, player):
                        rotate(player['matrix'], -1)
                elif event.key == pygame.K_SPACE:
                    hard_drop(arena, player, state, bag)
                elif event.key == pygame.K_p:
                    paused = not paused

        # 자동 낙하
        if not paused:
            now = pygame.time.get_ticks()
            if now - last_drop > state['drop_interval']:
                player['pos']['y'] += 1
                if collide(arena, player):
                    player['pos']['y'] -= 1
                    merge(arena, player)
                    arena_sweep(arena, state)
                    bag = spawn(arena, player, bag) or bag
                last_drop = now

        # 그리기
        screen.fill((10,15,25))
        play_surf = pygame.Surface((WIDTH, HEIGHT))
        play_surf.fill((0,0,0))
        draw_grid(play_surf, arena)
        if player['matrix']:
            draw_piece(play_surf, player)
        screen.blit(play_surf, (0,0))

        # 사이드 패널
        panel_x = WIDTH + 10
        score_surf = font.render(f"점수: {state['score']}", True, (220,220,220))
        level_surf = font.render(f"레벨: {state['level']}", True, (220,220,220))
        lines_surf = font.render(f"라인: {state['lines']}", True, (220,220,220))
        screen.blit(score_surf, (panel_x, 20))
        screen.blit(level_surf, (panel_x, 50))
        screen.blit(lines_surf, (panel_x, 80))

        # 다음 블록(간단 표시): bag[-1]
        if bag:
            next_type = bag[-1]
            next_matrix = create_piece(next_type)
            nx = panel_x
            ny = 120
            for y in range(len(next_matrix)):
                for x in range(len(next_matrix[y])):
                    v = next_matrix[y][x]
                    if v:
                        rect = pygame.Rect(nx + x*20, ny + y*20, 18, 18)
                        pygame.draw.rect(screen, COLORS[v*1], rect)

        if paused:
            pause_surf = font.render('일시정지 (P)', True, (255,200,60))
            screen.blit(pause_surf, (panel_x, HEIGHT-60))

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
