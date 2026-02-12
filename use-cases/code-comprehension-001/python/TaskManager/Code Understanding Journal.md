# Code Understanding Journal

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

---

# Exercise 2: Algorithm Deconstruction - Task Priority Sorting

## Algorithm Selected
**Task Priority Sorting Algorithm** - A weighted scoring system that sorts tasks based on multiple factors including priority level, due date proximity, completion status, tags, and recent activity.

## Algorithm Breakdown

### High-Level Purpose
This algorithm calculates a numeric score for each task and sorts them in descending order (highest priority first). The scoring system combines multiple factors to provide intelligent task prioritization beyond simple priority levels.

### Component Analysis

#### 1. `calculate_task_score(task)` Function

**Purpose**: Calculate a single numeric score representing task urgency/importance.

**Scoring Components**:

```
Base Score Calculation:
├── Priority Weight (10-60 points)
│   ├── LOW (1):      10 points
│   ├── MEDIUM (2):   20 points
│   ├── HIGH (4):     40 points
│   └── URGENT (6):   60 points
│
├── Due Date Factor (0-35 points)
│   ├── Overdue:           +35 points
│   ├── Due today:         +20 points
│   ├── Due in ≤2 days:    +15 points
│   └── Due in ≤7 days:    +10 points
│
├── Status Penalty/Adjustment
│   ├── DONE:              -50 points (push to bottom)
│   └── REVIEW:            -15 points (reduce priority)
│
├── Special Tags Boost (+8 points)
│   └── "blocker", "critical", "urgent" tags
│
└── Recent Activity Boost (+5 points)
    └── Updated within last day
```

**Score Range**: 
- Minimum: -40 (completed low-priority task)
- Maximum: ~108 (urgent overdue task with critical tags, recently updated)

**Execution Flow**:
1. Start with base priority weight (multiply enum value by 10)
2. Check if due_date exists and calculate days until due
3. Add bonus points based on urgency (overdue > today > soon)
4. Apply status penalties (completed tasks sink to bottom)
5. Check for special tags and boost score
6. Check last update time and boost if recent

#### 2. `sort_tasks_by_importance(tasks)` Function

**Purpose**: Sort a list of tasks by their calculated scores (highest first).

**Execution Flow**:
1. Create list of tuples: `[(score, task), (score, task), ...]`
2. Sort by score using Python's `sorted()` with `reverse=True`
3. Extract just the task objects from tuples
4. Return sorted list

**Key Design Decision**: Calculate scores once before sorting (efficient - O(n log n) instead of calculating multiple times during sort comparisons).

#### 3. `get_top_priority_tasks(tasks, limit=5)` Function

**Purpose**: Get the top N most important tasks.

**Execution Flow**:
1. Call `sort_tasks_by_importance()`
2. Slice the first `limit` items
3. Return top N tasks

## Visual Representation

### Data Flow Diagram
```
Input: List of Task objects
         ↓
    For each task:
         ↓
    calculate_task_score()
         ↓
    ┌─────────────────────────────────┐
    │  Score Components Combined:     │
    │  • Base priority × 10           │
    │  • Due date urgency             │
    │  • Status adjustments           │
    │  • Tag bonuses                  │
    │  • Recent activity bonus        │
    └─────────────────────────────────┘
         ↓
    [(score1, task1), (score2, task2), ...]
         ↓
    Sort by score (descending)
         ↓
    Extract tasks from tuples
         ↓
    Output: Sorted task list (highest priority first)
```

### Score Calculation Example

**Example Task**:
- Title: "Fix critical production bug"
- Priority: HIGH (value=4)
- Due date: Tomorrow
- Status: IN_PROGRESS
- Tags: ["critical", "backend"]
- Updated: 3 hours ago

**Score Calculation**:
```
Base priority:     4 × 10 = 40 points
Due date (≤2 days):     = +15 points
Status (in_progress):   = 0 points (no penalty)
Critical tag:           = +8 points
Recent update (<1 day): = +5 points
─────────────────────────────────
TOTAL SCORE:            = 68 points
```

### Algorithm Complexity
- **Time Complexity**: O(n log n) where n = number of tasks
  - Score calculation: O(n)
  - Sorting: O(n log n)
  - Overall: O(n log n) dominated by sort
- **Space Complexity**: O(n) for storing tuples and sorted list

## Key Insights and Learning Points

### 1. Multi-Factor Decision Making
The algorithm doesn't rely on a single criterion but combines multiple signals:
- **Static properties** (priority level)
- **Time-sensitive data** (due dates, recent activity)
- **Workflow state** (status)
- **Contextual metadata** (tags)

This mirrors real-world prioritization where no single factor determines importance.

### 2. Weighted Scoring Design
The weights are carefully balanced:
- Priority provides the base layer (10-60 points)
- Overdue tasks get significant boost (+35) - more than base priority difference
- Completed tasks get strong penalty (-50) ensuring they sink to bottom
- Tags and recent activity provide fine-tuning (+5-8 points)

### 3. Smart Status Handling
The algorithm elegantly handles completed tasks by applying a penalty larger than any possible boost, ensuring they always rank lowest while still being sortable among themselves.

### 4. Efficiency Consideration
Pre-calculating scores and storing in tuples is more efficient than using a key function in sort, especially if scores might be reused.

### 5. Date Handling Edge Case
The algorithm uses `datetime.now()` for calculations, which means:
- Scores are point-in-time calculations
- Re-running same function later produces different scores
- This is intentional - due dates become more urgent over time

