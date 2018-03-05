import matplotlib.pyplot as plt 
from dantzig import dantzig

def main():
	data_path = 'dat.dat'
	# tuple(0) := solutions, tuple(1) := ) 
	tuple_dantzig = dantzig(data_path)
	plt.plot(tuple_dantzig[1],tuple_dantzig[2])

if __name__ == '__main__':
	main()
