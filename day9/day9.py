class Disk:

    def __init__(self, string):
        self.blocks = []

        file_id = 0
        file_next = True
        for ch in string:
            size = int(ch)
            if file_next:
                self.blocks.extend([str(file_id)] * size)
                file_id += 1
                file_next = False
            else:
                self.blocks.extend(["."] * size)
                file_next = True

    def __str__(self):
        return "".join(self.blocks)
    def __repr__(self):
        return self.__str__()

    def trim(self):
        while self.blocks[-1] == ".":
            self.blocks = self.blocks[:-1]

    def get_files(self):
        # Return a list of all files, giving their fid and indexes
        files = []
        i = 0
        while i < len(self.blocks):
            if self.blocks[i] == ".":
                i += 1
                continue
            fid = self.blocks[i]
            idxes = []
            for j in range(i, len(self.blocks)):
                if self.blocks[j] == fid:
                    idxes.append(j)
                else:
                    break # First change in char is the end of this file
            files.append([fid, idxes])
            i += len(idxes)
        return files

    def compress(self):
        files = self.get_files() # Get these only once, for the initial order
        for fid, idxes in files[::-1]: # Take once only in reverse order
            size = len(idxes)
            for j, ch in enumerate(self.blocks):
                # If it's not free, keep looking
                if ch != ".":
                    continue
                # If we've gone past the first index, there's nothing more compact
                if j >= idxes[0]:
                    print(f"Didn't find a block of size {size} for file {fid}")
                    break # Move onto the next fid
                # Are there enough dots in a run for the full file?
                if all([self.blocks[n]=="." for n in range(j, j+size) if n < len(self.blocks)]):
                    print(f"Found block of {size} free space at, writing to [{j}:{j+size}]")
                    self.blocks[j:j+size] = self.blocks[idxes[0]:idxes[-1]+1]
                    self.blocks[idxes[0]:idxes[-1]+1] = ["."]*size
                    self.trim()
                    #print(f"Blocks is now {self}")
                    break # Move onto the next fid

    def checksum(self):
        return sum([i*int(fid) for i, fid in enumerate(self.blocks) if fid != "."])



#with open("d9_test.txt", "r") as f:
with open("d9_input.txt", "r") as f:
    lines = f.readlines()

line = lines[0].strip()
d = Disk(line)
print(f"Length of input is {len(line)}, data structure is {len(d.blocks)}")
print(d)

d.compress()
print(d)

print(f"Final checksum is {d.checksum()}")
