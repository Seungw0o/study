import numpy as np
import matplotlib.pyplot as plt

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