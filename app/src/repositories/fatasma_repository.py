from src.models.fantasma import Fantasma
from typing import List, Optional
from abc import ABC, abstractmethod


class FantasmaRepository(ABC):
    """Interface para repositório de Fantasma"""

    @abstractmethod
    def find_all(self) -> List[Fantasma]:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Fantasma]:
        pass

    @abstractmethod
    def save(self, fantasma: Fantasma) -> Fantasma:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def find_by_tipo(self, tipo: str) -> List[Fantasma]:
        pass

    @abstractmethod
    def find_by_chunk(self, chunk_nome: str) -> List[Fantasma]:
        pass


class FantasmaRepositoryImpl(FantasmaRepository):
    def __init__(self):
        self._fantasmas: List[Fantasma] = []

    def find_all(self) -> List[Fantasma]:
        return self._fantasmas

    def find_by_id(self, id: int) -> Optional[Fantasma]:
        return next((f for f in self._fantasmas if f.id == id), None)

    def save(self, fantasma: Fantasma) -> Fantasma:
        existente = self.find_by_id(fantasma.id)
        if existente:
            self._fantasmas.remove(existente)
        self._fantasmas.append(fantasma)
        return fantasma

    def delete(self, id: int) -> bool:
        fantasma = self.find_by_id(id)
        if fantasma:
            self._fantasmas.remove(fantasma)
            return True
        return False

    def find_by_tipo(self, tipo: str) -> List[Fantasma]:
        return [f for f in self._fantasmas if f.tipo == tipo]

    def find_by_chunk(self, chunk_nome: str) -> List[Fantasma]:
        return [f for f in self._fantasmas if f.chunk == chunk_nome]
