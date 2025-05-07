import json
from core.models.graph import EscapeRoomGraph
from core.models.room import Room
from core.models.trap import Trap
from integration.bridge import PrologBridge

def load_escape_room_from_file(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)

    graph = EscapeRoomGraph()

    # 1. Crear habitaciones
    rooms_data = data.get("rooms", [])
    traps_data = data.get("traps", {})

    for room_name in rooms_data:
        trap = None
        # Si el cuarto tiene una trampa definida, la cargamos
        if room_name in traps_data:
            trap_info = traps_data[room_name]
            if isinstance(trap_info, dict):
                # Por ejemplo: {"type": "wait", "value": 3}
                trap_type = trap_info.get("type")
                trap_value = trap_info.get("value")
                trap = Trap(trap_type, trap_value)
        room = Room(room_name, trap=trap)
        graph.add_room(room)

    # 2. Establecer posiciones
    if "room_positions" in data:
        graph.set_room_positions(data["room_positions"])

    # 3. Crear puertas (y reversas)
    for door in data.get("doors", []):
        graph.add_door(
            door["from"],
            door["to"],
            locked=door.get("locked", False),
            key_required=door.get("key"),
            trapped=door.get("trapped", False)
        )
        graph.add_door(
            door["to"],
            door["from"],
            locked=door.get("locked", False),
            key_required=door.get("key"),
            trapped=door.get("trapped", False)
        )

    # 4. Añadir ítems
    for room_name, items in data.get("items", {}).items():
        for item in items:
            graph.add_item_to_room(room_name, item)

    # 5. Inicializar el puente a Prolog
    bridge = PrologBridge("prolog/main.pl")

    # 6. Insertar trampas en Prolog también
    for room_name, trap_info in traps_data.items():
        if isinstance(trap_info, dict):
            trap_type = trap_info.get("type")
            trap_value = trap_info.get("value")
            # Ejemplo: trap(hall, wait(3)).
            if trap_type and trap_value is not None:
                bridge.prolog.assertz(f"trap({room_name}, {trap_type}({trap_value}))")

    # 7. Parámetros iniciales
    start = data.get("start", None)
    goal = data.get("goal", None)
    inventory_limit = data.get("inventory_limit", 2)
    max_turns = data.get("max_turns", 10)

    return graph, start, goal, inventory_limit, max_turns
