def deepcopy(a):
    if (type(a) != type([])):
        return a
    else:
        b = []
        for v in a:
            b.append(deepcopy(v))
        return b

def is_num(a):
    return type(a) == type(0) or type(a) == type(0.0)

def generate_permutations(sz, sz_one):
    ans = []
    for i in range(sz ** sz_one):
        now = []
        for j in range(sz):
            now.append(i % sz_one)
            i //= sz_one
        ans.append(now)
    return ans

class Tensor():
    t = 0
    sz_one = 0
    sz = 0

    def get(self, al):
        g = self.t
        for i in al:
            g = g[i]
        return g

    def set(self, al, val):
        g = self.t
        for i in al[:-1]:
            g = g[i]
        g[al[-1]] = val

    def __init__(self, other):
        if (type(other) == type(self)):
            self.t = deepcopy(other.t)
        elif (type(other) == type([]) or is_num(other)):
            self.t = other
        else:
            raise TypeError("Unknown type of tensor initializer")
        self.sz = 0
        self.sz_one = 0
        if (not is_num(other)):
            self.sz_one = len(self.t[0])
        g = self.t
        while (type(g) == type([])):
            self.sz-=-1
            g = g[0]

    def __add__(self, other):
        ans = Tensor(self)
        if (self.sz != other.sz or self.sz_one != other.sz_one):
            return TypeError("Uncorrect size if tensors")
        for perm in generate_permutations(self.sz, self.sz_one):
            ans.set(perm, self.get(perm) + other.get(perm))
        return ans

    def __mult__(self, a):
        ans = Tensor(self)
        for perm in generate_permutations(self.sz, self.sz_one):
            ans.set(perm, self.get(perm) * a)
        return ans
