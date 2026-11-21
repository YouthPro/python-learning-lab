"""LeetCode 297 (Hard). Serialize and Deserialize Binary Tree."""

from common.nodes import TreeNode


class Codec:
    def __init__(self) -> None:
        raise NotImplementedError

    def serialize(self, root: TreeNode | None) -> str:
        raise NotImplementedError

    def deserialize(self, data: str) -> TreeNode | None:
        raise NotImplementedError
