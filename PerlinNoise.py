import numpy as np
from scipy.ndimage import zoom


def perlineNoise():
	np.set_printoptions(threshold=2 ** 31 - 1)

	arr = np.random.uniform(size=(4, 4))
	arr = zoom(arr, 8)
	arr = arr > 0.5
	arr = np.where(arr, '-', '#')
	# arr = np.array_str(arr, max_line_width=500)
	# print(arr)
	return arr


def xd():
	arr = np.array(perlineNoise())
	arr = zoom(arr, 8)
	arr = arr > 0.5
	arr = np.where(arr, '-', '#')
	# arr = np.array_str(arr, max_line_width=500)
	# print(arr)
	return arr


if __name__ == "__main__":
	print(perlineNoise())