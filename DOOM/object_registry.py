from typing import Dict, Type, Any


class ObjectRegistry:
    def __init__(self) -> None:
        self.lookup: Dict[str, Any] = {}
    
    def register(self, c: Type[Any]) -> Type[Any]:
        self.lookup[c.NAME] = c
        return c

    def has(self, name: str) -> bool:
        return name in self.lookup

    def get(self, name: str) -> Type[Any]:
        return self.lookup[name]
