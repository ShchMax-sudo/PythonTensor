class Tensor():
    t = 0
    sz_one = 0
    sz = 0

    def deepcopy(self, a):
        if (isinstance(a, list)):
            return a
        else:
            b = []
            for v in a:
                b.append(self.deepcopy(v))
            return b

    def is_num(self, a):
        return isinstance(a, int) or isinstance(a, float)

    def generate_permutations(self, sz, sz_one):
        ans = []
        for i in range(sz_one ** sz):
            now = []
            for j in range(sz):
                now.append(i % sz_one)
                i //= sz_one
                ans.append(now)
        return ans

    def make_blanc_tensor_array(self, sz, sz_one):
        if (sz == 0):
            return 0
        else:
            ans = []
            for i in range(sz_one):
                ans.append(self.make_blanc_tensor_array(sz - 1, sz_one))
            return ans

    def get(self, al):
        g = self.t
        for i in al:
            g = g[i]
        return g

    def set(self, al, val):
        g = self.t
        for i in al[:-1]:
            g = g[i]
        if (len(al) != 0):
            g[al[-1]] = val
        else:
            self.t = val

    def __init__(self, *args):
        if (len(args) == 0):
            self.t = 0
            self.sz = 0
            self.sz_one = 0
        elif (len(args) == 1):
            other = args[0]
            if (isinstance(other, Tensor)):
                self.t = self.deepcopy(other.t)
            elif (isinstance(other, list) or self.is_num(other)):
                self.t = other
            else:
                raise TypeError("Unknown type of tensor initializer")
            self.sz = 0
            self.sz_one = 0
            if (not self.is_num(self.t)):
                self.sz_one = len(self.t)
            g = self.t
            while (isinstance(g, list)):
                self.sz -= -1
                g = g[0]
        elif (len(args) == 2):
            self.sz = args[0]
            self.sz_one = args[1]
            self.t = self.make_blanc_tensor_array(self.sz, self.sz_one)

    def __add__(self, other):
        ans = Tensor(self)
        if (self.sz_one != other.sz_one):
            return TypeError("Incorrect size of tensors")
        if (self.sz != other.sz):
            return TypeError("Incorrect dimension count of tensors")
        for perm in self.generate_permutations(self.sz, self.sz_one):
            ans.set(perm, self.get(perm) + other.get(perm))
        return ans

    def __mul__(self, a):
        if (self.is_num(a)):
            ans = Tensor(self)
            for perm in self.generate_permutations(self.sz, self.sz_one):
                ans.set(perm, self.get(perm) * a)
            return ans
        elif (type(a) == type(self)):
            other = a
            if (self.sz_one != other.sz_one):
                raise TypeError("Incorrect size of tensors")
            ans = Tensor(self.sz + other.sz, self.sz_one)
            as_ = self.generate_permutations(self.sz, self.sz_one)
            bs_ = self.generate_permutations(other.sz, other.sz_one)
            for i in as_:
                for j in bs_:
                    ans.set(i + j, self.get(i) * other.get(j))
            return ans

    def __sub__(self, other):
        return a + b * -1
