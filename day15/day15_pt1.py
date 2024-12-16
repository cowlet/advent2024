class Room:
    def __init__(self, lines):
        self.grid = [list(row) for row in lines]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        self.robot = self._find("@")[0]
        self.boxes = self._find("O")
        self.walls = self._find("#")

    def __str__(self):
        return "\n".join(["".join(row) for row in self.grid]) + \
                f"\nRobot at {self.robot}"#\nBoxes at {self.boxes}"
    def __repr__(self):
        return self.__str__()

    def _find(self, char):
        return [[i, j, char] for i in range(self.rows) \
                        for j in range(self.cols) \
                            if self.grid[i][j] == char]

    @staticmethod
    def _move_coords(m, item):
        #print(f"Moving item {item} in direction {m}")
        if m == "^":
            next_c = [item[0]-1, item[1]] # Same col, -1 row
        elif m == "v":
            next_c = [item[0]+1, item[1]] # Same col
        elif m == "<":
            next_c = [item[0], item[1]-1] # Same row, -1 col
        elif m == ">":
            next_c = [item[0], item[1]+1] # Same row
        else:
            raise ValueError(f"Uh oh, found move {m}")
        return next_c

    def move_robot(self, m):
        next_c = Room._move_coords(m, self.robot)
        # Are we still in bounds? Must be, bc of walls
        # Are there items blocking (including walls)?
        can_move = self.grid[next_c[0]][next_c[1]] == "."
        if can_move:
            #print(f"Easy robot move")
            self.grid[self.robot[0]][self.robot[1]] = "."
            self.robot = next_c + [self.robot[2]]
            self.grid[self.robot[0]][self.robot[1]] = self.robot[2]
            return
        # If we can't move, can we move the item which is
        # blocking up? (ie, is it a box?)
        stack = []
        while self.grid[next_c[0]][next_c[1]] == "O":
            stack.append(next_c + ["O"])
            next_c = Room._move_coords(m, next_c)
        # Now we have a stack of zero or more O in front of @
        if self.grid[next_c[0]][next_c[1]] == "#":
            # We can't move anything. No board updates!
            #print(f"No movement")
            return
        # There should be room to move
        if self.grid[next_c[0]][next_c[1]] != ".":
            raise ValueError(f"Found "
            f"{self.grid[next_c[0]][next_c[1]]} when expecting '.'")
        #print(f"Move stack")
        for item in stack[::-1]:
            # next_c is the spare slot
            #print(f"Moving {item}")
            self.grid[next_c[0]][next_c[1]] = item[2]
            next_c = item
        # Original spot is now clear
        #print(f"Robot prev at {self.robot}, next_c is {next_c}")
        self.grid[self.robot[0]][self.robot[1]] = "."
        self.robot = next_c[:-1] + [self.robot[2]]
        self.grid[self.robot[0]][self.robot[1]] = self.robot[2]
        # Update all placement records to match board
        self.robot = self._find("@")[0]
        self.boxes = self._find("O")
        return

    def gps(self):
        pos = []
        for box in self.boxes:
            pos.append(100 * box[0] + box[1])
        return sum(pos)

#with open("d15_test1.txt", "r") as f:
#with open("d15_test2.txt", "r") as f:
with open("d15_input.txt", "r") as f:
    lines = f.readlines()

grid = []
moves = ""
for line in lines:
    if len(line) > 0 and line[0] == "#":
        grid.append(line.strip())
    else:
        moves += line.strip()

#print([f">{g}<" for g in grid])
print(f"${moves}$")

room = Room(grid)
print(room)

for m in moves:
    room.move_robot(m)
    print(room)

print(f"Final GPS is {room.gps()}")
