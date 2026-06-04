import pickle

with open("vectors.pkl", "rb") as f:
    data = pickle.load(f)

chunks = data["chunks"]

print("Number of chunks:", len(chunks))
print("\nFirst chunk preview:\n", chunks[0][:500])
