import tkinter as tk
from tkinter import Canvas
import numpy as np

# 定义颜色
WALL_COLOR = "#154164"    # 深蓝色，代表障碍
TRAP_COLOR = "#FF0000"    # 红色，代表陷阱
EXIT_COLOR = "#32CD32"    # 绿色，代表出口
ROAD_COLOR = "#FFFFFF"    # 白色，代表可通行道路
AGENT_COLOR = "#000000"   # 黑色，代表智能体
POLICY_COLOR = "#FFD700"  # 金色，代表最优策略箭头

# 地图元素定义
MAP_DATA = [
    ["A", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "1", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "1", "0", "0", "0"],
    ["0", "0", "0", "0", "1", "0", "-10", "0"],
    ["0", "0", "1", "0", "0", "0", "0", "0"],
    ["0", "-10", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "+10"]
]

CELL_SIZE = 50            # 单元格大小
DISCOUNT_FACTOR = 0.5     # 折扣因子
NOISE = 0.2               # 噪声
MOVE_COST = -1            # 每移动一步的消耗

ACTION_DELAY = 500        # 动作之间的时间间隔，单位为毫秒

ACTIONS = ['up', 'down', 'left', 'right']

# 定义动作转向概率
ACTION_PROBS = {
    'up': {'up': 0.8, 'left': 0.1, 'right': 0.1},
    'down': {'down': 0.8, 'left': 0.1, 'right': 0.1},
    'left': {'left': 0.8, 'down': 0.1, 'up': 0.1},
    'right': {'right': 0.8, 'up': 0.1, 'down': 0.1},
}

# 定义方向移动
DELTA = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1),
}

class MDP:
    def __init__(self, map_data):
        self.map_data = map_data
        self.rows = len(map_data)
        self.cols = len(map_data[0])
        self.states = []
        self.rewards = {}
        self.terminal_states = []
        self.obstacles = []
        self.traps = []
        self.exit = None
        self.agent_start = None
        self._parse_map()

    def _parse_map(self):
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.map_data[i][j]
                if cell == '1':
                    self.obstacles.append((i, j))
                elif cell == '-10':
                    self.states.append((i, j))
                    self.rewards[(i, j)] = -10
                    self.traps.append((i, j))
                    self.terminal_states.append((i, j))
                elif cell == '+10':
                    self.states.append((i, j))
                    self.rewards[(i, j)] = 10
                    self.exit = (i, j)
                    self.terminal_states.append((i, j))
                elif cell == 'A':
                    self.states.append((i, j))
                    self.rewards[(i, j)] = MOVE_COST
                    self.agent_start = (i, j)
                else:  # '0'
                    self.states.append((i, j))
                    self.rewards[(i, j)] = MOVE_COST

    def is_valid_state(self, state):
        i, j = state
        return 0 <= i < self.rows and 0 <= j < self.cols and state not in self.obstacles

    def get_possible_actions(self, state):
        if state in self.terminal_states:
            return []
        else:
            return ACTIONS

    def get_transition_states_and_probs(self, state, action):
        result = []
        for a, prob in ACTION_PROBS[action].items():
            new_state = (state[0] + DELTA[a][0], state[1] + DELTA[a][1])
            if not self.is_valid_state(new_state):
                new_state = state  # 碰壁，留在原地
            result.append((new_state, prob))
        return result

    def get_reward(self, state):
        return self.rewards.get(state, MOVE_COST)

def value_iteration(mdp, epsilon=0.01):
    V = {}
    for state in mdp.states:
        V[state] = 0  # 初始化价值函数

    while True:
        delta = 0
        V_old = V.copy()
        for state in mdp.states:
            if state in mdp.terminal_states:
                continue
            max_value = float('-inf')
            for action in mdp.get_possible_actions(state):
                value = 0
                for next_state, prob in mdp.get_transition_states_and_probs(state, action):
                    reward = mdp.get_reward(next_state)
                    value += prob * (reward + DISCOUNT_FACTOR * V_old[next_state])
                if value > max_value:
                    max_value = value
            delta = max(delta, abs(V[state] - max_value))
            V[state] = max_value
        if delta < epsilon:
            break

    # 提取最优策略
    policy = {}
    for state in mdp.states:
        if state in mdp.terminal_states:
            policy[state] = None
            continue
        max_value = float('-inf')
        best_action = None
        for action in mdp.get_possible_actions(state):
            value = 0
            for next_state, prob in mdp.get_transition_states_and_probs(state, action):
                reward = mdp.get_reward(next_state)
                value += prob * (reward + DISCOUNT_FACTOR * V[next_state])
            if value > max_value:
                max_value = value
                best_action = action
        policy[state] = best_action

    return V, policy

