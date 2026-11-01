from __future__ import annotations

from pathlib import Path


def list_files(path: str | Path) -> list[Path]:
    """01. List Files Recursively
    Difficulty: Easy
    知识点: pathlib

    递归列出普通文件，返回按完整路径字符串排序的 Path 列表，不包含目录。

    示例: 含 a.txt 和 sub/b.txt → [a.txt,sub/b.txt]；空目录 → []
    边界: 不存在路径抛 FileNotFoundError；根路径必须为目录，不跟随目录符号链接。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def read_csv(path: str | Path) -> list[dict[str, str]]:
    """02. CSV Reader
    Difficulty: Easy
    知识点: csv.DictReader

    读取带表头 UTF-8 CSV，保留所有值为字符串，返回行字典列表。

    示例: a,b\n1,2 → [{a:"1",b:"2"}]；仅表头 → []
    边界: 空文件返回 []；支持带逗号的引号字段。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def normalize_json(data: object) -> object:
    """03. JSON Normalizer
    Difficulty: Medium
    知识点: dict, recursion, json

    递归按键名排序字典，并去掉字符串两端空白；列表保持顺序；数值、布尔和 None 保持不变。不是扁平化操作。

    示例: {b:" x ",a:1} → {a:1,b:"x"}；[" y "] → ["y"]
    边界: 键保证为字符串；空容器保持原类型；不修改输入。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def calculate_file_hash(path: str | Path) -> str:
    """04. File Hash Calculator
    Difficulty: Medium
    知识点: hashlib, chunked I/O

    分块计算文件 SHA-256 十六进制摘要。

    示例: 内容 b"abc" → ba7816bf…15ad；空文件 → e3b0c442…b855
    边界: 返回 64 字符；不整体读入；缺失文件传播异常。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def find_duplicates(directory: str | Path) -> list[list[Path]]:
    """05. Duplicate File Finder
    Difficulty: Medium
    知识点: pathlib, hashlib

    递归找出内容完全相同的文件组，仅返回组内至少两个文件的组；组内路径排序，组间按首路径排序。

    示例: a、b 内容相同 → [[a,b]]；无重复 → []
    边界: 空文件也可重复；不能仅按文件名或大小判断。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError


def batch_rename(
    directory: str | Path, mapping: dict[str, str], dry_run: bool = True
) -> list[tuple[Path, Path]]:
    """06. Safe Batch Rename
    Difficulty: Medium
    知识点: pathlib, exceptions

    mapping 只接受目录直接子文件的文件名。验证所有源存在、目标唯一且不存在，返回源/目标计划；dry_run=False 才执行。身份映射允许并跳过。交换或循环重命名不支持。

    示例: {a:b} 默认只返回 [(root/a,root/b)]；{} → []
    边界: 拒绝绝对路径、..、目录、覆盖、重复目标；验证失败必须零修改；不必处理并发进程修改目录。
    Hint: 优先查阅本 Section 官方参考资料；不要修改测试约定。
    """

    # TODO: Implement your solution
    raise NotImplementedError
