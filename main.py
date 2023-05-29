import utils
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def main():
    x = np.linspace(0, 50, 2000)
    y = np.sin(x/np.pi)
    xy_array = np.array([x, y]).T
    
    interval_1m_path = utils.get_interval_1m_path(xy_array)
    
    print(interval_1m_path[:10])
    plt.scatter(interval_1m_path.T[0], interval_1m_path.T[1])
    plt.show()

if __name__ == "__main__":
    main()