from collections import deque

CONVEYORS = {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}
STEPS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def maze_solver_with_conveyors(maze: list[list[str]]) -> dict:
    """
    Rules (inferred from the examples):
      - Stepping from a normal cell to an adjacent non-wall cell costs 1.
      - Standing on a conveyor forces a move in its direction at cost 0.
        Chained conveyors keep carrying you for free.
      - A conveyor pointing into a wall or off the grid leaves you stuck.
    Uses 0-1 BFS (deque): 0-cost edges go to the front, 1-cost to the back.
    """
    if not maze or not maze[0]:
        return {"distance": -1, "path": []}

    rows, cols = len(maze), len(maze[0])
    start = end = None
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)
    if start is None or end is None:
        return {"distance": -1, "path": []}

    INF = float('inf')
    dist = [[INF] * cols for _ in range(rows)]
    parent = {start: None}
    dist[start[0]][start[1]] = 0
    dq = deque([(0, start)])

    while dq:
        d, (r, c) = dq.popleft()
        if d > dist[r][c]:
            continue  # stale entry
        if (r, c) == end:
            break

        cell = maze[r][c]
        if cell in CONVEYORS:
            moves = [(CONVEYORS[cell], 0)]
        else:
            moves = [(step, 1) for step in STEPS]

        for (dr, dc), w in moves:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols) or maze[nr][nc] == '#':
                continue
            nd = d + w
            if nd < dist[nr][nc]:
                dist[nr][nc] = nd
                parent[(nr, nc)] = (r, c)
                if w == 0:
                    dq.appendleft((nd, (nr, nc)))
                else:
                    dq.append((nd, (nr, nc)))

    if dist[end[0]][end[1]] == INF:
        return {"distance": -1, "path": []}

    path, node = [], end
    while node is not None:
        path.append([node[0], node[1]])
        node = parent[node]
    path.reverse()
    return {"distance": dist[end[0]][end[1]], "path": path}


if __name__ == "__main__":
    maze = [
        ['S', '.', '>', '>', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    print(maze_solver_with_conveyors(maze))
    # {'distance': 2, 'path': [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]}

    maze = [
        ['S', '.', '>', '#', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    print(maze_solver_with_conveyors(maze))
    # {'distance': -1, 'path': []}

    maze = [
        ['S', '.', 'v', '.', 'E'],
        ['#', '#', 'v', '.', '#'],
        ['.', '.', 'v', '.', '.'],
        ['#', '#', '.', '.', '#'],
        ['.', '.', '.', '.', '.']
    ]
    print(maze_solver_with_conveyors(maze))
    # {'distance': 7, 'path': [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [3, 2], [3, 3], [2, 3], [1, 3], [0, 3], [0, 4]]}