import matplotlib.pyplot as plt 
from dantzig import dantzig

def main():
    data_path = '../data/dat11.dat'
    # tuple(0) := solutions, tuple(1) := ) 
    tuple_dantzig = dantzig(data_path)
    # TIME:x Upperbound:y
    #plt.plot(tuple_dantzig[2],tuple_dantzig[1])

    # Iteration:x Upperbound:y
    plt.plot([x+1 for x in range(len(tuple_dantzig[1]))],tuple_dantzig[1])

    plt.show()

if __name__ == '__main__':
	main()
