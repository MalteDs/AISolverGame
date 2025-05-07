def get_matrix_layout(graph):
    positions = graph.positions
    max_x = max(pos[0] for pos in positions.values())
    max_y = max(pos[1] for pos in positions.values())

    matrix = [[None for _ in range(max_y + 1)] for _ in range(max_x + 1)]
    room_lookup = {}

    for room_name, (x, y) in positions.items():
        matrix[x][y] = room_name
        room_lookup[(x, y)] = room_name

    return matrix, room_lookup
