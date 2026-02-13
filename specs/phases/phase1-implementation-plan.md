# Phase I - Implementation Plan

> Last Updated: 2026-02-12
> Version: 1.0.0
> Status: In Progress

## References

- @specs/phases/phase1.md
- @specs/features/todo.md

## Overview

This document outlines the implementation plan for Phase I - Console Todo App.

## Implementation Strategy

Following clean architecture principles, we'll implement from the bottom up:
1. Domain layer (entities, repository interface)
2. Infrastructure layer (in-memory repository)
3. Use case layer (business logic)
4. CLI layer (user interface)

This approach ensures that each layer depends only on abstractions from lower layers.

## Step-by-Step Implementation

### Step 1: Project Setup

**Tasks:**
1. Create directory structure
2. Initialize UV project
3. Create pyproject.toml
4. Create __init__.py files

**Commands:**
```bash
mkdir -p phase1/src/{cli,domain,use_cases,infrastructure}
cd phase1
uv init --no-readme
```

**pyproject.toml:**
```toml
[project]
name = "todo-cli"
version = "0.1.0"
description = "Console Todo Application - Phase I"
requires-python = ">=3.13"
dependencies = []

[project.scripts]
todo = "todo_cli.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = []
```

### Step 2: Domain Layer

**Files to create:**
- `src/domain/__init__.py`
- `src/domain/todo.py`
- `src/domain/repository.py`

**Implementation details:**
- Todo dataclass with id, title, description, completed, created_at
- TodoRepository abstract base class with CRUD methods
- Type hints throughout
- Docstrings for all classes and methods

### Step 3: Infrastructure Layer

**Files to create:**
- `src/infrastructure/__init__.py`
- `src/infrastructure/in_memory_repository.py`

**Implementation details:**
- InMemoryTodoRepository implements TodoRepository
- Uses dict for storage (key: id, value: Todo)
- Implements all abstract methods
- Generates UUID for new todos

### Step 4: Use Cases Layer

**Files to create:**
- `src/use_cases/__init__.py`
- `src/use_cases/add_todo.py`
- `src/use_cases/list_todos.py`
- `src/use_cases/update_todo.py`
- `src/use_cases/delete_todo.py`
- `src/use_cases/complete_todo.py`

**Implementation details:**
- Each use case is a class with execute() method
- Depends on TodoRepository via dependency injection
- Validates input before operations
- Returns results or raises ValueError for errors

### Step 5: CLI Layer

**Files to create:**
- `src/cli/__init__.py`
- `src/cli/commands.py`
- `src/main.py`

**Implementation details:**
- Use argparse for CLI argument parsing
- Commands for: add, list, update, delete, complete, incomplete, help
- Formatted output for todos with status indicators
- User-friendly error messages

### Step 6: Documentation

**Files to create:**
- `README.md` - Installation and usage instructions
- `CLAUDE.md` - AI assistant context

**README.md content:**
- Project description
- Installation instructions (uv sync, uv run todo)
- Usage examples for all commands
- Project structure

**CLAUDE.md content:**
- Project overview
- Architecture description
- Important file locations
- Development workflow

## Implementation Tasks

### Task 1: Create Project Structure
- [ ] Create all directories
- [ ] Initialize UV project
- [ ] Create pyproject.toml
- [ ] Create all __init__.py files

### Task 2: Implement Domain Layer
- [ ] Create Todo entity
- [ ] Create TodoRepository interface
- [ ] Add type hints and docstrings

### Task 3: Implement Infrastructure Layer
- [ ] Create InMemoryTodoRepository
- [ ] Implement CRUD methods
- [ ] Add UUID generation

### Task 4: Implement Use Cases
- [ ] AddTodoUseCase
- [ ] ListTodosUseCase
- [ ] UpdateTodoUseCase
- [ ] DeleteTodoUseCase
- [ ] CompleteTodoUseCase

### Task 5: Implement CLI
- [ ] Create argument parser
- [ ] Implement all commands
- [ ] Add formatted output
- [ ] Add error handling

### Task 6: Create Documentation
- [ ] Write README.md
- [ ] Write CLAUDE.md
- [ ] Add usage examples

### Task 7: Testing & Validation
- [ ] Manual testing of all commands
- [ ] Validate against acceptance criteria
- [ ] Fix any issues found

## Acceptance Criteria Checklist

### Functional Requirements
- [ ] Can add a task with title and optional description
- [ ] Can view all tasks with status indicators
- [ ] Can update task title and/or description
- [ ] Can delete a task
- [ ] Can mark task as complete
- [ ] Can mark task as incomplete
- [ ] All commands work in-memory
- [ ] No persistence required

### Non-Functional Requirements
- [ ] Clean architecture separation of concerns
- [ ] Type hints throughout
- [ ] Docstrings for all public methods
- [ ] Clear CLI help text
- [ ] User-friendly error messages

### Documentation Requirements
- [ ] README.md with installation and usage instructions
- [ ] CLAUDE.md with AI assistant context
- [ ] pyproject.toml with project metadata

## Testing Plan

### Manual Testing Commands

1. **Add tasks:**
```bash
uv run todo add "Buy groceries" --description "Milk, eggs, bread"
uv run todo add "Clean room"
```

2. **List tasks:**
```bash
uv run todo list
```

3. **Update task:**
```bash
uv run todo update 1 --title "Buy groceries and snacks"
uv run todo update 1 --description "Milk, eggs, bread, snacks"
```

4. **Complete task:**
```bash
uv run todo complete 1
```

5. **Mark incomplete:**
```bash
uv run todo incomplete 1
```

6. **Delete task:**
```bash
uv run todo delete 1
```

### Expected Behaviors

| Command | Expected Output |
|---------|----------------|
| `todo add "Test"` | "Added: Test" with generated ID |
| `todo list` (empty) | "No tasks found" |
| `todo list` (with tasks) | List with [✓] and [ ] indicators |
| `todo update 999` | "Task not found" |
| `todo delete 999` | "Task not found" |

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Clean architecture violations | Code review against architectural specs |
| Missing type hints | Use mypy for static type checking |
| Poor error messages | User testing of error scenarios |
| Missing documentation | Documentation review before completion |

## Success Criteria

- All functional requirements met
- Code follows clean architecture principles
- Documentation is complete and accurate
- CLI works as specified without errors
- No breaking changes to domain layer (for Phase II migration)