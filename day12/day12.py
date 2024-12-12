class Plot:
    def __init__(self, i, j):
        self.i, self.j = i, j
        self.crop = FIELD[i][j]
        self.neighbours = []
    def __str__(self):
        return f"({self.i}, {self.j})"
    def __repr__(self):
        return self.__str__()

    def isneighbour(self, other):
        if (self.i == other.i and self.j == other.j-1) or \
           (self.i == other.i and self.j == other.j+1) or \
           (self.i == other.i-1 and self.j == other.j) or \
           (self.i == other.i+1 and self.j == other.j):
            return True
        return False

    def find_neighbours(self, plots):
        self.right, self.left, self.up, self.down = None, None, None, None
        for p in plots:
            if p.i == self.i and p.j == self.j-1:
                self.left = p
            elif p.i == self.i and p.j == self.j+1:
                self.right = p
            elif p.i == self.i-1 and p.j == self.j:
                self.up = p
            elif p.i == self.i+1 and p.j == self.j:
                self.down = p

        self._l_fence = (not self.left)
        self._r_fence = (not self.right)
        self._t_fence = (not self.up)
        self._b_fence = (not self.down)


class Region:
    def __init__(self, plots):
        self.plots = plots

        self.area = len(self.plots)
        self.perimeter = 0
        for plot in self.plots:
            neighbours = sum([1 for o in self.plots if plot.isneighbour(o)])
            self.perimeter += (4-neighbours)
            #print(f"Plot {plot} has {neighbours} neighbours, therefore {4-neighbours} fences")

        # Make connections
        for plot in self.plots:
            plot.find_neighbours(self.plots)

        # How many top fences do we have?
        tops = [p for p in plots if p._t_fence]
        btms = [p for p in plots if p._b_fence]
        ls = [p for p in plots if p._l_fence]
        rs = [p for p in plots if p._r_fence]

        def find_discontinuities(container):
            count = 0
            for i, js in container.items():
                count += 1 # must be at least one
                if len(js) == 1:
                    continue
                vals = sorted(js)
                for idx, v in enumerate(vals[:-1]):
                    # discontinuities?
                    if v+1 != vals[idx+1]:
                        count += 1
            return count

        def collect_rows(fences):
            rows = {}
            for f in fences:
                try:
                    rows[f.i].append(f.j)
                except KeyError:
                    rows[f.i] = [f.j]
            return rows

        def collect_cols(fences):
            cols = {}
            for f in fences:
                try:
                    cols[f.j].append(f.i)
                except KeyError:
                    cols[f.j] = [f.i]
            return cols

        # Tops on the same row don't count, unless there's a discontinuity
        rows = collect_rows(tops)
        top_sides = find_discontinuities(rows)
        #print(f"Top sides: {top_sides}")
        rows = collect_rows(btms)
        btm_sides = find_discontinuities(rows)
        #print(f"Btm sides: {btm_sides}")
        cols = collect_cols(ls)
        l_sides = find_discontinuities(cols)
        #print(f"Left sides: {l_sides}")
        cols = collect_cols(rs)
        r_sides = find_discontinuities(cols)
        #print(f"Right sides: {r_sides}")

        self.sides = top_sides + btm_sides + l_sides + r_sides


    def __str__(self):
        return "; ".join([str(p) for p in self.plots])
    def __repr__(self):
        return self.__str__()
    def price(self):
        #return self.area * self.perimeter
        return self.area * self.sides


def find_first_neighbour(source, region):
    # Are any plots in source neighbours of region?
    for p1 in source:
        for p2 in region:
            if p1.isneighbour(p2):
                return p1
    return None

def find_contiguous(plots):
    if len(plots) < 2:
        return plots
    regions = []
    cur, unallocated = plots[0], plots[1:]
    while cur:
        new_region = [cur]
        # Find anything in unallocated that is a neighbour
        neighbour = find_first_neighbour(unallocated, new_region)
        while neighbour:
            # Move neighbour from unallocated to new_region
            new_region.append(neighbour)
            unallocated.remove(neighbour)
            #print(f"{neighbour} is neighbour of {new_region}. Unall is {unallocated}")
            neighbour = find_first_neighbour(unallocated, new_region)

        #print(f"After checking all unall, new_region is {new_region}, unall is {unallocated}")
        regions.append(new_region)

        if len(unallocated) == 0:
            return regions
        if len(unallocated) == 1:
            regions.append(unallocated)
            return regions
        cur, unallocated = unallocated[0], unallocated[1:]
    raise ValueError("Don't think we should get here")




with open("d12_input.txt", "r") as f:
#with open("d12_test.txt", "r") as f:
    lines = f.readlines()
FIELD = [line.strip() for line in lines]
ROWS = len(FIELD)
COLS = len(FIELD[0])

# Convert squares into Plots
crop_plots = {}
for i in range(ROWS):
    for j in range(COLS):
        try:
            crop_plots[FIELD[i][j]].append(Plot(i, j))
        except KeyError:
            crop_plots[FIELD[i][j]] = [Plot(i, j)]

print(f"There are {len(crop_plots)} crops")

# Convert Plots into Regions
crop_regions = {}
for crop in crop_plots:
    crop_regions[crop] = [Region(plots) for plots in find_contiguous(crop_plots[crop])]
    print(f"For crop {crop}: {len(crop_regions[crop])} regions")
    #print(crop_regions[crop])

# Calculate prices
prices = []
for crop in crop_regions:
    regions = crop_regions[crop]
    for region in regions:
        prices.append(region.price())
        #print(f"Price {prices[-1]} for region {region}")

print(f"Total price of all crops is {sum(prices)}")

