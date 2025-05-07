from pyswip import Prolog
import time

class PrologBridge:
    def __init__(self, prolog_file_path):
        self.prolog = Prolog()
        self.prolog.consult(prolog_file_path)
        self.initialize_game()

    def initialize_game(self):
        """Inicializa todo el juego en Prolog."""
        list(self.prolog.query("initialize_game"))

    def set_current_room(self, room):
        """Actualiza la posición actual del jugador en Prolog."""
        self.prolog.query("retractall(current_room(_))")
        self.prolog.assertz(f"current_room({room})")

    def can_move(self, from_room, to_room):
        """Consulta si el jugador puede moverse de una sala a otra."""
        return bool(list(self.prolog.query(f"can_move({from_room}, {to_room})")))

    def is_locked(self, from_room, to_room):
        """Determina si una puerta está bloqueada."""
        self.set_current_room(from_room)
        if not self.can_move(from_room, to_room):
            q = list(self.prolog.query(f"door({from_room}, {to_room}, locked)"))
            return bool(q)
        return False

    def get_required_key(self, from_room, to_room):
        """Devuelve la llave requerida para una puerta bloqueada."""
        q = list(self.prolog.query(f"door({from_room}, {to_room}, locked), key_unlocks(Key, {to_room})"))
        return q[0]["Key"] if q else None

    def get_inventory(self):
        """Devuelve el inventario actual del jugador."""
        q = list(self.prolog.query("inventory(Inv)"))
        return q[0]["Inv"] if q else []

    def pick(self, item):
        """Intenta recoger un objeto."""
        try:
            return bool(list(self.prolog.query(f"pick({item})")))
        except:
            return False

    def load_traps_from_prolog(self):
        """Carga las trampas desde el archivo de reglas Prolog."""
        traps = {}

        # Consultar las trampas de penalización por turnos
        penalty_query = list(self.prolog.query("trap(Room, turns(Turns))"))
        for penalty in penalty_query:
            room = penalty["Room"]
            turns = int(penalty["Turns"])
            if room not in traps:
                traps[room] = {}
            traps[room]["turns"] = turns

        # Consultar las trampas de tiempo de espera
        wait_query = list(self.prolog.query("trap(Room, wait(WaitTime))"))
        for wait in wait_query:
            room = wait["Room"]
            wait_time = int(wait["WaitTime"])
            if room not in traps:
                traps[room] = {}
            traps[room]["wait_time"] = wait_time

        return traps


    def has_trap(self, room):
        """Consulta si una sala tiene trampa."""
        result = list(self.prolog.query(f"trap({room}, _)"))
        print(f"Resultado de trampas en {room}: {result}")
        return bool(result)

    def get_trap_penalty(self, room):
        """Obtiene el número de turnos que penaliza una trampa en una sala."""
        result = list(self.prolog.query(f"trap({room}, turns(Turns))"))
        if result:
            return int(result[0]["Turns"])
        return 0  # No hay trampa → no penaliza

    def get_trap_wait_time(self, room):
        """Obtiene el tiempo de espera que impone una trampa en una sala."""
        result = list(self.prolog.query(f"trap({room}, wait(WaitTime))"))
        if result:
            return int(result[0]["WaitTime"])
        return 0  # No hay trampa de espera

    def apply_trap_penalty(self, room):
        """Aplica la penalización de la trampa si corresponde."""
        penalty = self.get_trap_penalty(room)
        if penalty > 0:
            print(f"🔴 ¡Trampa activada! Reduce {penalty} movimientos en {room}.")
            return penalty
        return 0

    def apply_trap_wait(self, room):
        """Aplica la trampa de espera si corresponde."""
        wait_time = self.get_trap_wait_time(room)
        if wait_time > 0:
            print(f"🔴 ¡Trampa activada! Esperando {wait_time} segundos en {room}.")
            time.sleep(wait_time)  # Pausa para simular espera en segundos
            return wait_time
        return 0

    def handle_trap(self, room):
        """Gestiona las trampas al entrar a una sala."""
        penalty = self.apply_trap_penalty(room)
        wait_time = self.apply_trap_wait(room)
        return penalty, wait_time

    def enter_room(self, room):
        """Simula entrar a una sala y aplica efectos de trampas."""
        print(f"Entrando en {room}...")
        self.set_current_room(room)
        
        # Manejar trampas
        penalty, wait_time = self.handle_trap(room)
        
        if penalty > 0:
            print(f"Se aplicó una penalización de {penalty} movimientos en {room}.")
        if wait_time > 0:
            print(f"Esperando por {wait_time} segundos en {room}.")

        print(f"Puedes moverte con una penalización de {penalty} movimientos.")
        return penalty, wait_time