## Reflection Questions

### 1. How did the AI's explanation change your understanding?

Initially, I saw this as a simple sorting algorithm. The AI-guided breakdown revealed:
- The sophisticated weighting system balancing multiple concerns
- The intentional design choice to make overdue tasks dominate priority
- The efficiency consideration of pre-calculating scores
- The temporal nature of the scoring (scores change over time)

I understood **what** it did, but not **why** the specific weights were chosen or how they interact.

### 2. What aspects were still difficult to understand?

- **Weight calibration**: Why 35 for overdue vs 20 for today? Are these empirically determined or arbitrary?
- **Tag matching**: Uses simple substring matching (`any()` with `in`) - is this sufficient or could it miss edge cases?
- **Negative scores**: Can a task score go negative (yes, if low priority + completed), and is this intentional?
- **Timezone handling**: `datetime.now()` uses system time - could cause issues in distributed systems

### 3. How would you explain this to another junior developer?

*"Imagine you have a pile of tasks and need to figure out which to work on first. This algorithm gives each task a 'urgency score' by adding up points from different factors:*

*Start with the priority level (10-60 points). Then check if it's overdue - those get a huge boost. Subtract points if it's already done so completed tasks sink to the bottom. Add small bonuses for special tags like 'critical' or if you just worked on it recently.*

*Finally, sort all tasks by their scores, highest first. So an overdue urgent task with critical tags will beat everything else, while completed tasks appear at the end of your list."*

### 4. Did you test this understanding against AI?

Yes, I would ask the AI:
- "Given these two tasks [provide examples], which would score higher and why?"
- "What happens if a low-priority task is 2 days overdue vs a high-priority task due in a week?"
- "Can you walk through the score calculation for this specific task?"

This validates that I understand not just the code, but the decision logic.

### 5. How might you improve this algorithm?

**Potential Improvements**:

1. **Configurable Weights**: Make weights configurable rather than hardcoded
   ```python
   def calculate_task_score(task, weights=DEFAULT_WEIGHTS):
       score = weights['priority'][task.priority.name] * weights['base_multiplier']
       # ... use weights throughout
   ```

2. **Consider Task Dependencies**: Boost score for tasks blocking others
   ```python
   if task.is_blocking_other_tasks():
       score += 20
   ```

3. **Age Factor**: Old incomplete tasks should gradually increase in priority
   ```python
   days_old = (datetime.now() - task.created_at).days
   if days_old > 30 and task.status != TaskStatus.DONE:
       score += min(days_old // 7, 15)  # Cap at 15 points
   ```

4. **Workload Balancing**: Consider estimated time - quick wins vs long tasks
   ```python
   if task.estimated_minutes and task.estimated_minutes <= 15:
       score += 3  # Boost quick wins
   ```

5. **Diminishing Returns for Very Old Completed Tasks**: 
   ```python
   if task.status == TaskStatus.DONE:
       days_since_completion = (datetime.now() - task.completed_at).days
       score -= min(50, 50 + days_since_completion * 2)  # Fade further over time
   ```

6. **Normalize Scores**: Keep scores in predictable range (0-100) for better interpretability
   ```python
   # Apply sigmoid or min-max normalization
   normalized_score = min(100, max(0, raw_score))
   ```

7. **Add Context Awareness**: Time of day, user energy levels, task type
   ```python
   if task.requires_deep_focus and is_peak_productivity_hours():
       score += 10
   ```

## Summary

This algorithm is a well-designed priority scoring system that balances multiple concerns effectively. Its strength lies in combining objective factors (due dates, priority) with contextual signals (tags, recent activity) to produce practical task rankings. The main areas for enhancement would be making it more configurable and adding support for dependencies and task age considerations.

---

# Exercise 3: Knowing Where to Start - Unfamiliar Codebase Analysis

## Part 1: Understanding Project Structure

### Initial Exploration (Before AI)

#### Directory Structure Observed
```
TaskManager/
├── cli.py              # Command-line interface entry point
├── models.py           # Data structures/entities
├── storage.py          # Persistence layer
├── task_manager.py     # Core business logic
├── README.md           # Documentation
├── .gitignore          # Git exclusions
└── tests/              # Test suite
    ├── test_task_manager.py
    └── __init__.py
```

#### Configuration Files Analysis
- **No requirements.txt** - Uses only Python standard library
- **No package.json or setup.py** - Not packaged as installable module
- **No external dependencies** - Pure Python 3.11+ project

#### Initial Understanding (My Hypothesis)

**Technologies & Frameworks:**
- Python 3.11+ (standard library only)
- JSON for data persistence (guessed from storage.py)
- `argparse` for CLI (seen in cli.py imports)
- `unittest` for testing
- No web framework - purely CLI-based application

**Main Components:**
1. **CLI Layer** (cli.py) - User interaction
2. **Business Logic** (task_manager.py) - Operations orchestration
3. **Domain Model** (models.py) - Task entities, enums
4. **Persistence** (storage.py) - Data storage/retrieval
5. **Tests** (tests/) - Unit tests

**Architecture Pattern Guess:**
Appears to be a **layered architecture**:
- Presentation → Business Logic → Data Access
- Possibly Repository pattern for storage abstraction

### AI-Guided Analysis

#### Project Structure & Technology Stack

