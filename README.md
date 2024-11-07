# IntroToAI_exp
东北大学人工智能导论实验
## 实验简介

本项目实现了迷宫智能体的模拟，主要包括两个部分：

1. **问题一：迷宫搜索**

   - 自动生成大规模随机迷宫地图（尺寸至少为50×50）。
   - 允许手动控制智能体（Agent-A）从起点移动到终点。
   - 实现多种搜索算法（深度优先、广度优先、统一代价、贪心和 A*）自动搜索路径，动画展示搜索过程和最终路径，并显示路径代价。
   - 提供友好的用户界面，包括操作工具栏和菜单。

2. **问题二：不确定性搜索**

   - 构建包含障碍、陷阱和出口的迷宫地图，红色表示陷阱，绿色表示出口。
   - 智能体只能上下左右移动，每移动一步消耗体力1（记作-1），折扣因子为0.5，动作存在噪声0.2（左右各0.1）。
   - 使用值迭代算法计算最优策略，自动完成从起点到出口的路径规划。
   - 可视化展示最优策略和智能体的移动过程，输出详细的状态信息。

---

## 问题描述与解决方案

### 问题一：迷宫搜索

#### 1. 自动构建地图

- **要求**：程序自动生成尺寸不小于50×50的迷宫地图，保存为`.map`文件，格式如下：    
"1,@,1,1,1,1,1,1",    
"1,0,0,0,0,0,1,1",    
"1,0,1,0,1,0,0,1",   
"1,0,1,0,0,1,0,1",   
"1,0,1,1,0,0,0,1",   
"1,0,0,1,0,1,0,1",   
"1,1,0,0,0,0,0,1",   
"1,1,1,1,1,1,$,1",   
其中，`1`表示墙壁，`0`表示通路，`@`表示起点，`$`表示终点。

- **解决方案**：

- 使用随机生成算法创建连通的迷宫，确保从起点到终点有一条可行路径。
- 地图以二维列表形式存储，提供方法将其保存为`.map`文件。

#### 2. 手动搜索

- **要求**：用户可以通过上下左右键（WASD）控制智能体在迷宫中移动，有墙壁阻挡时不可移动。

- **解决方案**：

- 使用 Tkinter 库创建图形用户界面，绘制迷宫地图。
- 绑定键盘事件，实现智能体的移动控制。
- 在智能体移动过程中，实时更新界面，直观展示智能体的位置。

#### 3. 自动搜索

- **要求**：实现深度优先、广度优先、统一代价、贪心和 A*搜索算法，自动搜索从起点到终点的路径，并动画展示搜索过程和最终路径，显示路径代价。

- **解决方案**：

- 为每种搜索算法创建对应的类，统一继承自基类 `SearchAlgorithm`，方便扩展和维护。
- 在搜索过程中，使用生成器（`yield`）逐步返回搜索状态，以实现动画展示。
- 在界面上提供按钮，用户可以选择不同的搜索算法，程序将动态展示搜索过程。
- 计算并显示最终路径的代价（步数）。

#### 4. 用户界面

- **要求**：程序提供上述功能的操作工具栏或菜单，用户可以方便地选择不同的功能。

- **解决方案**：

- 使用 Tkinter 创建按钮和菜单，组织良好的布局，提升用户体验。
- 提供地图模式选择（随机生成或预定义），以及刷新地图、手动搜索和自动搜索等功能。

---

### 问题二：不确定性搜索

#### 1. 构建迷宫地图

- **要求**：构建包含障碍、陷阱和出口的迷宫地图，其中红色表示陷阱，绿色表示出口。

- **解决方案**：

- 使用二维数组表示地图，元素包括障碍（`1`）、陷阱（`-10`）、出口（`+10`）等。
- 使用 Tkinter 绘制迷宫地图，使用不同颜色区分各类元素。

#### 2. 智能体移动规则

- **要求**：智能体只能上下左右移动，每移动一步消耗体力1（记作-1），折扣因子为0.5，动作存在噪声0.2（左右各0.1），找到出口即结束。

- **解决方案**：

- 定义动作集合和对应的转移概率，考虑动作噪声的影响。
- 在状态转移时，累加可能到达同一状态的概率，确保概率分布的准确性。

#### 3. 值迭代算法

- **要求**：设计算法自动完成上述过程，给出最优的行为策略及路线。

- **解决方案**：

- 使用值迭代算法计算每个状态的价值函数，考虑折扣因子和即时奖励。
- 提取最优策略，即在每个状态下选择使预期累积奖励最大的动作。
- 通过模拟智能体按照最优策略的移动过程，展示其从起点到出口的路径。

#### 4. 可视化展示

- **要求**：可视化展示最优策略（使用箭头表示）和智能体的移动过程，提供详细的信息输出。

- **解决方案**：

- 在 Tkinter 画布上绘制迷宫地图，使用箭头表示最优策略。
- 模拟智能体的移动过程，动画展示其在迷宫中的位置变化。
- 在界面上添加文本区域，实时输出智能体的当前位置、即时奖励、采取的行动、实际移动方向和累积总奖励等信息。

---

## 运行说明

### 环境要求

- Python 3.x
- 必要的第三方库：
- Tkinter（通常随 Python 一起安装）
- NumPy
- Pillow（用于图像处理）
 ```bash
 pip install numpy pillow
```
## 文件目录结构    
 
├── src/                       
│   ├── main_problem1.py       # 问题一的主程序入口        
│   ├── main_problem2.py       # 问题二的主程序入口    
│   ├── My_Map.py              # 迷宫地图类，处理地图的生成和渲染    
│   ├── Search.py              # 各种搜索算法的实现    
│   └── images/                # 存放智能体和起点/终点的图片    
│    │   ├── Agent.png    
│     │  └── Start_Goal.png      
└── README.md              # 项目说明文档  
