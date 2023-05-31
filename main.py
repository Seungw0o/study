import utils
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

class CarSpec:
    # 아반떼 AD
    vehicle_length = 4.57
    wheel_base = 2.7
    max_steering = 35
    min_steering = -35

class BicycleModel:
    width = 0.405
    height = 0.8

def main():
    # 1m 경로 생성하기
    x = np.linspace(0, 50, 2000)
    y = 5*np.sin(x/4)
    xy_array = np.array([x, y]).T
    
    interval_1m_path = utils.get_interval_1m_path(xy_array)

    # 차량 초기위치 설정
    car_pos = np.array([-3, -0.5, 90]) # x, y, yaw(heading)
    car_spec = CarSpec()
    bike_model = BicycleModel()

    fig, ax = plt.subplots(figsize=(18, 4))
    ax.add_patch(
    patches.Rectangle(
      (car_pos[0], car_pos[1]),                   # (x, y)
      bike_model.width, bike_model.height,                     # width, height
      angle=car_pos[2],
      edgecolor = 'black',
      facecolor = 'lightgray',
      fill=False,
      rotation_point='center',
    ))

    ax.add_patch(
    patches.Rectangle(
      (car_pos[0]+car_spec.wheel_base, car_pos[1]),                   # (x, y)
      bike_model.width, bike_model.height,                     # width, height
      angle=car_pos[2],
      edgecolor = 'black',
      facecolor = 'lightgray',
      fill=False,
      rotation_point='center',
    ))

    theta = np.radians(car_pos[2])
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                [np.sin(theta), np.cos(theta)]])
    original_center = np.array([car_pos[0], car_pos[1]])
    rotated_center = original_center + np.dot(rotation_matrix, np.array([bike_model.width/2, bike_model.height/2]))
    x_prime, y_prime = rotated_center[0], rotated_center[1]

    # plt.plot([car_pos[0], car_pos[0]+car_spec.wheel_base], [car_pos[1], car_pos[1]], 'g--')
    plt.plot([x_prime, car_pos[0]+car_spec.wheel_base], [y_prime, car_pos[1]], 'g--')

    plt.plot(interval_1m_path.T[0], interval_1m_path.T[1])
    plt.scatter(interval_1m_path.T[0], interval_1m_path.T[1])
    plt.show()

if __name__ == "__main__":
    main()