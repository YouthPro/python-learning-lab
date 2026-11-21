"""Local equivalents of the LeetCode list and tree nodes."""

from __future__ import annotations


class ListNode:
    """A node in a singly linked list."""

    def __init__(self, val: int = 0, next: ListNode | None = None) -> None:
        self.val = val
        self.next = next


class TreeNode:
    """A node in a binary tree."""

    def __init__(
        self,
        val: int = 0,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right
