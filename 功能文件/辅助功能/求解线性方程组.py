from scipy import linalg
import numpy as np





if __name__=='__main__':
    A = np.array([[10, -1, -2], [-1, 10, -2], [-1, -1, 5]])  # A代表系数矩阵
    b = np.array([72, 83, 42])  # b代表常数列
    x = linalg.solve(A, b)
    print(x)















