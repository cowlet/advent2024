
with open("d2_data.txt", "r") as f:
    lines = f.readlines()

data = [[int(chunk) for chunk in line.split()] for line in lines]

def monotonic(row):
    diffs = [row[i]-row[i+1] for i in range(len(row)-1)]
    direction = [d>0 for d in diffs]
    change = [d!=0 for d in diffs]
    return all(change) and (all(direction) or not any(direction))

def test_numbers(row):
    max_diff = max([abs(row[i]-row[i+1]) for i in range(len(row)-1)])
    if max_diff >= 1 and max_diff <= 3 and monotonic(row):
        return True

def test_row(row):
    # If it's fine as is, great!
    if test_numbers(row):
        return True
    # Otherwise, try leaving one out
    for i in range(len(row)):
        subrow = row[:i] + row[i+1:]
        if test_numbers(subrow):
            return True
    return False


safe = [test_row(row) for row in data]
print("\n".join([f"{a}: {b}" for a, b in list(zip(data, safe))[:8]]))

print(f"{sum(safe)} reports are safe (of {len(safe)})")
