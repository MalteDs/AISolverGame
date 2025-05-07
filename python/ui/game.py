# import pygame
# import sys

# # Tamaño de cada celda en píxeles
# CELL_SIZE = 80

# # Colores
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# GRAY = (160, 160, 160)
# BLUE = (0, 128, 255)
# GREEN = (0, 255, 0)
# RED = (255, 0, 0)
# YELLOW = (255, 255, 0)

# def play_with_arrows_pygame(engine):
#     pygame.init()

#     graph = engine.graph
#     positions = graph.positions
#     matrix, room_lookup = build_matrix(graph)

#     width = len(matrix[0]) * CELL_SIZE
#     height = (len(matrix) + 2) * CELL_SIZE

#     screen = pygame.display.set_mode((width, height))
#     pygame.display.set_caption("Escape Room - Manual Mode")

#     clock = pygame.time.Clock()

#     player_room = engine.current_room
#     visited = set()

#     # ⚡ Variables cacheadas (actualizables después de movimientos)
#     player_inventory = engine.get_inventory()
#     moves_left = engine.get_moves_left()

#     running = True
#     while running:
#         screen.fill(WHITE)

#         for i, row in enumerate(matrix):
#             for j, cell in enumerate(row):
#                 rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
#                 pygame.draw.rect(screen, GRAY, rect, 1)

#                 if cell:
#                     room = graph.rooms[cell]
#                     color = WHITE

#                     if cell == player_room:
#                         color = BLUE
#                     elif room.has_trap:
#                         color = RED
#                     elif room.items:
#                         color = YELLOW
#                     else:
#                         for door in graph.get_neighbors(cell):
#                             if door.locked:
#                                 color = BLACK
#                                 break
#                         else:
#                             if cell in visited:
#                                 color = GREEN
#                             else:
#                                 color = GRAY

#                     pygame.draw.rect(screen, color, rect)

#         # Mostrar info
#         font = pygame.font.SysFont(None, 24)
#         inv_text = font.render(f"Inventory: {', '.join(player_inventory) or 'Empty'}", True, BLACK)
#         moves_text = font.render(f"Moves Left: {moves_left}", True, BLACK)
#         screen.blit(inv_text, (10, height - CELL_SIZE * 2 + 10))
#         screen.blit(moves_text, (10, height - CELL_SIZE + 10))

#         pygame.display.flip()

#         visited.add(player_room)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#                 break

#             if event.type == pygame.KEYDOWN:
#                 dx, dy = 0, 0
#                 if event.key == pygame.K_UP:
#                     dx, dy = -1, 0
#                 elif event.key == pygame.K_DOWN:
#                     dx, dy = 1, 0
#                 elif event.key == pygame.K_LEFT:
#                     dx, dy = 0, -1
#                 elif event.key == pygame.K_RIGHT:
#                     dx, dy = 0, 1

#                 if dx != 0 or dy != 0:
#                     x, y = positions[player_room]
#                     new_x, new_y = x + dx, y + dy

#                     if 0 <= new_x < len(matrix) and 0 <= new_y < len(matrix[0]):
#                         next_room = room_lookup.get((new_x, new_y))
#                         if next_room:
#                             if engine.move_to(next_room):
#                                 pygame.event.pump()
#                                 player_room = next_room
#                                 for item in list(graph.rooms[next_room].items):
#                                     engine.pick_item(item)

#                                 # 📥 Solo aquí ACTUALIZAMOS los datos de Prolog
#                                 player_inventory = engine.get_inventory()
#                                 moves_left = engine.get_moves_left()

#                                 if engine.is_game_over():
#                                     print("💀 Game Over!")
#                                     running = False
#                                     break

#         clock.tick(10)  # 10 FPS

#     pygame.quit()
#     sys.exit()

# def build_matrix(graph):
#     positions = graph.positions
#     max_x = max(pos[0] for pos in positions.values())
#     max_y = max(pos[1] for pos in positions.values())

#     matrix = [[None for _ in range(max_y + 1)] for _ in range(max_x + 1)]
#     room_lookup = {}

#     for room_name, (x, y) in positions.items():
#         matrix[x][y] = room_name
#         room_lookup[(x, y)] = room_name

#     return matrix, room_lookup
