# Phase I - Console Todo App Specification

> Last Updated: 2026-02-12
> Version: 1.0.0
> Status: In Progress

## Overview

Phase I builds a Python CLI Todo application that stores tasks in memory only. This establishes the foundation for all subsequent phases.

## References

- @specs/overview.md
- @specs/architecture.md

## Objectives

1. Create a functional console-based Todo application
2. Implement clean architecture patterns from the start
3. Store tasks in memory (no persistence)
4. Use UV for Python package management
5. Follow spec-driven development workflow

## Features (Basic Level - ALL REQUIRED)

### 1. Add Task
- Accept title (required)
- Accept description (optional)
- Generate unique ID
- Default status: incomplete
- Display confirmation message

### 2. View Tasks
- Display all tasks
- Show status indicator ([✓] for complete, [ ] for incomplete)
- Display task ID, title, and description
- Handle empty list gracefully

### 3. Update Task
- Accept task ID
- Accept new title (optional)
- Accept new description (optional)
- Update task if found
- Display error message if not found

### 4. Delete Task
- Accept task ID
- Delete task if found
- Display confirmation message
- Display error message if not found

### 5. Mark Task Complete/Incomplete
- Accept task ID
- Toggle task completion status
- Display confirmation message
- Display error message if not found

## Requirements

### Technology Stack
- Python 3.13+
- UV package manager
- No external dependencies beyond standard library

### Project Structure
```
phase1/
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── cli/
│   │   ├── __init__.py
│   │   └── commands.py      # CLI command handlers
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── todo.py          # Todo entity
│   │   └── repository.py    # Repository interface
│   ├── use_cases/
│   │   ├── __init__.py
│   │   ├── add_todo.py      # Add todo use case
│   │   ├── list_todos.py    # List todos use case
│   │   ├── update_todo.py   # Update todo use case
│   │   ├── delete_todo.py   # Delete todo use case
│   │   └── complete_todo.py # Complete todo use case
│   └── infrastructure/
│       ├── __init__.py
│       └── in_memory_repository.py
├── pyproject.toml
├── README.md
└── CLAUDE.md
```

### Domain Model

#### Todo Entity
```python
@dataclass
class Todo:
    id: str
    title: str
    description: str
    completed: bool
    created_at: datetime
```

#### TodoRepository Interface
```python
class TodoRepository(ABC):
    @abstractmethod
    def add(self, todo: Todo) -> Todo: ...

    @abstractmethod
    def get_all(self) -> list[Todo]: ...

    @abstractmethod
    def get_by_id(self, todo_id: str) -> Todo | None: ...

    @abstractmethod
    def update(self, todo: Todo) -> Todo: ...

    @abstractmethod
    def delete(self, todo_id: str) -> bool: ...
```

### Use Cases

#### AddTodoUseCase
- Input: title (str), description (str | None)
- Output: Todo
- Validates input (title not empty)
- Generates unique ID
- Sets default values
- Persists via repository

#### ListTodosUseCase
- Input: None
- Output: list[Todo]
- Retrieves all todos from repository
- Returns empty list if none exist

#### UpdateTodoUseCase
- Input: todo_id (str), title (str | None), description (str | None)
- Output: Todo | None
- Validates input
- Retrieves existing todo
- Updates provided fields
- Persists changes

#### DeleteTodoUseCase
- Input: todo_id (str)
- Output: bool (success)
- Validates input
- Retrieves existing todo
- Deletes from repository

#### CompleteTodoUseCase
- Input: todo_id (str)
- Output: Todo | None
- Validates input
- Retrieves existing todo
- Toggles completed status
- Persists changes

### CLI Interface

#### Command Structure
```
todo <command> [options]

Commands:
  add <title> [--description <desc>]    Add a new task
  list                                  List all tasks
  update <id> [--title <title>]         Update a task
         [--description <desc>]
  delete <id>                           Delete a task
  complete <id>                         Mark task as complete
  incomplete <id>                       Mark task as incomplete
  help                                  Show help
```

#### Output Format
```
[✓] ID: 1 - Title: Buy groceries (optional description)
[ ] ID: 2 - Title: Clean room
```

### Error Handling
- Display clear, user-friendly error messages
- Handle invalid IDs gracefully
- Handle empty input where applicable
- No stack traces shown to user

## Acceptance Criteria

### Functional Requirements
- [x] Can add a task with title and optional description
- [x] Can view all tasks with status indicators
- [x] Can update task title and/or description
- [x] Can delete a task
- [x] Can mark task as complete
- [x] Can mark task as incomplete
- [x] All commands work in-memory
- [x] No persistence required

### Non-Functional Requirements
- [x] Clean architecture separation of concerns
- [x] Type hints throughout
- [x] Docstrings for all public methods
- [x] Clear CLI help text
- [x] User-friendly error messages

### Documentation Requirements
- [x] README.md with installation and usage instructions
- [x] CLAUDE.md with AI assistant context
- [x] pyproject.toml with project metadata

## Deliverables

1. Constitution file (CLAUDE.md at root)
2. `/specs` with full history (this spec and related specs)
3. `/src` Python code with clean architecture
4. README.md with installation and usage
5. Working CLI demo

## Success Metrics

- All required features implemented
- Code follows clean architecture principles
- Documentation is complete and accurate
- CLI works as specified
- No breaking changes to domain layer for future phases

## Constraints

- No external libraries allowed (standard library only)
- No file I/O or persistence
- No networking or API calls
- No user authentication (Phase I only)

## Future Considerations

### Phase II Migration Path
- Domain layer (Todo entity, TodoRepository interface) remains unchanged
- Infrastructure layer adds PostgreSQL repository implementation
- CLI layer replaced/replaced with REST API
- New frontend layer (Next.js) added

### Design Decisions for Phase I
- Repository interface designed to support PostgreSQL implementation
- Use cases isolated for reuse in Phase II
- In-memory repository as reference implementation