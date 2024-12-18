import time 

class Step:
    def __init__(self, x, y, parent=None):
        self.x, self.y = x, y
        self.end_x, self.end_y = W-1, W-1
        self.parent = parent
    def at_end(self):
        return self.x == self.end_x and self.y == self.end_y
    def ever_in(self, other):
        cur = other
        while cur.parent:
            if cur.x == self.x and cur.y == self.y:
                return True
            cur = cur.parent
        return False
    def __str__(self):
        return f"({self.x}, {self.y})"
    def __repr__(self):
        return self.__str__()
    def draw(self, maze):
        grid = [[ch for ch in row] for row in maze.grid]
        cur = self
        while cur.parent:
            grid[cur.y][cur.x] = "O"
            cur = cur.parent
        print("-------")
        print("\n".join(["".join(row) for row in grid]))
        print("-------")
    def count(self):
        steps = 0
        cur = self
        while cur.parent:
            steps += 1
            cur = cur.parent
        return steps


class Maze:
    def __init__(self, coords, t, x, y):
        # Memory space
        self.grid = [["." for _ in range(W)] for _ in range(W)]
        # My location
        self.start_x, self.start_y = x, y
        self.grid[y][x] = "@"
        # All events up to time t have happened
        for i in range(t):
            self.grid[coords[i][1]][coords[i][0]] = "#"

    def __str__(self):
        return "\n".join(["".join(row) for row in self.grid])
    def __repr__(self):
        return self.__str__()

    def _can_move(self, m, prev_step):
        if m == ">":
            next_y, next_x = prev_step.y, prev_step.x+1
        elif m == "<":
            next_y, next_x = prev_step.y, prev_step.x-1
        elif m == "^":
            next_y, next_x = prev_step.y-1, prev_step.x
        elif m == "v":
            next_y, next_x = prev_step.y+1, prev_step.x
        # Stay on valid board
        if next_x < 0 or next_x > W-1 or next_y < 0 or next_y > W-1 \
                or self.grid[next_y][next_x] == "#":
            return False, next_x, next_y
        # Don't retrace steps
        if prev_step.parent and next_y == prev_step.parent.y and \
                next_x == prev_step.parent.x:
            return False, next_x, next_y
        return True, next_x, next_y

    def solve(self):
        others = [ Step(self.start_x, self.start_y) ] # no history
        # Shortest is best, so bfs always finds the best first
        while len(others) > 0:
            cur, others = others[0], others[1:]
            for m in "^v<>":
                can, next_x, next_y = self._can_move(m, cur)
                if not can:
                    continue
                d = Step(next_x, next_y, parent=cur)
                seen = False
                for other in others:
                    if d.ever_in(other): # Discard d
                        seen = True
                if not seen:
                    others.append(d)
                    if d.at_end():
                        print(f"Reached the end!")
                        return d
        return None

#W = 7 # 71
#with open("d18_test.txt", "r") as f:
W = 71
with open("d18_input.txt", "r") as f:
    lines = f.readlines()

coords = [[int(p) for p in line.strip().split(",")] for line in lines]

m = Maze(coords, 1024, 0, 0)
print("-------")
print(m)
print("-------")
soln = m.solve()
soln.draw(m)
print(f"This takes {soln.count()} steps")

# Unsolvable
#print(Maze(coords, len(coords), [0, 0]))
#print("------------------------")
