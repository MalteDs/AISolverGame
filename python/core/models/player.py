class Player:
    def __init__(self, start_room):
        self.current_room = start_room
        self.inventory = set()
        self.moves_done = 0
