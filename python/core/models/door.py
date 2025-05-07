class Door:
    def __init__(self, from_room, to_room, locked=False, key_required=None, trapped=False):
        self.from_room = from_room
        self.to_room = to_room
        self.locked = locked
        self.key_required = key_required
        self.trapped = trapped

    def __repr__(self):
        attrs = []
        if self.locked:
            attrs.append("locked")
        if self.trapped:
            attrs.append("trapped")
        if self.key_required:
            attrs.append(f"key={self.key_required}")
        attr_str = ", ".join(attrs) if attrs else "unlocked"
        return f"Door({self.from_room} -> {self.to_room}, {attr_str})"