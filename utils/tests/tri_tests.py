import sys
sys.path.append("..")

from tri import Tri
t = Tri()

names = [
    "The Walrus",
    "Rio Grande",
    "The West End Tavern",
    "License No 1",
]

for n in names:
    t.insert(n)

print(t.lookup("Th"))
print(t.lookup("th"))
print(t.lookup("wal"))
print(t.lookup("x"))
print(t.lookup("west en"))
