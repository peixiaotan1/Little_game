import random
import curses

# Initialize the screen
stdscr = curses.initscr()
curses.curs_set(0)
sh, sw = stdscr.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(100)

# Initialize the game board and score
board = [[0 for _ in range(4)] for _ in range(4)]
score = 0

def spawn_tile():
    # 90% chance for 2, 10% chance for 4
    return random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])

def draw_board():
    for y in range(4):
        for x in range(4):
            w.addstr(y*2, x*4, str(board[y][x]))
    w.addstr(sh-1, 0, f"Score: {score}")
    w.refresh()

def merge(row):
    global score
    new_row = [0, 0, 0, 0]
    index = 0
    for i in range(4):
        if row[i] != 0:
            if new_row[index] == 0:
                new_row[index] = row[i]
            elif new_row[index] == row[i]:
                new_row[index] *= 2
                score += new_row[index]
                index += 1
            else:
                index += 1
                new_row[index] = row[i]
    return new_row

#Move operation
def move(direction):
    global board
    if direction == 'up':
        board = [merge(row) for row in zip(*board)]
    elif direction == 'down':
        board = [list(reversed(merge(row[::-1]))) for row in zip(*board)]
    elif direction == 'left':
        board = [merge(row) for row in board]
    elif direction == 'right':
        board = [list(reversed(merge(row[::-1]))) for row in board]

#detect whether the game is over
def is_full():
    for row in board:
        if 0 in row:
            return False
    return True

def game_over():
    return is_full() and not any(board[i][j] == board[i][j + 1] or board[i][j] == board[i + 1][j] for i in range(3) for j in range(3))

# Initial spawn of two tiles
for _ in range(2):
    row = random.randint(0, 3)
    col = random.randint(0, 3)
    while board[row][col] != 0:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
    board[row][col] = spawn_tile()

while True:
    draw_board()
    key = w.getch()
    if key == ord('q'):
        break

    if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
        direction = ""
        if key == curses.KEY_UP:
            direction = 'up'
        elif key == curses.KEY_DOWN:
            direction = 'down'
        elif key == curses.KEY_LEFT:
            direction = 'left'
        elif key == curses.KEY_RIGHT:
            direction = 'right'

        move(direction)

        if not is_full():
            # Spawn a new tile after each move
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            while board[row][col] != 0:
                row = random.randint(0, 3)
                col = random.randint(0, 3)
            board[row][col] = spawn_tile()

        if game_over():
            w.addstr(sh // 2, sw // 2 - 5, "Game Over!")
            w.addstr(sh // 2 + 1, sw // 2 - 8, f"Your Score: {score}")
            w.refresh()
            while True:
                key = w.getch()
                if key == ord('q'):
                    curses.endwin()
                    quit()

curses.endwin()