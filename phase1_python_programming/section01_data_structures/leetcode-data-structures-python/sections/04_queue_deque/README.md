# Section 04 · Queue / Deque

## 数据结构

普通队列按先进先出顺序处理数据，双端队列允许从两端插入和删除。Python 标准库的 `collections.deque` 支持两种访问方式。

| 项目 | 要点 |
| --- | --- |
| 基本操作 | 队尾入队、队头出队、查看两端、定容量队列的判满与判空。 |
| 时间复杂度 | `deque` 的两端插入和移除为 `O(1)`。固定容量的循环队列可用 `O(1)` 时间更新首尾位置。 |
| 空间复杂度 | 存储 `n` 个待处理元素需要 `O(n)` 空间。容量为 `k` 的循环队列使用 `O(k)` 空间。 |
| 常见使用场景 | 按到达顺序处理请求、轮转调度、流式窗口和滑动窗口极值。 |

## 核心知识点

FIFO Queue 关注处理顺序，Circular Queue 关注容量与回绕，Deque 关注双端操作，Monotonic Deque 关注窗口过期与队列候选顺序。

## 题目

本节共 11 题。子方向对应 YAML 中的 `subsection`。

第 346 题的主站 Python3 模板待核实，骨架采用力扣标注的同题接口。 [力扣 LCR 041](https://leetcode.cn/problems/qIsx9U/)

### Easy

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 933 | [Number of Recent Calls](https://leetcode.com/problems/number-of-recent-calls/) | Easy | FIFO Queue | 请求顺序、时间窗口边界 | [.py](easy/p0933_number_of_recent_calls.py) |
| 346 | [Moving Average from Data Stream](https://leetcode.com/problems/moving-average-from-data-stream/) | Easy | FIFO Queue | 定长窗口、队列累计状态 | [.py](easy/p0346_moving_average_from_data_stream.py) |
| 2073 | [Time Needed to Buy Tickets](https://leetcode.com/problems/time-needed-to-buy-tickets/) | Easy | FIFO Queue | 轮转顺序、队列退出条件 | [.py](easy/p2073_time_needed_to_buy_tickets.py) |
| 1700 | [Number of Students Unable to Eat Lunch](https://leetcode.com/problems/number-of-students-unable-to-eat-lunch/) | Easy | FIFO Queue | 队首匹配、无法服务时的停止条件 | [.py](easy/p1700_number_of_students_unable_to_eat_lunch.py) |

### Medium

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 622 | [Design Circular Queue](https://leetcode.com/problems/design-circular-queue/) | Medium | Circular Queue | 定容量队列、下标回绕 | [.py](medium/p0622_design_circular_queue.py) |
| 641 | [Design Circular Deque](https://leetcode.com/problems/design-circular-deque/) | Medium | Circular Queue | 定容量双端操作、头尾边界 | [.py](medium/p0641_design_circular_deque.py) |
| 649 | [Dota2 Senate](https://leetcode.com/problems/dota2-senate/) | Medium | FIFO Queue | 按轮处理、队列内的相对次序 | [.py](medium/p0649_dota2_senate.py) |
| 950 | [Reveal Cards In Increasing Order](https://leetcode.com/problems/reveal-cards-in-increasing-order/) | Medium | FIFO Queue | 牌序、队列中的位置 | [.py](medium/p0950_reveal_cards_in_increasing_order.py) |
| 1823 | [Find the Winner of the Circular Game](https://leetcode.com/problems/find-the-winner-of-the-circular-game/) | Medium | Circular Queue | 循环轮转、淘汰计数 | [.py](medium/p1823_find_the_winner_of_the_circular_game.py) |
| 1670 | [Design Front Middle Back Queue](https://leetcode.com/problems/design-front-middle-back-queue/) | Medium | Deque | 两端操作、中间位置与长度平衡 | [.py](medium/p1670_design_front_middle_back_queue.py) |

### Hard

| 编号 | LeetCode 题目 | 难度 | 子方向 | 训练方向 | 骨架 |
| --- | --- | --- | --- | --- | --- |
| 239 | [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | Hard | Monotonic Deque | 单调双端队列、窗口过期判定 | [.py](hard/p0239_sliding_window_maximum.py) |
