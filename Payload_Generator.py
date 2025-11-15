import os

filename = "payload.txt"

# Create the file if it doesn't exist
if not os.path.exists(filename):
    open(filename, "w").close()

# Write a-z and 0-9 each on a new line
with open(filename, "w") as f:
    # a-z
    for c in range(ord('a'), ord('z') + 1):
        f.write(chr(c) + "\n")
    
    # 0-9
    for n in range(10):
        f.write(str(n) + "\n")

print("payload.txt generated successfully!")
