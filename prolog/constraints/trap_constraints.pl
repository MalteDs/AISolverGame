:- dynamic trap/2, turns_in_room/2, game_over/0, wait_time/2.

initialize_trap_constraints :-
    retractall(trap(_, _)),
    retractall(turns_in_room(_, _)),
    retractall(game_over),
    retractall(wait_time(_, _)), 
    assertz(trap(storage, reduce_movement(1))),    
    assertz(trap(library, reduce_movement(1))),    
    assertz(trap(hall, wait(10))),             
    assertz(trap(keyroom2, wait(15))),              
    assertz(trap(deadend1, reduce_movement(2))),    
    assertz(trap(deadend2, reduce_movement(1))),   

    write('Trap constraints initialized.'), nl.

% Lógica para entrar a una sala
enter_room(Room) :-
    ( turns_in_room(Room, N) ->
        NewN is N + 1,
        retract(turns_in_room(Room, N)),
        assertz(turns_in_room(Room, NewN)),
        format("🔄 Turno en ~w: ~w~n", [Room, NewN])
    ;
        assertz(turns_in_room(Room, 1)),
        format("🆕 Primera vez en ~w~n", [Room])
    ),
    check_trap(Room).

% Verifica si la trampa se activa
check_trap(Room) :-
    trap(Room, reduce_movement(Reduction)),
    turns_in_room(Room, N),
    format("⏳ Revisando trampa en ~w: Reducción de movimientos: ~w~n", [Room, Reduction]),
    Reduction > 0,
    N >= Reduction,
    \+ game_over,
    write('💥 ¡Trampa activada! Reducción de movimientos.'), nl,
    assertz(game_over).

check_trap(Room) :-
    trap(Room, wait(WaitTime)),
    turns_in_room(Room, N),
    format("⏳ Revisando trampa en ~w: Espera de ~w segundos~n", [Room, WaitTime]),
    N >= 1,
    \+ game_over,
    write('💥 ¡Trampa activada! Se detendrá durante ~w segundos.', [WaitTime]),
    % Aquí harías una pausa de espera en un juego real, pero en Prolog se representa simplemente como un mensaje
    sleep(WaitTime),  % Simula el tiempo de espera
    assertz(game_over).

check_trap(Room) :-
    \+ trap(Room, _),
    format("✅ No hay trampa en ~w.~n", [Room]).

check_trap(Room) :-
    trap(Room, reduce_movement(_)),
    turns_in_room(Room, N),
    format("⏱️ Aún no se activa la trampa de reducción de movimiento en ~w (turno ~w).~n", [Room, N]).

check_trap(Room) :-
    trap(Room, wait(_)),
    turns_in_room(Room, N),
    format("⏱️ Aún no se activa la trampa de espera en ~w (turno ~w).~n", [Room, N]).
