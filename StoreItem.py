from typing import TypeVar, Generic, List
T = TypeVar('T')


class StoreItem(Generic[T]):

    def __init__(self,data:T) -> None:
        self.data: T = data

    def getState(self) -> T:
        return self.data
 