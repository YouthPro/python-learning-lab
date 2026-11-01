# Section 05 练习题目录

约定优先于习惯性题解：按这里的排序、返回类型、缺失值和边界行为实现。

## 01. Line Plot

- 难度：Easy
- 知识点：Figure, Axes, labels
- 文件：[exercises/basic_plots.py](exercises/basic_plots.py)

```python
def plot_line(x: Sequence, y: Sequence) -> tuple[Figure, Axes]
```

绘制一条标记为 data 的曲线，设置标题、x/y 标签。 返回 (fig,ax)，不调用 show()。

输入输出示例：[0,1],[2,3] → 一条线；[],[] → 空数据曲线

边界条件：空数据可绘制；长度不相等的 x/y 抛 ValueError（适用时）。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 02. Bar Chart

- 难度：Easy
- 知识点：Figure, Axes, labels
- 文件：[exercises/basic_plots.py](exercises/basic_plots.py)

```python
def plot_bar(categories: Sequence[str], values: Sequence[float]) -> tuple[Figure, Axes]
```

绘制柱形图，设置标题、x/y 标签。 返回 (fig,ax)，不调用 show()。

输入输出示例：[A,B],[1,2] → 两根柱；[],[] → 无柱

边界条件：空数据可绘制；长度不相等的 x/y 抛 ValueError（适用时）。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 03. Histogram

- 难度：Easy
- 知识点：Figure, Axes, labels
- 文件：[exercises/basic_plots.py](exercises/basic_plots.py)

```python
def plot_hist(data: Sequence[float]) -> tuple[Figure, Axes]
```

绘制 10 个 bin 的直方图，设置标题、x/y 标签。 返回 (fig,ax)，不调用 show()。

输入输出示例：[1,1,2] → 频数总和 3；[] → 总和 0

边界条件：空数据可绘制；长度不相等的 x/y 抛 ValueError（适用时）。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 04. Scatter Plot

- 难度：Easy
- 知识点：Figure, Axes, labels
- 文件：[exercises/basic_plots.py](exercises/basic_plots.py)

```python
def plot_scatter(x: Sequence, y: Sequence) -> tuple[Figure, Axes]
```

绘制散点图，设置标题、x/y 标签。 返回 (fig,ax)，不调用 show()。

输入输出示例：[1,2],[3,4] → 两点；[],[] → 零点

边界条件：空数据可绘制；长度不相等的 x/y 抛 ValueError（适用时）。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 05. Box Plot

- 难度：Easy
- 知识点：Figure, Axes, labels
- 文件：[exercises/basic_plots.py](exercises/basic_plots.py)

```python
def plot_box(data: Sequence[Sequence[float]]) -> tuple[Figure, Axes]
```

每个内部序列画一个箱体，使用 patch_artist=True，设置标题、x/y 标签；空外层不创建箱体。 返回 (fig,ax)，不调用 show()。

输入输出示例：[[1,2],[3,4]] → 两个箱体；[] → 零箱体

边界条件：空数据可绘制；长度不相等的 x/y 抛 ValueError（适用时）。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 06. Correlation Heatmap

- 难度：Medium
- 知识点：imshow, colorbar
- 文件：[exercises/advanced_plots.py](exercises/advanced_plots.py)

```python
def plot_correlation(df: pd.DataFrame) -> tuple[Figure, Axes]
```

对数值列计算 Pearson 相关性，用 imshow 显示，色域固定 [-1,1]，附 colorbar 和列名刻度、标题及轴标签。

输入输出示例：两列 → 2×2 图像；一列 → 1×1 图像

边界条件：没有数值列抛 ValueError；常数列 NaN 保留。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 07. Multiple Subplots

- 难度：Medium
- 知识点：subplots
- 文件：[exercises/advanced_plots.py](exercises/advanced_plots.py)

```python
def plot_dashboard(data: dict[str, Sequence[float]]) -> tuple[Figure, np.ndarray]
```

输入 x、y、values；创建 2×2 子图：依次为 x/y 折线、x/y 散点、values 直方、values 箱线；每幅有标题和轴标签。

输入输出示例：x=[1,2],y=[3,4],values=[1,2] → 4 子图；空序列 → 空图

边界条件：返回 fig 与 shape (2,2) 的 axes；不 show。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 08. Save Figure

- 难度：Easy
- 知识点：savefig, pathlib
- 文件：[exercises/advanced_plots.py](exercises/advanced_plots.py)

```python
def save_figure(fig: Figure, path: str | Path) -> Path
```

创建父目录，以 PNG 格式、dpi=150、bbox_inches=tight 保存图像，返回 Path。

输入输出示例：fig,out/a.png → 创建文件并返回 Path；空白 fig → 合法 PNG

边界条件：不关闭调用方 fig；不依赖桌面环境。

提示：先运行对应测试，理解返回结构，再查官方文档。
