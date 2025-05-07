from core.parser import load_escape_room_from_file
from core.engine import EscapeRoomEngine
from ui.live_game import play_with_arrows, animate_path
# from ui.game import play_with_arrows_pygame
from search.a_star import a_star_search

if __name__ == "__main__":
    graph, start, goal, inventory_limit, max_turns = load_escape_room_from_file("data/example01.json")

    engine = EscapeRoomEngine(
        prolog_path="prolog/main.pl",
        graph=graph,
        start_room=start,
        inventory_limit=inventory_limit,
        max_moves=max_turns
    )

    print("Selecciona el modo de juego:")
    print("1. Manual (con flechas del teclado)")
    print("2. Automático (A* resolverá la sala)")
    choice = input("Ingresa 1 o 2: ")

    if choice == "1":
        play_with_arrows(engine) 
    elif choice == "2":
        path = a_star_search(engine, goal)  
        if path:
            print("Ruta encontrada por A*:", " → ".join(path))
            input("Presiona Enter para ver la animación del recorrido...")
            animate_path(engine, path)
        else:
            print("No se encontró una ruta.")
