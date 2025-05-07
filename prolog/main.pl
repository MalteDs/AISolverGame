:- ensure_loaded('core/room_definitions.pl').
:- ensure_loaded('core/movement_rules.pl').
:- ensure_loaded('core/puzzle_rules.pl').
:- ensure_loaded('core/inventory_system.pl').
:- ensure_loaded('constraints/trap_constraints.pl').
:- ensure_loaded('constraints/move_constraints.pl').
:- ensure_loaded('search/pathfinding.pl').

:- initialization(setup_log).

% Inicialización del juego
initialize_game :-
    % Inicializar el estado del jugador
    retractall(current_room(_)),
    retractall(inventory(_)),
    asserta(current_room(entrance)),
    asserta(inventory([])),

    % Inicializar las definiciones de habitaciones
    initialize_rooms,

    % Inicializar reglas de movimiento
    initialize_movement_rules,

    % Inicializar reglas de puzzles
    initialize_puzzle_rules,

    % Inicializar sistema de inventario
    initialize_inventory_system,

    % Inicializar restricciones de trampas
    initialize_trap_constraints,

    % Inicializar restricciones de movimiento
    initialize_move_constraints,

    % Inicializar sistema de búsqueda
    initialize_pathfinding.

% Inicializar el sistema de logging
setup_log :-
    tell('prolog_log.txt'),  % Redirige todo output
    write('--- PROLOG LOG START ---'), nl.