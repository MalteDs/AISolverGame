from .trap import Trap  # ✅ Importamos la clase Trap

class Room:
    def __init__(self, name, trap=None):
        self.name = name
        self.items = []          # Lista de objetos en la habitación
        self.trap = trap        
    def __repr__(self):
        return f"Room({self.name})"
