# ВАРИАНТ 18
# С клавиатуры вводится два числа K и N. Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц, B,C,D,E заполняется случайным образом целыми числами в интервале
# [-10,10]. Для тестирования использовать не случайное заполнение, а целенаправленное.

# Матрица A имеет вид B - 11, C - 12, D - 21, E - 22.
# Каждая из матриц B, C, D, E выглядит следующим образом:

#   2
# 1   3
#   4

# ЗАДАНИЕ
# Формируется матрица F следующим образом: если в Е количество чисел, больших К в четных столбцах в области 1 больше,
# чем произведение чисел в нечетных строках в области 4, то поменять в Е симметрично области 2 и 3 местами, иначе С и В поменять
# местами несимметрично. При этом матрица А не меняется. После чего вычисляется выражение: (К*(A*F))* F T. Выводятся по мере
# формирования А, F и все матричные операции последовательно.
import random


def create_matrix(N):
    return [[random.randint(0, 10) for _ in range(N)] for _ in range(N)]


def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))
    print()


def transpose_matrix(matrix):
    return [list(row) for row in zip(*matrix)]


def multiply_matrix_by_scalar(matrix, scalar):
    return [[scalar * cell for cell in row] for row in matrix]


def matrix_multiplication(A, B):
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result


def count_greater_than_K_in_even_columns(E, K):
    count = 0
    for i in range(len(E) // 2):
        for j in range(0, i, 2):
            if E[i][j] > K:
                count += E[i][j]
    for i in range(len(E) // 2, len(E)):
        for j in range(0, len(E) - (i + 1), 2):
            if E[i][j] > K:
                count += E[i][j]
    return count


def product_in_odd_rows(E):
    product = 1
    for i in range(len(E) // 2, len(E), 3):
        for j in range(len(E) - (i + 1) + 1, len(E) // 2):
            product *= E[i][j]
    for i in range(len(E) // 2, len(E), 3):
        for j in range(len(E) // 2, i):
            product *= E[i][j]
    return product


def swap_elements(E):
    for i in range(len(E) // 2):
        for j in range(i + 1, len(E) - (i + 1)):
            E[i][j], E[len(E) - j - 1][len(E) - i - 1] = E[len(E) - j - 1][len(E) - i - 1], E[i][j]
    return E


def main():
    try:
        K = int(input("Введите число K: "))
        N = int(input("Введите размерность матрицы N: "))
    except ValueError:
        print('Число N ,или число K ,или оба числа не целые')
        return

    if N < 6:
        print("N должно быть больше , как минимум -6- , для корректного выполнения.")
        return

    A = create_matrix(N)
    print("Матрица A:")
    print_matrix(A)

    mid = N // 2
    B = [row[:mid] for row in A[:mid]]
    C = [row[mid:] for row in A[:mid]]
    D = [row[:mid] for row in A[mid:]]
    E = [row[mid:] for row in A[mid:]]

    if count_greater_than_K_in_even_columns(E, K) > product_in_odd_rows(E):
        swap_elements(E)
    else:
        C, B = B, C

    F = [B[i] + C[i] for i in range(mid)] + [D[i] + E[i] for i in range(mid)]

    print("Матрица F после преобразований:")
    print_matrix(F)

    AF = matrix_multiplication(A, F)
    KAF = multiply_matrix_by_scalar(AF, K)
    F_transposed = transpose_matrix(F)
    result = matrix_multiplication(KAF, F_transposed)

    print("Матрица AF (A умноженное на F):")
    print_matrix(AF)

    print("Матрица KAF (K умноженное на AF):")
    print_matrix(KAF)

    print("Матрица F транспонированная:")
    print_matrix(F_transposed)

    print("Результат выражения (К(AF))*F^T:")
    print_matrix(result)


if __name__ == "__main__":
    main()