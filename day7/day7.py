def flatten(list_of_lists):
    new_list = []
    _ = [new_list.extend(l) for l in list_of_lists]
    return new_list

def flatten_all(list_of_n):
    new_list = list_of_n
    while isinstance(new_list[0], list):
        new_list = flatten(new_list)
    return new_list

class Node:
    def __init__(self, v, orig_val, parent, op):
        self.v = v
        self.add = None
        self.mul = None
        self.cat = None

        self.orig = orig_val
        self.parent = parent
        self.parent_op = op

    def children(self):
        if self.add:
            return [self.add, self.mul, self.cat]
        return None

    def __str__(self):
        return f"[{self.add} ({self.v} / {self.orig}) {self.mul} {self.cat}]"

    def __repr__(self):
        return self.__str__()

class Tree:

    def __init__(self, v):
        self.root = Node(v, v, None, None)

    def find_depth(self, d):
        cur = [self.root]
        for i in range(d):
            children = [node.children() for node in cur]
            children = flatten_all(children)
            if None in children:
                return []
            cur = children
        return cur

    def __str__(self):
        s = ""
        cur = [self.root]
        while len(cur) > 0:
            s += "\n"
            s += "  ".join([f"{n.v}/{n.orig}" for n in cur])
            new_cur = []
            for n in cur:
                children = n.children()
                if children:
                    new_cur.extend(children)
            cur = new_cur
        return s

    def __repr__(self):
        return self.__str__()
            
def test_pair(a, b):
    return a+b, a*b


#with open("d7_test.txt", "r") as f:
with open("d7_input.txt", "r") as f:
    lines = f.readlines()

matches = []

for line in lines:
    tot, tail = line.strip().split(": ")
    tot = int(tot)
    tail = [int(t) for t in tail.split(" ")]
    print(tot, ":", tail)

    tree = Tree(tail[0])

    for d in range(1, len(tail)):
        # add and mul tail[d] to the leaf nodes
        nodes = tree.find_depth(d-1)
        for n in nodes:
            n.add = Node(n.v + tail[d], tail[d], n, "+")
            n.mul = Node(n.v * tail[d], tail[d], n, "*")
            n.cat = Node(int(f"{n.v}{tail[d]}"), tail[d], n, "||")
            #print(f"New values calculated are {n.add}, {n.mul}, {n.cat}")
        #print("Interim tree:", tree)

    #print(f"Final tree for this line: {tree}")

    # Do any of the leaves match the total?
    leaves = tree.find_depth(len(tail)-1)
    match = [n for n in leaves if n.v == tot]
    if len(match) > 0:
        rev = []
        cur = match[0]
        while cur.parent:
            rev.extend([str(cur.orig), cur.parent_op])
            cur = cur.parent
        rev.append(str(tree.root.orig))
        #print(" ".join(rev[::-1]))

        matches.append(tot)

print(f"In total, we have {len(matches)} matches")
print(f"This sums to {sum(matches)}")