**Confirmed Technologies:**
- **Python 3.11+** with standard library only (datetime, json, os, uuid, argparse, enum, copy, re)
- **No external frameworks** - minimalist design
- **JSON file-based storage** - simple, portable persistence
- **CLI interface** using argparse - no GUI or web interface
- **unittest** framework for testing

**Architecture Pattern - CONFIRMED:**
The codebase follows a **3-tier layered architecture**:

```
┌─────────────────────────────────────┐
│   Presentation Layer (CLI)          │
│   - cli.py                          │
│   - Parses commands, formats output │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│   Business Logic Layer              │
│   - task_manager.py                 │
│   - Orchestrates operations         │
│   - Validates inputs                │
│   - Coordinates domain & storage    │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│   Domain Model Layer                │
│   - models.py                       │
│   - Task, TaskStatus, TaskPriority  │
│   - Business rules & behavior       │
└─────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────┐
│   Data Access Layer                 │
│   - storage.py                      │
│   - Repository pattern              │
│   - JSON serialization              │
└─────────────────────────────────────┘
```

#### Entry Points Identified

**Primary Entry Point:**
- [cli.py](cli.py) `main()` function
- Invoked via: `python cli.py <command>`

**Key Components & Responsibilities:**

1. **CLI (cli.py)**
   - Command parsing (create, list, status, priority, due, tag, untag, show, delete, stats)
   - User input validation
   - Output formatting (`format_task()` function)
   - Delegates to TaskManager for all operations

2. **TaskManager (task_manager.py)**
   - **Role**: Facade/Orchestrator
   - Validates business rules
   - Converts CLI inputs to domain objects
   - Coordinates between Storage and Models
   - Methods: `create_task()`, `update_task_status()`, `list_tasks()`, `get_statistics()`, etc.

3. **Models (models.py)**
   - `Task` class - Core entity
   - `TaskStatus` enum (TODO, IN_PROGRESS, REVIEW, DONE)
   - `TaskPriority` enum (LOW=1, MEDIUM=2, HIGH=3, URGENT=4)
   - Domain methods: `update()`, `mark_as_done()`, `is_overdue()`

4. **Storage (storage.py)**
   - **Repository Pattern** implementation
   - In-memory dictionary + JSON persistence
   - Custom `TaskEncoder` and `TaskDecoder` for serialization
   - CRUD operations: `add_task()`, `get_task()`, `update_task()`, `delete_task()`
   - Query methods: `get_tasks_by_status()`, `get_tasks_by_priority()`, `get_overdue_tasks()`

5. **Tests (tests/)**
   - Unit tests for TaskManager
   - Uses mocking for storage layer
   - Tests both success and failure paths

### Misconceptions Corrected

**Initial Misconception → Reality:**

1. **Packaging**: Thought it might have setup.py → It's a simple script collection, not packaged
2. **Database**: Assumed it might use SQLite → Uses plain JSON files
3. **Complexity**: Expected more layers/abstractions → Intentionally simple for learning
4. **Entry point**: Thought there might be `__main__.py` → Direct script execution via cli.py
5. **Configuration**: Expected config files for settings → Hardcoded defaults (storage path, etc.)

### Key Architectural Decisions

1. **Separation of Concerns**: Clean boundaries between layers
2. **Dependency Direction**: CLI → TaskManager → Storage/Models (unidirectional)
3. **Encapsulation**: Domain logic in Task class (e.g., `mark_as_done()`)
4. **Repository Pattern**: Storage abstraction allows easy switching (JSON → DB)
5. **No external dependencies**: Simplifies deployment, reduces complexity

## Part 2: Finding Feature Implementation - "Task Export to CSV"

### Initial Search & Hypothesis

#### Search Strategy Used

**Search Terms:**
- "export" - No matches
- "csv" - No matches
- "file" - Found in storage.py (JSON file operations)
- "write" - Found JSON writing in storage.py
- "format" - Found `format_task()` in cli.py (text formatting)

**Relevant Files Found:**
1. [storage.py](storage.py) - Has `save()` method that writes to JSON
2. [cli.py](cli.py) - Has `format_task()` for text output
3. [task_manager.py](task_manager.py) - Has `get_all_tasks()` and `list_tasks()`

#### Initial Hypothesis

**Where CSV export would belong:**
- **Option A**: Add new CLI command `export` in cli.py
- **Option B**: Add method in TaskManager: `export_to_csv(filepath)`
- **Option C**: Create separate utility module: `export_utils.py`

**My Initial Plan:**
1. Add `export` subcommand to CLI parser
2. Add `TaskManager.export_tasks_to_csv(filepath)` method
3. Reuse existing `get_all_tasks()` for data retrieval
4. Use Python's `csv` module (standard library)
5. Format similar to current text output

### AI-Guided Feature Location

#### Pattern Analysis

**Similar Existing Patterns:**

1. **Data Retrieval Pattern** (from task_manager.py):
   ```python
   def list_tasks(self, status_filter=None, priority_filter=None, show_overdue=False):
       # Get filtered tasks from storage
       # Return list of Task objects
   ```
   → CSV export should follow same pattern: get tasks, transform, write

2. **Output Formatting Pattern** (from cli.py):
   ```python
   def format_task(task):
       # Convert Task object to human-readable string
       # Returns formatted string
   ```
   → Need similar function: `task_to_csv_row(task)`

