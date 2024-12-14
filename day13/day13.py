import math
import numpy as np

class Machine:
    def __init__(self, line_a, line_b, line_p):
        eq_a = line_a[10:].strip().split(", ")
        ax = int(eq_a[0].split("+")[1])
        ay = int(eq_a[1].split("+")[1])
        ac = 3
        self.a = np.array([ax, ay, ac])

        eq_b = line_b[10:].strip().split(", ")
        bx = int(eq_b[0].split("+")[1])
        by = int(eq_b[1].split("+")[1])
        bc = 1
        self.b = np.array([bx, by, bc])

        # Pt 2: these have an offset
        offset = 10000000000000
        prize = line_p[7:].strip().split(", ")
        px = int(prize[0].split("=")[1]) + offset
        py = int(prize[1].split("=")[1]) + offset
        self.p = np.array([px, py])

    def __str__(self):
        return f"A: x+{self.a[0]}, y+{self.a[1]}, " +\
               f"B: x+{self.b[0]}, y+{self.b[1]}: " +\
               f"Prize: x={self.p[0]}, y={self.p[1]}"
    def __repr__(self):
        return self.__str__()

    def solve(self):
        # p = m*a + n*b; m and n must be whole numbers

        # 8400 = 94m + 22n    (1)
        # 5400 = 34m + 67n    (2)
        # 94m + 22n - 8400 = 34m + 67n - 5400
        # (67 - 22)n = (94 - 34)m - (8400 + 5400)
        # 45n = 60m - 3000
        # n = (60/45)m - 3000/45

        a_diff = self.a[0] - self.a[1] # 60
        b_diff = self.b[1] - self.b[0] # opposite dir to a_diff: 45
        p_diff = self.p[0] - self.p[1] # same dir as a_diff: 3000
        if b_diff != 0:
            # Eqn 1
            m = self.p[0] /(self.a[0] + self.b[0]*a_diff/b_diff) + \
                    self.b[0]*p_diff/(b_diff*self.a[0] + self.b[0]*a_diff)
            # Make sure we're on an int boundary
            if np.isclose(round(m), m, rtol=1e-15):
                m = round(m)

            n = m*a_diff/b_diff - p_diff/b_diff
            if np.isclose(round(n), n, rtol=1e-15):
                n = round(n)
        else:
            # b_diff is zero, so the equation for m simplifies
            # m = n*b_diff/a_diff + p_diff/a_diff
            #   = 0 + p_diff/a_diff
            m = p_diff/a_diff
            if np.isclose(round(m), m, rtol=1e-15):
                m = round(m)

            # Now n
            # 8400 = 94m + 22n    (1)
            # n = (8400 - 94m)/22
            n = (self.p[0] - self.a[0]*m) / self.b[0]
            if np.isclose(round(n), n, rtol=1e-15):
                n = round(n)

        if not isinstance(m, int) or not isinstance(n, int):
            # Invalid
            return None

        cost = 3*m + n
        return [m, n, cost]

with open("d13_input.txt", "r") as f:
#with open("d13_test.txt", "r") as f:
    lines = f.readlines()

results = []
for i in range(0, len(lines), 4):
    m = Machine(lines[i], lines[i+1], lines[i+2])
    result = m.solve()
    if result:
        print(f"Machine {i//4}: {result[0]} As and {result[1]} Bs")
        results.append(result[2])

print(f"In total {len(results)} prizes, costing {sum(results)}")
