class Machine:
    def __init__(self, line_a, line_b, line_p):
        eq_a = line_a[10:].strip().split(", ")
        self.ax = int(eq_a[0].split("+")[1])
        self.ay = int(eq_a[1].split("+")[1])
        self.ac = 3

        eq_b = line_b[10:].strip().split(", ")
        self.bx = int(eq_b[0].split("+")[1])
        self.by = int(eq_b[1].split("+")[1])
        self.bc = 1

        prize = line_p[7:].strip().split(", ")
        self.px = int(prize[0].split("=")[1])
        self.py = int(prize[1].split("=")[1])

    def __str__(self):
        return f"A: x+{self.ax}, y+{self.ay}, B: x+{self.bx}, y+{self.by}: " +\
               f"Prize: x={self.px}, y={self.py}"
    def __repr__(self):
        return self.__str__()

    def solve(self):
        # p = m*a + n*b; m and n must be whole numbers
        # min(3m + 1n); cost must be minimized

        # 8400 = 94m + 22n
        # 5400 = 34m + 67n
        # 94m + 22n - 8400 = 34m + 67n - 5400
        # (67 - 22)n = (94 - 34)m - (8400 + 5400)
        # 45n = 60m - 3000
        # n = (60/45)m - 3000/45
        #
        # a costs 3 and b costs 1
        # so m = 3n
        #
        # n = (60/45)3n - 3000/45
        # 3(60/45)n - n = 3000/45
        # (180/45 - 1)n = 3000/45
        # n = 3000/45 / (180/45 - 1)
        #   = 3000 / (45 * (180/45 - 1))
        #   = 3000 / (180 - 45)
        #m_scale = 3 # m == 3n
        #n = (self.px-self.py) / \
        #        (m_scale*(self.ax-self.ay) - (self.by-self.bx)) 
        #m = m_scale * n

        #print(f"n = {n}, m = {m}")
        # If negative, there's no solution
        #if n < 0:
        #    return False, 0, 0

        #print(f"self.px = m * self.ax + n * self.bx")
        #print(f"{self.px} = {m} * {self.ax} + {n} * {self.bx}")
        #print(f"{m * self.ax} + {n * self.bx}")
        #print(f"{m * self.ax + n * self.bx}")

        #print(f"self.py = m * self.ay + n * self.by")
        #print(f"{self.py} = {m} * {self.ay} + {n} * {self.by}")
        #print(f"{m * self.ay} + {n * self.by}")
        #print(f"{m * self.ay + n * self.by}")
        valids = []
        for i in range(100):
            for j in range(100):
                # Do we get whole numbers?
                if i*self.ax + j*self.bx == self.px and \
                        i*self.ay + j*self.by == self.py:
                    valids.append([i, j, 3*i+j])
        #print(f"Valid pairs are: {valids}")
        if len(valids) < 1:
            return None

        # If there are multiple, which is the cheapest?
        min_cost = min([v[2] for v in valids])
        for v in valids:
            if v[2] == min_cost:
                return v

with open("d13_input.txt", "r") as f:
#with open("d13_test.txt", "r") as f:
    lines = f.readlines()

results = []
for i in range(0, len(lines), 4):
    m = Machine(lines[i], lines[i+1], lines[i+2])
    #print(m)
    result = m.solve()
    if result:
        print(f"Machine {i//4}: {result[0]} As and {result[1]} Bs")
        results.append(result[2])

print(f"In total {len(results)} prizes, costing {sum(results)}")
