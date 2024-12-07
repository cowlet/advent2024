import itertools

guard = "^>v<"

class Obstacle:
    def __init__(self, i, j, side=None):
        self.i = i
        self.j = j
        self.side = side

    def __str__(self):
        if self.side:
            return f"[({self.i}, {self.j}): {self.side}]"
        return f"[({self.i}, {self.j})]"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j and self.side == other.side

def make_blank_grid(lines):
    grid = [list(line.strip()) for line in lines]
    for i, line in enumerate(grid):
        for j, ch in enumerate(line):
            if ch in guard:
                grid[i][j] = "."
    return grid

def trace_path(grid):
    gi, gj = 0, 0
    obstacles = []
    for i, line in enumerate(grid):
        for j, ch in enumerate(line):
            if ch in guard:
                print(f"Found the guard at ({i}, {j})")
                gi, gj = i, j
            if ch == "#":
                obstacles.append(Obstacle(i, j))

    # Did we really find the guard, or did we run out of board?
    on_grid = True
    if grid[gi][gj] not in guard:
        print(f"*** Error: Could not find the guard at the start!! ***")
        on_grid = False

    print(f"Found {len(obstacles)} obstacles")

    obstacles_hit = []
    while on_grid:
        grid, gi, gj, on_grid, obs = step(gi, gj, grid)
        if obs:
            if obs in obstacles_hit:
                print(f"Loop found!! We have hit twice into {obs}")
                raise ValueError("Loop!")
            obstacles_hit.append(obs)

    return grid, obstacles, obstacles_hit


def step(i, j, grid):
    obs = None # Obstacles hit
    r = len(grid)
    c = len(grid[0])

    if grid[i][j] == "^":
        new_i, new_j = i-1, j
    elif grid[i][j] == "v":
        new_i, new_j = i+1, j
    elif grid[i][j] == "<":
        new_i, new_j = i, j-1
    elif grid[i][j] == ">":
        new_i, new_j = i, j+1
    else:
        print(f"Lost the guard! ({i}, {j}) == {grid[i][j]}")
        return grid, i, j, False, obs

    if new_i < 0 or new_i >= c or new_j < 0 or new_j >= r:
        print(f"Guard exited the grid at ({new_i}, {new_j})")
        return grid, new_i, new_j, False, obs

    if grid[new_i][new_j] == "#":
        obs = Obstacle(new_i, new_j, grid[i][j]) # Save for later
        # Stay in place and rotate
        idx = guard.index(grid[i][j]) + 1
        if idx >= len(guard):
            idx = 0
        grid[i][j] = guard[idx]
        new_i, new_j = i, j

    #print(f"Taking a step to ({new_i}, {new_j})")
    grid[new_i][new_j] = grid[i][j]

    return grid, new_i, new_j, True, obs


with open("d6_test.txt", "r") as f:
    lines = f.readlines()

grid = [list(line.strip()) for line in lines]
for row in grid:
    print("".join(row))

grid, obstacles, obstacles_hit = trace_path(grid)

print(f"Finished")
for row in grid:
    print("".join(row))

steps = sum([1 if ch in guard else 0 for row in grid for ch in row])
print(f"Steps == {steps}")

print(f"{len(obstacles_hit)} obstacles hit by guard")

def find_fourth(three_obs):
    #   .a....
    #   .+--+b
    #   .|..|.
    #   d+--+.
    #   ....c.
    three_obs = sorted(three_obs, key=lambda x: x.i)
    # Becomes abdc, missing one

    a, b, c, d = None, None, None, None
    # We could have a, b, c: place d
    # a, b, d: place c
    # a, c, d: place b
    # b, c, d: place a
    if three_obs[0].i == (three_obs[1].i-1) and \
       three_obs[0].j < three_obs[1].j and \
       three_obs[1].j == (three_obs[2].j+1) and \
       three_obs[1].i < three_obs[2].i:
        a = three_obs[0]
        b = three_obs[1]
        c = three_obs[2]
        print(three_obs, a, b, c, None)
    elif three_obs[0].i == (three_obs[1].i-1) and \
         three_obs[0].j > three_obs[2].j and \
         three_obs[2].j == (three_obs[0].j-1) and \
         three_obs[2].i > three_obs[1].i:
        a = three_obs[0]
        b = three_obs[1]
        d = three_obs[2]
        print(three_obs, a, b, None, d)
    elif three_obs[0].j == (three_obs[1].j+1) and \
         three_obs[0].i < three_obs[2].i and \
         three_obs[1].i == (three_obs[2].i-1) and \
         three_obs[1].j < three_obs[2].j:
        a = three_obs[0]
        d = three_obs[1]
        c = three_obs[2]
        print(three_obs, a, None, c, d)
    elif three_obs[0].j == (three_obs[2].j+1) and \
         three_obs[0].i < three_obs[1].i and \
         three_obs[1].i == (three_obs[2].i-1) and \
         three_obs[1].j < three_obs[2].j:
        b = three_obs[0]
        d = three_obs[1]
        c = three_obs[2]
        print(three_obs, None, b, c, d)
    else:
        # Can't place
        return None

    # Now place
    if not a:
        obs = Obstacle(b.i-1, d.j+1)
        print(f"Placing a at {obs}")
    elif not b:
        obs = Obstacle(a.i+1, c.j+1)
        print(f"Placing b at {obs}")
    elif not c:
        obs = Obstacle(d.i+1, b.j-1)
        print(f"Placing c at {obs}")
    elif not d:
        obs = Obstacle(c.i-1, a.j-1)
        print(f"Placing d at {obs}")

    # Last step: is there a complete path? Or do other obstacles
    # block the way? Make a new grid with the obstacle in place.
    grid = make_blank_grid(lines)
    grid[obs.i][obs.j] = "#"
    if not a: # d exists, so place guard next to d
        grid[d.i][d.j+1] = "^"
    else: # a exists, so place under a
        grid[a.i+1][a.j] = ">"
    try:
        grid, _, obstacles_hit = trace_path(grid)
        print(f"--> No loop, so drop obstacle {obs}")
        for row in grid:
            print("".join(row))
    except ValueError:
        # If we hit a loop exception, we completed the path!
        print(f"Valid new object at {obs}")
        return obs

    # Otherwise, we didn't complete the path
    return None



possibles = []
for a, b, c in itertools.combinations(obstacles, 3):
    place = find_fourth([a, b, c])
    if place:
        print(place)
        possibles.append(place)

print("Possible objects to place:")
for p in possibles:
    print(p)
"""
# Weed out any dups
uniq = []
for p in possibles:
    match = [1 for u in uniq if p.i==u.i and p.j==u.j]
    if len(match) == 0:
        uniq.append(p)

print(f"{len(uniq)} possible new objects to place")
"""
