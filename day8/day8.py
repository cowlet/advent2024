class Node:
    def __init__(self, i, j, freq):
        self.i, self.j = i, j
        self.freq = freq
    def __str__(self):
        return f"({self.i}, {self.j})"
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def antinodes(self, other):
        if self.freq != other.freq:
            return None

        t, b = (self, other) if self.i == min([self.i, other.i]) else (other, self)
        l, r = (self, other) if self.j == min([self.j, other.j]) else (other, self)

        antis = [self, other] # These also count!
        i_shift = b.i - t.i
        j_shift = r.j - l.j
        if t == l:
            # s.  or  o.
            # .o      .s
            # All those above
            new_i, new_j = t.i - i_shift, t.j - j_shift
            while new_i >= 0 and new_j >= 0:
                antis.append(Node(new_i, new_j, self.freq))
                new_i, new_j = new_i - i_shift, new_j - j_shift
            # All those below
            new_i, new_j = b.i + i_shift, b.j + j_shift
            while new_i < ROWS and new_j < COLS:
                antis.append(Node(new_i, new_j, self.freq))
                new_i, new_j = new_i + i_shift, new_j + j_shift
        else:
            # .s  or  .o
            # o.      s.
            # All those above
            new_i, new_j = t.i - i_shift, t.j + j_shift
            while new_i >= 0 and new_j < COLS:
                antis.append(Node(new_i, new_j, self.freq))
                new_i, new_j = new_i - i_shift, new_j + j_shift
            # All those below
            new_i, new_j = b.i + i_shift, b.j - j_shift
            while new_i < ROWS and new_j >= 0:
                antis.append(Node(new_i, new_j, self.freq))
                new_i, new_j = new_i + i_shift, new_j - j_shift

        return antis

    def all_antinodes(self, others):
        all_antis = []
        for other in others:
            antis = self.antinodes(other)
            all_antis.extend(antis)
        return all_antis


with open("d8_input.txt", "r") as f:
#with open("d8_test.txt", "r") as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]
ROWS = len(lines)
COLS = len(lines[0])

nodes = {}
for i, line in enumerate(lines):
    for j, ch in enumerate(line):
        if ch == ".":
            continue
        try:
            nodes[ch].append(Node(i, j, ch))
        except KeyError:
            nodes[ch] = [Node(i, j, ch)]

all_antis = []
for freq in nodes:
    # For each node of this freq in turn, find the antinodes
    # of it and every other later node in this freq's list
    for idx, n in enumerate(nodes[freq]):
        all_antis.extend(n.all_antinodes(nodes[freq][idx+1:]))
# Dups from multiple freqs
uniqs = []
for an in all_antis:
    if an not in uniqs:
        uniqs.append(an)
print(f"There are {len(uniqs)} antinodes ({len(all_antis)} with dups)")

