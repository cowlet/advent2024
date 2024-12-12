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

def apply_rules(stone):
    if stone.value_i == 0:
        yield create_stone(1)
    elif stone.even_dig:
        yield create_stone(stone.value_s[:stone.mid])
        yield create_stone(stone.value_s[stone.mid:])
    else:
        yield create_stone(stone.value_i * 2024)


with open("d11_input.txt", "r") as f:
#with open("d11_test.txt", "r") as f:
    line = f.read().strip()

BLINKS = 75

stones = [create_stone(int(v)) for v in line.split(" ")]
counts = {}
for stone in stones:
    try:
        counts[stone.value_i] += 1
    except KeyError:
        counts[stone.value_i] = 1


for b in range(BLINKS):
    new_counts = {}
    for stone_v in counts:
        blink = apply_rules(create_stone(stone_v))
        for output_stone in blink:
            try:
                new_counts[output_stone.value_i] += (1*counts[stone_v])
            except KeyError:
                new_counts[output_stone.value_i] = (1*counts[stone_v])
    counts = new_counts

total = sum(counts.values())

print(f"{len(stones)} stones turns into {total} stones after {BLINKS} blinks")

