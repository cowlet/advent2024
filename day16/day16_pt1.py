import copy
import time

class Path:
    def __init__(self, maze):
        self.maze = maze
        self.moves = [
                [[i, j, ">", 0] for i in range(maze.h) for j in range(maze.w) \
                        if maze.grid[i][j] == "S"][0]
        ]
        #print(f"Start reindeer at {self.moves[0]}")

    def dup(self):
        other = Path(maze)
        other.moves = copy.deepcopy(self.moves)
        return other

    def at_end(self):
        # Find the last move in the Path
        last = self.moves[-1]
        if last[0] == self.maze.end[0] and last[1] == self.maze.end[1]:
            return True
        return False

    def __str__(self):
        return str(self.moves)
    def __repr__(self):
        return self.__str__()

    def ever_in(self, other):
        last = self.moves[-1]
        for oth in other.moves:
            if last[0] == oth[0] and last[1] == oth[1]:
                return oth[3] # the other's score
        return False

class Maze:
    def __init__(self, lines):
        self.grid = [list(line.strip()) for line in lines]
        self.h = len(self.grid)
        self.w = len(self.grid[0])
        self.end = [[i, j] for i in range(self.h) for j in range(self.w) \
                        if self.grid[i][j] == "E"][0]
        print(f"Found end at {self.end}")
        self.deer = Path(self)
        print(self.deer)

    def __str__(self):
        return "\n".join(["".join(row) for row in self.grid])
    def __repr__(self):
        return self.__str__()

    def _can_move(self, m, deer):
        # Speculative deer, not self.deer
        if m == ">":
            next_i, next_j = deer.moves[-1][0], deer.moves[-1][1]+1
        elif m == "<":
            next_i, next_j = deer.moves[-1][0], deer.moves[-1][1]-1
        elif m == "^":
            next_i, next_j = deer.moves[-1][0]-1, deer.moves[-1][1]
        elif m == "v":
            next_i, next_j = deer.moves[-1][0]+1, deer.moves[-1][1]

        if self.grid[next_i][next_j] == "#":
            return False, [next_i, next_j]
        return True, [next_i, next_j, m]

    def _score(self, last_c, next_c):
        # 1 for a step, 1000 for a turn
        total = last_c[3] + 1
        if last_c[2] != next_c[2]:
            # We're turning for sure!
            if (last_c[2] in "<>" and next_c[2] in "<>") or \
                    (last_c[2] in "^v" and next_c[2] in "^v"):
                total += 2000 # 180 degrees
            else:
                total += 1000
        return total

    def _edit_moves(self, last_c):
        if last_c[2] == "<":
            return "<^v"
        if last_c[2] == ">":
            return ">^v"
        if last_c[2] == "^":
            return "<>^"
        return "<>v"

    def solve(self):
        cur = self.deer
        others = [self.deer]
        solves = []

        while len(others) > 0:
            cur, others = others[0], others[1:]
            if len(solves) > 0 and any([cur.moves[-1][3] > s.moves[-1][3] for s in solves]):
                #print(f"Skipping definitely worse score {cur.moves[-1][3]}")
                continue
            #print(f"Looking at deer path of length {len(cur.moves)}")
            # Try moving in all directions except the one we just came from
            moves = self._edit_moves(cur.moves[-1])
            #print(f"For last move {cur.moves[-1]} we're looking at {moves}")
            for m in moves:
                can, next_c = self._can_move(m, cur)
                if not can:
                    continue
                #print(f"Can move {m} to {next_c}")
                d = cur.dup()
                #print(f"Deer {d} is a dup of {cur}")
                d.moves.append(next_c + [self._score(cur.moves[-1], next_c)])
                # Is this a new location we haven't seen before?
                seen = False
                for other in others:
                    oth_score = d.ever_in(other)
                    if oth_score:
                        # d's last pos exists in other, so it's a dup
                        # If d is lower score than oth, discard oth
                        if d.moves[-1][3] < oth_score:
                            others.remove(other)
                        # If d is not lower score than oth, discard d (mark seen)
                        else:
                            seen = True
                if not seen: # or seen but better score than before
                    others.append(d)
                    if d.at_end():
                        #print(f"This is an end state! {d}")
                        solves.append(d)

            #time.sleep(1)
        print(f"Reached end")
        if len(solves) == 0:
            raise AttributeError("Reached all possible locations "
                                 "without finding the end!")

        print(f"{len(solves)} valid solutions")
        #print(solves)
        lowest = min([p.moves[-1][3] for p in solves])
        idx = [i for i, p in enumerate(solves) if p.moves[-1][3] == lowest][0]
        #print(f"Best path is {solves[idx]}")
        return lowest




#with open("d16_test1.txt", "r") as f:
#with open("d16_test2.txt", "r") as f:
with open("d16_input.txt", "r") as f:
    lines = f.readlines()

maze = Maze(lines)
print(maze)

cost = maze.solve()
print(f"Final score is {cost}")
