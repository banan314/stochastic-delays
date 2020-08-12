from delay.matrix.Path import Path

p1 = Path(1, [1, -1])
p2 = Path(1, [1, 1])
print(p1, '←', p2)
print(Path.checkAccordance(p1, p2))

print(p1.previous())
print(p2.previous())
print(p1.path)
