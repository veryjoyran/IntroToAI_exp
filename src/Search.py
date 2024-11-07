# Search.py

from collections import deque
import heapq

# 定义地图符号
WALL = '1'
ROAD = '0'
START = '@'
GOAL = '$'

class SearchAlgorithm:
    """基类，定义搜索算法的接口"""
    def __init__(self, map_data, start, goal):
        self.map_data = map_data
        self.start = start
        self.goal = goal
        self.height = len(map_data)
        self.width = len(map_data[0]) if self.height > 0 else 0

    def get_neighbors(self, position):
        """获取当前位置的可行邻居"""
        i, j = position
        neighbors = []
        directions = [(-1,0), (1,0), (0,-1), (0,1)]  # 上下左右

        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.height and 0 <= nj < self.width:
                if self.map_data[ni][nj] in [ROAD, GOAL, START]:
                    neighbors.append((ni, nj))
        return neighbors

    def reconstruct_path(self, parent, current):
        """重建路径从起点到终点"""
        path = []
        while current != self.start:
            path.append(current)
            current = parent.get(current)
            if current is None:
                return []  # 无法到达
        path.append(self.start)
        path.reverse()
        return path

    def heuristic(self, position):
        """启发式函数，默认不使用"""
        return 0

    def search(self):
        """执行搜索，需在子类中实现"""
        raise NotImplementedError("必须在子类中实现此方法")

    def step_search(self):
        """执行逐步搜索，需在子类中实现"""
        raise NotImplementedError("必须在子类中实现此方法")
class DFS(SearchAlgorithm):
    """深度优先搜索算法"""
    def step_search(self):
        stack = []
        visited = set()
        parent = {}

        stack.append(self.start)
        visited.add(self.start)

        while stack:
            current = stack.pop()
            yield current  # 返回当前节点以进行可视化

            if current == self.goal:
                path = self.reconstruct_path(parent, current)
                yield path  # 返回最终路径
                return
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    stack.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = current

        yield []  # 没有找到路径



class BFS(SearchAlgorithm):
    """广度优先搜索算法"""
    def step_search(self):
        queue = deque()
        visited = set()
        parent = {}

        queue.append(self.start)
        visited.add(self.start)

        while queue:
            current = queue.popleft()
            yield current  # 返回当前节点以进行可视化

            if current == self.goal:
                path = self.reconstruct_path(parent, current)
                yield path  # 返回最终路径
                return
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = current

        yield []  # 没有找到路径



class UniformCostSearch(SearchAlgorithm):
    """统一代价搜索算法"""
    def step_search(self):
        heap = []
        heapq.heappush(heap, (0, self.start))
        visited = set()
        parent = {}
        cost_so_far = {self.start: 0}

        while heap:
            current_cost, current = heapq.heappop(heap)
            yield current  # 返回当前节点以进行可视化

            if current == self.goal:
                path = self.reconstruct_path(parent, current)
                yield path  # 返回最终路径
                return
            if current in visited:
                continue
            visited.add(current)
            for neighbor in self.get_neighbors(current):
                new_cost = current_cost + 1  # 假设每步代价为1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(heap, (new_cost, neighbor))
                    parent[neighbor] = current

        yield []  # 没有找到路径



class GreedySearch(SearchAlgorithm):
    """贪心搜索算法"""
    def heuristic(self, position):
        """使用曼哈顿距离作为启发式函数"""
        return abs(position[0] - self.goal[0]) + abs(position[1] - self.goal[1])

    def step_search(self):
        heap = []
        heapq.heappush(heap, (self.heuristic(self.start), self.start))
        visited = set()
        parent = {}

        while heap:
            _, current = heapq.heappop(heap)
            yield current  # 返回当前节点以进行可视化

            if current == self.goal:
                path = self.reconstruct_path(parent, current)
                yield path  # 返回最终路径
                return
            if current in visited:
                continue
            visited.add(current)
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    heapq.heappush(heap, (self.heuristic(neighbor), neighbor))
                    parent[neighbor] = current

        yield []  # 没有找到路径



class AStarSearch(SearchAlgorithm):
    """A* 搜索算法"""
    def heuristic(self, position):
        """使用曼哈顿距离作为启发式函数"""
        return abs(position[0] - self.goal[0]) + abs(position[1] - self.goal[1])

    def step_search(self):
        heap = []
        heapq.heappush(heap, (self.heuristic(self.start), 0, self.start))
        visited = set()
        parent = {}
        cost_so_far = {self.start: 0}

        while heap:
            _, current_cost, current = heapq.heappop(heap)
            yield current  # 返回当前节点以进行可视化

            if current == self.goal:
                path = self.reconstruct_path(parent, current)
                yield path  # 返回最终路径
                return
            if current in visited:
                continue
            visited.add(current)
            for neighbor in self.get_neighbors(current):
                new_cost = current_cost + 1  # 假设每步代价为1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor)
                    heapq.heappush(heap, (priority, new_cost, neighbor))
                    parent[neighbor] = current

        yield []  # 没有找到路径
