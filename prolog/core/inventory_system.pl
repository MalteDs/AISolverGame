% Sistema de inventario para el jugador
% Maneja la recolección, uso y capacidad de objetos


% Inicializar el sistema de inventario
initialize_inventory_system :-
    retractall(inventory(_)),
    assertz(inventory([])), % Inventario vacío al inicio
    write('Inventory system initialized.'), nl.

:- dynamic inventory/1, key_in_room/2, item_in_room/2.

% Inicializar inventario
init_inventory :-
    retractall(inventory(_)),
    assertz(inventory([])).

% Recoger un objeto del suelo
pick(Item) :-
    current_room(Room),
    (key_in_room(Room, Item); item_in_room(Room, Item)),
    inventory(CurrentInv),
    max_inventory(Max),
    length(CurrentInv, Count),
    Count < Max,
    retract(key_in_room(Room, Item)),
    retract(inventory(CurrentInv)),
    assertz(inventory([Item|CurrentInv])),
    write('Picked up: '), write(Item), nl.

pick(Item) :-
    inventory(CurrentInv),
    max_inventory(Max),
    length(CurrentInv, Count),
    Count >= Max,
    write('Cannot pick up '), write(Item), write('. Inventory full!'), nl,
    fail.

% Soltar un objeto
drop(Item) :-
    current_room(Room),
    inventory(CurrentInv),
    member(Item, CurrentInv),
    delete(CurrentInv, Item, NewInv),
    retract(inventory(CurrentInv)),
    assertz(inventory(NewInv)),
    assertz(item_in_room(Room, Item)),
    write('Dropped: '), write(Item), nl.

% Usar un objeto del inventario
use(Item) :-
    inventory(CurrentInv),
    member(Item, CurrentInv),
    item_effect(Item).

% Efectos específicos de cada objeto
item_effect(key(KeyName)) :-
    current_room(Room),
    door(Room, NextRoom, locked),
    key_unlocks(key(KeyName), NextRoom),
    retract(door(Room, NextRoom, locked)),
    assertz(door(Room, NextRoom, unlocked)),
    write('Used '), write(KeyName), write(' to unlock door to '), write(NextRoom), nl.

item_effect(torch) :-
    current_room(Room),
    room_dark(Room),
    retract(room_dark(Room)),
    write('The torch illuminates the room. You can now see puzzles and doors.'), nl.

% Verificar qué llave abre qué puerta
key_unlocks(key(key1), library).
key_unlocks(key(key2), treasure).

% Mostrar inventario
show_inventory :-
    inventory(Items),
    (Items = [] ->
        write('Your inventory is empty.'), nl
    ;
        write('Inventory: '), nl,
        list_items(Items)
    ).

list_items([]).
list_items([H|T]) :-
    write('- '), write(H), nl,
    list_items(T).

% Capacidad máxima del inventario
max_inventory(3).