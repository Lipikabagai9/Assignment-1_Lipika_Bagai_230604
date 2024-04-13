import pygame as pg
from random import randrange

def get_random_position(window, tile_size):
    RANGE = (tile_size // 2, window - tile_size // 2, tile_size)
    return [randrange(*RANGE), randrange(*RANGE)]

window = 750
tile_size = 40
snake = pg.rect.Rect([0, 0, tile_size - 2, tile_size - 2])
snake.center = get_random_position(window, tile_size)
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, 160
food = snake.copy()
food.center = get_random_position(window, tile_size)
screen = pg.display.set_mode([window] * 2)
clock = pg.time.Clock()
dirs = {pg.K_w: (0, -tile_size), pg.K_s: (0, tile_size), pg.K_a: (-tile_size, 0), pg.K_d: (tile_size, 0)}
score = 0  # initialize score
# Initialize font
pg.init()  # Initialize pygame
font_game_over = pg.font.Font(None, 72)  # Larger font size for "Game Over"
font_score = pg.font.Font(None, 36)  # Regular font size for score


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key in dirs:
                new_dir = dirs[event.key]
                # Prevent the snake from reversing direction
                if (new_dir[0] != -snake_dir[0]) or (new_dir[1] != -snake_dir[1]):
                    snake_dir = new_dir

    screen.fill('black')
    # check borders and selfeating
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
    if snake.left < 0 or snake.right > window or snake.top < 0 or snake.bottom > window or self_eating:
        snake.center, food.center = get_random_position(window, tile_size), get_random_position(window, tile_size)
        length, snake_dir = 1, (0, 0)
        segments = [snake.copy()]
        # Display "Game Over" and score
        game_over_text = font_game_over.render("Game Over", True, (255, 255, 255))
        score_text = font_score.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(game_over_text, (window // 2 - game_over_text.get_width() // 2, window // 2 - 30))
        screen.blit(score_text, (window // 2 - score_text.get_width() // 2, window // 2 + 10))
        pg.display.flip()
        pg.time.delay(2000)  # Delay for 2 seconds
        # Reset score
        score = 0
        # Reset time step
        time_step = 160
        # Reset window size
        window = 750
        screen = pg.display.set_mode([window] * 2)
        continue  # Skip the rest of the loop iteration
    # check food
    if snake.center == food.center:
        food.center = get_random_position(window, tile_size)
        length += 1
        # Increment score when food is eaten
        score += 10
        # Decrease time step to increase snake speed
        time_step -= 5 if time_step > 50 else 0
        # Reduce game boundary
        window -= 5
        screen = pg.display.set_mode([window] * 2)
    # draw food
    pg.draw.rect(screen, 'red', food)
    # draw snake
    [pg.draw.rect(screen, 'green', segment) for segment in segments]
    # Display score
    score_text = font_score.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    # move snake
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]
    pg.display.flip()
    clock.tick(60)