3. **File Writing Pattern** (from storage.py):
   ```python
   def save(self):
       with open(self.storage_path, 'w') as f:
           json.dump(list(self.tasks.values()), f, cls=TaskEncoder, indent=2)
   ```
   → CSV export should use similar file handling with error handling

#### Recommended Implementation Location

**Best Practice Approach:**

Create a new module: **export_utils.py** in the TaskManager directory

**Rationale:**
- **Single Responsibility**: Export is a separate concern from core task management
- **Reusability**: Export logic can be reused by CLI or future API
- **Testability**: Easy to unit test independently
- **Maintainability**: Changes to export format don't affect core logic

**Structure:**
```
TaskManager/
├── cli.py
├── models.py
├── storage.py
├── task_manager.py
├── export_utils.py    # NEW MODULE
└── tests/
    └── test_export.py  # NEW TEST FILE
```

### Implementation Plan

#### Step 1: Create export_utils.py

```python
import csv
from datetime import datetime

def task_to_csv_row(task):
    """Convert Task object to CSV row (list)."""
    return [
        task.id,
        task.title,
        task.description,
        task.priority.name,
        task.status.value,
        task.created_at.isoformat(),
        task.updated_at.isoformat(),
        task.due_date.isoformat() if task.due_date else '',
        task.completed_at.isoformat() if task.completed_at else '',
        ', '.join(task.tags)
    ]

def export_tasks_to_csv(tasks, filepath):
    """Export list of tasks to CSV file."""
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow([
                'ID', 'Title', 'Description', 'Priority', 'Status',
                'Created At', 'Updated At', 'Due Date', 'Completed At', 'Tags'
            ])
            # Write tasks
            for task in tasks:
                writer.writerow(task_to_csv_row(task))
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False
```

#### Step 2: Add method to TaskManager (task_manager.py)

```python
def export_to_csv(self, filepath, status_filter=None, priority_filter=None):
    """Export tasks to CSV file with optional filtering."""
    from export_utils import export_tasks_to_csv
    
    tasks = self.list_tasks(status_filter, priority_filter)
    return export_tasks_to_csv(tasks, filepath)
```

#### Step 3: Add CLI command (cli.py)

```python
# In argument parser setup:
export_parser = subparsers.add_parser("export", help="Export tasks to CSV")
export_parser.add_argument("filepath", help="Path to CSV file")
export_parser.add_argument("-s", "--status", help="Filter by status", 
                          choices=["todo", "in_progress", "review", "done"])
export_parser.add_argument("-p", "--priority", help="Filter by priority", 
                          type=int, choices=[1, 2, 3, 4])

# In command handler:
elif args.command == "export":
    if task_manager.export_to_csv(args.filepath, args.status, args.priority):
        print(f"Tasks exported to {args.filepath}")
    else:
        print("Failed to export tasks")
```

#### Step 4: Add tests (tests/test_export.py)

```python
import unittest
import os
import csv
from export_utils import export_tasks_to_csv, task_to_csv_row
from models import Task, TaskPriority

class TestExport(unittest.TestCase):
    def test_task_to_csv_row(self):
        task = Task("Test task")
        row = task_to_csv_row(task)
        self.assertEqual(len(row), 10)
        self.assertEqual(row[1], "Test task")
    
    def test_export_tasks_to_csv(self):
        tasks = [Task("Task 1"), Task("Task 2")]
        filepath = "test_export.csv"
        
        result = export_tasks_to_csv(tasks, filepath)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(filepath))
        
        # Cleanup
        os.remove(filepath)
```

### Related Components Affected

1. **task_manager.py** - Add `export_to_csv()` method
2. **cli.py** - Add `export` subcommand
3. **export_utils.py** - New module (create)
4. **tests/test_export.py** - New test file (create)
5. **README.md** - Update with export command documentation

### Key Insights

- Export functionality fits naturally as a new module (follows SRP)
- Can reuse existing `list_tasks()` method for data retrieval
- CSV format is straightforward with Python's csv module
- Similar pattern to existing JSON export in storage.py
- Easy to extend later (Excel, PDF, etc.)

## Part 3: Understanding Domain Model

### Initial Domain Model Extraction

#### Core Entities Identified

1. **Task** (models.py)
   - Primary entity
   - Attributes: id, title, description, priority, status, dates, tags

2. **TaskStatus** (models.py)
   - Enum: TODO, IN_PROGRESS, REVIEW, DONE
   - Workflow states

3. **TaskPriority** (models.py)
   - Enum: LOW=1, MEDIUM=2, HIGH=3, URGENT=4
   - Importance levels

4. **TaskStorage** (storage.py)
   - Repository/Collection
   - Not part of domain model but manages Task persistence

5. **TaskManager** (task_manager.py)
   - Service/Orchestrator
   - Coordinates operations, not a domain entity

#### Initial Entity Relationship Diagram

```
┌─────────────────────────────────────────┐
│              Task                       │
├─────────────────────────────────────────┤
│ - id: UUID                              │
│ - title: string                         │
│ - description: string                   │
│ - priority: TaskPriority (enum)         │
│ - status: TaskStatus (enum)             │
│ - created_at: datetime                  │
│ - updated_at: datetime                  │
│ - due_date: datetime?                   │
│ - completed_at: datetime?               │
│ - tags: list[string]                    │
├─────────────────────────────────────────┤
│ + update(**kwargs)                      │
│ + mark_as_done()                        │
│ + is_overdue() → bool                   │
└─────────────────────────────────────────┘
           │
           │ has-a (composition)
           │
    ┌──────┴────────┐
    │               │
┌───▼───────┐  ┌────▼──────┐
│TaskStatus │  │TaskPriority│
├───────────┤  ├───────────┤
│ TODO      │  │ LOW = 1   │
│IN_PROGRESS│  │ MEDIUM = 2│
│ REVIEW    │  │ HIGH = 3  │
│ DONE      │  │ URGENT = 4│
└───────────┘  └───────────┘
```

