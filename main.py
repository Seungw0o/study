import utils
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
'''
pure pursuit 에서 입력해야하는 값

vehicle length
look f d
velocity

만드는 순서
1m 간격 경로 만들기
차 모양 만들기

'''
def draw_car_model(center_points, wheel_base, vehicle_length, heading, overall_width, overhang):
    '''
    vehicle_length=4.6,
    heading=30, 
    overall_width=1.8, 
    overhang=1.11
    '''
    fig, ax = plt.subplots()
    ax.add_patch(
    patches.Rectangle(
    #   (center_points[0]-overhang, center_points[1]-overall_width/2),                   # (x, y)
      (center_points[0]-vehicle_length/2, center_points[1]-overall_width/2),                   # (x, y)
      vehicle_length, overall_width,                     # width, height
      angle=heading,
      edgecolor = 'black',
      facecolor = 'lightgray',
      fill=True,
      rotation_point='center',
    ))

def main():
    x = np.linspace(0, 50, 2000)
    y = 5*np.sin(x/4)
    xy_array = np.array([x, y]).T
    
    interval_1m_path = utils.get_interval_1m_path(xy_array)

    draw_car_model(interval_1m_path[20], None, 
                   vehicle_length=4.6,
                   heading=-45, 
                   overall_width=1.8, 
                   overhang=1.11,
                   )
    
    plt.plot(interval_1m_path.T[0], interval_1m_path.T[1])
    plt.scatter(interval_1m_path.T[0], interval_1m_path.T[1])
    plt.show()

if __name__ == "__main__":
    main()