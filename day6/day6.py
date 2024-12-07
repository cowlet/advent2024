import itertools

with open("d6_input.txt", "r") as f:
    lines = f.readlines()

grid = [list(line.strip()) for line in lines]
for row in grid:
    print("".join(row))

r = len(grid)
c = len(grid[0])
guard = "^>v<"
gi, gj = 0, 0

for i, line in enumerate(grid):
    for j, ch in enumerate(line):
        if ch in guard:
            print(f"Found the guard at ({i}, {j})")
            gi, gj = i, j
            break

# Did we really find the guard, or did we run out of board?
on_grid = True
if grid[gi][gj] not in guard:
    print(f"*** Error: Could not find the guard at the start!! ***")
    on_grid = False

class Obstacle:
    def __init__(self, i, j, side):
        self.i = i
        self.j = j
        self.side = side

    def __str__(self):
        return f"[({self.i}, {self.j}): {self.side}]"

    def __repr__(self):
        return self.__str__()

def step(i, j):
    obs = None # Obstacles hit
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
        return i, j, False, obs

    if new_i < 0 or new_i >= c or new_j < 0 or new_j >= r:
        print(f"Guard exited the grid at ({new_i}, {new_j})")
        return new_i, new_j, False, obs

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

    return new_i, new_j, True, obs


obstacles = []
while on_grid:
    gi, gj, on_grid, obs = step(gi, gj)
    if obs:
        obstacles.append(obs)

print(f"Finished")
for row in grid:
    print("".join(row))

steps = sum([1 if ch in guard else 0 for row in grid for ch in row])
print(f"Steps == {steps}")

print(f"{len(obstacles)} obstacles found!")

def find_fourth(three_obs):
    top = min([x.i for x in three_obs])
    btm = max([x.i for x in three_obs])
    l = min([x.j for x in three_obs])
    r = max([x.j for x in three_obs])

    #   .a....
    #   .+--+b
    #   .|..|.
    #   d+--+.
    #   ....c.
    a = [x for x in three_obs if x.i==top][0]
    b = [x for x in three_obs if x.j==r][0]
    c = [x for x in three_obs if x.i==btm][0]
    d = [x for x in three_obs if x.j==l][0]

    #print(f"We have {a}, {b}, {c}, {d}")
    if a.i == (b.i-1) and b.j == (c.j+1):
        # We're placing d
        #print(f"We're placing d")
        # Check facing
        #if a.side == "^" and b.side == ">" and c.side == "v":
        return Obstacle(c.i-1, a.j-1, "<")
    elif a.i == (b.i-1) and d.j == (a.j-1):
        # We're placing c
        #print(f"We're placing c")
        #if d.side == "<" and a.side == "^" and b.side == ">":
        return Obstacle(d.i+1, b.j-1, "v")
    elif d.j == (a.j-1) and c.i == (d.i+1):
        # We're placing b
        #print(f"We're placing b")
        #if c.side == "v" and d.side == "<" and a.side == "^":
        return Obstacle(c.i-1, a.j-1, ">")
    elif b.j == (c.j-1) and c.i == (d.j-1):
        # We're placing a
        #print(f"We're placing a")
        #if b.side == ">" and c.side == "v" and d.side == "<":
        return Obstacle(b.i-1, d.j+1, "^")

    # Can't place!
    #print(f"Can't place")
    return None

possibles = []
for a, b, c in itertools.combinations(obstacles, 3):
    place = find_fourth([a, b, c])
    if place:
        possibles.append(place)

# Weed out any dups
uniq = []
for p in possibles:
    match = [1 for u in uniq if p.i==u.i and p.j==u.j]
    if len(match) == 0:
        uniq.append(p)

print(f"{len(uniq)} possible new objects to place")
