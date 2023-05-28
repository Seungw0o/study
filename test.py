import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

x = np.linspace(0, 50, 2000)
y = np.sin(x/np.pi)
xy_array = np.array([x, y]).T
interval_1m_path = np.empty((0, 2))

print(f"shape of xy array : {xy_array.shape}")
idx = 0

# @TODO : 1M 간격의 경로 만들기 ㅅㅂ
while True:
    try:
        tmp = 1
        while (idx <= len(xy_array)):
            dist = np.linalg.norm(xy_array[idx]-xy_array[idx+tmp])
            if 0.95 < dist < 1.05:
                print(f"got cha! dist : {dist} / idx : {idx}, tmp : {tmp}")
                interval_1m_path = np.append(interval_1m_path, np.array([xy_array[idx+tmp]]), axis=0)
                idx = idx + tmp
                break
            tmp += 1
    except IndexError as e:
        print(e)
        print(f"finally idx value : {idx}")
        np.delete(interval_1m_path, 0, axis=0)
        break

plt.scatter(interval_1m_path.T[0], interval_1m_path.T[1])
plt.show()

# @TODO : Pure Pursuit Guidance