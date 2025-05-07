% filepath: /home/alejandro-mu-oz/Documentos/APO III/Integrative_Task_1/ti1-2025-1-e13-pythoneros/src/constraints/move_constraints.pl

:- dynamic move_count/1.

% Inicializar restricciones de movimiento
initialize_move_constraints :-
    retractall(move_count(_)), % Limpia cualquier estado previo
    assertz(move_count(0)),    % Inicializa el contador de movimientos en 0
    write('Move constraints initialized.'), nl.

% Actualizar conteo de movimientos
log_move :-
    move_count(Count),
    NewCount is Count + 1,
    retract(move_count(Count)),
    assertz(move_count(NewCount)).

% Verificar si el jugador puede moverse
check_move_constraints(From, To) :-
    can_move(From, To),
    inventory(Inventory),
    length(Inventory, Count),
    max_inventory(Max), % Usa la definición de core/inventory_system.pl
    Count =< Max,
    write('Move allowed.'), nl.