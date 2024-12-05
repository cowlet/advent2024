
with open("d4_input.txt", "r") as f:
    grid = f.readlines()
grid = [row.strip() for row in grid]

def find_xmas_row(s):
    count = 0
    xmas = "XMAS"
    for i in range(len(s)):
        if s[i:i+len(xmas)] == xmas:
            count += 1
            i = i+len(xmas)
    return count

def find_xmas(rows):
    xmas = 0
    for row in rows:
        tmp = find_xmas_row(row)
        if tmp > 0:
            print(f"Found {tmp} instances of XMAS in {row}")
        xmas += tmp
    return xmas

def find_fwd(grid):
    return find_xmas(grid)

def find_back(grid):
    print("** Backwards **")
    rows = [row[::-1] for row in grid]
    return find_xmas(rows)

def find_down(grid):
    print("** Down **")
    ncols = len(grid[0])
    rows = ["".join([row[i] for row in grid]) for i in range(ncols)]
    return find_xmas(rows)

def find_up(grid):
    print("** Up **")
    ncols = len(grid[0])
    rows = ["".join(reversed([row[i] for row in grid])) for i in range(ncols)]
    print(rows)
    return find_xmas(rows)

def find_diag_r(grid):
    print("** Diag r **")
    nrows = len(grid)
    ncols = len(grid[0])
    ndiag = ncols+nrows-1

    # Start in the bottom right towards top left, reading down
    rows = ["" for i in range(ndiag)]

    for k in range(ndiag):
        i = 0
        j = ndiag-1-k
        while i < nrows and j >= 0:
            #print(f"Looking at grid({i}, {j}) on row {k}")
            if i >= 0 and j < nrows: # else, skip
                rows[k] += grid[i][j]
            i+=1
            j-=1
    
    count_down = find_xmas(rows)
    #print(rows)
    #print(f"{count_down} right down diags")

    # Reverse these strings for same direction, reading up
    rows = ["".join(reversed(row)) for row in rows]
    count_up = find_xmas(rows)
    #print(rows)
    #print(f"{count_up} right up diags")
    return count_down + count_up


def find_diag_l(grid):
    print("** Diag l **")
    # What if we reversed the order of the rows and passed to find_diag_r?
    rows = ["".join(reversed(row)) for row in grid]
    return(find_diag_r(rows))


fwd = find_fwd(grid)
bck = find_back(grid)
down = find_down(grid)
up = find_up(grid)
diag_r = find_diag_r(grid)
diag_l = find_diag_l(grid)

total = fwd + bck + down + up + diag_r + diag_l

print(f"In total there are {total} XMASes")

