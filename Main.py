class Tensor():
    t = 0
    sz_one = 0
    sz = 0

    def deepcopy(self, a):
        """Creates a full copy of array reccurently"""
        if (not isinstance(a, list)):
            return a
        else:
            b = []
            for v in a:
                b.append(self.deepcopy(v))
            return b

    def is_num(self, a):
        """Checking, what a is a num"""
        return isinstance(a, int) or isinstance(a, float)

    def generate_permutations(self, sz, sz_one):
        """Generate tensor "indexes" by count of dimensions
        & size of dimension"""
        ans = []
        for i in range(sz_one ** sz):
            now = []
            for j in range(sz):
                now.append(i % sz_one)
                i //= sz_one
                ans.append(now)
        if (len(ans) == 0):
            ans.append([])
        return ans

    def make_blanc_tensor_array(self, sz, sz_one):
        """Creates clear tensor array of given dimensions count & size"""
        if (sz == 0):
            return 0
        else:
            ans = []
            for i in range(sz_one):
                ans.append(self.make_blanc_tensor_array(sz - 1, sz_one))
            return ans

    def get(self, al):
        """Returns value from tensor "index"""
        g = self.t
        for i in al:
            g = g[i]
        return g

    def set(self, al, val):
        """Sets value to tensor "index"""
        g = self.t
        for i in al[:-1]:
            g = g[i]
        if (len(al) != 0):
            g[al[-1]] = val
        else:
            self.t = val

    def __init__(self, *args):
        """
        Creates tensor by:

        1) Another tensor (full copy)
        2) Tensor array
        3) Nothing (creates 0)
        4) Dimensions count & size
        """
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
            if (self.sz == 0):
                self.sz_one = 0
            self.t = self.make_blanc_tensor_array(self.sz, self.sz_one)
        else:
            raise TypeError("Unkown type of tensor constructor")

    def __add__(self, other):
        """Tensor addition"""
        if (not isinstance(other, Tensor)):
            raise TypeError("Unknown type of second operand to addition")
        ans = Tensor(self)
        if (self.sz_one != other.sz_one):
            raise TypeError("Incorrect size of tensors")
        if (self.sz != other.sz):
            raise TypeError("Incorrect dimension count of tensors")
        for perm in self.generate_permutations(self.sz, self.sz_one):
            ans.set(perm, self.get(perm) + other.get(perm))
        return ans

    def __mul__(self, a):
        """
        Tensor multiplication by:

        1) Number
        2) Another tensor
        """
        if (self.is_num(a)):
            ans = Tensor(self)
            for perm in self.generate_permutations(self.sz, self.sz_one):
                ans.set(perm, self.get(perm) * a)
            return ans
        elif (isinstance(a, Tensor)):
            other = a
            if (self.is_num(self.t)):
                return other * self.t
            elif (self.is_num(other.t)):
                return self * other.t
            if (self.sz_one != other.sz_one):
                raise TypeError("Incorrect size of tensors")
            ans = Tensor(self.sz + other.sz, self.sz_one)
            as_ = self.generate_permutations(self.sz, self.sz_one)
            bs_ = self.generate_permutations(other.sz, other.sz_one)
            for i in as_:
                for j in bs_:
                    ans.set(i + j, self.get(i) * other.get(j))
            return ans
        else:
            raise TypeError("Unknown type of second operand to multiply")

    def __sub__(self, other):
        """Tensor substraction"""
        if (not isinstance(other, Tensor)):
            raise TypeError("Unknown type of second operand to substraction")
        return self + other * -1

    def get_convolution(self, g, a, b, v):
        """Returns one of tensor convolution summ"""
        if (not isinstance(g, list)):
            return g
        if (a == 0 or b == 0):
            return self.get_convolution(g[v], a - 1, b - 1, v)
        ans = []
        for i in range(self.sz_one):
            ans.append(self.get_convolution(g[i], a - 1, b - 1, v))
        return ans

    def convolution(self, a, b):
        """Tensor convolution by index a & b (numerating from 0)"""
        if (not self.is_num(a) or not self.is_num(b)):
            raise TypeError("Unknown type of index to convolution")
        elif (max(a, b) >= self.sz):
            raise TypeError("At least one of convolution index more than "
                            + "tensor dimentions sount")
        ans = Tensor(self.sz - 2, self.sz_one)
        for i in range(self.sz_one):
            ans = ans + Tensor(self.get_convolution(self.t, a, b, i))
        return ans


# Sample of square of norm of vector a in ortonormal bazis, ans other bazis
a = Tensor([1, 7, 9])
g = Tensor([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
])
A = Tensor([
    [1, 7, 9],
    [0, 5, 4],
    [3, 3, 7],
])
B = Tensor([
    [-23 / 28, 11 / 14, 17 / 28],
    [-3 / 7, 5 / 7, 1 / 7],
    [15 / 28, -9 / 14, -5 / 28],
])
g_ = ((g * B).convolution(0, 2) * B).convolution(0, 2)
a_ = (A * a).convolution(1, 2)
print(g_.t)
print(a_.t)
print(((g * a).convolution(0, 2) * a).convolution(0, 1).t)
print(((g_ * a_).convolution(0, 2) * a_).convolution(0, 1).t)
