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

def count(stones):
    if not isinstance(stones, list):
        return 1
    return sum([count(s) for s in stones])



with open("d11_input.txt", "r") as f:
#with open("d11_test.txt", "r") as f:
    line = f.read().strip()

stones = [create_stone(int(v)) for v in line.split(" ")]
BLINKS = 75

def pursue_stone(stone, blinks=0):
    if blinks >= BLINKS:
        raise ValueError(f"Pursuing {blinks} blinks")
    #if blinks%5 == 0:
    #    print(f"* {blinks} *")
    stored = [] # If it's our last blink, store these values
    blink = apply_rules(stone)
    for output_stone in blink:
        if blinks == BLINKS-1:
            stored.append(output_stone)
        else:
            stored.append(pursue_stone(output_stone, blinks=blinks+1))
    return stored


end = []
for stone in stones:
    print(f"*** Starting new stone {stone}")
    final = pursue_stone(stone)
    #print(f"Final output for stone {stone} is {final}")
    end.append(count(final))

print(f"{len(stones)} stones turns into {sum(end)} stones after {BLINKS} blinks")
#print(end)

