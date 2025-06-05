def read_matrix(filename):
    with open(filename, 'r') as file:
        return [list(map(int, line.split())) for line in file]


def print_matrix(matrix, name):
    print(f"\n{name}:")
    for row in matrix:
        print(" ".join(f"{x:4}" for x in row))


def get_regions(n):
    r1, r2, r3, r4 = [], [], [], []
    for i in range(n):
        for j in range(n):
            if i < j and i + j < n - 1:
                r1.append((i, j))
            elif i < j and i + j > n - 1:
                r2.append((i, j))
            elif i > j and i + j > n - 1:
                r3.append((i, j))
            elif i > j and i + j < n - 1:
                r4.append((i, j))
    return r1, r2, r3, r4


def swap_symmetric(F, region1, region2):
    for (i1, j1), (i2, j2) in zip(region1, region2):
        F[i1][j1], F[i2][j2] = F[i2][j2], F[i1][j1]
    return F


def swap_asymmetric(F, region1, region3):
    for (i1, j1), (i2, j2) in zip(region1, region3):
        F[i1][j1], F[i2][j2] = F[i2][j2], F[i1][j1]
    return F


def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix))]


def multiply_matrices(A, B):
    n = len(A)а
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def scalar_multiply(K, M):
    return [[K * M[i][j] for j in range(len(M))] for i in range(len(M))]


def add_matrices(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A))] for i in range(len(A))]


def build_F(A):
    n = len(A)
    F = [row[:] for row in A]
    r1, r2, r3, r4 = get_regions(n)

    zeros_r1 = sum(1 for (i, j) in r1 if (i + j) % 2 == 0 and A[i][j] == 0)

    perimeter_r2 = [A[i][j] for (i, j) in r2 if i == 0 or j == 0 or i == n - 1 or j == n - 1]
    product_r2 = 1
    for num in perimeter_r2:
        product_r2 *= num if num != 0 else 1

    print(f"\nКоличество нулей в области 1 с четной суммой индексов: {zeros_r1}")
    print(f"Элементы на периметре области 2: {perimeter_r2}")
    print(f"Произведение чисел на периметре области 2: {product_r2}")

    if zeros_r1 > product_r2:
        print("Условие выполнено: меняем симметрично области 1 и 2.")
        F = swap_symmetric(F, r1, r2)
    else:
        print("Условие не выполнено: меняем несимметрично области 2 и 3.")
        F = swap_asymmetric(F, r2, r3)

    return F


def main():
    K = int(input("Введите K: "))
    A = read_matrix('matrix.txt')
    print_matrix(A, "Матрица A")

    F = build_F(A)
    print_matrix(F, "Матрица F")

    AT = transpose(A)
    FT = transpose(F)

    result = multiply_matrices(AT, add_matrices(F, A))
    result = add_matrices(result, scalar_multiply(-K, FT))

    print_matrix(result, "Результат A^T * (F + A) - K * F^T")


main()