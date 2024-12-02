import pandas as pd

df = pd.read_csv("d2_data.txt", sep=" ", header=None)
cols = df.columns

def monotonic(row):
    row = row.dropna()
    diffs = [row[i]-row[i+1] for i in range(len(row)-1)]
    direction = [d>0 for d in diffs]
    change = [d!=0 for d in diffs]
    return all(change) and (all(direction) or not any(direction))

df["max diff"] = df[cols].apply(lambda row: max([abs(row[i]-row[i+1]) for i in range(len(row)-1)]), axis=1)
df["monotonic"] = df[cols].apply(monotonic, axis=1)

df["safe"] = (df["max diff"]>=1)&(df["max diff"]<=3)&df["monotonic"]
print(df.head(8))

print(f"{df['safe'].sum()} reports are safe (of {df.shape[0]})")