#### Initial Understanding

**Task Entity:**
- Represents a work item to be completed
- Has lifecycle from TODO → IN_PROGRESS → REVIEW → DONE
- Can have priority assigned (affects sorting/importance)
- Can be tagged for categorization
- Tracks temporal information (creation, updates, due dates, completion)

**Business Rules (Observed):**
1. Tasks must have a title
2. Default status is TODO
3. Default priority is MEDIUM
4. Marking as DONE sets completed_at timestamp
5. Tasks with due_date < now() and status != DONE are overdue
6. Tags can be added/removed dynamically
7. Status can be updated throughout lifecycle
8. Completed tasks have completed_at set

**Questions/Confusion:**
- Can a task go from DONE back to TODO?
- What is the purpose of REVIEW status?
- Are there any constraints on transitions (state machine)?
- Can tasks have dependencies on other tasks?

### AI-Guided Domain Understanding

#### Refined Domain Model

**Task - Complete Analysis:**

The Task entity is the **Aggregate Root** in DDD terms. It encapsulates:

1. **Identity**: UUID-based, immutable
2. **Properties**: Title (required), description (optional), tags (flexible)
3. **Value Objects**: Priority and Status (enums - immutable, type-safe)
4. **Temporal Tracking**: Full audit trail of changes
5. **Business Methods**: 
   - `update()` - Generic property setter with timestamp update
   - `mark_as_done()` - Specialized status transition with completion tracking
   - `is_overdue()` - Business rule evaluation

**Status Workflow:**

```
    ┌──────┐
    │ TODO │ (Initial state)
    └──┬───┘
       │
       ▼
┌──────────────┐
│ IN_PROGRESS  │ (Work started)
└──────┬───────┘
       │
       ▼
    ┌────────┐
    │ REVIEW │ (Work completed, awaiting approval)
    └───┬────┘
        │
        ▼
     ┌──────┐
     │ DONE │ (Final state)
     └──────┘
```

**Note**: The current implementation doesn't enforce this workflow - any status transition is allowed. This could be a design choice (flexibility) or a missing validation.

**Priority System:**

The numeric values (1-4) enable:
- Sorting and comparison
- Weighted scoring algorithms
- Filtering and grouping

Higher numbers = higher priority (URGENT > HIGH > MEDIUM > LOW)

#### Domain Terminology Glossary

| Term | Definition | Usage |
|------|------------|-------|
| **Task** | A unit of work to be completed | Primary domain entity |
| **Status** | Current workflow state of a task | Tracks progress through lifecycle |
| **Priority** | Relative importance/urgency of a task | Used for sorting and filtering |
| **Due Date** | Deadline for task completion | Optional; used for overdue calculation |
| **Overdue** | Task past due date and not completed | Computed property, not stored |
| **Tag** | Categorical label for grouping/filtering | Multiple tags allowed per task |
| **Completed At** | Timestamp when task was marked done | Set automatically on completion |
| **Created At** | Task creation timestamp | Immutable after creation |
| **Updated At** | Last modification timestamp | Auto-updated on any change |

#### Testing My Understanding - Q&A

**Q1: Can a completed task become uncompleted?**

Based on code analysis:
- `mark_as_done()` method only transitions TO done
- No `unmark_done()` or reverse method
- `update_task_status()` in TaskManager allows any status change
- **Answer**: Technically yes (via generic update), but no explicit support. This might be intentional flexibility or oversight.

**Q2: What's the difference between REVIEW and DONE?**

- **REVIEW**: Work is finished but awaiting validation/approval
- **DONE**: Work is complete and approved
- This suggests a workflow where tasks need approval before final completion
- REVIEW tasks could be rejected and moved back to IN_PROGRESS

**Q3: Are there any constraints on task transitions?**

Code analysis shows:
- No state machine implementation
- No validation in `Task.update()` or `TaskManager.update_task_status()`
- **Answer**: No enforced constraints - any status can transition to any other status
- This is likely intentional for flexibility in small teams

**Q4: Can tasks have subtasks or dependencies?**

- No references to parent/child relationships in Task model
- No dependency tracking fields
- No methods for managing relationships
- **Answer**: No, this is a flat task list system without hierarchy

**Q5: How are overdue tasks handled?**

- `is_overdue()` checks if due_date < now() AND status != DONE
- No automatic status changes
- No notifications or escalations
- Used for filtering: `get_overdue_tasks()` in storage
- **Answer**: Overdue is a computed status for filtering/display only; no automatic actions

#### Revised Entity Diagram

