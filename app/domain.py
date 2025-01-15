from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID


@dataclass
class Todo:
    """Represents a single todo item"""

    id: UUID
    title: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    @classmethod
    def create(cls, title: str) -> "Todo":
        """Factory method to create a new todo"""
        return cls(
            id=UUID(int=0),  # TODO: Generate real UUIDs
            title=title,
            created_at=datetime.utcnow(),
        )

    def complete(self) -> None:
        """Mark the todo as completed"""
        self.completed_at = datetime.utcnow()

    def uncomplete(self) -> None:
        """Mark the todo as not completed"""
        self.completed_at = None


@dataclass
class FlashMessage:
    """Represents a flash message to display to the user"""

    message: str
    category: str  # success, error, info, warning


class TodoList:
    """Manages a collection of todos"""

    def __init__(self) -> None:
        self._todos: List[Todo] = []

    def add(self, todo: Todo) -> None:
        """Add a todo to the list"""
        self._todos.append(todo)

    def remove(self, todo_id: UUID) -> None:
        """Remove a todo from the list"""
        self._todos = [t for t in self._todos if t.id != todo_id]

    def get(self, todo_id: UUID) -> Optional[Todo]:
        """Get a specific todo by ID"""
        return next((t for t in self._todos if t.id == todo_id), None)

    def all(self) -> List[Todo]:
        """Get all todos"""
        return sorted(self._todos, key=lambda t: t.created_at)

    def complete(self, todo_id: UUID) -> None:
        """Mark a todo as completed"""
        todo = self.get(todo_id)
        if todo:
            todo.complete()

    def uncomplete(self, todo_id: UUID) -> None:
        """Mark a todo as not completed"""
        todo = self.get(todo_id)
        if todo:
            todo.uncomplete()


@dataclass
class Page:
    """Represents page-level metadata and content"""

    title: str
    flash_messages: List[FlashMessage]
    todos: TodoList

    @classmethod
    def create(
        cls,
        title: str,
        todos: Optional[TodoList] = None,
        flash_messages: Optional[List[FlashMessage]] = None,
    ) -> "Page":
        """Factory method to create a new page"""
        return cls(
            title=title,
            flash_messages=flash_messages or [],
            todos=todos or TodoList(),
        )
