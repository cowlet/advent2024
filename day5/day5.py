from copy import deepcopy

with open("d5_input.txt", "r") as f:
    lines = f.readlines()

rule_lines = [line for line in lines if "|" in line]
page_lines = [line for line in lines if "," in line]

fwd_rules = {}
bck_rules = {}
for line in rule_lines:
    parts = line.strip().split("|")
    parts = [int(part) for part in parts]
    try:
        fwd_rules[parts[0]].append(parts[1])
    except KeyError:
        fwd_rules[parts[0]] = [parts[1]]
    try:
        bck_rules[parts[1]].append(parts[0])
    except KeyError:
        bck_rules[parts[1]] = [parts[0]]

#print(fwd_rules)
#print(bck_rules)

def validate_pages(pages):
    for i, p in enumerate(pages):
        # Do all subsequent pages validate?
        tail = pages[i+1:]
        for t in tail:
            # There must be a constraint on p and t for us to care
            if p in fwd_rules and t in bck_rules:
                if t not in fwd_rules[p]:
                    #print(f"*** Violation of rule {p}|{t}! {t} is not in {fwd_rules[p]}")
                    return False
        # Do all previous pages validate?
        head = pages[:i]
        for h in head:
            # Violation if p|h is a rule, because h comes before p
            if p in fwd_rules and h in bck_rules:
                if h in fwd_rules[p]:
                    #print(f"*** Violation of rule {p}|{h}! {h} is in {fwd_rules[p]} but comes before {p}")
                    return False
    # If we get here, all pages in this list meet the rules
    return True


total = 0
to_fix = []
for i, line in enumerate(page_lines):
    pages = [int(p) for p in line.strip().split(",")]
    if validate_pages(pages):
        # Find middle
        m = len(pages)//2
        total += pages[m]
    else:
        to_fix.append(pages)

print(f"Total validating page sum is {total}")

print(len(to_fix))

def reorder(pages):
    update = []
    for p in pages:
        for i in range(len(update)):
            #print("**", i, p, "->", update, "**")
            tmp = deepcopy(update)
            tmp.insert(i, p)
            if validate_pages(tmp):
                update.insert(i, p) # Add it for real
        if p not in update:
            update.append(p) # Add it to the end
    print(f"{update}: Does it finally validate? {validate_pages(update)}")
    return update

update_total = 0
for pages in to_fix:
    update = reorder(pages)
    # Find middle
    m = len(update)//2
    update_total += update[m]

print(f"Total fixed page sum is {update_total}")