```
┌───────────────────────────────────────────────────┐
│                    Task                           │
│                (Aggregate Root)                   │
├───────────────────────────────────────────────────┤
│ IDENTITY                                          │
│  • id: UUID (immutable, unique)                   │
├───────────────────────────────────────────────────┤
│ PROPERTIES                                        │
│  • title: string (required)                       │
│  • description: string (optional, default="")     │
│  • tags: list[string] (mutable)                   │
├───────────────────────────────────────────────────┤
│ VALUE OBJECTS                                     │
│  • priority: TaskPriority (enum, default=MEDIUM)  │
│  • status: TaskStatus (enum, default=TODO)        │
├───────────────────────────────────────────────────┤
│ TEMPORAL TRACKING                                 │
│  • created_at: datetime (immutable)               │
│  • updated_at: datetime (auto-updated)            │
│  • due_date: datetime? (optional)                 │
│  • completed_at: datetime? (set on DONE)          │
├───────────────────────────────────────────────────┤
│ BUSINESS METHODS                                  │
│  • update(**kwargs) → void                        │
│    - Updates any field, sets updated_at           │
│  • mark_as_done() → void                          │
│    - Sets status=DONE, completed_at=now           │
│  • is_overdue() → bool                            │
│    - Returns true if past due and not done        │
└───────────────────────────────────────────────────┘
                 │
                 │ (composition)
         ┌───────┴────────┐
         │                │
    ┌────▼─────────┐  ┌───▼──────────┐
    │ TaskStatus   │  │ TaskPriority │
    │ (Enum)       │  │ (Enum)       │
    ├──────────────┤  ├──────────────┤
    │ TODO         │  │ LOW = 1      │
    │ IN_PROGRESS  │  │ MEDIUM = 2   │
    │ REVIEW       │  │ HIGH = 3     │
    │ DONE         │  │ URGENT = 4   │
    └──────────────┘  └──────────────┘

INVARIANTS (Business Rules):
• Task must always have a title (enforced in __init__)
• Task must always have a status (default=TODO)
• Task must always have a priority (default=MEDIUM)
• completed_at is only set when status=DONE
• is_overdue() only true for non-DONE tasks
• tags is always a list (never None)
```

### Key Domain Insights

1. **Simplicity by Design**: Flat structure, no complex relationships
2. **Flexible Workflow**: No enforced state transitions (pro/con)
3. **Temporal Awareness**: Comprehensive timestamp tracking
4. **Computed Properties**: Overdue status is derived, not stored
5. **Extensibility**: Tag system allows flexible categorization

## Part 4: Practical Application - "Auto-Abandon Overdue Tasks"

### Business Rule to Implement

**Rule**: "Tasks that are overdue for more than 7 days should be automatically marked as abandoned unless they are marked as high priority."

### Analysis & Planning

#### Breaking Down the Requirement

1. **Trigger Condition**: Task is overdue for > 7 days
2. **Exception**: High priority tasks (HIGH or URGENT) are exempt
3. **Action**: Mark as "abandoned"
4. **Questions for Team**:
   - Should "abandoned" be a new status or a tag?
   - When should this rule be evaluated (scheduled job, on-access)?
   - Should we notify users of abandoned tasks?
   - Can abandoned tasks be recovered?

#### Design Decisions

**Decision 1: Status vs Tag**

**Option A**: Add ABANDONED to TaskStatus enum
```python
class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    ABANDONED = "abandoned"  # NEW
```

**Option B**: Use a tag "abandoned"
```python
# Mark as abandoned
task.tags.append("abandoned")
task.status = TaskStatus.DONE  # or keep current status?
```

**Recommendation**: **Option A - New Status**
- More semantically correct
- Allows status-based filtering
- Clearer in reports and UI
- Consistent with existing workflow states

**Decision 2: Execution Trigger**

**Option A**: Scheduled background job (cron/scheduled task)
**Option B**: On-demand when listing tasks
**Option C**: On each task access

**Recommendation**: **Option B - On-demand**
- Simple to implement
- No external scheduler needed
- Consistent with current architecture
- Add `auto_abandon_overdue_tasks()` method called before list operations

### Implementation Plan

#### Files to Modify

1. **models.py** - Add ABANDONED status
2. **task_manager.py** - Add auto-abandon logic
3. **cli.py** - Integrate auto-abandon into list command
4. **tests/test_task_manager.py** - Add tests for auto-abandon

#### Detailed Changes

**1. models.py - Add ABANDONED Status**

```python
class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    ABANDONED = "abandoned"  # NEW

# In Task class, add method:
def should_be_abandoned(self, days_threshold=7):
    """
    Check if task should be auto-abandoned.
    
    Returns True if:
    - Task has a due date
    - Task is overdue by more than days_threshold days
    - Task is not DONE or ABANDONED
    - Task is not HIGH or URGENT priority
    """
    if not self.due_date:
        return False
    
    if self.status in (TaskStatus.DONE, TaskStatus.ABANDONED):
        return False
    
    if self.priority in (TaskPriority.HIGH, TaskPriority.URGENT):
        return False
    
    days_overdue = (datetime.now() - self.due_date).days
    return days_overdue > days_threshold

def mark_as_abandoned(self):
    """Mark task as abandoned and update timestamp."""
    self.status = TaskStatus.ABANDONED
    self.updated_at = datetime.now()
```

**2. task_manager.py - Add Auto-Abandon Logic**

