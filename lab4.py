#Формируется матрица F следующим образом: скопировать в нее А и  если в Е максимальный элемент в нечетных столбцах больше, чем сумма чисел в нечетных строках, то поменять местами С и В симметрично, иначе В и Е поменять местами несимметрично. При этом матрица А не меняется. После чего если определитель матрицы А больше суммы диагональных элементов матрицы F, то вычисляется выражение: A-1*AT – K * F-1, иначе вычисляется выражение (AТ +G-FТ)*K, где G-нижняя треугольная матрица, полученная из А. Выводятся по мере формирования А, F и все матричные операции последовательно.
import copy
import numpy as np
import matplotlib.pyplot as plt


def read_matrix_from_file(filename):
    with open(filename, 'r') as file:
        matrix = [list(map(int, line.split())) for line in file]
    return matrix


def extract_submatrix(matrix, n):
    return [row[:n] for row in matrix[:n]]


def print_matrix(m, title):
    print(f"\n{title}:")
    for row in m:
        print(" ".join(f"{x:4}" for x in row))


def get_max_in_odd_columns_E(matrix, n):
    half = n // 2
    max_val = -float('inf')
    for i in range(half, n):
        for j in range(half, n):
            if j % 2 == 1:
                if matrix[i][j] > max_val:
                    max_val = matrix[i][j]
    return max_val


def sum_in_odd_rows_E(matrix, n):
    half = n // 2
    total = 0
    for i in range(half, n):
        for j in range(half, n):
            if i % 2 == 0:
                total += matrix[i][j]
    return total


def swap_C_B_symmetrically(matrix, n):
    half = n // 2
    for i in range(half):
        for j in range(half):
            matrix[i][j], matrix[i][n - 1 - j] = matrix[i][n - 1 - j], matrix[i][j]


def swap_B_E_asymmetrically(matrix, n):
    half = n // 2
    for i in range(half):
        for j in range(half, n):
            matrix[i][j], matrix[i + half][j] = matrix[i + half][j], matrix[i][j]


def create_lower_triangular(matrix):
    n = len(matrix)
    G = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            G[i][j] = matrix[i][j]
    return G


def plot_matrices(matrices, titles):
    plt.figure(figsize=(15, 5))
    for i, (matrix, title) in enumerate(zip(matrices, titles), 1):
        plt.subplot(1, 3, i)
        plt.imshow(matrix, cmap='viridis')
        plt.colorbar()
        plt.title(title)
    plt.tight_layout()
    plt.show()


k = int(input('Введите число k: '))
n = int(input('Введите число n: '))

try:
    file_matrix = read_matrix_from_file('matrix2.txt')
    if len(file_matrix) < n or any(len(row) < n for row in file_matrix):
        raise ValueError("Файл содержит матрицу меньшего размера, чем требуется")
    A = extract_submatrix(file_matrix, n)
except Exception as e:
    print(f"Ошибка при чтении матрицы из файла: {e}")
    exit()

A_np = np.array(A)
print_matrix(A, "Матрица A")

F = copy.deepcopy(A)
F_np = np.array(F)

max_in_odd_cols_E = get_max_in_odd_columns_E(F, n)
sum_in_odd_rows_E = sum_in_odd_rows_E(F, n)

print(f"\nМаксимальный элемент в нечетных столбцах E: {max_in_odd_cols_E}")
print(f"Сумма в нечетных строках E: {sum_in_odd_rows_E}")

if max_in_odd_cols_E > sum_in_odd_rows_E:
    print("\nУсловие: max в нечетных столбцах E > суммы в нечетных строках E")
    swap_C_B_symmetrically(F, n)
else:
    print("\nУсловие: max в нечетных столбцах E <= суммы в нечетных строках E")
    swap_B_E_asymmetrically(F, n)

F_np = np.array(F)
print_matrix(F, "Матрица F после преобразований")

det_A = np.linalg.det(A_np)
sum_diag_F = np.trace(F_np)

print(f"\nОпределитель матрицы A: {det_A}")
print(f"Сумма диагональных элементов матрицы F: {sum_diag_F}")

if det_A > sum_diag_F:
    print("\nУсловие: det(A) > sum(diag(F))")
    A_inv = np.linalg.inv(A_np)
    A_T = A_np.T
    F_inv = np.linalg.inv(F_np)

    term1 = np.dot(A_inv, A_T)
    term2 = k * F_inv
    result = term1 - term2

    print("\nA^(-1):")
    print(A_inv)
    print("\nA^T:")
    print(A_T)
    print("\nF^(-1):")
    print(F_inv)
    print("\nРезультат A^(-1)*A^T - K*F^(-1):")
    print(result)
else:
    print("\nУсловие: det(A) <= sum(diag(F))")
    A_T = A_np.T
    G = create_lower_triangular(A)
    G_np = np.array(G)
    F_T = F_np.T

    term = A_T + G_np - F_T

result = k * term

print("\nA^T:")
print(A_T)
print("\nG (нижняя треугольная из A):")
print(G_np)
print("\nF^T:")
print(F_T)
print("\nРезультат (A^T + G - F^T)*K:")
print(result)

plot_matrices([A_np, F_np, result],
              ["Матрица A", "Матрица F", "Результат вычислений"])