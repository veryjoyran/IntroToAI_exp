import tkinter as tk
from tkinter import Canvas, simpledialog, messagebox
from My_Map import My_Map

def open_selection_window():
    """选择地图模式的窗口"""
    selection_window = tk.Toplevel(root)
    selection_window.title("选择地图模式")
    tk.Label(selection_window, text="请选择地图模式：").pack(pady=10)

    random_button = tk.Button(
        selection_window, text="随机生成地图", command=lambda: [set_mode("random"), selection_window.destroy()]
    )
    predefined_button = tk.Button(
        selection_window, text="使用预定义地图", command=lambda: [set_mode("predefined"), selection_window.destroy()]
    )

    random_button.pack(pady=5)
    predefined_button.pack(pady=5)

def set_mode(mode):
    """根据用户选择的模式初始化地图"""
    global map_mode
    map_mode = mode
    if map_mode == "random":
        enter_random_map_mode()
    else:
        enter_predefined_map_mode()

def enter_random_map_mode():
    """进入随机地图模式，用户输入参数生成地图"""
    global map_width, map_height, cell_size, start_x, start_y, goal_x, goal_y

    # 用户输入地图参数
    map_width = simpledialog.askinteger("输入", "请输入地图宽度：", minvalue=5, maxvalue=50)
    map_height = simpledialog.askinteger("输入", "请输入地图高度：", minvalue=5, maxvalue=50)
    cell_size = simpledialog.askinteger("输入", "请输入单元格大小（像素）：", minvalue=10, maxvalue=100)
    start_x = simpledialog.askinteger("输入", "请输入起点的X坐标：", minvalue=1, maxvalue=map_width - 2)
    start_y = simpledialog.askinteger("输入", "请输入起点的Y坐标：", minvalue=1, maxvalue=map_height - 2)
    goal_x = simpledialog.askinteger("输入", "请输入终点的X坐标：", minvalue=1, maxvalue=map_width - 2)
    goal_y = simpledialog.askinteger("输入", "请输入终点的Y坐标：", minvalue=1, maxvalue=map_height - 2)

    # 调整画布大小
    canvas.config(width=map_width * cell_size, height=map_height * cell_size)

    # 初始化 My_Map 对象
    global my_map
    my_map = My_Map(width=map_width, height=map_height, cell_size=cell_size, canvas=canvas)

    # 生成随机地图
    generate_random_map()

    # 显示地图和控制按钮
    display_map()

def generate_random_map():
    """生成随机地图，保留之前输入的数据"""
    my_map.generate_random_map(
        width=map_width,
        height=map_height,
        cell_size=cell_size,
        start_position=(start_x, start_y),
        goal_position=(goal_x, goal_y)
    )
    my_map.render_map()  # 实时更新地图
    messagebox.showinfo("地图已刷新", "随机地图已成功刷新！")  # 刷新后显示提示

def enter_predefined_map_mode():
    """进入预定义地图模式，直接显示固定地图"""
    MAP = [
        "1,@,1,1,1,1,1,1",
        "1,0,0,0,0,0,1,1",
        "1,0,1,0,1,0,0,1",
        "1,0,1,0,0,1,0,1",
        "1,0,1,1,0,0,0,1",
        "1,0,0,1,0,1,0,1",
        "1,1,0,0,0,0,0,1",
        "1,1,1,1,1,1,$,1",
    ]
    map_width = len(MAP[0].split(','))
    map_height = len(MAP)
    cell_size = 50

    # 调整画布大小
    canvas.config(width=map_width * cell_size, height=map_height * cell_size)

    # 初始化 My_Map 对象
    global my_map
    my_map = My_Map(width=map_width, height=map_height, cell_size=cell_size, canvas=canvas)

    # 设置预定义地图
    my_map.set_map(MAP)

    # 显示地图和控制按钮
    display_map()

def display_map():
    """显示地图和相关搜索按钮"""
    my_map.render_map()
    canvas.pack()  # 现在显示画布
    button_frame.pack(pady=10)  # 现在显示按钮框架

if __name__ == "__main__":
    # 创建 Tkinter 主窗口
    root = tk.Tk()
    root.title("地图搜索可视化")

    # 创建画布，初始不显示
    canvas = Canvas(root)

    # 打开地图模式选择窗口
    open_selection_window()

    # 创建按钮框架，但初始不显示
    button_frame = tk.Frame(root)

    # 创建刷新按钮（仅在随机地图模式下显示）
    refresh_button = tk.Button(
        button_frame,
        text="刷新随机地图",
        command=generate_random_map
    )
    refresh_button.grid(row=0, column=0, padx=5)

    # 创建搜索按钮
    manual_search_button = tk.Button(
        button_frame,
        text="手动搜索",
        command=lambda: [my_map.start_manual_search(), my_map.bind_keys(root)]
    )
    manual_search_button.grid(row=0, column=1, padx=5)

    dfs_button = tk.Button(
        button_frame,
        text="DFS",
        command=lambda: my_map.run_all_searches("DFS")
    )
    dfs_button.grid(row=0, column=2, padx=5)

    bfs_button = tk.Button(
        button_frame,
        text="BFS",
        command=lambda: my_map.run_all_searches("BFS")
    )
    bfs_button.grid(row=0, column=3, padx=5)

    ucs_button = tk.Button(
        button_frame,
        text="统一代价搜索",
        command=lambda: my_map.run_all_searches("Uniform Cost Search")
    )
    ucs_button.grid(row=0, column=4, padx=5)

    greedy_button = tk.Button(
        button_frame,
        text="贪心搜索",
        command=lambda: my_map.run_all_searches("Greedy Search")
    )
    greedy_button.grid(row=0, column=5, padx=5)

    astar_button = tk.Button(
        button_frame,
        text="A* 搜索",
        command=lambda: my_map.run_all_searches("A* Search")
    )
    astar_button.grid(row=0, column=6, padx=5)

    root.mainloop()