```python
def auto_abandon_overdue_tasks(self, days_threshold=7):
    """
    Automatically abandon tasks that are overdue beyond threshold.
    
    Args:
        days_threshold: Number of days past due before abandoning (default: 7)
    
    Returns:
        list: IDs of tasks that were abandoned
    """
    abandoned_ids = []
    all_tasks = self.storage.get_all_tasks()
    
    for task in all_tasks:
        if task.should_be_abandoned(days_threshold):
            task.mark_as_abandoned()
            abandoned_ids.append(task.id)
    
    if abandoned_ids:
        self.storage.save()  # Persist changes
    
    return abandoned_ids

def list_tasks(self, status_filter=None, priority_filter=None, show_overdue=False, auto_abandon=True):
    """
    List tasks with optional auto-abandonment of old overdue tasks.
    
    Args:
        ... (existing args)
        auto_abandon: If True, run auto-abandon before listing (default: True)
    """
    # NEW: Auto-abandon check
    if auto_abandon:
        self.auto_abandon_overdue_tasks()
    
    # Existing list logic...
    if show_overdue:
        return self.storage.get_overdue_tasks()
    # ... rest of method unchanged
```

**3. cli.py - Integrate into List Command**

```python
# In list command handler:
elif args.command == "list":
    tasks = task_manager.list_tasks(args.status, args.priority, args.overdue)
    if tasks:
        for task in tasks:
            print(format_task(task))
            print("-" * 50)
    else:
        print("No tasks found matching the criteria.")
    
    # Optional: Show abandonment message
    # Could add --verbose flag to show which tasks were abandoned

# Update format_task to handle ABANDONED status:
def format_task(task):
    status_symbol = {
        TaskStatus.TODO: "[ ]",
        TaskStatus.IN_PROGRESS: "[>]",
        TaskStatus.REVIEW: "[?]",
        TaskStatus.DONE: "[✓]",
        TaskStatus.ABANDONED: "[✗]"  # NEW
    }
    # ... rest unchanged
```

**4. tests/test_task_manager.py - Add Tests**

```python
def test_auto_abandon_overdue_tasks(self):
    """Test auto-abandonment of tasks overdue > 7 days."""
    task_manager = TaskManager()
    
    # Create a task overdue by 8 days, low priority
    past_date = datetime.now() - timedelta(days=8)
    task_id = task_manager.create_task(
        "Old task",
        priority_value=1,  # LOW
        due_date_str=past_date.strftime("%Y-%m-%d")
    )
    
    # Run auto-abandon
    abandoned = task_manager.auto_abandon_overdue_tasks(days_threshold=7)
    
    # Verify task was abandoned
    self.assertIn(task_id, abandoned)
    task = task_manager.get_task_details(task_id)
    self.assertEqual(task.status, TaskStatus.ABANDONED)

def test_auto_abandon_respects_high_priority(self):
    """Test that high priority tasks are NOT auto-abandoned."""
    task_manager = TaskManager()
    
    # Create overdue HIGH priority task
    past_date = datetime.now() - timedelta(days=10)
    task_id = task_manager.create_task(
        "Important old task",
        priority_value=3,  # HIGH
        due_date_str=past_date.strftime("%Y-%m-%d")
    )
    
    # Run auto-abandon
    abandoned = task_manager.auto_abandon_overdue_tasks(days_threshold=7)
    
    # Verify task was NOT abandoned
    self.assertNotIn(task_id, abandoned)
    task = task_manager.get_task_details(task_id)
    self.assertNotEqual(task.status, TaskStatus.ABANDONED)

def test_task_should_be_abandoned(self):
    """Test the should_be_abandoned logic on Task entity."""
    # Test case 1: Old overdue low priority task
    task = Task("Old task", priority=TaskPriority.LOW)
    task.due_date = datetime.now() - timedelta(days=10)
    task.status = TaskStatus.TODO
    self.assertTrue(task.should_be_abandoned())
    
    # Test case 2: High priority overdue task
    task2 = Task("Important", priority=TaskPriority.HIGH)
    task2.due_date = datetime.now() - timedelta(days=10)
    self.assertFalse(task2.should_be_abandoned())
    
    # Test case 3: Completed task (even if overdue)
    task3 = Task("Done task")
    task3.due_date = datetime.now() - timedelta(days=10)
    task3.status = TaskStatus.DONE
    self.assertFalse(task3.should_be_abandoned())
```

### Questions for Team Before Implementation

1. **Status vs Tag**: Should ABANDONED be a status or a tag? (Recommended: Status)

2. **Execution Timing**: 
   - Run on every list operation? (Simple but may have performance impact)
   - Add explicit CLI command `python cli.py auto-abandon`? (More control)
   - Scheduled background job? (Requires external scheduler)

3. **Threshold Configuration**: 
   - Hardcode 7 days or make configurable?
   - Different thresholds for different priorities?

4. **Notification**: 
   - Should users be notified when tasks are abandoned?
   - Log abandoned tasks to a file?

5. **Recovery**: 
   - Can abandoned tasks be un-abandoned and restored?
   - Should abandoned tasks be hidden by default in listings?

6. **Scope**: 
   - Only TODO/IN_PROGRESS or also REVIEW status?
   - Current implementation checks all non-DONE statuses

7. **Edge Cases**:
   - Tasks without due dates - never abandoned?
   - Manually set ABANDONED status - should auto-abandon skip these?

### Reflection

#### How AI Prompts Helped

The AI-guided analysis helped me:
1. **Clarify ambiguity** - Status vs tag decision
2. **Identify edge cases** - High priority exception, REVIEW status handling
3. **Consider timing** - When to execute the auto-abandon logic
4. **Plan testing** - Comprehensive test scenarios

#### Remaining Uncertainties

