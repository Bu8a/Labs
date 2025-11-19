import numpy as np
import matplotlib.pyplot as plt


def print_matrix(matrix, name):
    print(f"\n{name}:")
    with np.printoptions(suppress=True, precision=4):
        print(matrix)

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
    h = D.shape[0]
    
    zeros_perimeter_C = np.sum(C[0, :] == 0) + np.sum(C[-1, :] == 0) + \
                        np.sum(C[:, 0] == 0) + np.sum(C[:, -1] == 0)
    
    perimeter_values_C = C[[0, 0, -1, -1], [0, -1, 0, -1]]
    product_perimeter_C = 1
    for value in perimeter_values_C:
        if value != 0:
            product_perimeter_C *= value

    print(f"\nКоличество нулей по периметру области C: {zeros_perimeter_C}")
    print(f"Элементы на периметре области C: {perimeter_values_C}")
    print(f"Произведение чисел на периметре области C: {product_perimeter_C}")

    if zeros_perimeter_C > product_perimeter_C:
        print("Меняем симметрично области D и B")
        F[:h, :h], F[h:, h:] = B, D
    else:
        print("Меняем несимметрично области C и B")
        F[h:, :h], F[h:, h:] = B, C
    
    return F

def compute_result(A, F, K):

        if np.linalg.det(A) > np.trace(F):
            print("\nОпределитель A больше суммы диагональных элементов F")
            return A @ A.T - K * F
        else:
            print("\nОпределитель A меньше или равен сумме диагональных элементов F")
            G = np.tril(A)

            det_A = np.linalg.det(A)
            det_F = np.linalg.det(F)

            if np.isclose(det_A, 0.0) or np.isclose(det_F, 0.0):
                print(f" Матрица A (det={det_A:.2e}) или F (det={det_F:.2e}) сингулярна. Вычисление (A^-1 + G - F^-1) * K невозможно.")
                return np.zeros_like(A)

        return (np.linalg.inv(A) + G - np.linalg.inv(F)) * K


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
    N_possible_sizes = np.arange(4, 10, 2)
    N = np.random.choice(N_possible_sizes)
    print(f"Случайный размер матрицы N: {N}x{N}")
    A = np.random.randint(-10, 11, size=(N, N))
    print_matrix(A, "Матрица A")
    
    F = build_F(A)
    print_matrix(F, "Матрица F")
    
    result = compute_result(A, F, K)
    print_matrix(result, "Результат")
    
    plot_graphs(F)

main()
