import timeit
import pandas as pd
import matplotlib.pyplot as plt
import functools

#Задана рекуррентная функция. Область определения функции – натуральные числа.
# Написать программу сравнительного вычисления данной функции рекурсивно и итерационно (значение, время).
# Определить (смоделировать) границы применимости рекурсивного и итерационного подхода.
#F(n<3) = 3; F(n) = (-1)*(F(n-1)/(2n)!-2(n-2)) (пpи n >25), F(n)=F(n-1) (пpи 3<n<=25)

@functools.lru_cache(maxsize=None)
def factorial_recursive_cached(n):

    if n < 0:
        raise ValueError("Факториал не определен для отрицательных чисел")
    if n == 0:
        return 1
    return n * factorial_recursive_cached(n - 1)

def F_recursive(n):
    if n < 3:
        return 3
    if n <= 25:
        return F_recursive(n - 1)

    factorial_2n = factorial_recursive_cached(2 * n)
    sign = 1 if n % 2 == 0 else -1
    return sign * (F_recursive(n - 1) / factorial_2n - 2 * (n - 2))

def F_iterative(n):
    if n < 3:
        return 3

    F_prev = 3

    for i in range(4, n + 1):
        F_cur = 0
        if i <= 25:
            F_cur = F_prev
        else:
            factorial_2i = factorial_recursive_cached(2 * i)
            sign = 1 if i % 2 == 0 else -1
            F_cur = sign * (F_prev / factorial_2i - 2 * (i - 2))
        F_prev = F_cur
    return F_prev

results = []
for n in range(2, 41):
    t_rec = timeit.timeit(lambda n=n: F_recursive(n), number=5)
    t_itr = timeit.timeit(lambda n=n: F_iterative(n), number=5)
    results.append((n, t_rec, t_itr))

df = pd.DataFrame(results, columns=['n', 'Время рекурсивно (с)', 'Время итеративно (с)'])
print(df.to_string(index=False))

plt.figure(figsize=(10, 6))
plt.plot(df['n'], df['Время рекурсивно (с)'], '--o', label='Рекурсивно')
plt.plot(df['n'], df['Время итеративно (с)'], '-o', label='Итеративно ')
plt.xlabel('n')
plt.ylabel('Время (с)')
plt.title('Сравнение времени вычисления F(n)')
plt.legend()
plt.grid(True)
plt.show()
