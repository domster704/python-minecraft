import numpy as np


def perlineNoise():
	np.set_printoptions(threshold=2 ** 31 - 1)
	from scipy.ndimage.interpolation import zoom

	arr = np.random.uniform(size=(4, 4))
	arr = zoom(arr, 8)
	arr = arr > 0.5
	arr = np.where(arr, '-', '#')
	# arr = np.array_str(arr, max_line_width=500)
	# print(arr)
	return arr


if __name__ == "__main__":
	print(perlineNoise())