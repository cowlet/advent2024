class Stone:
    def __init__(self, value):
        self.value_i = int(value)
        self.value_s = str(self.value_i) # Cut leading zeros
        self.digs = len(self.value_s)
        self.even_dig = self.digs % 2 == 0
        self.mid = self.digs // 2
    def __str__(self):
        return self.value_s
    def __repr__(self):
        return self.__str__()


cache = {}
def create_stone(i):
    i = int(i)
    try:
        return cache[i]
    except KeyError:
        cache[i] = Stone(i)
        return cache[i]

def apply_rules(stones):
    # How many will split?
    dups = [i for i, s in enumerate(stones) if s.even_dig]
    result = [None] * (len(stones) + len(dups))
    #print(f"Preallocating {len(stones) + len(dups)} spaces")
    idx = 0
    for stone in stones:
        if stone.value_i == 0:
            result[idx] = create_stone(1)
            idx += 1
        elif stone.even_dig:
            #print(f"* Even number of digits: {stone}")
            result[idx] = create_stone(stone.value_s[:stone.mid])
            result[idx+1] = create_stone(stone.value_s[stone.mid:])
            idx += 2
        else:
            result[idx] = create_stone(stone.value_i * 2024)
            idx += 1
    return result

def count(stones):
    if not isinstance(stones, list):
        return 1
    return sum([count(s) for s in stones])

with open("d11_input.txt", "r") as f:
#with open("d11_test.txt", "r") as f:
    line = f.read().strip()

stones = [create_stone(int(v)) for v in line.split(" ")]
b = 75

end = []
for stone in stones:
    print(f"*** Starting new stone {stone}")
    results = [stone]
    for i in range(b):
        if i%5 == 0:
            print(f"* {i} *")
        #print(f"Input: {results}")
        results = apply_rules(results)
        #print(f"Output: {results}")
    end.append(count(results))

print(f"{len(stones)} stones turns into {sum(end)} stones after {b} blinks")
print(end)

