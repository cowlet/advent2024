class Step:
    def __init__(self, i, j, prev=None):
        self.i, self.j = i, j
        self.v = GRID[i][j]
        self.prev = prev

        # Connections
        self.up, self.down, self.right, self.left = None, None, None, None
        if self.i-1 >= 0 and GRID[self.i-1][self.j] == self.v+1:
            self.up = Step(self.i-1, self.j, self)
        if self.i+1 < ROWS and GRID[self.i+1][self.j] == self.v+1:
            self.down = Step(self.i+1, self.j, self)
        if self.j-1 >= 0 and GRID[self.i][self.j-1] == self.v+1:
            self.left = Step(self.i, self.j-1, self)
        if self.j+1 < COLS and GRID[self.i][self.j+1] == self.v+1:
            self.right = Step(self.i, self.j+1, self)

    def __str__(self):
        return f"[{self.v}: ({self.i}, {self.j})]"
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def path_to_nine(self, nine):
        # Can we get from here to there?
        if self == nine:
            return True
        # Test all 4 directions and propagate a True
        if self.up and self.up.path_to_nine(nine):
            return True
        if self.down and self.down.path_to_nine(nine):
            return True
        if self.left and self.left.path_to_nine(nine):
            return True
        if self.right and self.right.path_to_nine(nine):
            return True
        return False

    def all_paths(self, nine, routes=None):
        # How many ways from here to there?
        if not routes:
            routes = ["0"]

        if self == nine:
            return routes # We're finished!

        updated = []
        if self.up:
            # Add the up path onto the routes, and pass along
            updated.extend(self.up.all_paths(nine, [f"{r}u" for r in routes]))
        if self.down:
            updated.extend(self.down.all_paths(nine, [f"{r}d" for r in routes]))
        if self.left:
            updated.extend(self.left.all_paths(nine, [f"{r}l" for r in routes]))
        if self.right:
            updated.extend(self.right.all_paths(nine, [f"{r}r" for r in routes]))

        return updated


with open("d10_input.txt", "r") as f:
#with open("d10_test.txt", "r") as f:
    lines = f.readlines()
GRID = [[int(ch) for ch in line.strip()] for line in lines]
ROWS = len(GRID)
COLS = len(GRID[0])

theads = []
nines = []
for i, row in enumerate(GRID):
    for j, v in enumerate(row):
        if v == 0:
            theads.append(Step(i, j))
        if v == 9:
            nines.append(Step(i, j))

print(f"There are {len(theads)} trail heads and {len(nines)} nines")

scores = []
for th in theads:
    print(f"Considering trail {th}")
    all_paths = []
    for nine in nines:
        paths = th.all_paths(nine)
        #print(f"There are {len(paths)} routes between {th} and {nine}: {'; '.join(paths)}")
        all_paths.extend(paths)

    scores.append(len(all_paths))
#print(f"Scores are {scores}")
print(f"Total is {sum(scores)}")


