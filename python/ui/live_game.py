import curses
import re
import time
from core.visualizer import get_matrix_layout

def play_with_arrows(engine):
    player_room = engine.current_room
    visited = set()

    graph = engine.graph
    positions = graph.positions
    matrix, room_lookup = get_matrix_layout(graph)

    def draw(stdscr):
        nonlocal player_room, visited
        curses.curs_set(0)
        stdscr.nodelay(False)
        stdscr.clear()

        while True:
            stdscr.clear()
            visited.add(player_room)
            x, y = positions[player_room]

            for i, row in enumerate(matrix):
                for j, cell in enumerate(row):
                    symbol = "   "
                    if cell is None:
                        symbol = " # "
                    else:
                        room = graph.rooms[cell]
                        if cell == player_room:
                            symbol = "[P]"
                        elif room.has_trap:
                            symbol = " T "
                        elif room.items:
                            symbol = " K "
                        else:
                            for door in graph.get_neighbors(cell):
                                if door.locked:
                                    symbol = " L "
                                    break
                            else:
                                if cell in visited:
                                    symbol = " . "
                                else:
                                    symbol = " ? "
                    stdscr.addstr(i, j * 4, symbol)

            # Mostrar datos del jugador
            stdscr.addstr(len(matrix) + 2, 0, f"Room: {player_room}")
            # stdscr.addstr(len(matrix) + 3, 0, f"Inventory: {', '.join(engine.get_inventory()) or 'Empty'}")
            stdscr.addstr(len(matrix) + 4, 0, f"Moves Left: {engine.get_moves_left()}")
            stdscr.addstr(len(matrix) + 5, 0, "Use arrow keys to move. Press Q to quit.")

            key = stdscr.getch()

            if key == ord('q'):
                break

            dx, dy = 0, 0
            if key == curses.KEY_UP:
                dx, dy = -1, 0
            elif key == curses.KEY_DOWN:
                dx, dy = 1, 0
            elif key == curses.KEY_LEFT:
                dx, dy = 0, -1
            elif key == curses.KEY_RIGHT:
                dx, dy = 0, 1
            else:
                continue

            curr_x, curr_y = positions[player_room]
            new_x, new_y = curr_x + dx, curr_y + dy

            if 0 <= new_x < len(matrix) and 0 <= new_y < len(matrix[0]):
                next_room = room_lookup.get((new_x, new_y))
                if next_room:
                    if engine.move_to(next_room):
                        player_room = next_room
                        # Recoger automáticamente todos los ítems de la sala
                        for item in list(graph.rooms[next_room].items):
                            engine.pick_item(item)

                        if engine.is_game_over():
                            stdscr.addstr(len(matrix) + 6, 0, "💀 Game Over!")
                            stdscr.refresh()
                            time.sleep(3)
                            return

            stdscr.refresh()

    curses.wrapper(draw)


def animate_path(engine, path):
    graph = engine.graph
    matrix, room_lookup = get_matrix_layout(graph)

    def draw(stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
        visited = set()

        for room in path:
            stdscr.clear()
            visited.add(room)
            x, y = graph.get_position(room)

            for i, row in enumerate(matrix):
                for j, cell in enumerate(row):
                    symbol = "   "
                    if cell is None:
                        symbol = " # "
                    else:
                        r = graph.rooms[cell]
                        if cell == room:
                            symbol = "[P]"
                        elif r.has_trap:
                            symbol = " T "
                        elif r.items:
                            symbol = " K "
                        else:
                            for door in graph.get_neighbors(cell):
                                if door.locked:
                                    symbol = " L "
                                    break
                            else:
                                if cell in visited:
                                    symbol = " . "
                                else:
                                    symbol = " ? "
                    stdscr.addstr(i, j * 4, symbol)

            # ⚡ Importante: actualizar el motor de juego
            engine.move_to(room)

            stdscr.addstr(len(matrix) + 2, 0, f"IA se mueve por: {room}")
            stdscr.refresh()
            time.sleep(0.5)

    curses.wrapper(draw)