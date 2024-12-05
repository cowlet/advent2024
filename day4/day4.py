
with open("d4_input.txt", "r") as f:
    grid = f.readlines()
grid = [row.strip() for row in grid]


nrows = len(grid)
ncols = len(grid[0])

def print_xmas(a_i, a_j):
    print(f"Found an x-mas at ({a_i}, {a_j}):")
    print("\n".join([
        "".join([grid[a_i-1][a_j-1], grid[a_i][a_j-1], grid[a_i+1][a_j-1]]),
        "".join([grid[a_i-1][a_j], grid[a_i][a_j], grid[a_i+1][a_j]]),
        "".join([grid[a_i-1][a_j+1], grid[a_i][a_j+1], grid[a_i+1][a_j+1]])
    ]))

# As are the pivot point, and must be 1 char in from all sides
# to give space for M and S
xmases = 0

for i in range(1, nrows-1):
    for j in range(1, ncols-1):
        if grid[i][j] != "A":
            continue

        if (grid[i-1][j-1] == "M" and grid[i+1][j+1] == "S") or \
           (grid[i+1][j+1] == "M" and grid[i-1][j-1] == "S"):
            if (grid[i-1][j+1] == "M" and grid[i+1][j-1] == "S") or \
               (grid[i+1][j-1] == "M" and grid[i-1][j+1] == "S"):
                   #print_xmas(i, j)
                   xmases += 1
        elif (grid[i-1][j+1] == "M" and grid[i+1][j-1] == "S") or \
             (grid[i+1][j-1] == "M" and grid[i-1][j+1] == "S"):
            if (grid[i-1][j-1] == "M" and grid[i+1][j+1] == "S") or \
               (grid[i+1][j+1] == "M" and grid[i-1][j-1] == "S"):
                   #print_xmas(i, j)
                   xmases += 1
 
print(f"In total there are {xmases} XMASes")

