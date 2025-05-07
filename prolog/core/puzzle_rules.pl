% Sistema de puzzles para la escape room
% Implementa diferentes tipos de puzzles que el jugador debe resolver

% Inicializar reglas de puzzles
initialize_puzzle_rules :-
    retractall(puzzle(_, _)),

    % Definir puzzles en habitaciones
    assertz(puzzle(library, riddle)),
    assertz(puzzle(treasure, lever_combination)),

    write('Puzzle rules initialized.'), nl.



:- dynamic puzzle_solved/1, door/3.

% Predicado principal para resolver puzzles
solve_puzzle(PuzzleName) :-
    current_room(Room),
    puzzle(Room, PuzzleName),
    puzzle_handler(PuzzleName),
    assertz(puzzle_solved(PuzzleName)),
    write('Puzzle "'), write(PuzzleName), write('" solved!'), nl.

% Manejadores de puzzles específicos
puzzle_handler(book_puzzle) :-
    % Puzzle de ordenar libros: requiere tener la llave correcta
    inventory(Inventory),
    member(key(key2), Inventory),
    retract(door(hall, library, locked)),
    assertz(door(hall, library, unlocked)),
    write('You arranged the books in the correct order using key2.'), nl.

puzzle_handler(riddle) :-
    % Acertijo: responder una pregunta
    write('The riddle asks: "What has keys but can\'t open locks?"'), nl,
    write('Your answer: '),
    read_line_to_string(user_input, Answer),
    (Answer = "keyboard" ->
        retract(door(library, treasure, locked)),
        assertz(door(library, treasure, unlocked)),
        write('Correct! The door to the treasure room unlocks.'), nl
    ;
        write('Incorrect answer. Try again.'), nl,
        fail
    ).

puzzle_handler(lever_combination) :-
    % Combinación de palancas: encontrar la secuencia correcta
    write('There are 3 levers. Each can be up (u) or down (d).'), nl,
    write('Enter combination (e.g., u,d,d): '),
    read_line_to_string(user_input, CombStr),
    split_string(CombStr, ",", "", CombList),
    (CombList = ["u","d","u"] ->
        retract(door(kitchen, secret, locked)),
        assertz(door(kitchen, secret, unlocked)),
        write('You pulled the levers in the correct combination! The secret door unlocks.'), nl
    ;
        write('Incorrect combination. Try again.'), nl,
        fail
    ).