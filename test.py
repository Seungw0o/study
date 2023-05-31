import numpy as np
import matplotlib.pyplot as plt
import math 
from matplotlib.animation import FuncAnimation

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

def pure_pursuit_guidance(path, lookahead_dist, vehicle_pos, vehicle_length):
    def find_closest_point(path, vehicle_pos):
        # 차량과 가장 가까운 점 추출
        dist = np.sqrt((path[:, 0] - vehicle_pos[0])**2 + (path[:, 1] - vehicle_pos[1])**2)
        closest_idx = np.argmin(dist)
        return path[closest_idx]

    def find_prev_next_points(path, closest_point):
        closest_idx = np.argwhere((path == closest_point).all(axis=1))[0][0] # 경로 중 가장 가까운 점의 idx 추출
        prev_idx = closest_idx - 1
        next_idx = closest_idx + 1
        if prev_idx < 0:
            prev_idx = len(path) - 1
        if next_idx >= len(path):
            next_idx = 0
        return path[prev_idx], path[next_idx]

    def find_lookahead_point(prev_point, next_point, closest_point, lookahead_dist):
        prev_to_next = next_point - prev_point
        prev_to_closest = closest_point - prev_point
        t = np.dot(prev_to_closest, prev_to_next) / np.dot(prev_to_next, prev_to_next)
        lookahead_point = prev_point + t * prev_to_next
        dist = np.sqrt((lookahead_point[0] - closest_point[0])**2 + (lookahead_point[1] - closest_point[1])**2)
        if dist > lookahead_dist:
            lookahead_point = closest_point
        return lookahead_point

    closest_point = find_closest_point(path, vehicle_pos)
    prev_point, next_point = find_prev_next_points(path, closest_point)
    dist = np.sqrt((vehicle_pos[0] - closest_point[0])**2 + (vehicle_pos[1] - closest_point[1])**2)
    lookahead_point = find_lookahead_point(prev_point, next_point, closest_point, lookahead_dist)
    print("lookahead_point", lookahead_point)
    # alpha = np.arctan2(lookahead_point[1] - vehicle_pos[1], lookahead_point[0] - vehicle_pos[0]) - vehicle_pos[2]
    
    dx= lookahead_point[0] - vehicle_pos[0]
    dy= lookahead_point[1] - vehicle_pos[1]
    rotated_point_x=np.cos(vehicle_pos[2])*dx + np.sin(vehicle_pos[2])*dy
    rotated_point_y=np.sin(vehicle_pos[2])*dx - np.cos(vehicle_pos[2])*dy
    alpha=math.atan2(rotated_point_y,rotated_point_x)
    # steer_angle = 2 * np.arctan2(2 * vehicle_length * np.sin(alpha) / lookahead_dist)
    steer_angle = math.atan2((2*vehicle_length*np.sin(alpha)),lookahead_dist)*180/np.pi * 0.1 #deg 
    if steer_angle > 30:
        steer_angle = 30
    elif steer_angle < -30:
        steer_angle = -30
    print("steer_angle", steer_angle)
    return steer_angle

def main():
    x = np.linspace(0, 50, 2000)
    y = 5*np.sin(x/4)
    xy_array = np.array([x, y]).T
    
    path = get_interval_1m_path(xy_array)

    # path = np.array([[0, 0], [2, 2], [4, 4], [6, 2], [8, 0]])
    vehicle_pos = np.array([0, 0, 0])
    lookahead_dist = 1.0
    vehicle_speed = 3.0

    def animate(i, vehicle_pos):
        # print(i)
        if i == 0:
            vehicle_pos[0] = 0.0
            vehicle_pos[1] = 0.0
            vehicle_pos[2] = 0.0
        vehicle_pos[0] += np.cos(vehicle_pos[2]) * vehicle_speed
        vehicle_pos[1] += np.sin(vehicle_pos[2]) * vehicle_speed
        vehicle_pos[2] += pure_pursuit_guidance(path, lookahead_dist, vehicle_pos, 4.6)

        # print(np.cos(vehicle_pos[2]) * vehicle_speed)
        # print(np.cos(vehicle_pos[2]), vehicle_speed)
        # print(vehicle_speed)
        # print(vehicle_speed)
        # print(vehicle_pos)
        plt.cla()
        plt.plot(path[:, 0], path[:, 1], 'b--', label='Path')
        plt.plot(vehicle_pos[0], vehicle_pos[1], 'ro', label='Vehicle')
        plt.xlim(-10, 60)
        plt.ylim(-10, 10)
        plt.legend()

    fig, ax = plt.subplots()
    ax.set_xlim(-10, 60)
    ax.set_ylim(-10, 10)
    ax.plot(path[:, 0], path[:, 1], 'b--', label='Path')
    ax.legend()

    anim = FuncAnimation(fig, animate, frames=100, interval=100, fargs=(vehicle_pos,))
    plt.show()

if __name__ == '__main__':
    main()