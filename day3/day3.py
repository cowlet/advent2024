
#with open("d3_test2.txt", "r") as f:
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
    mul = "mul("
    stride = len(mul)
    if text[i:i+stride] != mul:
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


def look_for_validity(i, mul_on):
    if mul_on:
        # Are we turning it off?
        off = "don't()"
        if text[i:i+len(off)] == off:
            return False, (0, 0, i+len(off), False) # skip the off chars
        return True, look_for_mul(i) # Otherwise mul is still on, and look for it
    # It's off, are we turning it on?
    on = "do()"
    if text[i:i+len(on)] == on:
        return True, look_for_mul(i+len(on)) # Turn mul on, skip the on chars, look for it
    return False, (0, 0, i, False) # Still off, keep going

i = 0
stack = []
mul_on = True
while i < len(text):
    mul_on, (a, b, i, success) = look_for_validity(i, mul_on)
    if success:
        print(a, b, i, success)
        stack.append(a*b)
    i += 1

print(f"Total is {sum(stack)}. (Stack contains {len(stack)} valid muls)")