def render_map(canvas, map_data, agent_position=None, policy=None):
    """在Tkinter画布上渲染地图"""
    canvas.delete("all")  # 清除画布内容
    for i, row in enumerate(map_data):
        for j, cell in enumerate(row):
            x1, y1 = j * CELL_SIZE, i * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE

            if cell == "1":  # 障碍
                color = WALL_COLOR
            elif cell == "0":  # 可通行道路
                color = ROAD_COLOR
            elif cell == "-10":  # 陷阱
                color = TRAP_COLOR
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="-10", fill="white", font=("Arial", 12))
                continue
            elif cell == "+10":  # 出口
                color = EXIT_COLOR
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="+10", fill="white", font=("Arial", 12))
                continue
            elif cell == "A":  # 起始位置
                color = ROAD_COLOR
            else:
                color = ROAD_COLOR

            # 绘制方块
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

            # 绘制最优策略
            if policy and (i, j) in policy and policy[(i, j)] is not None:
                action = policy[(i, j)]
                x, y = j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2
                if action == 'up':
                    dx, dy = 0, -15
                elif action == 'down':
                    dx, dy = 0, 15
                elif action == 'left':
                    dx, dy = -15, 0
                elif action == 'right':
                    dx, dy = 15, 0
                canvas.create_line(x, y, x + dx, y + dy, arrow=tk.LAST, fill=POLICY_COLOR, width=2)

    # 绘制智能体
    if agent_position:
        i, j = agent_position
        x1, y1 = j * CELL_SIZE, i * CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill=AGENT_COLOR)

def simulate_agent(mdp, policy):
    """生成智能体按照最优策略的行走路径"""
    state = mdp.agent_start
    path = [state]
    while state not in mdp.terminal_states:
        action = policy[state]
        # 由于有噪声，这里模拟一次实际动作
        probs = []
        next_states = []
        for a, prob in ACTION_PROBS[action].items():
            next_state = (state[0] + DELTA[a][0], state[1] + DELTA[a][1])
            if not mdp.is_valid_state(next_state):
                next_state = state
            probs.append(prob)
            next_states.append(next_state)
        # 根据概率选择下一个状态
        idx = np.random.choice(range(len(next_states)), p=probs)
        state = next_states[idx]
        path.append(state)
        if len(path) > 100:  # 防止无限循环
            break
    return path

def main():
    # 创建MDP
    mdp = MDP(MAP_DATA)
    # 值迭代求解最优策略
    V, policy = value_iteration(mdp)
    # 生成智能体的路径
    path = simulate_agent(mdp, policy)

    # 创建Tkinter主窗口
    root = tk.Tk()
    root.title("迷宫最优策略与路径")

    # 创建画布
    canvas = Canvas(root, width=mdp.cols * CELL_SIZE, height=mdp.rows * CELL_SIZE)
    canvas.pack()

    # 渲染初始地图和最优策略
    render_map(canvas, MAP_DATA, agent_position=mdp.agent_start, policy=policy)

    # 开始动画
    def animate(step=0):
        if step < len(path):
            agent_position = path[step]
            render_map(canvas, MAP_DATA, agent_position=agent_position, policy=policy)
            root.after(ACTION_DELAY, animate, step + 1)
        else:
            # 动画结束，显示结束信息
            state = path[-1]
            if state == mdp.exit:
                canvas.create_text(mdp.cols * CELL_SIZE // 2, mdp.rows * CELL_SIZE // 2, text="到达出口！", fill="green", font=("Arial", 24))
            elif state in mdp.traps:
                canvas.create_text(mdp.cols * CELL_SIZE // 2, mdp.rows * CELL_SIZE // 2, text="掉入陷阱！", fill="red", font=("Arial", 24))
            else:
                canvas.create_text(mdp.cols * CELL_SIZE // 2, mdp.rows * CELL_SIZE // 2, text="模拟结束", fill="blue", font=("Arial", 24))

    # 添加“开始”按钮
    def start_animation():
        animate()

    start_button = tk.Button(root, text="开始", command=start_animation)
    start_button.pack()

    # 运行主循环
    root.mainloop()

# 运行程序
main()
