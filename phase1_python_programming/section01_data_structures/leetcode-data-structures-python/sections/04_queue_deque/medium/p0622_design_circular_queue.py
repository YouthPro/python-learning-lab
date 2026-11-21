"""LeetCode 622 (Medium). Design Circular Queue."""


class MyCircularQueue:
    def __init__(self, k: int) -> None:
        raise NotImplementedError

    def enQueue(self, value: int) -> bool:
        raise NotImplementedError

    def deQueue(self) -> bool:
        raise NotImplementedError

    def Front(self) -> int:
        raise NotImplementedError

    def Rear(self) -> int:
        raise NotImplementedError

    def isEmpty(self) -> bool:
        raise NotImplementedError

    def isFull(self) -> bool:
        raise NotImplementedError
