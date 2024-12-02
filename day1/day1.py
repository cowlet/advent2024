import pandas as pd

df = pd.read_csv("day1_input.txt", sep="   ", header=None)

df = pd.DataFrame(data={0: df.sort_values(by=0)[0].tolist(),
                        1: df.sort_values(by=1)[1].tolist()})
df["diff"] = df[1]-df[0]
print(df.head())

print(f"Total distance is: {df['diff'].sum()}")
print(f"Total abs distance is: {df['diff'].abs().sum()}")

sim = lambda v, ser: v * (v==ser).sum()

df["sim"] = df[0].apply(sim, args=(df[1],))
print(df.head())

print(f"Total similarity is: {df['sim'].sum()}")
