import pygame
import random

pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 600))
worm = [
    (300, 300),
    (310, 300),
    (320, 300)
]
worm_direction = pygame.K_LEFT
dune = pygame.image.load('img/Background/Dunes.png')
dune_guy_img = pygame.image.load('img/Characters/Dune_guy.png')
worm_img = [
    pygame.image.load('img/Characters/Worm15.png'),
    pygame.image.load('img/Characters/Worm15_up.png'),
    pygame.image.load('img/Characters/Worm15_down.png'),
    pygame.image.load('img/Characters/Worm15_right.png')
]
worm_img_middle = [
    pygame.image.load('img/Characters/Worm15_body_left.png'),
    pygame.image.load('img/Characters/Worm15_body_up.png'),
    pygame.image.load('img/Characters/Worm15_body_down.png'),
    pygame.image.load('img/Characters/Worm15_body_right.png')
]
worm_img_back = [
    pygame.image.load('img/Characters/Worm15_back_left.png'),
    pygame.image.load('img/Characters/Worm15_back_up.png'),
    pygame.image.load('img/Characters/Worm15_back_down.png'),
    pygame.image.load('img/Characters/Worm15_back_right.png')
]
worm_body = [
    pygame.image.load('img/Characters/Worm15.png'),
    pygame.image.load('img/Characters/Worm15_body_left.png'),
    pygame.image.load('img/Characters/Worm15_back_left.png')
]

pixel_size = 15
ct = 0
record = 0
human_pos = (0, 0)
up, right, down, left = 0, 1, 2, 3
font = pygame.font.SysFont("Monospace", 10, True, True)


def collision(pos1, pos2):
    return pos1 == pos2


# place the human in a random position, ensuring alignment with the grid
def random_human(window):
    x = random.randint(0, window[0] // pixel_size - 1) * pixel_size
    y = random.randint(0, window[1] // pixel_size - 1) * pixel_size
    return x, y


# If the worm is inside the window game_over = false
def walls(pos, window):
    if 0 <= pos[0] < window[0] and 0 <= pos[1] < window[1]:
        return False
    else:
        return True


# restart game with the initial settings
def restart_game(window):
    global worm, worm_direction, human_pos, ct, screen
    worm = [(300, 300), (310, 300), (320, 300)]
    worm_direction = pygame.K_LEFT
    human_pos = random_human(window)
    ct = 0


def main():

    global worm, human_pos, worm_direction, ct, record
    window = (600, 600)  # ([0],[1])
    pygame.display.set_caption('Dune')

    # loop until game over
    game_over = False
    while not game_over:
        clock.tick(15)  # (15fps)
        for event in pygame.event.get():  # return a list of occurred events
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:  # key updates the value of the worm direction
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    worm_direction = event.key

        screen.blit(dune, (0, 0))  # ensures that the background is redrawn for the visual appearance of the movement
        screen.blit(dune_guy_img, human_pos)  # draws the human every update

        # Increases an element of the worm upon colliding with the human
        if collision(human_pos, worm[0]):
            human_pos = random_human(window)
            worm.append(worm[-1])  # adds a new element to the worm list by copying the last element of the list
            ct += 1  # score counter
            if ct > record:
                record = ct

        # defines the record and the points, and displays them on the screen
        score = f"Score: {ct}"
        format_text_s = font.render(score, False, (0, 0, 0))
        screen.blit(format_text_s, (470, 40))
        max_record = f"Record: {record}"
        format_text_r = font.render(max_record, False, (0, 0, 0))
        screen.blit(format_text_r, (470, 60))

        # display the worm's position on the screen, know the value of the element, and its position in the list
        for i, pos in enumerate(worm):
            if i == 0:  # head
                if worm_direction == pygame.K_LEFT:
                    screen.blit(worm_img[0], pos)
                elif worm_direction == pygame.K_UP:
                    screen.blit(worm_img[1], pos)
                elif worm_direction == pygame.K_DOWN:
                    screen.blit(worm_img[2], pos)
                elif worm_direction == pygame.K_RIGHT:
                    screen.blit(worm_img[3], pos)
            elif i == len(worm) - 1:  # back
                if worm[i - 1][0] < worm[i][0]:
                    screen.blit(worm_img_back[0], pos)
                elif worm[i - 1][1] < worm[i][1]:
                    screen.blit(worm_img_back[1], pos)
                elif worm[i - 1][1] > worm[i][1]:
                    screen.blit(worm_img_back[2], pos)
                elif worm[i - 1][0] > worm[i][0]:
                    screen.blit(worm_img_back[3], pos)
            else:  # middle
                if worm[i - 1][0] < worm[i][0]:
                    screen.blit(worm_img_middle[0], pos)
                elif worm[i - 1][1] < worm[i][1]:
                    screen.blit(worm_img_middle[1], pos)
                elif worm[i - 1][1] > worm[i][1]:
                    screen.blit(worm_img_middle[2], pos)
                elif worm[i - 1][0] > worm[i][0]:
                    screen.blit(worm_img_middle[3], pos)

        # iterates through the worm list from the second element from the back to the front
        for i in range(len(worm) - 1, 0, -1):
            if collision(worm[0], worm[i]) or walls(worm[0], window):
                restart_game(window)
                break
            # move each segment of the snake (i) to the position of the previous one (i-1)
            worm[i] = worm[i - 1]

        # operation to move the worm
        if worm_direction == pygame.K_UP:
            worm[0] = (worm[0][0], worm[0][1] - pixel_size)
        elif worm_direction == pygame.K_DOWN:
            worm[0] = (worm[0][0], worm[0][1] + pixel_size)
        elif worm_direction == pygame.K_LEFT:
            worm[0] = (worm[0][0] - pixel_size, worm[0][1])
        elif worm_direction == pygame.K_RIGHT:
            worm[0] = (worm[0][0] + pixel_size, worm[0][1])

        pygame.display.update()
    pygame.quit()


main()
