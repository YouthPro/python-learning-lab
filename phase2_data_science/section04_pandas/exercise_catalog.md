# Section 04 练习题目录

约定优先于习惯性题解：按这里的排序、返回类型、缺失值和边界行为实现。

## 01. Load Dataset

- 难度：Easy
- 知识点：read_csv
- 文件：[exercises/dataframe_basics.py](exercises/dataframe_basics.py)

```python
def load_dataset(path: str | Path) -> pd.DataFrame
```

加载带表头 CSV，按 Pandas 默认规则推断 dtype。

输入输出示例：a,b\n1,2 → 一行两列；仅表头 a,b → 零行两列

边界条件：零字节文件抛 pd.errors.EmptyDataError；路径缺失传播异常。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 02. Select Columns

- 难度：Easy
- 知识点：loc, copy
- 文件：[exercises/dataframe_basics.py](exercises/dataframe_basics.py)

```python
def select_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame
```

按 columns 给定顺序选择列并返回独立副本，保留索引。

输入输出示例：a,b 选择 [b,a] → b,a；选择 [] → 无列

边界条件：缺失列抛 KeyError；支持空行。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 03. Conditional Filtering

- 难度：Easy
- 知识点：boolean indexing
- 文件：[exercises/dataframe_basics.py](exercises/dataframe_basics.py)

```python
def filter_rows(df: pd.DataFrame, condition: pd.Series) -> pd.DataFrame
```

用与 df 索引对齐的布尔 Series 筛选，NA 当 False，保留原索引。

输入输出示例：a=[1,2],mask=[False,True] → 第二行；全 False → 空表

边界条件：空表合法；不修改输入。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 04. Column Transformation

- 难度：Easy
- 知识点：map, strings
- 文件：[exercises/dataframe_basics.py](exercises/dataframe_basics.py)

```python
def transform_column(df: pd.DataFrame, column: str) -> pd.DataFrame
```

返回副本，将指定字符串列去首尾空白并小写；缺失值保持缺失。

输入输出示例：[" A ","B"] → ["a","b"]；[None] → [None]

边界条件：空表合法；其他列与索引不变。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 05. Date Conversion

- 难度：Medium
- 知识点：to_datetime
- 文件：[exercises/dataframe_basics.py](exercises/dataframe_basics.py)

```python
def convert_dates(df: pd.DataFrame, column: str) -> pd.DataFrame
```

在副本中把指定 ISO 日期字符串列转 datetime64[ns]；无效值与缺失值为 NaT。

输入输出示例：["2025-01-01","bad"] → [Timestamp,NaT]；空列 → datetime 空列

边界条件：保留索引；不修改输入。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 06. Data Type Conversion

- 难度：Medium
- 知识点：nullable dtypes, convert_dtypes
- 文件：[exercises/dataframe_basics.py](exercises/dataframe_basics.py)

```python
def convert_dtypes(df: pd.DataFrame) -> pd.DataFrame
```

使用 Pandas 可空类型自动转换列（等同 df.convert_dtypes() 的默认 numpy_nullable 后端），返回新表。

输入输出示例：[1,None] → Int64；[True,None] → boolean

边界条件：空表合法；字符串保留 string dtype。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 07. Missing Value Analysis

- 难度：Medium
- 知识点：isna, sum
- 文件：[exercises/data_cleaning.py](exercises/data_cleaning.py)

```python
def missing_summary(df: pd.DataFrame) -> pd.DataFrame
```

返回以列名为索引的表，列为 missing_count 和 missing_ratio；比例为 0..1，空表比例定义为 0。

输入输出示例：a=[1,None] → count=1,ratio=.5；空 a 列 → 0,0

边界条件：顺序与输入列顺序一致。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 08. Missing Value Imputation

- 难度：Medium
- 知识点：fillna, median
- 文件：[exercises/data_cleaning.py](exercises/data_cleaning.py)

```python
def fill_missing(df: pd.DataFrame) -> pd.DataFrame
```

