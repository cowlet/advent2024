class Room:
    def __init__(self, lines):
        self.grid = [
                list("".join([Room._convert(ch) for ch in row])) \
                            for row in lines]

        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        self.robot = self._find("@")[0]
        self.l_boxes = self._find("[")
        self.r_boxes = self._find("]")
        self.walls = self._find("#")

    @staticmethod
    def _convert(ch):
        c = {"#": "##", "O": "[]", ".": "..", "@": "@."}
        return c[ch]

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

    def _can_move_boxes(self, m, items):
        if m not in "^v":
            raise ValueError(f"We should only move up or down! Not {m}")
        print(f"Items are {items}")
        # item is half a box. Can we move all the box?
        to_move = []
        for item in items:
            print(item)
            if item[2] == "[":
                to_move.extend([item,  [item[0], item[1]+1, "]"]])
            else:
                to_move.extend([[item[0], item[1]-1, "["], item])
        # Thin out dups
        print(f"Trying to move {len(to_move)} spots")
        print(to_move)
        all_next_coords = [Room._move_coords(m, it) for it in to_move]
        # If any can't move, none can move
        all_next_chars = [self.grid[i][j] for i, j in all_next_coords]
        print(f"all_next_chars are: {all_next_chars}")
        if any([ch == "#" for ch in all_next_chars]):
            # We can't move anything. No board updates!
            print(f"No movement")
            return False, []
        # Are they . or []?
        next_boxes = [idx for idx, ch in enumerate(all_next_chars) if ch in "[]"]
        if len(next_boxes) > 0:
            # Try moving those! Thin out dups?
            print(f"Next boxes is {next_boxes}")
            #next_boxes = [b for i, b in enumerate(next_boxes) if i%2==0]
            #print(f"Thins out to {next_boxes}")
            # Convert next_boxes indices to positions
            # Call _can_move_box on all of these
            can_move_next, all_next = self._can_move_boxes(m,
                        [all_next_coords[idx]+[all_next_chars[idx]]\
                                for idx in next_boxes])
            if not can_move_next:
                print(f"No movement of stack")
                return False, []

            return True, [to_move] + [all_next]
            # If we get here, we can actually move them?
        # Might have some next_boxes, otherwise all_next_chars are "."
        return True, to_move

    def _simple_stack(self, m, next_c):
        stack = []
        while self.grid[next_c[0]][next_c[1]] in "[]":
            stack.append(next_c + [self.grid[next_c[0]][next_c[1]]])
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
            print(f"Moving {item}")
            self.grid[next_c[0]][next_c[1]] = item[2]
            next_c = item
        # Original spot is now clear
        #print(f"Robot prev at {self.robot}, next_c is {next_c}")
        self.grid[self.robot[0]][self.robot[1]] = "."
        self.robot = next_c[:-1] + [self.robot[2]]
        self.grid[self.robot[0]][self.robot[1]] = self.robot[2]
        # Update all placement records to match board
        self.robot = self._find("@")[0]
        self.l_boxes = self._find("[")
        self.r_boxes = self._find("]")

    def move_robot(self, m):
        next_c = Room._move_coords(m, self.robot)
        # Are we still in bounds? Must be, bc of walls
        # Are there items blocking (including walls)?
        can_move = self.grid[next_c[0]][next_c[1]] == "."
        if can_move:
            print(f"Easy robot move")
            self.grid[self.robot[0]][self.robot[1]] = "."
            self.robot = next_c + [self.robot[2]]
            self.grid[self.robot[0]][self.robot[1]] = self.robot[2]
            return
        # If we can't move, can we move the item which is
        # blocking? (ie, is it a box?). Different if we're
        # moving in a row or a columns
        if m in "<>":
            # Same as part 1 case
            self._simple_stack(m, next_c)
            return

        # If we're here, moving a column. Need to be able to
        # move the full width of box(es)
        char = self.grid[next_c[0]][next_c[1]]
        if char not in "[]":
            print(f"Not a box")
            return
        can_move_box, stack = \
                    self._can_move_boxes(m, [next_c + [char]])
        if not can_move_box:
            print(f"Can't move stack")
            return
        # Now we have a stack of zero or more [] in front of @
        print(f"Move stack: {stack}")
        for row in stack[::-1]:
            # next_c is the spare slot
            print(f"Moving {row}")
            for item in row:
                next_c = Room._move_coords(m, item)
                self.grid[item[0]][item[1]] = "."
                self.grid[next_c[0]][next_c[1]] = item[2]
        # Original spot is now clear
        next_c = Room._move_coords(m, self.robot)
        print(f"Robot prev at {self.robot}, next_c is {next_c}")
        self.grid[self.robot[0]][self.robot[1]] = "."
        self.robot = next_c[:2] + [self.robot[2]]
        print(self.robot)
        self.grid[self.robot[0]][self.robot[1]] = self.robot[2]
        # Update all placement records to match board
        self.robot = self._find("@")[0]
        self.l_boxes = self._find("[")
        self.r_boxes = self._find("]")
        return

    def gps(self):
        pos = []
        for box in self.l_boxes:
            pos.append(100 * box[0] + box[1])
        return sum(pos)

#with open("d15_test1.txt", "r") as f:
#with open("d15_test2.txt", "r") as f:
with open("d15_test3.txt", "r") as f:
#with open("d15_input.txt", "r") as f:
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

#print(f"Final GPS is {room.gps()}")
