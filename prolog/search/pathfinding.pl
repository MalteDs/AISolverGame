% Inicializar el sistema de búsqueda de rutas
initialize_pathfinding :-
    write('Pathfinding system initialized.'), nl.

% DFS para encontrar rutas
find_path(Start, End, Path) :-
    dfs(Start, End, [Start], Path).

dfs(End, End, Visited, Visited).

dfs(Current, End, Visited, Path) :-
    (door(Current, Next, unlocked); 
     (door(Current, Next, locked), has_key_for(Next))),
    \+ member(Next, Visited),
    dfs(Next, End, [Next|Visited], Path).