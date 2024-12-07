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

print(gi, gj)

def step(i, j):
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
        return i, j, False

    if new_i < 0 or new_i >= c or new_j < 0 or new_j >= r:
        print(f"Guard exited the grid at ({new_i}, {new_j})")
        return new_i, new_j, False

    if grid[new_i][new_j] == "#":
        # Stay in place and rotate
        idx = guard.index(grid[i][j]) + 1
        if idx >= len(guard):
            idx = 0
        grid[i][j] = guard[idx]
        new_i, new_j = i, j

    #print(f"Taking a step to ({new_i}, {new_j})")
    grid[new_i][new_j] = grid[i][j]

    return new_i, new_j, True


while on_grid:
    gi, gj, on_grid = step(gi, gj)

print(f"Finished")
for row in grid:
    print("".join(row))

steps = sum([1 if ch in guard else 0 for row in grid for ch in row])
print(f"Steps == {steps}")
