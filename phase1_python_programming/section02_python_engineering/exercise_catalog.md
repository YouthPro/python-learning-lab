# Section 02 练习题目录

约定优先于习惯性题解：按这里的排序、返回类型、缺失值和边界行为实现。

## 01. List Files Recursively

- 难度：Easy
- 知识点：pathlib
- 文件：[exercises/file_operations.py](exercises/file_operations.py)

```python
def list_files(path: str | Path) -> list[Path]
```

递归列出普通文件，返回按完整路径字符串排序的 Path 列表，不包含目录。

输入输出示例：含 a.txt 和 sub/b.txt → [a.txt,sub/b.txt]；空目录 → []

边界条件：不存在路径抛 FileNotFoundError；根路径必须为目录，不跟随目录符号链接。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 02. CSV Reader

- 难度：Easy
- 知识点：csv.DictReader
- 文件：[exercises/file_operations.py](exercises/file_operations.py)

```python
def read_csv(path: str | Path) -> list[dict[str, str]]
```

读取带表头 UTF-8 CSV，保留所有值为字符串，返回行字典列表。

输入输出示例：a,b\n1,2 → [{a:"1",b:"2"}]；仅表头 → []

边界条件：空文件返回 []；支持带逗号的引号字段。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 03. JSON Normalizer

- 难度：Medium
- 知识点：dict, recursion, json
- 文件：[exercises/file_operations.py](exercises/file_operations.py)

```python
def normalize_json(data: object) -> object
```

递归按键名排序字典，并去掉字符串两端空白；列表保持顺序；数值、布尔和 None 保持不变。不是扁平化操作。

输入输出示例：{b:" x ",a:1} → {a:1,b:"x"}；[" y "] → ["y"]

边界条件：键保证为字符串；空容器保持原类型；不修改输入。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 04. File Hash Calculator

- 难度：Medium
- 知识点：hashlib, chunked I/O
- 文件：[exercises/file_operations.py](exercises/file_operations.py)

```python
def calculate_file_hash(path: str | Path) -> str
```

分块计算文件 SHA-256 十六进制摘要。

输入输出示例：内容 b"abc" → ba7816bf…15ad；空文件 → e3b0c442…b855

边界条件：返回 64 字符；不整体读入；缺失文件传播异常。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 05. Duplicate File Finder

- 难度：Medium
- 知识点：pathlib, hashlib
- 文件：[exercises/file_operations.py](exercises/file_operations.py)

```python
def find_duplicates(directory: str | Path) -> list[list[Path]]
```

递归找出内容完全相同的文件组，仅返回组内至少两个文件的组；组内路径排序，组间按首路径排序。

输入输出示例：a、b 内容相同 → [[a,b]]；无重复 → []

边界条件：空文件也可重复；不能仅按文件名或大小判断。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 06. Safe Batch Rename

- 难度：Medium
- 知识点：pathlib, exceptions
- 文件：[exercises/file_operations.py](exercises/file_operations.py)

```python
def batch_rename(directory: str | Path, mapping: dict[str, str], dry_run: bool = True) -> list[tuple[Path, Path]]
```

mapping 只接受目录直接子文件的文件名。验证所有源存在、目标唯一且不存在，返回源/目标计划；dry_run=False 才执行。身份映射允许并跳过。交换或循环重命名不支持。

输入输出示例：{a:b} 默认只返回 [(root/a,root/b)]；{} → []

边界条件：拒绝绝对路径、..、目录、覆盖、重复目标；验证失败必须零修改；不必处理并发进程修改目录。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 07. Logged JSON Loader

- 难度：Medium
- 知识点：custom exception, try/except, logging
- 文件：[exercises/error_handling.py](exercises/error_handling.py)

```python
def load_json_safely(path: str | Path, logger: logging.Logger) -> object
```

读取 UTF-8 JSON，文件或 JSON 错误时记录 ERROR 并抛自定义 DatasetError，使用 raise ... from ... 保留原因。

输入输出示例：合法 {"a":1} → dict；非法 JSON → DatasetError + ERROR 日志

边界条件：成功不记 ERROR；缺失路径、空文件均为失败。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 08. Dataset Record

- 难度：Medium
- 知识点：dataclass, type hints
- 文件：[exercises/oop_and_testing.py](exercises/oop_and_testing.py)

```python
@dataclass
class DatasetRecord:
    row_id: int
    values: dict

    def __len__(self) -> int: ...
```

实现 dataclass，字段 row_id:int 和 values:dict；__len__ 返回 values 列数；使用默认 dataclass __repr__ 和相等语义。

输入输出示例：DatasetRecord(1,{a:2}) 的 len → 1；空 values → 0

边界条件：每条记录值独立；字段必须有类型注解。

提示：先运行对应测试，理解返回结构，再查官方文档。

## 09. Dataset Collection

- 难度：Medium
- 知识点：composition, special methods
- 文件：[exercises/oop_and_testing.py](exercises/oop_and_testing.py)

```python
class DatasetCollection:
    def __init__(self, records: Iterable) -> None: ...
    def add(self, record: DatasetRecord) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[DatasetRecord]: ...
    def __repr__(self) -> str: ...
```

实现组合类，将 DatasetRecord 保存在内部。支持 len、迭代；__repr__ 严格为 DatasetCollection(rows=N)；add(record) 追加记录。

输入输出示例：空集合 repr → DatasetCollection(rows=0)；add 一项后 len → 1

边界条件：接受一次性迭代器；构造时复制输入容器。

提示：先运行对应测试，理解返回结构，再查官方文档。
