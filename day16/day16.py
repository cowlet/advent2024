import copy
import time

class Path:
    def __init__(self, i, j, m, parent=None):
        self.i, self.j = i, j
        self.m = m
        self.parent = parent
        if parent:
            if m == parent.m: # no turns
                self.score = parent.score + 1
            else:
                self.score = parent.score + 1001
        else:
            self.score = 0
    def at_end(self, end_c):
        return self.i == end_c[0] and self.j == end_c[1]
    def ever_in(self, other):
        cur = other
        while cur.parent:
            if cur.i == self.i and cur.j == self.j:
                return cur.score, cur # Return the other's score here
            cur = cur.parent
        return False, None
    def __str__(self):
        return f"({self.i}, {self.j})"
    def __repr__(self):
        return self.__str__()

class Maze:
    def __init__(self, lines):
        self.grid = [list(line.strip()) for line in lines]
        self.h = len(self.grid)
        self.w = len(self.grid[0])
        self.start = [[i, j] for i in range(self.h) for j in range(self.w) \
                        if self.grid[i][j] == "S"][0]
        self.end = [[i, j] for i in range(self.h) for j in range(self.w) \
                        if self.grid[i][j] == "E"][0]
        print(f"Found end at {self.end}")
        self.deer = Path(self.start[0], self.start[1], ">")
        print(self.deer)

    def __str__(self):
        return "\n".join(["".join(row) for row in self.grid])
    def __repr__(self):
        return self.__str__()

    def draw(self, deer):
        output = copy.deepcopy(self.grid)
        cur = deer
        while cur.parent:
            output[cur.i][cur.j] = cur.m
            cur = cur.parent
        return "\n".join(["".join(row) for row in output])

    def _can_move(self, m, prev):
        # Speculative deer, not self.deer
        if m == ">":
            next_i, next_j = prev.i, prev.j+1
        elif m == "<":
            next_i, next_j = prev.i, prev.j-1
        elif m == "^":
            next_i, next_j = prev.i-1, prev.j
        elif m == "v":
            next_i, next_j = prev.i+1, prev.j

        # Stay on board
        if self.grid[next_i][next_j] == "#":
            return False, next_i, next_j
        # Don't retrace steps
        if prev.parent and next_i == prev.parent.i and next_j == prev.parent.j:
            return False, next_i, next_j
        return True, next_i, next_j

    def solve(self):

        solns = self._greedy_find()
        print(f"There are {len(solns)} best paths with scores {[s.score for s in solns]}")
        #print(f"One is:")
        #print(self.draw(some_best[0]))
        # Look for all
        all_best = self._all_matching(solns[0])
        print(f"Ends up as {len(all_best)} best paths")
        #all_best = some_best
        uniques = []
        for s in all_best:
            cur = s
            while cur.parent:
                exists = False
                for u in uniques:
                    if cur.i == u[0] and cur.j == u[1]:
                        exists = True
                if not exists:
                    uniques.append([cur.i, cur.j])
                cur = cur.parent
        return len(uniques) + 1 # 1 for the start tile

    def _all_matching(self, soln):
        # Find all paths which match soln.score
        others = [self.deer]
        solves = []

        while len(others) > 0:
            # Still breadth first, since we know our target now
            cur, others = others[0], others[1:]
            if cur.score > soln.score:
                print(f"Skipping definitely worse score {cur.score}. "
                      f"{len(others)} others")
                continue
            print(self.draw(cur))
            print(len(others))

            for m in "^v<>":
                can, next_i, next_j = self._can_move(m, cur)
                if not can:
                    continue
                d = Path(next_i, next_j, m, parent=cur)
                if d.score > soln.score: # Can't do better
                    continue
                # Discard d if we are in a loop, or if we have been here in
                # soln with a better score. Inspect others to cut out those
                # with the same position and facing.
                seen = False
                # Loop
                p = d.parent
                while p:
                    if p.i == d.i and p.j == d.j:
                        seen = True
                    p = p.parent
                # In soln: actually check if two steps in a row are the same.
                # Otherwise, we don't know if we have turned in alignment
                p = soln
                while p:
                    if p.i == d.i and p.j == d.j and p.parent and d.parent and \
                        p.parent.i == d.parent.i and p.parent.j == p.parent.j and \
                            p.score < d.score:
                        seen = True
                    p = p.parent
                # Inspect others
                for other in others:
                    p = other
                    while p:
                        if p.i == d.i and p.j == d.j and p.parent and d.parent and \
                           p.parent.i == d.parent.i and p.parent.j == p.parent.j:
                            if d.score < p.score:
                                others.remove(other)
                            elif d.score > p.score:
                                seen = True
                        p = p.parent

                # If none happened
                if not seen:
                    others.append(d)
                    if d.at_end(self.end):
                        solves.append(d)
        return solves

    def _greedy_find(self):
        ## Greedy algorithm first to find the best path score
        others = [self.deer]
        solves = []

        while len(others) > 0:
            cur, others = others[0], others[1:]
            if len(solves) > 0 and any([cur.score > s.score for s in solves]):
                #print(f"Skipping definitely worse score {cur.moves[-1][3]}. "
                #      f"{len(others)} others")
                continue
            for m in "^v<>":
                can, next_i, next_j = self._can_move(m, cur)
                if not can:
                    continue
                d = Path(next_i, next_j, m, parent=cur)
                # Is this a new location we haven't seen before?
                seen = False
                for other in others:
                    oth_score, _ = d.ever_in(other)
                    if oth_score:
                        # d's last pos exists in other, so it's a dup
                        if d.score < oth_score:
                            #    print(f"Removing other from others")
                            others.remove(other)
                        # If d is higher score than oth, discard d (mark seen)
                        elif d.score > oth_score:
                            #    print(f"Discarding d")
                            seen = True
                        # else, they're even or potentially so. keep both
                if not seen: # or seen but better score than before
                    others.append(d)
                    if d.at_end(self.end):
                        #print(f"This is an end state! {d}")
                        solves.append(d)

            #time.sleep(1)
        print(f"Reached end")
        if len(solves) == 0:
            raise AttributeError("Reached all possible locations "
                                 "without finding the end!")

        #print(f"{len(solves)} valid solutions")
        print([s.score for s in solves])
        lowest = min([s.score for s in solves])
        idxes = [i for i, s in enumerate(solves) if s.score == lowest]
        print(f"{len(idxes)} with the same score")
        #print(f"Best path is {solves[idx]}")
        return [s for i, s in enumerate(solves) if i in idxes]




#with open("d16_test1.txt", "r") as f:
#with open("d16_test2.txt", "r") as f:
with open("d16_input.txt", "r") as f:
    lines = f.readlines()

maze = Maze(lines)
print(maze)

cost = maze.solve()
print(f"Final score is {cost}")
