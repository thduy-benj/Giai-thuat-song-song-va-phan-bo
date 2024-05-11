import numpy as np
import time
import multiprocessing
def padding(matrix1,matrix2):
    matrix2=matrix2.tolist()
    matrix1=matrix1.tolist()
    size=len(matrix1)
    mangp = [0]*(size+1)
    for i in range(size):
        matrix2[i].append(0)
        matrix1[i].append(0)
    matrix1.append(mangp)
    matrix2.append(mangp)
    return np.array(matrix1) , np.array(matrix2)
    
def strassen(matrix1,matrix2):
    haveadd=False
    length=matrix1.shape[0]
    if length <= 128:
        return np.matmul(matrix1, matrix2)
    elif matrix1.shape[0]%2!=0:
        matrix1,matrix2=padding(matrix1,matrix2)
        length+=1
        haveadd=True
    n = length // 2
    a11, a12, a21, a22 = matrix1[:n, :n], matrix1[:n, n:], matrix1[n:, :n], matrix1[n:, n:]
    b11, b12, b21, b22 = matrix2[:n, :n], matrix2[:n, n:], matrix2[n:, :n], matrix2[n:, n:]
    St1 = strassen(a11 + a22, b11 + b22)
    St2 = strassen(a21 + a22, b11)
    St3 = strassen(a11, b12 - b22)
    St4 = strassen(a22, b21 - b11)
    St5 = strassen(a11 + a12, b22)
    St6 = strassen(a21 - a11, b11 + b12)
    St7 = strassen(a12 - a22, b21 + b22)
    c1 = St1 + St4 - St5 + St7
    c2 = St3 + St5
    c3 = St2 + St4
    c4 = St1 - St2 + St3 + St6
    result = np.vstack((np.hstack((c1, c2)), np.hstack((c3, c4))))
    if haveadd:
        result=result[:-1,:-1]
    return result

def parallel_multiply_matrices(matrix1, matrix2):
    haveadd=False
    blocks = []
    matrix1 = np.array(matrix1)
    matrix2 = np.array(matrix2)
    if len(matrix1)%2!=0:
        matrix1, matrix2 = padding(matrix1,matrix2)
        haveadd=True
    n=matrix1.shape[0]//2
    a11, a12, a21, a22 = matrix1[:n, :n], matrix1[:n, n:], matrix1[n:, :n], matrix1[n:, n:]
    b11, b12, b21, b22 = matrix2[:n, :n], matrix2[:n, n:], matrix2[n:, :n], matrix2[n:, n:]

    blocks.append((a11+a22,b11 + b22))
    blocks.append((a21+a22,b11))
    blocks.append((a11,b12-b22))
    blocks.append((a22,b21-b11))
    blocks.append((a11+a12,b22))
    blocks.append((a21-a11,b11+b12))
    blocks.append((a12-a22,b21+b22))
    pool = multiprocessing.Pool()
    results = pool.starmap(strassen,blocks)
    pool.close()
    pool.join()
    c1 = results[0] + results[3] - results[4] + results[6]
    c2 = results[2] + results[4]
    c3 = results[1] + results[3]
    c4 = results[0] - results[1] + results[2] + results[5]
    result = np.vstack((np.hstack((c1, c2)), np.hstack((c3, c4))))
    if haveadd:
        result=result[:-1,:-1]
    return result

if __name__=='__main__':
    n=2000
    matrix1 = np.random.randint(0, 100, size=(n, n))
    matrix2 = np.random.randint(0, 100, size=(n, n))

    start=time.time()
    result = parallel_multiply_matrices(matrix1, matrix2)
    end=time.time()
    print("Exe time:= ",end-start)
    print("Result:")
    print(result)
    



