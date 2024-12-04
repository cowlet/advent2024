
#with open("d3_test.txt", "r") as f:
with open("d3_input.txt", "r") as f:
    text = f.read()

print(len(text))


def find_digit(i):
    dig = ""
    for stride in range(3):
        if text[i+stride] in "01234567890":
            dig += text[i+stride]
        else:
            break
    print(f"Found int {dig} with stride {len(dig)}, i is {i}")
    if len(dig) > 0:
        return int(dig), i+len(dig), True
    return 0, i, False


def look_for_mul(i):
    stride = len("mul(")
    if text[i:i+stride] != "mul(":
        return 0, 0, i, False

    dig1, i, success = find_digit(i+stride)
    if not success:
        return 0, 0, i, False

    if text[i] != ",":
        return 0, 0, i-1, False # i-1 to look for a new mul()

    dig2, i, success = find_digit(i+1) # +1 for the comma
    if not success:
        return 0, 0, i, False

    if text[i] != ")":
        return 0, 0, i-1, False # i-1 to look for a new mul()

    return int(dig1), int(dig2), i, True


i = 0
stack = []
while i < len(text):
    a, b, i, success = look_for_mul(i)
    if success:
        print(a, b, i, success)
        stack.append(a*b)
    i += 1

print(f"Total is {sum(stack)}. (Stack contains {len(stack)} valid muls)")
