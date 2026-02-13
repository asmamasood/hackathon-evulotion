# Todo CLI - Phase I

A console-based Todo application with clean architecture.

## Installation

```bash
uv sync
```

## Usage

### Add a task

```bash
uv run todo add "Buy groceries" --description "Milk, eggs, bread"
```

### List all tasks

```bash
uv run todo list
```

### Update a task

```bash
uv run todo update 1 --title "Buy groceries and snacks"
uv run todo update 1 --description "Milk, eggs, bread, snacks"
```

### Mark a task as complete

```bash
uv run todo complete 1
```

### Mark a task as incomplete

```bash
uv run todo incomplete 1
```

### Delete a task

```bash
uv run todo delete 1
```

## Architecture

This application follows clean architecture principles:

- **Domain Layer**: Core business entities and interfaces
- **Infrastructure Layer**: Repository implementations
- **Use Cases**: Business logic and operations
- **CLI Layer**: Command-line interface

## Development

Run the application directly:

```bash
python -m todo_cli.main --help
```