返回副本：数值列用该列中位数填充，全缺失数值列用 0；其他列用字符串 unknown；输入为普通 float/object 类型。

输入输出示例：[1,NaN,3] → [1,2,3]；类别 [None] → [unknown]

边界条件：空表保留 shape；不修改输入。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 09. Duplicate Removal

- 难度：Easy
- 知识点：duplicated
- 文件：[exercises/data_cleaning.py](exercises/data_cleaning.py)

```python
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame
```

按整行去重，保留第一次出现，保留原索引。

输入输出示例：a=[1,1,2] → 索引 [0,2]；空表 → 空表

边界条件：两个缺失值视为重复；不修改输入。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 10. Outlier Detection

- 难度：Medium
- 知识点：quantile, IQR
- 文件：[exercises/data_cleaning.py](exercises/data_cleaning.py)

```python
def detect_outliers(df: pd.DataFrame, column: str) -> pd.Series
```

用 1.5×IQR 规则返回布尔 Series，严格小于下界或大于上界为异常；缺失值 False；IQR=0 仍按相同公式。

输入输出示例：[1,1,1,1,100] → 最后一项 True；[2,2] → 全 False

边界条件：空列返回空 bool Series；保留索引和列名。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 11. Group Statistics

- 难度：Medium
- 知识点：groupby, agg
- 文件：[exercises/groupby_merge.py](exercises/groupby_merge.py)

```python
def group_statistics(df: pd.DataFrame) -> pd.DataFrame
```

输入列 category、amount；按 category 分组（缺失组丢弃），输出 sum、mean、count；category 为排序索引。

输入输出示例：A:1,A:3 → A sum=4 mean=2 count=2；空输入 → 空结果

边界条件：amount 的 NaN 不参与 count；分类列为普通字符串。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 12. Group Transformation

- 难度：Medium
- 知识点：transform
- 文件：[exercises/groupby_merge.py](exercises/groupby_merge.py)

```python
def group_transform(df: pd.DataFrame) -> pd.DataFrame
```

输入 category、amount；返回副本，新增 category_mean 为同类别 amount 均值，保持行顺序和索引。

输入输出示例：A:1,A:3 → category_mean=[2,2]；B:8 → 8

边界条件：缺失类别的均值为 NaN；空输入支持。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 13. Merge Tables

- 难度：Medium
- 知识点：merge, validate
- 文件：[exercises/groupby_merge.py](exercises/groupby_merge.py)

```python
def merge_tables(left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame
```

按 user_id 左连接，right 的 user_id 必须唯一，使用 validate=many_to_one，保留左表顺序。

输入输出示例：left id=[1,2],right id=[1] → 两行，第二行右列缺失；空左表 → 空表

边界条件：重复右键抛 pd.errors.MergeError；列重名使用默认 _x/_y。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 14. Pivot Data

- 难度：Medium
- 知识点：pivot_table
- 文件：[exercises/groupby_merge.py](exercises/groupby_merge.py)

```python
def create_pivot(df: pd.DataFrame) -> pd.DataFrame
```

输入 city、category、amount；以 city 为索引、category 为列，求销售额 sum，缺失组合填 0，排序行列。

输入输出示例：X,A:2 与 X,B:3 → X 行 [2,3]；同组合多行求和

边界条件：空表支持；使用 observed=True。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 15. Rolling Average

- 难度：Medium
- 知识点：rolling
- 文件：[exercises/groupby_merge.py](exercises/groupby_merge.py)

```python
def rolling_average(df: pd.DataFrame, window: int) -> pd.DataFrame
```

输入按时间排好的 amount 列；返回副本，增加 rolling_mean，使用 window 和 min_periods=1；不重新排序。

输入输出示例：[1,3,5],2 → [1,2,4]；[],2 → []

边界条件：window≤0 抛 ValueError；缺失数值按 Pandas rolling 规则。

提示：先运行对应测试，理解返回结构，再查官方文档。
