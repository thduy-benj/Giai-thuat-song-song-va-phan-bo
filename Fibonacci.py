import threading
import time
import numpy as np

def MatMul(matrixA, matrixB): 
    C00 = matrixA[0][0] * matrixB[0][0] + matrixA[0][1] * matrixB[1][0]
    C01 = matrixA[0][0] * matrixB[0][1] + matrixA[0][1] * matrixB[1][1]
    C10 = matrixA[1][0] * matrixB[0][0] + matrixA[1][1] * matrixB[1][0]
    C11 = matrixA[1][0] * matrixB[0][1] + matrixA[1][1] * matrixB[1][1]
    return [[C00, C01], [C10,C11]]

def fibo(n):
    results = []
    step = int(np.log2(n))
    temp = [[1,1],[1,0]]
    results.append(temp)
    for _ in range(step):
        temp = MatMul(temp, temp)
        results.append(temp)
    res = results[step]
    n -= int(np.power(2, step))
    while (n > 0):
        step = int(np.log2(n))     
        res = MatMul(res, results[step])
        n -= int(np.power(2, step))
    return res

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        fib1 = None
        fib2 = None
        lock = threading.Lock()

        def calculate_fib1():
            nonlocal fib1
            with lock:
                fib1 = fibo(n // 2)

        def calculate_fib2():
            nonlocal fib2
            with lock:
                fib2 = fibo(n - n // 2)

        thread1 = threading.Thread(target=calculate_fib1)
        thread2 = threading.Thread(target=calculate_fib2)

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        result = MatMul(fib1, fib2)
        return result[0][1]

if __name__ == "__main__":
    n = 100000
    print("So fibo thu ", n)
    start = time.time()
    fibo1 = fibonacci(n)
    end = time.time()
    exetime = end - start
    print("Matrix exetime: ", exetime)