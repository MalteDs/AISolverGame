import heapq

class State:
    def __init__(self, room, inventory, room_items, cost, path):
        self.room = room
        self.inventory = set(inventory)
        self.room_items = {k: list(v) for k, v in room_items.items()}  # Copia profunda
        self.cost = cost
        self.path = path

    def __lt__(self, other):
        return self.cost < other.cost

def a_star_search(engine, goal_room):
    graph = engine.graph
    start_room = engine.current_room

    open_list = []
    visited = set()

    initial_room_items = {name: list(room.items) for name, room in graph.rooms.items()}

    start_state = State(
        room=start_room,
        inventory=list(engine.get_inventory()),
        room_items=initial_room_items,
        cost=0,
        path=[start_room]
    )

    heapq.heappush(open_list, (0, start_state))

    while open_list:
        _, current_state = heapq.heappop(open_list)

        if current_state.room == goal_room:
            return current_state.path

        state_id = (
            current_state.room,
            frozenset(current_state.inventory),
            frozenset((k, tuple(v)) for k, v in current_state.room_items.items())
        )

        if state_id in visited:
            continue
        visited.add(state_id)

        # Simular movimiento y recolección de objetos
        neighbors = graph.get_neighbors(current_state.room)
        for door in neighbors:
            next_room = door.to_room

            # Si la puerta está cerrada y no tengo la llave, no puedo pasar
            if door.locked:
                required = door.key_required
                if required not in current_state.inventory and f"key({required})" not in current_state.inventory:
                    continue

            new_inventory = set(current_state.inventory)
            new_room_items = {k: list(v) for k, v in current_state.room_items.items()}

            # Simular recoger objetos en la siguiente sala
            for item in new_room_items[next_room]:
                if item.startswith("key"):
                    new_inventory.add(f"key({item})")
                else:
                    new_inventory.add(item)
            new_room_items[next_room] = []

            trap_penalty = 0
            room_obj = graph.rooms[next_room]
            if room_obj.has_trap:
                trap_penalty = 5  # Penalizar entrar en salas con trampa

            new_cost = current_state.cost + 1 + trap_penalty
            new_path = current_state.path + [next_room]

            next_state = State(
                room=next_room,
                inventory=new_inventory,
                room_items=new_room_items,
                cost=new_cost,
                path=new_path
            )

            priority = new_cost + heuristic(next_room, goal_room, graph)
            heapq.heappush(open_list, (priority, next_state))

    return None

def heuristic(current_room, goal_room, graph):
    x1, y1 = graph.get_position(current_room)
    x2, y2 = graph.get_position(goal_room)
    return abs(x1 - x2) + abs(y1 - y2)
