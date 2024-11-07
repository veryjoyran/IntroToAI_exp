import tkinter as tk
from tkinter import Canvas, messagebox
from PIL import Image, ImageTk  # 导入Pillow库
import random
import time
from Search import DFS, BFS, UniformCostSearch, GreedySearch, AStarSearch

# 定义地图符号
WALL = '1'
ROAD = '0'
START = '@'
GOAL = '$'
AGENT = 'A'
PATH = '.'  # 用于显示路径

# 定义RGB颜色并转换为十六进制颜色
def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb

# 定义颜色
wall_rgb = (21, 61, 100)
wall_bg = rgb_to_hex(wall_rgb)

road_rgb = (255, 255, 255)
road_bg = rgb_to_hex(road_rgb)

path_rgb = (173, 216, 230)  # 浅蓝色用于路径
path_bg = rgb_to_hex(path_rgb)

final_path_rgb = (50, 205, 50)  # 绿色用于最终路径
final_path_bg = rgb_to_hex(final_path_rgb)

class My_Map:
    def __init__(self, width, height, cell_size, canvas):
        """初始化地图的宽度、高度和每个单元格的大小"""
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.map_data = []  # 用于存储地图的二维列表
        self.canvas = canvas  # 画布引用

        # 调整图片大小并加载
        try:
            start_goal_image = Image.open("D:\python_project\IntroToAI_exp\src\image\Start_Goal.png")
            agent_image = Image.open("D:\python_project\IntroToAI_exp\src\image\Agent.png")
        except FileNotFoundError:
            # 使用简单的颜色块代替图片
            start_goal_image = Image.new("RGB", (self.cell_size - 1, self.cell_size - 1), (255, 0, 0))
            agent_image = Image.new("RGB", (self.cell_size - 1, self.cell_size - 1), (0, 255, 0))

        # 调整为与单元格相匹配的大小
        self.start_goal_bg = ImageTk.PhotoImage(start_goal_image.resize((self.cell_size-1, self.cell_size-1)))
        self.agent_bg = ImageTk.PhotoImage(agent_image.resize((self.cell_size-1, self.cell_size-1)))

        # AGENT 的初始位置
        self.agent_pos = None

        # 记录 START 和 GOAL 的位置
        self.start_pos = None
        self.goal_pos = None

        # 路径列表
        self.path = []

        # 动画控制
        self.is_animating = False

    def generate_random_map(self, width=None, height=None, cell_size=None, start_position=None, goal_position=None):
        """生成随机地图，确保起点和终点之间有通路，先生成路径，再随机设置其他方块"""
        if width:
            self.width = width
        if height:
            self.height = height
        if cell_size:
            self.cell_size = cell_size

        # 初始化空地图
        self.map_data = [[WALL for _ in range(self.width)] for _ in range(self.height)]

        # 设置起点和终点
        if start_position:
            start_x, start_y = start_position
            self.start_pos = (start_x, start_y)
        else:
            self.start_pos = (1, 1)

        if goal_position:
            goal_x, goal_y = goal_position
            if 1 <= goal_x < self.height - 1 and 1 <= goal_y < self.width - 1:
                self.goal_pos = (goal_x, goal_y)
            else:
                raise ValueError("终点位置超出地图范围")
        else:
            self.goal_pos = (self.height - 2, self.width - 2)

        # 确保起点和终点设置正确
        self.map_data[self.start_pos[0]][self.start_pos[1]] = START
        self.map_data[self.goal_pos[0]][self.goal_pos[1]] = GOAL

        # 随机生成一条从起点到终点的通路
        self.create_random_path(self.start_pos, self.goal_pos)

        # 随机设置剩余的格子
        for i in range(self.height):
            for j in range(self.width):
                if self.map_data[i][j] == ROAD:
                    continue  # 保留生成路径时设置的道路
                elif self.map_data[i][j] not in [START, GOAL]:
                    self.map_data[i][j] = random.choice([WALL, ROAD])

    def create_random_path(self, start, goal):
        """在起点和终点之间生成一条随机路径"""
        current = start
        path = [current]

        while current != goal:
            i, j = current
            neighbors = self.get_neighbors_for_path(i, j, goal)

            if not neighbors:
                raise ValueError("无法生成路径，请检查地图大小或起点终点位置")

            next_step = random.choice(neighbors)
            path.append(next_step)
            current = next_step

        # 将路径上的格子设置为道路
        for i, j in path:
            if self.map_data[i][j] not in [START, GOAL]:
                self.map_data[i][j] = ROAD

    def get_neighbors_for_path(self, i, j, goal):
        """获取用于生成路径的合法邻居（上下左右，并朝向终点优先）"""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上下左右
        neighbors = []

        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.height and 0 <= nj < self.width:
                if self.map_data[ni][nj] == WALL or (ni, nj) == goal:
                    neighbors.append((ni, nj))

        return neighbors

    def set_map(self, map_data):
        """根据指定的字符串地图数据来设置地图"""
        self.map_data = [row.split(',') for row in map_data]

        # 记录 START 和 GOAL 的位置
        for i, row in enumerate(self.map_data):
            for j, cell in enumerate(row):
                if cell == START:
                    self.start_pos = (i, j)
                elif cell == GOAL:
                    self.goal_pos = (i, j)

    def render_map(self):
        """在 Tkinter 画布中渲染地图"""
        self.canvas.delete("all")  # 清除之前的绘制

        # 根据 map_data 渲染地图
        for i, row in enumerate(self.map_data):
            for j, cell in enumerate(row):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                if cell == WALL:
                    color = wall_bg
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                elif cell == ROAD:
                    color = road_bg
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                elif cell == PATH:
                    color = path_bg
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                elif cell == START or cell == GOAL:
                    self.canvas.create_image(x1 + self.cell_size // 2, y1 + self.cell_size // 2,
                                             image=self.start_goal_bg)
                elif cell == AGENT:
                    self.canvas.create_image(x1 + self.cell_size // 2, y1 + self.cell_size // 2, image=self.agent_bg)
                elif cell == 'F':
                    # 渲染最终路径
                    color = final_path_bg
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def find_start_position(self):
        """找到起点的位置"""
        return self.start_pos

    def set_agent_position(self, position):
        """设置 AGENT 的位置"""
        if self.is_animating:
            return  # 在动画过程中禁止手动移动

        if self.agent_pos:
            # 将之前的位置恢复为原始符号（ROAD, START, GOAL）
            prev_i, prev_j = self.agent_pos
            if (prev_i, prev_j) == self.start_pos:
                self.map_data[prev_i][prev_j] = START
            elif (prev_i, prev_j) == self.goal_pos:
                self.map_data[prev_i][prev_j] = GOAL
            else:
                self.map_data[prev_i][prev_j] = ROAD

        i, j = position

        # 将新的位置设置为 AGENT
        if self.map_data[i][j] == START or self.map_data[i][j] == GOAL:
            # 如果新的位置是 START 或 GOAL，依然显示 AGENT
            self.map_data[i][j] = AGENT
        else:
            self.map_data[i][j] = AGENT

        self.agent_pos = position
        self.render_map()

    def move_agent(self, direction):
        """根据方向移动 AGENT"""
        if not self.agent_pos:
            messagebox.showwarning("警告", "请先点击“手动搜索”按钮开始移动。")
            return

        if self.is_animating:
            return  # 在动画过程中禁止手动移动

        i, j = self.agent_pos
        if direction == 'w':  # 上
            new_i, new_j = i - 1, j
        elif direction == 'a':  # 左
            new_i, new_j = i, j - 1
        elif direction == 's':  # 下
            new_i, new_j = i + 1, j
        elif direction == 'd':  # 右
            new_i, new_j = i, j + 1
        else:
            return

        # 检查边界
        if new_i < 0 or new_i >= self.height or new_j < 0 or new_j >= self.width:
            messagebox.showinfo("提示", "无法移动到地图外。")
            return

        target_cell = self.map_data[new_i][new_j]
        if target_cell == WALL:
            messagebox.showinfo("提示", "无法移动到墙壁！")
        elif target_cell in [ROAD, GOAL, START]:
            self.set_agent_position((new_i, new_j))
            if (new_i, new_j) == self.goal_pos:
                messagebox.showinfo("完成", "AGENT 已到达终点！")
        else:
            # 其他情况，如目标是 AGENT（不太可能）
            pass

    def start_manual_search(self):
        """初始化 AGENT 并绑定键盘事件"""
        if self.is_animating:
            return  # 在动画过程中禁止手动移动

        start_pos = self.find_start_position()
        if not start_pos:
            messagebox.showerror("错误", "找不到起点！")
            return
        self.set_agent_position(start_pos)

    def bind_keys(self, root):
        """绑定键盘事件"""
        root.bind('<w>', lambda event: self.move_agent('w'))
        root.bind('<a>', lambda event: self.move_agent('a'))
        root.bind('<s>', lambda event: self.move_agent('s'))
        root.bind('<d>', lambda event: self.move_agent('d'))

    def display_path(self, path, final=False):
        """在地图上显示路径，final参数用于区分是否为最终路径"""
        for pos in path:
            if pos != self.start_pos and pos != self.goal_pos:
                i, j = pos
                if final:
                    # 最终路径用绿色显示
                    self.map_data[i][j] = 'F'  # 标记为最终路径
                else:
                    # 探索路径用浅蓝色显示
                    self.map_data[i][j] = PATH
        self.render_map()

    def create_cost_label(self, root):
        """在窗口上创建一个用于显示路径代价的Label"""
        self.cost_label = tk.Label(root, text="路径代价: 未知", font=("Helvetica", 14), fg="black")
        self.cost_label.pack(side=tk.BOTTOM)

    def display_cost(self, cost):
        """在Label上显示路径代价"""
        self.cost_label.config(text=f"路径代价: {cost}")

    def animate_agent_movement(self, path, delay=300):
        """动画展示 AGENT 沿路径移动"""
        if not path:
            messagebox.showinfo("提示", "没有找到从起点到终点的路径。")
            return

        self.is_animating = True
        self.path = path
        self.current_step = 0
        self.animation_delay = delay
        self.total_steps = len(self.path)
        self.animate_step()

    def animate_step(self):
        """执行动画的每一步"""
        if self.current_step >= self.total_steps:
            self.is_animating = False
            messagebox.showinfo("完成", "AGENT 已到达终点！")
            return

        position = self.path[self.current_step]
        self.set_agent_position(position)
        self.current_step += 1

        # 调用下一步动画
        self.canvas.after(self.animation_delay, self.animate_step())

    def run_search_and_animate(self, algorithm_class):
        """运行指定的搜索算法并动画展示路径"""
        if self.is_animating:
            return  # 防止重复点击

        # 清除之前的路径和代理位置
        for i, row in enumerate(self.map_data):
            for j, cell in enumerate(row):
                if cell in [PATH, AGENT, 'F']:  # 清除之前标记的路径和最终路径
                    self.map_data[i][j] = ROAD
                elif cell == 'F':  # 清除最终路径标记为道路
                    self.map_data[i][j] = ROAD
                elif cell == AGENT:  # 清除AGENT位置
                    self.map_data[i][j] = ROAD

        self.render_map()  # 重绘地图，确保之前的路径已清除

        # 初始化搜索算法
        search_algo = algorithm_class(self.map_data, self.start_pos, self.goal_pos)
        self.search_generator = search_algo.step_search()
        self.is_animating = True
        self.animate_search_step()

    def animate_search_step(self):
        """逐步动画展示搜索过程"""
        try:
            result = next(self.search_generator)
            if isinstance(result, list):
                # 搜索完成，显示最终路径
                self.is_animating = False
                if result:
                    self.display_path(result, final=True)  # 用绿色显示最终路径
                    self.animate_agent_movement(result)

                    # 计算路径代价并显示
                    path_cost = len(result) - 1  # 路径代价为路径长度（步数），减去起点
                    self.display_cost(path_cost)

                else:
                    messagebox.showinfo("提示", "没有找到从起点到终点的路径。")
            else:
                # 更新地图，显示当前探索的节点
                i, j = result

                # 处理之前的AGENT位置
                if self.agent_pos:  # 将之前的AGENT位置标记为PATH或START/GOAL
                    prev_i, prev_j = self.agent_pos
                    if (prev_i, prev_j) == self.start_pos:
                        self.map_data[prev_i][prev_j] = START
                    elif (prev_i, prev_j) == self.goal_pos:
                        self.map_data[prev_i][prev_j] = GOAL
                    else:
                        self.map_data[prev_i][prev_j] = PATH

                # 将当前节点标记为AGENT
                self.map_data[i][j] = AGENT
                self.agent_pos = (i, j)  # 更新AGENT位置
                self.render_map()

                # 设置一个延迟，然后继续下一步
                self.canvas.after(100, self.animate_search_step)
        except StopIteration:
            self.is_animating = False
            messagebox.showinfo("提示", "搜索结束，没有找到路径。")

    def run_all_searches(self, algorithm_name):
        """根据算法名称运行对应的搜索算法"""
        algorithm_map = {
            "DFS": DFS,
            "BFS": BFS,
            "Uniform Cost Search": UniformCostSearch,
            "Greedy Search": GreedySearch,
            "A* Search": AStarSearch
        }

        algorithm_class = algorithm_map.get(algorithm_name)
        if not algorithm_class:
            messagebox.showerror("错误", f"未知的搜索算法：{algorithm_name}")
            return

        self.run_search_and_animate(algorithm_class)
