import time

class Robot:
    def __init__(self, line):
        p, v = line.strip().split(" ")
        self.x, self.y = [int(x) for x in p[2:].split(",")]
        self.dx, self.dy = [int(x) for x in v[2:].split(",")]
    def __str__(self):
        return f"({self.x}, {self.y}) -> ({self.dx}, {self.dy})"
    def __repr__(self):
        return self.__str__()

    def next(self, room):
        x = (self.x+self.dx) % room.W
        y = (self.y+self.dy) % room.H
        self.x, self.y = x, y

    def neighbourhood(self, room):
        n_size = 5
        neighbours = 0
        for y in range(self.y-n_size, self.y+n_size):
            for x in range(self.x-n_size, self.x+n_size):
                if self.y-n_size >= 0 and self.y+n_size < Room.H and \
                        self.x-n_size >= 0 and self.x+n_size < Room.W:
                    neighbours += room.grid[y][x]
        return neighbours

class Room:
    #W, H = 11, 7
    W, H = 101, 103
    def __init__(self, robots):
        self.robots = robots
        self._update_robots()

    def advance(self):
        [r.next(self) for r in self.robots]
        self._update_robots()

    def _update_robots(self):
        # Set up an empty grid
        self.grid = []
        for _ in range(Room.H):
            self.grid.append([0]*Room.W)
        # Place the robots
        for r in self.robots:
            self.grid[r.y][r.x] += 1

    def _is_tree(self):
        # A cluster of robots has a large average neighbourhood size
        neighbours = [r.neighbourhood(self) for r in self.robots]
        self.av_neighbours = sum(neighbours)/len(neighbours)
        return self.av_neighbours

    def score(self):
        # Split into quadrants
        mid_w = Room.W//2
        mid_h = Room.H//2
        print(mid_w, mid_h)

        top_left, top_right, btm_left, btm_right = 0, 0, 0, 0
        for r in self.robots:
            if r.x < mid_w and r.y < mid_h:
                top_left += 1
            elif r.x > mid_w and r.y < mid_h:
                top_right += 1
            elif r.x < mid_w and r.y > mid_h:
                btm_left += 1
            elif r.x > mid_w and r.y > mid_h:
                btm_right += 1
        print(f"Quads are tl={top_left}, tr={top_right}, "
              f"bl={btm_left}, br={btm_right}")
        return top_left * top_right * btm_left * btm_right

    def __str__(self):
        # Turn all 0s into "."
        return "\n".join(
                ["".join(
                    [str(i) if i > 0 else "." for i in row]) for row in self.grid])
    def __repr__(self):
        return self.__str__()

#with open("d14_test.txt", "r") as f:
with open("d14_input.txt", "r") as f:
    lines = f.readlines()

robots = [Robot(line) for line in lines]
print("\n".join([str(r) for r in robots]))
room = Room(robots)
spots = []
for i in range(10000):
    # Max is [[8053, 33.928]]
    if i == 8053:
        print(room)
        print(f"Step {i}", room.score())
        time.sleep(1)
        break
    spots.append([i, room._is_tree()])
    room.advance()
max_spots = max([s[1] for s in spots])
it = [s for s in spots if s[1] == max_spots]
print(f"Max neighbourhood is {it}")
