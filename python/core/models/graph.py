from core.models.room import Room
from core.models.door import Door

class EscapeRoomGraph:
    def __init__(self):
        self.rooms = {}  # Dict[str, Room]
        self.graph = {}  # Dict[str, List[Door]]

    def add_room(self, room: Room):
        """Agrega un objeto Room, si no existe."""
        if room.name not in self.rooms:
            self.rooms[room.name] = room
            self.graph[room.name] = []

    def add_door(self, from_room_name, to_room_name, locked=False, key_required=None, trapped=False):
        """Agrega una puerta, y asegura que las salas existan."""
        # Si las habitaciones no existen, crearlas vacías
        if from_room_name not in self.rooms:
            self.add_room(Room(from_room_name))
        if to_room_name not in self.rooms:
            self.add_room(Room(to_room_name))

        door = Door(from_room_name, to_room_name, locked, key_required, trapped)
        self.graph[from_room_name].append(door)

    def add_item_to_room(self, room_name, item):
        if room_name in self.rooms:
            self.rooms[room_name].items.append(item)

    def get_neighbors(self, room_name):
        return self.graph.get(room_name, [])
    
    def set_room_positions(self, positions):
        self.positions = positions
    
    def get_position(self, room_name):
        return self.positions.get(room_name, (0, 0)) 
    
    def __repr__(self):
        return f"EscapeRoomGraph({len(self.rooms)} rooms, {sum(len(v) for v in self.graph.values())} doors)"
