import copy
class Matrix:
    e = 1e-6

    def __init__(self, rows, cols, data):
        self.rows = rows
        self.cols = cols
        self.data = data

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.data[index][0]
        else:
            return self.data[index[0]][index[1]]

    def __setitem__(self, index, value):
        if isinstance(index, int):
            self.data[index][0] = value
        else:
            self.data[index[0]][index[1]] = value

    def __mul__(self, other):
        data = []
        if isinstance(other, Matrix):
            for r in range(self.rows):
                row = []
                for c in range(other.cols):
                    sum = 0
                    for k in range(0, self.cols):
                        sum += self.data[r][k] * other.data[k][c]
                    row.append(sum)
                data.append(row)
            return Matrix(self.rows, other.cols, data)

        else:
            for r in range(self.rows):
                row = []
                for c in range(self.cols):
                    row.append(self.data[r][c] * other)
                data.append(row)
            return Matrix(self.rows, self.cols, data)

    def copy(self):
        return Matrix(self.rows, self.cols, copy.deepcopy(self.data))

    def identity(n):
        rows = cols = n
        data = []
        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    row.append(1)
                else:
                    row.append(0)
            data.append(row)
        return Matrix(rows, cols, data)

    def swapRows(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def LUP(self):
        n = self.rows
        A = self
        P = Matrix.identity(n)

        for i in range(n - 1):
            pivot = i
            for j in range(i + 1, n):
                if abs(A[j, i]) > abs(A[pivot, i]):
                    pivot = j

            if abs(A[pivot, pivot]) < Matrix.e:
                print("Stožerni element je 0.")
                return P

            self.swapRows(pivot, i)
            P.swapRows(pivot, i)

            for j in range(i + 1, n):
                A[j, i] /= A[i, i]
                for k in range(i + 1, n):
                    A[j, k] -= A[i, k] * A[j, i]
        return P

    def zeros(rows, cols):
        data = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(0.0)
            data.append(row)
        return Matrix(rows, cols, data)

    def forwardSubstitution(A, b):
        n = A.rows
        y = b.copy()

        for i in range(n - 1):
            for j in range(i + 1, n):
                y[j] -= A[j, i] * y[i]
        return y

    def backwardSubstitution(A, b):
        n = A.rows
        y = b.copy()

        for i in range(n - 1, -1, -1):

            if abs(A[i, i]) < Matrix.e:
                print("Greška : dijeljenje s nulom.")
                return

            y[i] /= A[i, i]
            for j in range(0, i):
                y[j] -= A[j, i] * y[i]
        return y

    def inverse(self):
        n = self.rows
        A = self.copy()
        inv = self.copy()
        e = Matrix.zeros(n, 1)
        P = A.LUP()

        for i in range(n):
            e[i] = 1.0
            y = Matrix.forwardSubstitution(A, P * e)
            x = Matrix.backwardSubstitution(A, y)
            e[i] = 0.0

            for j in range(n):
                inv[j, i] = x[j]

        return inv