1. **Performance**: Impact of running auto-abandon on every list operation with large task counts
2. **User Experience**: Should abandonment be silent or notify users?
3. **Configuration**: Where to store threshold value (hardcoded vs config file)?
4. **Rollout**: Should this be opt-in initially?

#### Next Steps

1. **Prototype** - Implement basic version with status approach
2. **Team Review** - Present design decisions for feedback
3. **User Testing** - Validate UX with small group
4. **Documentation** - Update README with new status and behavior
5. **Monitoring** - Log abandonment events for analysis

## Final Reflection & Summary

### Initial vs. Final Understanding

#### Initial Understanding (Day 1)
- Saw it as a "simple CLI task manager"
- Focused on files and functions
- Missed architectural patterns
- Didn't understand domain concepts deeply
- Unclear about where new features would fit

#### Final Understanding (Post-Exercise)
- **Architecture**: Clean 3-tier layered design with repository pattern
- **Domain Model**: Rich understanding of Task entity, status workflow, priority system
- **Extension Points**: Clear understanding of where to add features
- **Design Philosophy**: Minimalist, standard library only, intentionally simple for learning
- **Testability**: Well-structured for unit testing with proper separation

### Most Valuable Insights by Exercise Part

#### Part 1: Project Structure
**Key Insight**: "Architecture patterns matter even in small projects"

The codebase demonstrates clean architecture principles:
- Layered design prevents coupling
- Repository pattern abstracts storage
- Domain logic lives in entities, not scattered
- CLI is thin presentation layer

**Value**: I can now quickly identify similar patterns in other codebases.

#### Part 2: Feature Location
**Key Insight**: "Follow existing patterns, don't reinvent"

The export feature analysis taught me:
- Look for similar functionality first
- Reuse data access patterns
- Keep separation of concerns
- Create new modules for new concerns

**Value**: I have a systematic approach for adding features to unfamiliar code.

#### Part 3: Domain Understanding
**Key Insight**: "Business rules are encoded in the model"

Understanding Task's methods (`mark_as_done()`, `is_overdue()`) revealed:
- Domain entities carry business logic
- Computed vs stored properties
- State transitions and workflows
- Invariants and constraints

**Value**: I can now extract business rules from code structure.

#### Part 4: Practical Application
**Key Insight**: "Design decisions have tradeoffs"

The auto-abandon feature planning revealed:
- Multiple valid approaches exist
- Questions to ask before coding
- Test scenarios emerge from requirements
- Integration points must be considered

**Value**: I think through implications before writing code.

### Approach to Implementing Auto-Abandon Feature

#### Phase 1: Design (Current)
- [✓] Analyze requirement
- [✓] Identify affected components
- [✓] Propose design options
- [✓] Plan testing approach
- [ ] Get team feedback

#### Phase 2: Implementation
1. Add ABANDONED status to TaskStatus enum
2. Implement `Task.should_be_abandoned()` method
3. Implement `Task.mark_as_abandoned()` method
4. Add `TaskManager.auto_abandon_overdue_tasks()` method
5. Integrate into `list_tasks()` with flag
6. Update CLI format_task() for ABANDONED display

#### Phase 3: Testing
1. Write unit tests for `should_be_abandoned()` logic
2. Write integration tests for auto-abandon flow
3. Test edge cases (high priority, no due date, already done)
4. Manual testing of CLI workflow

#### Phase 4: Documentation
1. Update README with ABANDONED status
2. Add examples of auto-abandon behavior
3. Document configuration options
4. Create migration guide if needed

### Strategies for Approaching Unfamiliar Code

#### 1. Top-Down + Bottom-Up Exploration
- **Top-Down**: Start with README, entry points, high-level structure
- **Bottom-Up**: Examine domain entities and core abstractions
- **Meet in Middle**: Trace feature flow from UI to storage

#### 2. Follow the Data
- Identify primary entities (Task)
- Trace data flow: Input → Processing → Storage
- Understand transformations at each layer

#### 3. Pattern Recognition
- Look for familiar architectural patterns (layered, repository, etc.)
- Identify design patterns (factory, builder, strategy)
- Notice naming conventions and project idioms

#### 4. Ask Structured Questions
- What problem does this solve?
- Who are the users?
- What are the main use cases?
- Where would feature X fit?
- How is concern Y handled?

#### 5. Incremental Understanding
- Don't try to understand everything at once
- Focus on one subsystem at a time
- Build mental model gradually
- Test understanding by explaining to others

### Additional Tools & Resources

#### Tools That Would Help

1. **Debugger** - Step through execution flow
2. **IDE Features** - Go to definition, find usages, call hierarchy
3. **Diagram Generators** - Visualize class relationships (pyreverse, PlantUML)
4. **Test Coverage** - See what's tested vs untested
5. **Git History** - Understand evolution and design decisions

#### Complementary Techniques

1. **Pair Programming** - Learn from experienced team members
2. **Code Reading Sessions** - Discuss code as a group
3. **Documentation** - Write docs to solidify understanding
4. **Refactoring Exercises** - Understand by improving
5. **Feature Implementation** - Best way to learn is to extend

### Conclusion

This exercise transformed my approach to unfamiliar codebases. I moved from "reading code linearly" to "understanding systems holistically." The combination of manual exploration and AI-guided analysis created deep understanding that neither approach alone could achieve.

**Key Takeaway**: Understanding code is not about reading every line - it's about identifying patterns, understanding design decisions, and knowing where things belong.
