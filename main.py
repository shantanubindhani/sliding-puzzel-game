from game_classes import Block, button
import pygame as pg
import sys
from random import shuffle


window = None
blocks = None
pose = None
bgpic = None
hs = 0
sc = 0

pg.init()
myFont = pg.font.SysFont("sans-serif", 30)


def show_msg(win, msg, color=(0, 0, 0), coords=(0, 0)):
    global myFont
    surf = myFont.render(msg, False, color)
    win.blit(surf, coords)

def about():
    win = pg.display.set_mode((350, 400))
    pg.display.set_caption("instructions")
    back = button("images/back.png")
    back.bindFun(main)
    back.x, back.y = 10, 0
    run = True
    text = ["Made by :", "   SHANTANU BINDHANI",
            "Email :", "   coder.shantanu@gmail.com"]

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                back.fun_if_pressed(mouse_pos, win)
        win.blit(back.img, (back.x, back.y))
        for i, val in enumerate(range(50, (20*len(text)+50), 25)):
            show_msg(win, text[i], (112, 187, 222), (5, val))
        pg.display.update()
    sys.exit()

def play_instructions():
    win = pg.display.set_mode((270, 400))
    pg.display.set_caption("instructions")
    back = button("images/back.png")
    back.bindFun(main)
    back.x, back.y = 10, 0
    run = True
    inst = pg.image.load("images/instruction.png")
    win.blit(inst, (0, 0))
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                back.fun_if_pressed(mouse_pos, win)
        win.blit(back.img, (back.x, back.y))
        pg.display.update()
    sys.exit()


def get_score(score=0, HS=False):
    if HS:
        try:
            with open("scores.txt", 'r') as file:
                HS = file.readline().split('/')[1]
                HS = HS[1:len(HS)-1]
            return int(HS)
        except:
            return 0
    else:
        try:
            with open("scores.txt", 'w') as file:
                hs = get_score(HS=True)

                if not hs:
                    file.write(f"97886/3{score}7/345623")
                elif hs > score:
                    file.write(f"97886/3{score}7/345623")

        except:
            raise file("Some file error occured. ")


def is_sorted():
    """ this function is only made particularly for this program. """
    global blocks
    start = 42
    end = start + 62*3 + 1
    coords = [[x, y] for y in range(start, end, 62)
              for x in range(start, end, 62)]
    values = []
    for x in blocks:
        x = x.rect.center
        values.append([x[0], x[1]])
    return not(values == coords)


def check_pos(m_pos, block_pos):
    for p in block_pos:
        if m_pos[0] >= (p[0]-30) and m_pos[0] <= (p[0]+30):
            if m_pos[1] >= (p[1]-30) and m_pos[1] <= (p[1]+30):
                return block_pos.index(p)
    return None


def update_frame():
    global window
    global blocks
    global pose
    global bgpic
    global hs
    global sc

    window.blit(bgpic, (0, 0))
    for idx, block in enumerate(blocks):
        x = pose[idx][0]
        y = pose[idx][1]
        blocks[idx].rect.center = (x, y)
        window.blit(block.img, (x-30, y-30))
        show_msg(window, hs, (255, 255, 0), (30, 300))
        show_msg(window, sc, (255, 255, 0), (30, 330))
    pg.display.update()


def game():
    global window
    global blocks
    global pose
    global bgpic
    global hs
    global sc

    game_name = "SLIDER-PUZZEL"

    win_width = 270
    win_height = 400
    bgpic = pg.image.load("images/bgpic.png")

    blocks = [Block(num) for num in range(16)]
    start = 42
    end = start + 62*3 + 1
    pose = [[x, y] for y in range(start, end, 62)
            for x in range(start, end, 62)]

    shuffle(pose)

    window = pg.display.set_mode((win_width, win_height),)
    window.blit(bgpic, (0, 0))
    pg.display.set_caption(game_name)

    high_score = get_score(HS=True)
    moves = 0
    run = True

    hs = f"high score : {high_score} moves."
    sc = f"your score : {moves} moves."

    while run:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                b_index = check_pos(mouse_pos, pose)

                if b_index != None and blocks[b_index].name != "images/img0.png":
                    dist = blocks[0].get_distance(blocks[b_index])
                    if dist <= 62:
                        white_index = 0
                        step = 2
                        x = pose[b_index]
                        if pose[white_index][0] == pose[b_index][0]:
                            if pose[white_index][1] < pose[b_index][1]:
                                step = -step
                                sign = 1
                            if pose[white_index][1] > pose[b_index][1]:
                                step = abs(step)
                                sign = -1

                            while (dist != 0):
                                pose[b_index][1] += step
                                update_frame()
                                dist -= abs(step)
                            while (dist < 62):
                                pose[white_index][1] -= step*15.5
                                update_frame()
                                dist -= step*sign*15.5

                        if pose[white_index][1] == pose[b_index][1]:
                            if pose[white_index][0] < pose[b_index][0]:
                                step = -step
                                sign = 1
                            if pose[white_index][0] > pose[b_index][0]:
                                step = abs(step)
                                sign = -1

                            while (dist != 0):
                                pose[b_index][0] += step
                                update_frame()
                                dist -= abs(step)
                            while (dist < 62):
                                pose[white_index][0] -= step*15.5
                                update_frame()
                                dist -= step*sign*15.5

                        moves += 1
            # pg.display.update()
        run = is_sorted()

        hs = f"high score : {high_score} moves."
        sc = f"your score : {moves} moves."

        update_frame()

        if not run:
            get_score(moves)
            img = pg.image.load("images/congo.png")
            window.blit(img, (0, 0))
            pg.display.update()
            while True:
                for ev in pg.event.get():
                    if ev.type == pg.QUIT:
                        sys.exit()
                        pg.quit()


def main():
    win = pg.display.set_mode((270, 400))
    pg.display.set_caption("instructions")
    run = True

    btns = [button(f"images/button{x+1}.png") for x in range(3)]
    for i, val in enumerate([40, 100, 160]):
        btns[i].x = 75
        btns[i].y = val

    btns[0].bindFun(game)
    btns[1].bindFun(play_instructions)
    btns[2].bindFun(about)

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                for b in btns:
                    b.fun_if_pressed(pg.mouse.get_pos(), win)
        for b in btns:
            win.blit(b.img, (b.x, b.y))
        pg.display.update()
    pg.quit()


if __name__ == "__main__":
    main()
    a = input()
    sys.exit()
    pg.quit()
