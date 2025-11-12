import numpy as np
import matplotlib.pyplot as plt

def load_matrix(filename):
    return np.loadtxt(filename, dtype=int)

def print_matrix(matrix, name):
    print(f"\n{name}:")
    for row in matrix:
        print(" ".join(f"{x:4}" for x in row))

def split_blocks(A):
    h = A.shape[0] // 2
    E = A[:h, :h]
    B = A[:h, h:]
    D = A[h:, :h]
    C = A[h:, h:]
    return D, E, C, B

def build_F(A):
    F = A.copy()
    D, E, C, B = split_blocks(A)
    
    zeros_perimeter_C = np.sum(C[0, :] == 0) + np.sum(C[-1, :] == 0) + \
                        np.sum(C[:, 0] == 0) + np.sum(C[:, -1] == 0)
    
    perimeter_values_C = list(map(int, list(C[0, :]) + list(C[-1, :]) + list(C[:, 0]) + list(C[:, -1])))
    product_perimeter_C = 1
    for value in perimeter_values_C:
        if value != 0:
            product_perimeter_C *= value

    print(f"\nКоличество нулей по периметру области C: {zeros_perimeter_C}")
    print(f"Элементы на периметре области C: {perimeter_values_C}")
    print(f"Произведение чисел на периметре области C: {product_perimeter_C}")

    if zeros_perimeter_C > product_perimeter_C:
        print("Меняем симметрично области E и B")
        F[:E.shape[0], :E.shape[1]], F[:B.shape[0], B.shape[1]:] = B, E
    else:
        print("Меняем несимметрично области B и C")
        F[:B.shape[0], B.shape[1]:], F[C.shape[0]:, C.shape[1]:] = C, B
    
    return F

def compute_result(A, F, K):
    try:
        if np.linalg.det(A) > np.trace(F):
            print("\nОпределитель A больше суммы диагональных элементов F")
            return A @ A.T - K * F
        else:
            print("\nОпределитель A меньше или равен сумме диагональных элементов F")
            G = np.tril(A)
            return (np.linalg.inv(A) + G - np.linalg.inv(F)) * K
    except np.linalg.LinAlgError:
        return "Ошибка: одна из матриц необратима"

def plot_graphs(F):
    plt.figure(figsize=(15, 4))
    
    plt.subplot(1, 3, 1)
    plt.imshow(F, cmap='viridis')
    plt.colorbar()
    plt.title("Тепловая карта матрицы F")
    
    plt.subplot(1, 3, 2)
    plt.plot(F.sum(axis=0), marker='o')
    plt.title("Сумма элементов по столбцам")
    
    plt.subplot(1, 3, 3)
    plt.hist(F.flatten(), bins=10, color='skyblue')
    plt.title("Гистограмма значений матрицы F")
    
    plt.tight_layout()
    plt.show()

def main():
    K = int(input("Введите K: "))
    A = load_matrix('matrix_data.txt')
    print_matrix(A, "Матрица A")
    
    F = build_F(A)
    print_matrix(F, "Матрица F")
    
    result = compute_result(A, F, K)
    print_matrix(result, "Результат")
    
    plot_graphs(F)

main()

