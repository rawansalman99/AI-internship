import heapq
def astar(maze, start, goal):
    rows, cols = len(maze), len(maze[0])

    open_list = []
    heapq.heappush(open_list, (0, start))

    came_from = {}
    g_score = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            return reconstruct_path(came_from, current)
        for move in [(0,1), (1,0), (0,-1), (-1,0)]:
            neighbor = (current[0] + move[0], current[1] + move[1])

            if not (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols):
                continue
            if maze[neighbor[0]][neighbor[1]] == 1:
                continue

            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_score, neighbor))

    return None  

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]


def print_maze(maze, path, start, goal):
    path_set = set(path) if path else set()

    print("\nMaze:\n")
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (i, j) == start:
                print("S", end=" ")
            elif (i, j) == goal:
                print("G", end=" ")
            elif (i, j) in path_set:
                print("*", end=" ")
            elif maze[i][j] == 1:
                print("#", end=" ")
            else:
                print(".", end=" ")
        print()


maze = [
    [0,0,0,0,1],
    [1,1,0,1,0],
    [0,0,0,1,0],
    [0,1,1,0,0],
    [0,0,0,0,0]
]

start = (0, 0)
goal = (4, 4)


path = astar(maze, start, goal)


if path:
    print("Shortest Path:", path)
    print_maze(maze, path, start, goal)
else:
    print("No path found (Goal unreachable)")
