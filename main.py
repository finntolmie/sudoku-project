import sys
import pygame
import requests
import random

show_mistakes = True
background_colour = (255, 255, 255)
N = 9
WIDTH = 800
HEIGHT = 800
font_size = 35
border = WIDTH / 12
box_size = (WIDTH - 2 * border) / 9
current_selection = [None, None]


def copy_grid(grid):
    new_grid = []
    for i in range(0, len(grid)):
        temp_list = []
        for j in range(0, len(grid[i])):
            temp_list.append(grid[i][j])
        new_grid.append(temp_list)
    return new_grid


def backtrack(grid, row, col):
    if row == N - 1 and col == N:
        return True

    if col == N:
        row += 1
        col = 0

    if grid[row][col] > 0:
        return backtrack(grid, row, col + 1)

    for num in range(1, N + 1, 1):
        if is_safe(grid, row, col, num):
            grid[row][col] = num
            if backtrack(grid, row, col + 1):
                return True
        grid[row][col] = 0
    return False


def check_complete(grid):
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if not check_validity((i, j)):
                return False
    return True


def is_safe(grid, row, col, num):
    # Check if we find the same num
    # in the similar row , we
    # return false
    for x in range(9):
        if grid[row][x] == num:
            return False

    # Check if we find the same num in
    # the similar column , we
    # return false
    for x in range(9):
        if grid[x][col] == num:
            return False

    # Check if we find the same num in
    # the particular 3*3 matrix,
    # we return false
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    return True


def check_validity(grid, coord):
    row = coord[0]
    col = coord[1]
    # Check if unique in its box
    sub_row = int(coord[0] // 3)
    sub_col = int(coord[1] // 3)
    for i in range(sub_row * 3, sub_row * 3 + 3):
        for j in range(sub_col * 3, sub_col * 3 + 3):
            if (i, j) != coord:
                if grid[i][j] == grid[row][col]:
                    return False

    # Check if unique in its row
    for i in range(0, len(grid[0])):
        if i != coord[0]:
            if grid[i][col] == grid[row][col]:
                return False

    # Check if unique in its column
    for i in range(0, len(grid[0])):
        if i != coord[1]:
            if grid[row][i] == grid[row][col]:
                return False

    return True


def give_hint(grid, grid_original, grid_solved):
    while True:
        rand_row = random.randint(0, 8)
        rand_col = random.randint(0, 8)
        if grid[rand_row][rand_col] == 0:
            grid_original[rand_row][rand_col] = grid_solved[rand_row][rand_col]
            grid[rand_row][rand_col] = grid_solved[rand_row][rand_col]
            break
    return


def modify(screen, grid, grid_original, grid_solved, x, y):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    give_hint(grid, grid_original, grid_solved)
                if event.key == pygame.K_LCTRL:
                    play_game(screen, copy_grid(grid_solved), grid_original, grid_solved)
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    grid[x][y] = 0
                if 0 < event.key - 48 < 10:
                    value = event.key - 48
                    grid[x][y] = value
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        font = pygame.font.SysFont('Comic Sans MS', 35)
        draw_grid(screen, grid, grid_original, grid_solved)


def draw_grid(screen, grid, grid_original, grid_solved):
    font = pygame.font.SysFont('Comic Sans MS', 35)
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            box = pygame.Rect(1 + border + (box_size * j), 1 + border + (box_size * i), box_size, box_size)
            back_colour = (255, 255, 255)
            if current_selection[0] == i and current_selection[1] == j:
                back_colour = (173, 216, 230)
            pygame.draw.rect(screen, back_colour, box)
            if grid_original[i][j] > 0:
                value = font.render(str(grid[i][j]), True, (0, 0, 0))
                screen.blit(value, (j * box_size + border + box_size / 3, i * box_size + border + box_size / 12))
            elif 0 < grid[i][j] < 10:
                colour = (0, 0, 255)
                if not check_validity(grid, (i, j)) and show_mistakes:
                    colour = (255, 0, 0)
                value = font.render(str(grid[i][j]), True, colour)
                screen.blit(value, (j * box_size + border + box_size / 3, i * box_size + border + box_size / 12))

    for i in range(0, 10):
        line_thickness = 2
        if i % 3 == 0:
            line_thickness = 4
        pygame.draw.line(screen, (0, 0, 0), (border + i * box_size, border), (border + i * box_size, 11 * border),
                         line_thickness)
        pygame.draw.line(screen, (0, 0, 0), (border, border + i * box_size), (11 * border, border + i * box_size),
                         line_thickness)
    pygame.display.update()


def play_game(screen, grid, grid_original, grid_solved):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos()
                column = int((position[0] - border) // box_size)
                row = int((position[1] - border) // box_size)
                if 0 <= row < 9 and 0 <= column < 9:
                    if grid_original[row][column] == 0:
                        pygame.display.update()
                        current_selection[0] = row
                        current_selection[1] = column
                        modify(screen, grid, grid_original, grid_solved, row, column)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    play_game(screen, copy_grid(grid_solved), grid_original, grid_solved)
        draw_grid(screen, grid, grid_original, grid_solved)


def main_menu(screen):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")
    screen.fill(background_colour)
    pygame.display.update()
    response = requests.get('https://sugoku.herokuapp.com/board?difficulty=medium')
    grid = response.json()['board']
    grid_original = copy_grid(grid)
    grid_solved = copy_grid(grid)
    backtrack(grid_solved, 0, 0)
    print('solved')
    play_game(screen, grid, grid_original, grid_solved)
    pygame.quit()
    sys.exit()


main()
