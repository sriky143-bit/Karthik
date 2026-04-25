import curses
import random
import time

def main(stdscr):
    # Initialize curses
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # Colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Text

    # Get screen dimensions
    sh, sw = stdscr.getmaxyx()
    w = sw // 2
    h = sh // 2

    # Initial snake position
    snake = [
        [h, w],
        [h, w-1],
        [h, w-2]
    ]

    # Initial direction
    direction = curses.KEY_RIGHT

    # Initial food
    food = [random.randint(1, sh-2), random.randint(1, sw-2)]
    stdscr.addch(food[0], food[1], 'O', curses.color_pair(2))

    # Score
    score = 0

    # Game loop
    while True:
        # Get next key
        key = stdscr.getch()

        # Change direction
        if key == curses.KEY_UP and direction != curses.KEY_DOWN:
            direction = key
        elif key == curses.KEY_DOWN and direction != curses.KEY_UP:
            direction = key
        elif key == curses.KEY_LEFT and direction != curses.KEY_RIGHT:
            direction = key
        elif key == curses.KEY_RIGHT and direction != curses.KEY_LEFT:
            direction = key

        # Calculate new head
        head = [snake[0][0], snake[0][1]]
        if direction == curses.KEY_UP:
            head[0] -= 1
        elif direction == curses.KEY_DOWN:
            head[0] += 1
        elif direction == curses.KEY_LEFT:
            head[1] -= 1
        elif direction == curses.KEY_RIGHT:
            head[1] += 1

        # Check boundaries
        if head[0] < 0 or head[0] >= sh or head[1] < 0 or head[1] >= sw:
            break

        # Check self collision
        if head in snake:
            break

        # Add new head
        snake.insert(0, head)

        # Check food
        if snake[0] == food:
            score += 1
            food = None
            while food is None:
                nf = [random.randint(1, sh-2), random.randint(1, sw-2)]
                if nf not in snake:
                    food = nf
            stdscr.addch(food[0], food[1], 'O', curses.color_pair(2))
        else:
            # Remove tail
            tail = snake.pop()
            stdscr.addch(tail[0], tail[1], ' ')

        # Draw snake
        stdscr.addch(snake[0][0], snake[0][1], '#', curses.color_pair(1))
        for segment in snake[1:]:
            stdscr.addch(segment[0], segment[1], '*', curses.color_pair(1))

        # Draw score
        stdscr.addstr(0, 0, f'Score: {score}', curses.color_pair(3))

        # Refresh
        stdscr.refresh()

        # Speed
        time.sleep(0.1)

    # Game over
    stdscr.clear()
    stdscr.addstr(sh//2, sw//2 - 5, f'Game Over! Score: {score}', curses.color_pair(3))
    stdscr.addstr(sh//2 + 1, sw//2 - 10, 'Press any key to exit', curses.color_pair(3))
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)