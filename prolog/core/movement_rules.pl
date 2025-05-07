% Declarar predicados dinámicos
:- dynamic can_move/2.

% Reglas básicas de movimiento

% Inicializar reglas de movimiento
initialize_movement_rules :-
    retractall(can_move(_, _)),

    % Definir reglas de movimiento entre habitaciones
    assertz(can_move(entrance, hall)),
    assertz(can_move(hall, entrance)),
    assertz(can_move(hall, library)),
    assertz(can_move(library, hall)),
    assertz(can_move(hall, kitchen)),
    assertz(can_move(kitchen, hall)),
    assertz(can_move(library, treasure)),
    assertz(can_move(treasure, library)),
    assertz(can_move(treasure, exit)),
    assertz(can_move(exit, treasure)),

    write('Movement rules initialized.'), nl.
    
% Verificar si el jugador puede moverse
can_move(From, To) :-
    current_room(From),
    (door(From, To, unlocked); 
     (door(From, To, locked), has_key_for(To))).

% Actualizar la habitación actual
update_current_room(Room) :-
    retract(current_room(_)),
    asserta(current_room(Room)),
    write('Moved to: '), write(Room), nl.

% Verificación de llaves
has_key_for(Room) :-
    door(_, Room, locked),
    inventory(Inventory),
    member(key(KeyName), Inventory),
    key_in_room(_, KeyName).

