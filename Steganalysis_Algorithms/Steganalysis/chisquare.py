# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
import numpy as np
import cv2 as ocv
import scipy.stats as scs
import matplotlib.pyplot as plt


img_r = ocv.imread("./pup.jpg", ocv.IMREAD_GRAYSCALE)
#print(img_r)

img = np.ndarray.flatten(img_r)
start = 201
end = 300
print(img[start:end])

groupSize = 4096

#print(len(img))

img =  np.append(img, np.full(groupSize -  len(img) % groupSize, 0))

#print(len(img))

blocks = np.split(img, len(img) // groupSize)
#print(blocks)

dof = 128
alpha = 0.05


def observed(lst):
    obs = []

    for i in range(0, len(lst) - 1):
        obs.append(lst[i]+1)

    return obs


def expected(lst):
    exp = []

    for i in range(0, len(lst) - 1, 2):
        exp.append((lst[i] + lst[i + 1]) / 2)

    return exp


def calcChiSquare(block, size, dof):
    auxX = [0] * 128
    auxY = [0] * 128

    for j in range(size):
        c = block[j]
        if c % 2 == 0:
            auxX[c // 2] += 1
        else:
            auxY[c // 2] += 1

    T = []
    auxZ = []
    for i in range(128):
        total = auxX[i] + auxY[i]
        if total != 0:
            T.append(auxX[i])
            auxZ.append(total / 2)

    # Adjust expected to match observed sum
    sum_T = sum(T)
    sum_Z = sum(auxZ)

    if sum_Z != 0:
        scaled_auxZ = [z * sum_T / sum_Z for z in auxZ]
    else:
        scaled_auxZ = auxZ

    chi, p = scs.chisquare(T, scaled_auxZ)
    return p
