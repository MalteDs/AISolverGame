% filepath: /home/alejandro-mu-oz/Documentos/APO III/Integrative_Task_1/ti1-2025-1-e13-pythoneros/src/core/room_definitions.pl

% Inicializar las habitaciones y sus conexiones
initialize_rooms :-
    % Limpiar datos previos
    retractall(room(_)),
    retractall(door(_, _, _)),
    retractall(key_in_room(_, _)),
    retractall(puzzle(_, _)),

    % Definir habitaciones
    assertz(room(entrance)),
    assertz(room(hall)),
    assertz(room(library)),
    assertz(room(kitchen)),
    assertz(room(treasure)),
    assertz(room(exit)),

    % Definir conexiones entre habitaciones
    assertz(door(entrance, hall, unlocked)),
    assertz(door(hall, library, locked)),
    assertz(door(hall, kitchen, unlocked)),
    assertz(door(library, treasure, locked)),
    assertz(door(treasure, exit, unlocked)),

    % Definir objetos en habitaciones
    assertz(key_in_room(library, key1)),
    assertz(key_in_room(kitchen, key2)),

    % Definir puzzles en habitaciones
    assertz(puzzle(library, book_puzzle)),
    assertz(puzzle(treasure, riddle)),

    write('Rooms, doors, keys, and puzzles initialized.'), nl.