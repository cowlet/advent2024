import math

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

        # 8400 = 94m + 22n    (1)
        # 5400 = 34m + 67n    (2)
        # 94m + 22n - 8400 = 34m + 67n - 5400
        # (67 - 22)n = (94 - 34)m - (8400 + 5400)
        # 45n = 60m - 3000
        # n = (60/45)m - 3000/45
        #
        # 8400 = 94m + 22[ m*60/45 - 3000/45 ]
        #      = 94m + m*1320/45 - 66000/45
        #      = m*(94 + 1320/45) - 66000/45
        # m = 8400/(94 + 1320/45) + 66000/[45*(94 + 1320/45)]
        # m = 8400/(94 + 1320/45) + 66000/[45*94 + 1320)]
        # m = 8400/123.333 + 66000/5550
        #   = 80

        a_diff = self.ax - self.ay # 60
        b_diff = self.by - self.bx # opposite dir to a_diff: 45
        p_diff = self.px - self.py # same dir as a_diff: 3000
        try:
            # Eqn 1
            m = self.px /(self.ax + self.bx*a_diff/b_diff) + \
                    self.bx*p_diff/(b_diff*self.ax + self.bx*a_diff)

            # Make sure we're on an int boundary
            if math.isclose(m, round(m)):
                m = round(m)

            n = m*a_diff/b_diff - p_diff/b_diff
            if math.isclose(n, round(n)):
                n = round(n)
        except ZeroDivisionError:
            # b_diff is zero, so we have to calc n first
            # 8400 = 94m + 22n    (1)
            # (94 - 34)m = (67 - 22)n + (8400 + 5400)
            # 60m = 45n + 3000
            # m = n45/60 + 3000/60
            #
            # 8400 = 94[ n45/60 + 3000/60] + 22n
            # 8400 = [94*45/60 + 22]n + 94*3000/60
            # n = 8400/[94*45/60 + 22] + 94*3000/60
            print(self)
            print("-->", a_diff, b_diff, p_diff)
            n = self.px/(self.ax*b_diff/a_diff + self.bx) + self.ax*p_diff/a_diff
            print(n)
            if math.isclose(n, round(n)):
                n = round(n)

            m = n*b_diff/a_diff + p_diff/a_diff
            print(m)
            if math.isclose(m, round(m)):
                m = round(m)

        if not isinstance(m, int) or not isinstance(n, int):
            # Invalid
            return None

        #print(f"self.px = m * self.ax + n * self.bx")
        #print(f"{self.px} = {m} * {self.ax} + {n} * {self.bx}")
        #print(f"{m * self.ax} + {n * self.bx}")
        #print(f"{m * self.ax + n * self.bx}")

        #print(f"self.py = m * self.ay + n * self.by")
        #print(f"{self.py} = {m} * {self.ay} + {n} * {self.by}")
        #print(f"{m * self.ay} + {n * self.by}")
        #print(f"{m * self.ay + n * self.by}")
        cost = 3*m + n
        return [m, n, cost]

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
