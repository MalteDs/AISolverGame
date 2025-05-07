import re
import time
from integration.bridge import PrologBridge
from core.models.player import Player

class EscapeRoomEngine:
    def __init__(self, prolog_path, graph, start_room, inventory_limit=3, max_moves=50):
        self.graph = graph
        self.bridge = PrologBridge(prolog_path)
        self.player = Player(start_room)
        self.inventory_limit = inventory_limit
        self.max_moves = max_moves

        self.bridge.set_current_room(start_room)
        self.update_inventory_prolog()

    def move_to(self, next_room):
        neighbors = self.graph.get_neighbors(self.player.current_room)
        for door in neighbors:
            if door.to_room == next_room:
                if door.locked and (door.key_required not in self.player.inventory and f"key({door.key_required})" not in self.player.inventory):
                    return False

                self.player.current_room = next_room
                self.player.moves_done += 1
                self.bridge.set_current_room(next_room)
                self.bridge.prolog.query(f"enter_room({next_room})")
                self.apply_trap_effects()
                return True
        return False

    def pick_item(self, item):
        if len(self.player.inventory) >= self.inventory_limit:
            return False

        room = self.graph.rooms.get(self.player.current_room)
        if room and item in room.items:
            self.player.inventory.add(item)
            room.items.remove(item)
            self.update_inventory_prolog()
            return True
        return False

    def update_inventory_prolog(self):
        prolog_inventory = []
        for item in self.player.inventory:
            if item.startswith("key") and not item.startswith("key("):
                prolog_inventory.append(f"key({item})")
            else:
                prolog_inventory.append(item)

        self.bridge.prolog.query("retractall(inventory(_))")
        self.bridge.prolog.assertz(f"inventory({list(prolog_inventory)})")

    def apply_trap_effects(self):
        traps = list(self.bridge.prolog.query(f"trap({self.player.current_room}, X)."))
        for trap in traps:
            trap_info = trap['X']
            if 'reduce_movement' in str(trap_info):
                match = re.search(r'reduce_movement\((\d+)\)', str(trap_info))
                if match:
                    reduction = int(match.group(1))
                    self.max_moves -= reduction
            elif 'wait' in str(trap_info):
                match = re.search(r'wait\((\d+)\)', str(trap_info))
                if match:
                    wait_seconds = int(match.group(1))
                    time.sleep(wait_seconds)

    def is_game_over(self):
        return bool(list(self.bridge.prolog.query("game_over."))) or self.player.moves_done >= self.max_moves

    def get_inventory(self):
        return list(self.player.inventory)

    def get_moves_left(self):
        return self.max_moves - self.player.moves_done
