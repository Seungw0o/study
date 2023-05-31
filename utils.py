import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


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

def get_interval_1m_path(xy_array):
    '''
    In an array of many points, leave only arrays with 1m intervals.
        Args:
            xy_array : 2-dim array \n
            [[x1, y1]
             [x2, y2] . . .]
        Returns:
            interval_1m_path \n
            [[x1, y1]
             [x2, y2] . . .]
    '''
    idx = 0
    interval_1m_path = np.empty((0, 2), dtype=np.float32)
    while True:
        try:
            tmp = 1
            if idx == 0:
                interval_1m_path = np.append(interval_1m_path, np.array([xy_array[idx]]), axis=0)
            while (idx <= len(xy_array)):
                dist = np.linalg.norm(xy_array[idx]-xy_array[idx+tmp])
                if 0.95 < dist < 1.05:
                # print(f"got cha! dist : {dist} / idx : {idx}, tmp : {tmp}")
                    interval_1m_path = np.append(interval_1m_path, np.array([xy_array[idx+tmp]]), axis=0)
                    idx = idx + tmp
                    break
                tmp += 1
        except IndexError as e:
            print(e)
            break
    return interval_1m_path