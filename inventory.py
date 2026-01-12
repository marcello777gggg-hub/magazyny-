import json
from pathlib import Path
from typing import Dict


class Inventory:
    def __init__(self, path: str = "data.json"):
        self.path = Path(path)
        self._data: Dict[str, int] = {}
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            try:
                with self.path.open("r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = {}
        else:
            self._data = {}

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def add_product(self, name: str, qty: int) -> None:
        if qty <= 0:
            raise ValueError("Ilość musi być dodatnia")
        self._data[name] = self._data.get(name, 0) + qty
        self._save()

    def remove_product(self, name: str, qty: int) -> None:
        if qty <= 0:
            raise ValueError("Ilość musi być dodatnia")
        if name not in self._data:
            raise KeyError(f"Produkt '{name}' nie istnieje")
        if self._data[name] < qty:
            raise ValueError("Brak wystarczającej ilości do usunięcia")
        self._data[name] -= qty
        if self._data[name] == 0:
            del self._data[name]
        self._save()

    def get_stock(self) -> Dict[str, int]:
        return dict(self._data)
