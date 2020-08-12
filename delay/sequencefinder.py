def find(x, seq):
    res = 0
    for i in range(len(x) - len(seq) - 1):
        match = True
        for j in range(len(seq)):
            if x[i + j] != seq[j]:
                match = False
        if match:
            res += 1
    return res