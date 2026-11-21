# Section 11 · Graph

## 数据结构

图用顶点和边表示关系。题目的输入可能是边列表、邻接关系或每个顶点的后继。

| 项目 | 要点 |
| --- | --- |
| 基本操作 | 建图、枚举邻居、递归 DFS、记录访问状态。 |
| 时间复杂度 | 对邻接表完整进行一次 DFS 需要 `O(V + E)`。枚举所有路径时还需计入输出规模。 |
| 空间复杂度 | 邻接表占 `O(V + E)`。一次 DFS 的访问标记和调用栈共占 `O(V)` 额外空间。 |
| 常见使用场景 | 连通性、依赖关系、可达性和有向图判环。 |

## 核心知识点

练习根据图的方向选择建模方式，以递归 DFS 和简单访问标记表示搜索状态。

## 题目

本节共 10 题。子方向对应 YAML 中的 `subsection`。

### Easy

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 1791 | [Find Center of Star Graph](https://leetcode.com/problems/find-center-of-star-graph/) | Easy | Graph Structure | 星形图、顶点度与中心 | [.py](easy/p1791_find_center_of_star_graph.py) |
| 997 | [Find the Town Judge](https://leetcode.com/problems/find-the-town-judge/) | Easy | Graph Structure | 有向边、入度和出度 | [.py](easy/p0997_find_the_town_judge.py) |
| 1971 | [Find if Path Exists in Graph](https://leetcode.com/problems/find-if-path-exists-in-graph/) | Easy | Connectivity | 无向图建模、递归 DFS 连通性 | [.py](easy/p1971_find_if_path_exists_in_graph.py) |

### Medium

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 207 | [Course Schedule](https://leetcode.com/problems/course-schedule/) | Medium | Cycles and States | 依赖边、递归状态与有向环 | [.py](medium/p0207_course_schedule.py) |
| 797 | [All Paths From Source to Target](https://leetcode.com/problems/all-paths-from-source-to-target/) | Medium | Path Tracking | DAG 路径枚举、递归路径状态 | [.py](medium/p0797_all_paths_from_source_to_target.py) |
| 802 | [Find Eventual Safe States](https://leetcode.com/problems/find-eventual-safe-states/) | Medium | Cycles and States | 安全状态、访问中的节点和环 | [.py](medium/p0802_find_eventual_safe_states.py) |
| 841 | [Keys and Rooms](https://leetcode.com/problems/keys-and-rooms/) | Medium | Connectivity | 有向可达性、访问状态 | [.py](medium/p0841_keys_and_rooms.py) |
| 1466 | [Reorder Routes to Make All Paths Lead to the City Zero](https://leetcode.com/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero/) | Medium | Connectivity | 有向边标记、以节点 0 为根的 DFS | [.py](medium/p1466_reorder_routes_to_make_all_paths_lead_to_the_city_zero.py) |
| 1376 | [Time Needed to Inform All Employees](https://leetcode.com/problems/time-needed-to-inform-all-employees/) | Medium | Path Tracking | 管理层级、路径累计时间 | [.py](medium/p1376_time_needed_to_inform_all_employees.py) |

### Hard

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 2360 | [Longest Cycle in a Graph](https://leetcode.com/problems/longest-cycle-in-a-graph/) | Hard | Cycles and States | 后继图、访问时间戳与环长 | [.py](hard/p2360_longest_cycle_in_a_graph.py) |
