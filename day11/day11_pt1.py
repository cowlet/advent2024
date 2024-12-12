def apply_rules(stones):
    result = []
    for stone in stones:
        s = str(stone)
        if stone == 0:
            result.append(1)
        elif len(s) % 2 == 0:
            #print(f"* Even number of digits: {stone}")
            mid = len(s)//2
            result.extend([int(s[:mid]), int(s[mid:])])
        else:
            result.append(stone * 2024)
    return result

def flatten(list_of_lists):
    result = []
    for l in list_of_lists:
        result.extend(l)
    return result

def count(stones):
    if not isinstance(stones, list):
        return 1
    return sum([count(s) for s in stones])

with open("d11_input.txt", "r") as f:
#with open("d11_test.txt", "r") as f:
    line = f.read().strip()

stones = [int(v) for v in line.split(" ")]
print(f"Starting with {len(stones)} stones: {stones}")

for i in range(75):
    stones = apply_rules(stones)
    print(f"After blink {i+1}: {count(stones)} stones")
    

