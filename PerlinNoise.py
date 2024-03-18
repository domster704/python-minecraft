import numpy as np
from scipy.ndimage import zoom


def perlinNoise():
    np.set_printoptions(threshold=2 ** 31 - 1)

    arr = np.random.uniform(size=(4, 4))
    arr = zoom(arr, 8)
    arr = arr > 0.5
    arr = np.where(arr, '-', '#')
    return arr


if __name__ == "__main__":
    print(perlinNoise())
