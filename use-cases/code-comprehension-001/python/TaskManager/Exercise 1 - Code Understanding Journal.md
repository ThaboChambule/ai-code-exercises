# Exercise 1: Code Understanding Journal

## 0) Initial scan (structure only)
- Main entry point: CLI in [cli.py](cli.py)
- Core logic: task orchestration in [task_manager.py](task_manager.py)
- Domain models: task, status, priority in [models.py](models.py)
- Persistence: JSON storage and serialization in [storage.py](storage.py)
- Tests: [tests/](tests/) (not explored in depth)

## 1) Feature understanding: task creation and status updates
### Files involved
- [cli.py](cli.py)
- [task_manager.py](task_manager.py)
- [models.py](models.py)
- [storage.py](storage.py)

### Main components involved
- `TaskManager` orchestrates operations and validates inputs.
- `Task` holds task data and behavior (`update()`, `mark_as_done()`).
- `TaskStorage` handles CRUD and persistence to JSON.
- `TaskEncoder`/`TaskDecoder` serialize/deserialize tasks.
- CLI maps user commands to `TaskManager` methods.

### Execution flow (create task)
1. CLI parses `create` command in [cli.py](cli.py).
2. `TaskManager.create_task()` validates date and converts priority in [task_manager.py](task_manager.py).
3. `Task` instance is created in [models.py](models.py).
4. `TaskStorage.add_task()` stores the task in memory and persists to disk in [storage.py](storage.py).
5. CLI prints the returned task id.

### Execution flow (update status)
1. CLI parses `status` command in [cli.py](cli.py).
2. `TaskManager.update_task_status()` converts input to `TaskStatus` in [task_manager.py](task_manager.py).
3. If status is `DONE`, it loads the task and calls `Task.mark_as_done()` in [models.py](models.py), then calls `TaskStorage.save()`.
4. Otherwise it calls `TaskStorage.update_task()` which triggers `Task.update()` and saves in [storage.py](storage.py).

### Data storage and retrieval
- Tasks are kept in-memory in a dictionary keyed by task id in `TaskStorage`.
- Persistence is a JSON file (default tasks.json) using `TaskEncoder` and `TaskDecoder` in [storage.py](storage.py).
- Date fields are serialized as ISO 8601 strings and restored via `datetime.fromisoformat`.

### Interesting design patterns
- Simple Repository pattern: `TaskStorage` abstracts persistence from the rest of the app.
- Encapsulation of domain logic in `Task` methods like `mark_as_done()`.

## 2) Guided exploration: task prioritization
### Initial understanding
- Priority is an enum with 4 levels; it is set at creation and can be updated via CLI.

### Guided questions used
1. Where is priority defined and how is it represented in storage?
2. How does the CLI validate priority values?
3. How are tasks filtered by priority?
4. Does priority affect any other behavior (sorting, overdue, stats)?

### What I discovered
- Definition: `TaskPriority` enum in [models.py](models.py). Stored as integer values in JSON via `TaskEncoder` in [storage.py](storage.py).
- CLI validation: `--priority` uses `choices=[1,2,3,4]` in [cli.py](cli.py).
- Filtering: `TaskStorage.get_tasks_by_priority()` used by `TaskManager.list_tasks()` in [storage.py](storage.py) and [task_manager.py](task_manager.py).
- No sorting or scheduling behavior is tied to priority; it only affects filtering, display and stats in [cli.py](cli.py) and [task_manager.py](task_manager.py).

### Misconceptions clarified
- I expected priority to impact ordering or overdue checks, but it does not. It is used only for filtering, display, and statistics.

## 3) Mapping data flow: marking a task as complete
### Entry points and components
- Entry point: CLI command `status <task_id> done` in [cli.py](cli.py).
- Orchestration: `TaskManager.update_task_status()` in [task_manager.py](task_manager.py).
- State mutation: `Task.mark_as_done()` in [models.py](models.py).
- Persistence: `TaskStorage.save()` in [storage.py](storage.py).

### Data flow diagram (text)
User CLI → `TaskManager.update_task_status()` → `TaskStorage.get_task()` → `Task.mark_as_done()` → `TaskStorage.save()` → JSON file

### State changes
- `Task.status` → `DONE`
- `Task.completed_at` set to current time
- `Task.updated_at` set to completion time

### Potential points of failure
- Invalid task id: `get_task()` returns None.
- JSON save errors: `TaskStorage.save()` exception handling prints an error.
- Invalid status input: prevented by CLI choices.

### Persistence
- The updated task list is written to JSON using `TaskEncoder` in [storage.py](storage.py).

## 4) Reflection and presentation notes
### High-level architecture
- CLI layer in [cli.py](cli.py)
- Domain logic in [task_manager.py](task_manager.py) and [models.py](models.py)
- Persistence layer in [storage.py](storage.py)

### How the three key features work
- Creation: CLI → `TaskManager.create_task()` → `TaskStorage.add_task()` → JSON
- Prioritization: `TaskPriority` enum + CLI validation + filtering via storage
- Completion: CLI → `TaskManager.update_task_status()` → `Task.mark_as_done()` → save

### Interesting pattern
- Repository-like storage abstraction in `TaskStorage`.

### Most challenging part
- Understanding where persistence actually happens (update vs. mark as done). The prompts helped trace the exact save points.
