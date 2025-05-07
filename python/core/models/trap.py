class Trap:
    def __init__(self, trap_type, value):
        self.type = trap_type  # "wait", "reduce_movement", "turns"
        self.value = value

    def __repr__(self):
        return f"Trap(type={self.type}, value={self.value})"
