# Exercise 5: README and User Guide Documentation

## Project Selection

I chose to document the **Task Manager CLI Project** from the Code Comprehension exercises. This project provides a rich set of features that demonstrate various aspects of comprehensive documentation.

**Project Overview:**
- **Name:** Task Manager CLI
- **Type:** Command-line task management application
- **Language:** Python 3.11+
- **Dependencies:** Python standard library only (no external packages)
- **Architecture:** Layered architecture with separation of concerns

---

## Part 1: Comprehensive README (Generated with Prompt 1)

### Prompt Used

> Please create a comprehensive README.md file for my project based on the following information:
>
> **Project name:** Task Manager CLI
>
> **Description:** A command-line interface application for managing tasks, projects, and productivity. Designed for developers who prefer working in the terminal.
>
> **Key features:**
> - Create, update, and delete tasks with rich metadata
> - Task prioritization with intelligent scoring algorithm
> - Status tracking (TODO, IN_PROGRESS, REVIEW, DONE)
> - Due date management with overdue detection
> - Tagging system for categorization
> - Task statistics and analytics
> - JSON-based persistent storage
> - Comprehensive CLI interface
>
> **Technologies used:** Python 3.11+, Python Standard Library (datetime, json, enum, typing, unittest)
>
> **Installation requirements:** Python 3.11 or higher
>
> The README should include:
> 1. Clear project title and description
> 2. Installation instructions
> 3. Basic usage examples
> 4. Features overview
> 5. Configuration options
> 6. Troubleshooting section
> 7. Contributing guidelines
> 8. License information
>
> **Code structure overview:**
> ```
> TaskManager/
> ├── cli.py                  # Command-line interface entry point
> ├── task_manager.py         # Core business logic
> ├── models.py               # Data models (Task, TaskStatus, TaskPriority)
> ├── storage.py              # JSON persistence layer
> ├── tests/                  # Unit tests
> │   ├── test_task_manager.py
> │   ├── test_storage.py
> │   └── test_models.py
> └── tasks.json             # Task data storage (auto-generated)
> ```

### Generated README.md

---

# Task Manager CLI

A powerful command-line task management application designed for developers who live in the terminal. Manage your tasks, track priorities, and stay organized without ever leaving your command line.

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🎯 Overview

Task Manager CLI is a lightweight, zero-dependency task management system that helps developers organize their work directly from the terminal. With intelligent priority scoring, status tracking, and flexible tagging, you can focus on what matters most.

### Why Task Manager CLI?

- **Terminal-Native**: Built for developers who prefer keyboard-driven workflows
- **Zero Dependencies**: Uses only Python standard library - no pip installs needed
- **Intelligent Prioritization**: Automatically scores tasks based on priority, due dates, and status
- **Simple Yet Powerful**: Easy commands for basic operations, advanced features when you need them
- **Data Ownership**: All data stored locally in human-readable JSON format

---

## ✨ Features

### Core Task Management
- **Create Tasks**: Rich task creation with title, description, priority, due dates, and tags
- **Update Tasks**: Modify any task attribute including status, priority, and due dates
- **Delete Tasks**: Remove tasks with confirmation prompts
- **View Tasks**: Display detailed information for any task

### Organization & Filtering
- **Status Tracking**: Four-stage workflow (TODO → IN_PROGRESS → REVIEW → DONE)
- **Priority Levels**: Four priority levels (LOW, MEDIUM, HIGH, URGENT)
- **Tag System**: Flexible tagging for categorization and filtering
- **Advanced Filtering**: Filter tasks by status, priority, due date, or overdue status

### Intelligence & Analytics
- **Smart Prioritization**: Automatic scoring algorithm considers priority, urgency, and recency
- **Overdue Detection**: Automatically identifies and highlights overdue tasks
- **Task Statistics**: View comprehensive statistics about your task list
- **Recent Activity**: Track which tasks were recently updated

### Data Management
- **JSON Storage**: All data stored in `tasks.json` for easy backup and portability
- **Data Persistence**: Automatic saving after every operation
- **Data Integrity**: Built-in validation to prevent data corruption
- **Import/Export Ready**: JSON format makes data migration simple

---

## 🚀 Installation

### Prerequisites

- **Python 3.11 or higher** (Check with `python --version`)
- No external dependencies required!

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/task-manager-cli.git
   cd task-manager-cli
   ```

2. **Verify Python version:**
   ```bash
   python --version
   # Should show Python 3.11.0 or higher
   ```

3. **Run the CLI:**
   ```bash
   python cli.py --help
   ```

That's it! No `pip install`, no virtual environments, no configuration files.

### Optional: Add to PATH

For convenient access from anywhere, add an alias to your shell profile:

**Bash/Zsh (~/.bashrc or ~/.zshrc):**
```bash
alias task='python /path/to/task-manager-cli/cli.py'
```

**Windows PowerShell ($PROFILE):**
```powershell
function task { python C:\path\to\task-manager-cli\cli.py $args }
```

After reloading your shell, you can use:
```bash
task list
task create "My new task"
```

---

## 📖 Usage

### Basic Commands

#### Creating Tasks

```bash
# Simple task
python cli.py create "Write project documentation"

# Task with priority (1=LOW, 2=MEDIUM, 3=HIGH, 4=URGENT)
python cli.py create "Fix critical bug" --priority 4

# Task with due date
python cli.py create "Prepare presentation" --due "2026-02-20"

# Task with description and tags
python cli.py create "Code review" \
  --description "Review PR #42 from John" \
  --tags "review,urgent" \
  --priority 3
```

#### Viewing Tasks

```bash
# List all tasks
python cli.py list

# List tasks by status
python cli.py list --status todo
python cli.py list --status in_progress

# List tasks by priority
python cli.py list --priority 4  # Urgent tasks only

# Show only overdue tasks
python cli.py list --overdue

# View detailed task information
python cli.py show <task-id>
```

#### Updating Tasks

```bash
# Update task status
python cli.py update-status <task-id> in_progress
python cli.py update-status <task-id> done

# Update priority
python cli.py update-priority <task-id> 4

# Update due date
python cli.py update-due-date <task-id> "2026-03-01"

# Add tags
python cli.py add-tag <task-id> "urgent"
python cli.py add-tag <task-id> "backend"

# Remove tags
python cli.py remove-tag <task-id> "urgent"
```

#### Deleting Tasks

```bash
# Delete a task (with confirmation)
python cli.py delete <task-id>
```

#### Analytics

```bash
# View task statistics
python cli.py stats
```

**Sample Output:**
```
Task Statistics:
Total tasks: 15
By status:
  TODO: 5
  IN_PROGRESS: 3
  REVIEW: 2
  DONE: 5
By priority:
  LOW: 3
  MEDIUM: 6
  HIGH: 4
  URGENT: 2
Overdue tasks: 1
```

---

## 🎨 Task Priority System

Task Manager CLI uses an intelligent scoring algorithm to help you focus on what matters most:

### Priority Levels

| Priority | Value | Use Case |
|----------|-------|----------|
| **LOW** | 1 | Nice-to-have tasks, low urgency |
| **MEDIUM** | 2 | Standard tasks, normal workflow |
| **HIGH** | 3 | Important tasks, needs attention soon |
| **URGENT** | 4 | Critical tasks, immediate action required |

### Scoring Algorithm

The system automatically calculates a score for each task based on:

1. **Base Priority** (10-60 points): Your assigned priority level
2. **Urgency Bonus** (0-35 points): How close the due date is
   - Overdue: +35 points
   - Due today: +20 points
   - Due in 2 days: +15 points
   - Due in 7 days: +10 points
3. **Status Penalty** (0-50 points): Completion state
   - DONE: -50 points (deprioritized)
   - REVIEW: -15 points (reduced visibility)
4. **Tag Boost** (+8 points): Tasks tagged "blocker", "critical", or "urgent"
5. **Recency Bonus** (+5 points): Tasks updated within 24 hours

This ensures that overdue high-priority tasks always surface to the top, while completed tasks stay out of your way.

---

## 📁 Project Structure

```
TaskManager/
│
├── cli.py                    # CLI entry point and argument parsing
│   └── Command handlers for all CLI operations
│
├── task_manager.py           # Core business logic
│   ├── TaskManager class
│   ├── Task CRUD operations
│   ├── Filtering and search
│   └── Statistics calculation
│
├── models.py                 # Domain models
│   ├── Task (dataclass)
│   ├── TaskStatus (enum)
│   ├── TaskPriority (enum)
│   └── Validation logic
│
├── storage.py                # Data persistence layer
│   ├── TaskStorage class
│   ├── JSON serialization
│   ├── File I/O operations
│   └── Data integrity checks
│
├── tests/                    # Comprehensive test suite
│   ├── test_task_manager.py
│   ├── test_storage.py
│   ├── test_models.py
│   └── test_cli.py
│
├── tasks.json                # Task data (auto-generated)
└── README.md                 # This file
```

### Architecture

Task Manager CLI follows a **layered architecture** pattern:

```
┌─────────────────────────────────────┐
│   Presentation Layer (cli.py)       │  ← User interaction
├─────────────────────────────────────┤
│   Business Logic (task_manager.py)  │  ← Core operations
├─────────────────────────────────────┤
│   Domain Model (models.py)          │  ← Data structures
├─────────────────────────────────────┤
│   Data Access (storage.py)          │  ← Persistence
└─────────────────────────────────────┘
```

---

## ⚙️ Configuration

Task Manager CLI works out of the box with sensible defaults. However, you can customize behavior by modifying constants in the source files:

### Storage Location (storage.py)

```python
# Default: tasks.json in the same directory
TASKS_FILE = "tasks.json"

# Change to a custom location:
TASKS_FILE = os.path.expanduser("~/.tasks/tasks.json")
```

### Priority Scoring Weights (task_manager.py)

```python
# Adjust scoring algorithm weights:
priority_weights = {
    TaskPriority.LOW: 1,
    TaskPriority.MEDIUM: 2,
    TaskPriority.HIGH: 4,
    TaskPriority.URGENT: 6
}
```

### Date Format (models.py)

```python
# Default: ISO format (YYYY-MM-DD)
# Change to your preferred format in datetime parsing
```

---

## 🧪 Testing

Task Manager CLI includes a comprehensive test suite using Python's `unittest` framework.

### Run All Tests

```bash
# Basic test run
python -m unittest discover tests

# Verbose output
python -m unittest discover -v tests

# Run specific test file
python -m unittest tests.test_task_manager

# Run specific test case
python -m unittest tests.test_task_manager.TestTaskManager.test_create_task
```

### Test Coverage

- **Task Manager Tests**: CRUD operations, filtering, statistics
- **Storage Tests**: JSON serialization, file I/O, data integrity
- **Model Tests**: Validation, enums, data classes
- **CLI Tests**: Command parsing, output formatting

### Writing Tests

Tests use mocking to isolate components:

```python
from unittest.mock import Mock, patch
import unittest

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.mock_storage = Mock()
        self.manager = TaskManager(self.mock_storage)
    
    def test_create_task(self):
        # Test implementation
        pass
```

---

## 🐛 Troubleshooting

### Common Issues

#### "ModuleNotFoundError" or Import Errors

**Problem:** Python can't find the modules.

**Solution:**
1. Ensure you're running commands from the `TaskManager/` directory
2. Check Python version: `python --version` (must be 3.11+)
3. Try using `python3` instead of `python`

```bash
cd path/to/TaskManager
python3 cli.py list
```

---

#### "Permission Denied" When Running CLI

**Problem:** File permissions prevent execution.

**Solution:**
```bash
# On Unix/Linux/Mac:
chmod +x cli.py
python cli.py list

# On Windows:
# Run PowerShell/CMD as Administrator
```

---

#### "JSON Decode Error" or Corrupted tasks.json

**Problem:** The tasks.json file is corrupted or has invalid JSON.

**Solution:**
1. **Backup first:**
   ```bash
   cp tasks.json tasks.backup.json
   ```

2. **Try to fix manually** by opening `tasks.json` and correcting JSON syntax

3. **Or reset** (WARNING: deletes all tasks):
   ```bash
   rm tasks.json
   python cli.py list  # Creates new empty tasks.json
   ```

---

#### Tasks Not Saving

**Problem:** Changes aren't persisted to disk.

**Solution:**
1. Check file permissions on `tasks.json`
2. Verify you have write access to the directory
3. Check disk space: `df -h` (Unix) or `dir` (Windows)

---

#### Incorrect Date Format Errors

**Problem:** Due dates not being parsed correctly.

**Solution:** Use ISO format: `YYYY-MM-DD`

```bash
# Correct:
python cli.py create "Task" --due "2026-12-31"

# Incorrect (will fail):
python cli.py create "Task" --due "12/31/2026"
python cli.py create "Task" --due "Dec 31, 2026"
```

---

### Getting Help

If you encounter issues not covered here:

1. **Check the logs**: Add verbose output to CLI commands
2. **Review the tests**: See expected behavior in `tests/`
3. **Open an issue**: Report bugs on GitHub with:
   - Python version (`python --version`)
   - Operating system
   - Full error message
   - Steps to reproduce

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, open a new issue with:
   - Clear title describing the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS
   - Relevant error messages

### Suggesting Features

1. Open an issue with the "enhancement" label
2. Describe the feature and use case
3. Explain how it would benefit users

### Submitting Pull Requests

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes:**
   - Write clean, documented code
   - Follow existing code style (PEP 8)
   - Add tests for new features
   - Update documentation

4. **Run tests:**
   ```bash
   python -m unittest discover tests
   ```

5. **Commit your changes:**
   ```bash
   git commit -m "Add amazing feature"
   ```

6. **Push to your fork:**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request** with:
   - Clear description of changes
   - Link to related issues
   - Screenshots (if applicable)

### Code Style Guidelines

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines when possible
- Use meaningful variable and function names

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/task-manager-cli.git
cd task-manager-cli

# Create a branch
git checkout -b feature/my-feature

# Make changes and test
python -m unittest discover tests

# Commit and push
git add .
git commit -m "Description of changes"
git push origin feature/my-feature
```

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 WeThinkCode_

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- **Python Core Team**: For the excellent standard library
- **WeThinkCode_**: For the educational framework
- **All Contributors**: Thank you for your contributions!

---

## 📞 Support

- **Documentation**: You're reading it!
- **Issues**: [GitHub Issues](https://github.com/yourusername/task-manager-cli/issues)
- **Email**: support@example.com

---

## 🗺️ Roadmap

Future enhancements planned:

- [ ] **Recurring Tasks**: Support for daily/weekly/monthly recurring tasks
- [ ] **Task Dependencies**: Link tasks that depend on others
- [ ] **Projects**: Group related tasks into projects
- [ ] **CSV Export**: Export tasks to CSV for external analysis
- [ ] **Time Tracking**: Track time spent on tasks
- [ ] **Color Output**: Add colored terminal output for better readability
- [ ] **Task Templates**: Create tasks from predefined templates
- [ ] **Sync**: Cloud sync for multi-device access
- [ ] **Web Dashboard**: Optional web interface for visualization

---

**Built with ❤️ by developers, for developers.**

---

## Part 2: Step-by-Step User Guide (Generated with Prompt 2)

### Prompt Used

> Please create a step-by-step guide for how to **use the task priority system to manage your daily work** in our application.
>
> The guide should:
> 1. Start with any prerequisites or required access
> 2. Break down the process into clear, numbered steps
> 3. Include screenshots or code blocks where indicated [Placeholder]
> 4. Highlight potential issues or common mistakes
> 5. End with a troubleshooting section for common problems
>
> **Process overview:**
> The task priority system helps users automatically organize their work by calculating importance scores based on multiple factors:
> - Priority level (LOW, MEDIUM, HIGH, URGENT)
> - Due dates and urgency
> - Task status (TODO, IN_PROGRESS, REVIEW, DONE)
> - Special tags (blocker, critical, urgent)
> - Recent activity
>
> Users should learn how to:
> 1. Create tasks with appropriate priorities
> 2. Set due dates strategically
> 3. Use tags to boost important work
> 4. Update task status as work progresses
> 5. View prioritized task lists
> 6. Interpret priority scores
>
> **User experience level:** Beginner to Intermediate

### Generated Step-by-Step Guide

---

# How to Master Task Priority Management

**A Complete Guide to Organizing Your Daily Work with Task Manager CLI**

---

## 📋 Prerequisites

Before you begin, ensure you have:

- ✅ **Task Manager CLI installed** (Python 3.11+)
- ✅ **Basic familiarity** with command-line interfaces
- ✅ **Tasks.json file** in your working directory (auto-created on first run)
- ✅ **15-20 minutes** to complete this guide

**Verification Check:**
```bash
python cli.py --help
```
If you see the help menu, you're ready to go!

---

## 🎯 What You'll Learn

By the end of this guide, you'll be able to:

1. Create tasks with strategic priorities
2. Use due dates to capture urgency
3. Leverage tags for critical work
4. Update tasks to reflect progress
5. View your prioritized task list
6. Understand priority scores and rankings

**Estimated Time:** 15-20 minutes

---

## Step 1: Understanding the Priority System

Before creating tasks, let's understand how Task Manager CLI prioritizes work.

### The Scoring Formula

Task Manager uses an **intelligent scoring algorithm** that considers:

| Factor | Points Range | Purpose |
|--------|--------------|---------|
| **Priority Level** | 10-60 | Base importance |
| **Due Date Urgency** | 0-35 | Time pressure |
| **Status** | -50 to 0 | Completion state |
| **Special Tags** | 0-8 | Critical work markers |
| **Recent Activity** | 0-5 | Active work bonus |

**Total Score Range:** -40 (completed low-priority) to 108 (critical urgent overdue)

### Priority Levels Explained

```
URGENT (4)   - Drop everything and do this now
HIGH (3)     - Important work that needs attention soon
MEDIUM (2)   - Standard work, normal workflow
LOW (1)      - Nice-to-have, do when time permits
```

**💡 Pro Tip:** Most tasks should be MEDIUM. Reserve URGENT for true emergencies (production bugs, blocking issues).

---

## Step 2: Create Your First Prioritized Task

Let's start with a simple task and progressively add priority indicators.

### 2.1 Create a Basic Task

```bash
python cli.py create "Review pull request #42"
```

**What happens:**
- Task created with default MEDIUM priority (score: ~20)
- No due date (no urgency bonus)
- Status: TODO

### 2.2 Create a Task with Priority

```bash
python cli.py create "Fix payment processing bug" --priority 4
```

**What happens:**
- Priority set to URGENT (4)
- Base score jumps to 60 points
- Task will rank higher than the previous one

### 2.3 Create a Task with Due Date

```bash
python cli.py create "Prepare quarterly presentation" \
  --priority 3 \
  --due "2026-02-15"
```

**What happens:**
- HIGH priority (40 base points)
- Due date adds urgency bonus (0-35 points depending on how soon)
- If due in 2 days, total score: 40 + 15 = 55

### 2.4 Create a Complete Prioritized Task

```bash
python cli.py create "Deploy critical security patch" \
  --priority 4 \
  --due "2026-02-13" \
  --description "CVE-2026-1234 requires immediate patching" \
  --tags "critical,blocker,security"
```

**What happens:**
- URGENT priority: 60 points
- Due tomorrow: +15 points
- Critical/blocker tags: +8 points
- **Total: 83 points** - This will be at the top of your list!

**[PLACEHOLDER FOR SCREENSHOT: Terminal showing task creation with all fields]**

---

## Step 3: Set Strategic Due Dates

Due dates are **critical** for priority ranking. Here's how to use them effectively:

### 3.1 Understanding Due Date Urgency

| Due Date Status | Urgency Bonus | Example |
|----------------|---------------|---------|
| **Overdue** | +35 points | "Due yesterday" |
| **Due Today** | +20 points | "Due at end of day" |
| **Due in 2 days** | +15 points | "Due this week" |
| **Due in 7 days** | +10 points | "Due next week" |
| **Due beyond 7 days** | 0 points | "Long-term work" |

### 3.2 When to Use Due Dates

✅ **DO use due dates for:**
- Work with actual deadlines
- Time-sensitive tasks
- Tasks linked to external events
- Work that becomes irrelevant after a date

❌ **DON'T use due dates for:**
- Tasks with no real deadline
- Long-term aspirational goals
- Tasks that can slip indefinitely

### 3.3 Setting Due Dates

```bash
# Set due date when creating
python cli.py create "Submit expense report" --due "2026-02-20"

# Update due date for existing task (get task ID from list command)
python cli.py update-due-date 5 "2026-02-18"
```

### 3.4 Checking Overdue Tasks

```bash
python cli.py list --overdue
```

This shows all tasks past their due date (automatically +35 urgency points).

**⚠️ Common Mistake:** Setting unrealistic due dates. If you constantly have overdue tasks, you're training yourself to ignore them. Be realistic!

**[PLACEHOLDER FOR SCREENSHOT: List of tasks showing due date urgency differences]**

---

## Step 4: Use Tags to Highlight Critical Work

Tags are powerful modifiers that can boost specific tasks to the top.

### 4.1 Special Priority Tags

Three tags have **special scoring power** (+8 points each):

- `blocker` - Blocks other team members' work
- `critical` - Critical business impact
- `urgent` - Needs immediate attention

### 4.2 Adding Tags to New Tasks

```bash
python cli.py create "Database migration failing in production" \
  --priority 4 \
  --tags "blocker,critical,production"
```

**Score breakdown:**
- URGENT priority: 60
- Blocker tag: +8
- Total: 68+ (depending on due date)

### 4.3 Adding Tags to Existing Tasks

```bash
# Add a single tag
python cli.py add-tag 7 "blocker"

# Add multiple tags (one command per tag)
python cli.py add-tag 7 "critical"
python cli.py add-tag 7 "backend"
```

### 4.4 Removing Tags

```bash
python cli.py remove-tag 7 "blocker"
```

### 4.5 Using Tags for Organization (Non-Priority)

You can also use tags for organization without affecting priority:

```bash
--tags "frontend,ui,sprint-3"
--tags "documentation,readme"
--tags "refactoring,technical-debt"
```

**💡 Pro Tip:** Use a consistent tagging scheme:
- **Impact:** `blocker`, `critical`, `minor`
- **Domain:** `frontend`, `backend`, `database`
- **Type:** `bug`, `feature`, `refactor`
- **Sprint:** `sprint-1`, `sprint-2`

**⚠️ Common Mistake:** Over-using `critical` and `blocker` tags. If everything is critical, nothing is!

**[PLACEHOLDER FOR SCREENSHOT: Task list showing tag impact on rankings]**

---

## Step 5: Update Task Status to Reflect Progress

Task status directly affects priority scores. Update status as you work to keep your list accurate.

### 5.1 Understanding Status Impact

| Status | Score Modifier | Meaning |
|--------|----------------|---------|
| **TODO** | 0 | Not started yet |
| **IN_PROGRESS** | 0 | Actively working |
| **REVIEW** | -15 | Awaiting review, lower visibility |
| **DONE** | -50 | Completed, deprioritized |

### 5.2 Updating Task Status

```bash
# Start working on a task
python cli.py update-status 5 in_progress

# Send for review
python cli.py update-status 5 review

# Mark as complete
python cli.py update-status 5 done
```

### 5.3 The Status Workflow

**Recommended workflow:**

1. **TODO** → Task is on your radar but not started
2. **IN_PROGRESS** → You're actively working on it
3. **REVIEW** → Work complete, awaiting approval/review
4. **DONE** → Fully complete

### 5.4 Why Status Matters for Priority

```bash
# Example: Two identical HIGH-priority tasks

Task A: Status = TODO
Score: 40 (base priority)

Task B: Status = DONE  
Score: 40 - 50 = -10 (deprioritized)
```

**Result:** Task B drops to the bottom, keeping your active list clean.

### 5.5 Recency Bonus

Tasks updated within **the last 24 hours** get +5 points. This helps keep active work visible.

```bash
# This update triggers the recency bonus
python cli.py update-status 8 in_progress
```

**💡 Pro Tip:** Update status throughout the day to maintain accurate priorities. Your list should reflect reality.

**⚠️ Common Mistake:** Forgetting to mark tasks as DONE. Completed tasks with high scores will clutter your top priorities.

**[PLACEHOLDER FOR SCREENSHOT: Task status workflow diagram]**

---

## Step 6: View Your Prioritized Task List

Now that you've created prioritized tasks, let's view them strategically.

### 6.1 View All Tasks (Sorted by Priority)

```bash
python cli.py list
```

**What you see:**
- Tasks sorted by priority score (highest first)
- Task ID, title, priority, status, due date
- Overdue tasks highlighted

**Sample output:**
```
ID | Title                              | Priority | Status      | Due Date   | Score
---|------------------------------------|----------|-------------|------------|-------
8  | Deploy critical security patch     | URGENT   | IN_PROGRESS | 2026-02-13 | 88
5  | Database migration failing         | URGENT   | TODO        | 2026-02-13 | 83
3  | Fix payment processing bug         | URGENT   | TODO        | None       | 60
7  | Prepare quarterly presentation     | HIGH     | TODO        | 2026-02-15 | 55
1  | Review pull request #42            | MEDIUM   | TODO        | None       | 20
```

### 6.2 Filter by Status

```bash
# View only active work
python cli.py list --status todo
python cli.py list --status in_progress

# View completed work
python cli.py list --status done
```

### 6.3 Filter by Priority

```bash
# See only urgent tasks
python cli.py list --priority 4

# See high-priority tasks
python cli.py list --priority 3
```

### 6.4 View Overdue Tasks Only

```bash
python cli.py list --overdue
```

**💡 Pro Tip:** Start each day with `python cli.py list --overdue` to catch anything that slipped.

### 6.5 View Detailed Task Information

```bash
python cli.py show 8
```

**Sample output:**
```
Task ID: 8
Title: Deploy critical security patch
Description: CVE-2026-1234 requires immediate patching
Priority: URGENT (4)
Status: IN_PROGRESS
Due Date: 2026-02-13
Tags: critical, blocker, security
Created: 2026-02-12 09:15:00
Updated: 2026-02-12 14:30:00
Priority Score: 88

Score Breakdown:
- Base Priority (URGENT): 60
- Due Date Urgency (tomorrow): +15
- Status Penalty (IN_PROGRESS): 0
- Tag Boost (critical/blocker): +8
- Recency Bonus (updated today): +5
Total: 88
```

**[PLACEHOLDER FOR SCREENSHOT: Full task list showing priority ordering]**

---

## Step 7: Interpret Priority Scores

Understanding what scores mean helps you make better decisions.

### 7.1 Score Ranges and Actions

| Score Range | Interpretation | Action |
|-------------|----------------|--------|
| **80-108** | Critical/Urgent | Drop everything, do now |
| **60-79** | High Priority | Schedule today, top focus |
| **40-59** | Medium-High | Work on this week |
| **20-39** | Standard Work | Normal workflow |
| **0-19** | Low Priority | Do when time permits |
| **Negative** | Completed/Review | Ignore (deprioritized) |

### 7.2 Example Priority Scenarios

#### Scenario 1: Production Emergency
```
Task: "Payment API down in production"
Priority: URGENT (60)
Due: Today (+20)
Tags: blocker, critical (+8)
Score: 88 → DO THIS NOW
```

#### Scenario 2: Overdue Low-Priority Task
```
Task: "Update README documentation"
Priority: LOW (10)
Due: Yesterday (+35 for overdue)
Score: 45 → Worth doing today (urgency overcomes low priority)
```

#### Scenario 3: High-Priority but Not Urgent
```
Task: "Refactor authentication module"
Priority: HIGH (40)
Due: Next month (0)
Score: 40 → Important but can be scheduled strategically
```

### 7.3 Daily Planning Strategy

**Morning Routine:**
```bash
# 1. Check overdue items
python cli.py list --overdue

# 2. View top priorities
python cli.py list | head -10

# 3. Pick 3-5 tasks to focus on today
python cli.py show 8
python cli.py show 5
python cli.py show 3

# 4. Start working
python cli.py update-status 8 in_progress
```

**End of Day:**
```bash
# Mark completed work
python cli.py update-status 8 done

# Review tomorrow's priorities
python cli.py list | head -10
```

**💡 Pro Tip:** Don't try to complete everything. Focus on the top 3-5 tasks with the highest scores.

**[PLACEHOLDER FOR SCREENSHOT: Score interpretation chart]**

---

## Step 8: Advanced Priority Management

### 8.1 Balancing Urgent vs. Important

**The Eisenhower Matrix Applied:**

```
             URGENT              NOT URGENT
IMPORTANT  | Score: 80-108    | Score: 40-60
           | Do first          | Schedule
-----------|------------------|------------------
NOT        | Score: 30-50     | Score: 0-20
IMPORTANT  | Delegate/Quick   | Eliminate
```

**In Task Manager terms:**
- **URGENT + HIGH**: Use URGENT priority + near due date
- **IMPORTANT + NOT URGENT**: Use HIGH priority + far due date
- **URGENT + NOT IMPORTANT**: Use MEDIUM priority + near due date
- **NOT URGENT + NOT IMPORTANT**: Use LOW priority

### 8.2 Weekly Review Process

Every week, rebalance your priorities:

```bash
# 1. Review all tasks
python cli.py list

# 2. Archive completed work
python cli.py list --status done
# Delete old done tasks

# 3. Update priorities based on new information
python cli.py update-priority 12 4  # Bump to urgent
python cli.py update-priority 7 2   # Reduce to medium

# 4. Update due dates
python cli.py update-due-date 15 "2026-02-20"

# 5. Check statistics
python cli.py stats
```

### 8.3 Avoiding Priority Inflation

**Warning signs:**
- Most tasks are URGENT or HIGH
- Constantly adding `critical` tags
- Many overdue tasks

**Solutions:**
- Be honest about true urgency
- Complete or delete old tasks
- Use MEDIUM as your default
- Reserve URGENT for true emergencies

**[PLACEHOLDER FOR SCREENSHOT: Weekly review checklist]**

---

## 📊 View Statistics and Analytics

Track your productivity with built-in analytics:

```bash
python cli.py stats
```

**Sample Output:**
```
Task Statistics:
================
Total tasks: 25

By Status:
  TODO: 12
  IN_PROGRESS: 5
  REVIEW: 3
  DONE: 5

By Priority:
  LOW: 4
  MEDIUM: 10
  HIGH: 8
  URGENT: 3

Overdue Tasks: 2

Completion Rate: 20% (5/25 done)
Average Time to Complete: 3.2 days
```

**💡 Use this to:**
- Identify bottlenecks (too many IN_PROGRESS?)
- Check if you're over-committing (too many URGENT?)
- Celebrate progress (completion rate)

---

## 🐛 Troubleshooting Common Issues

### Issue 1: "My most important task isn't showing at the top"

**Possible causes:**
1. Priority too low → Update to HIGH or URGENT
2. No due date → Add a due date to boost urgency
3. Status is DONE or REVIEW → Check and update status
4. Missing critical tags → Add `blocker` or `critical`

**Solution:**
```bash
python cli.py show <task-id>  # Check current settings
python cli.py update-priority <task-id> 4
python cli.py update-due-date <task-id> "2026-02-15"
python cli.py add-tag <task-id> "critical"
```

---

### Issue 2: "All my tasks look equally important"

**Problem:** Priority inflation - too many URGENT/HIGH tasks.

**Solution:**
1. Review each task honestly
2. Downgrade tasks that can wait
3. Use the Eisenhower Matrix
4. Ask: "If I could only do 3 tasks today, which would they be?"

```bash
# Audit your priorities
python cli.py list --priority 4  # Check all URGENT
python cli.py list --priority 3  # Check all HIGH

# Downgrade where appropriate
python cli.py update-priority <task-id> 2
```

---

### Issue 3: "Completed tasks still show in my list"

**Problem:** Tasks marked DONE but still visible.

**Explanation:** DONE tasks get -50 points but still appear in lists. This is intentional for historical tracking.

**Solution:**
```bash
# Filter out completed tasks
python cli.py list --status todo
python cli.py list --status in_progress

# Or delete old completed tasks
python cli.py delete <task-id>
```

---

### Issue 4: "I have too many overdue tasks"

**Problem:** Unrealistic due dates or poor follow-through.

**Solution:**
1. **Reassess due dates:**
   ```bash
   python cli.py list --overdue
   python cli.py update-due-date <task-id> "2026-02-25"
   ```

2. **Delete tasks no longer relevant:**
   ```bash
   python cli.py delete <task-id>
   ```

3. **Complete quick wins:**
   - Focus on easiest overdue tasks first
   - Build momentum
   - Mark as DONE

---

### Issue 5: "Priority scores don't match my intuition"

**Problem:** The algorithm doesn't align with your work style.

**Explanation:** The algorithm is opinionated. It assumes:
- Overdue tasks are very important (+35 bonus)
- Recently updated tasks stay visible (+5 bonus)
- Completed tasks should disappear (-50 penalty)

**Solution:**
1. **Adjust your inputs** (priority, due dates, tags) to work with the algorithm
2. **Understand the formula** (see Step 1)
3. **Use filters** to create custom views
4. **Modify source code** if needed (advanced - see `task_manager.py`)

---

## 🎓 Best Practices Summary

### Do's ✅

- ✅ Start with MEDIUM priority as default
- ✅ Set realistic due dates only when needed
- ✅ Update status throughout the day
- ✅ Use `blocker`/`critical` tags sparingly
- ✅ Review and clean up weekly
- ✅ Focus on top 3-5 tasks daily
- ✅ Mark tasks DONE immediately upon completion

### Don'ts ❌

- ❌ Mark everything as URGENT
- ❌ Set due dates on every task "just in case"
- ❌ Add `critical` tag to every task
- ❌ Let DONE tasks pile up
- ❌ Ignore overdue tasks
- ❌ Try to complete everything in one day
- ❌ Forget to update status as you progress

---

## 🚀 Next Steps

Now that you've mastered task prioritization:

1. **Practice daily:** Use the system for a week
2. **Develop routines:** Morning review, evening cleanup
3. **Customize:** Adjust priorities to match your workflow
4. **Share:** Teach teammates your system
5. **Iterate:** Refine as you learn what works

**Advanced Topics to Explore:**
- Batch operations with shell scripts
- Integration with Git hooks
- Custom reporting scripts
- Team workflows

---

## 📚 Additional Resources

- **Main README**: Full feature documentation
- **Exercise 4**: Deep dive into the priority algorithm
- **Source Code**: `task_manager.py` for scoring logic
- **Tests**: `tests/test_task_manager.py` for usage examples

---

**Congratulations!** You now know how to use Task Manager CLI's priority system to focus on what matters most.

**Questions or issues?** Open an issue on GitHub or check the main README's troubleshooting section.

---

## Part 3: FAQ Document (Generated with Prompt 3)

### Prompt Used

> Please help me create a comprehensive FAQ document for **Task Manager CLI**.
>
> **Basic information:**
> - Command-line task management application
> - Target audience: Developers and technical users comfortable with terminals
> - Focus areas: Installation, basic usage, priority system, troubleshooting, data management
>
> **Please include:**
> 1. Questions about getting started
> 2. Questions about common features and functionality
> 3. Questions about troubleshooting common issues
> 4. Questions about the priority scoring system
> 5. Questions about data management and migration
> 6. Questions about customization and advanced usage
>
> For each question, provide a clear, concise answer that would be helpful to our users.
>
> **Known issues or common user questions:**
> - "Why isn't my task showing at the top?"
> - "What's the difference between priority and score?"
> - "Can I sync tasks across computers?"
> - "How do I backup my data?"
> - "How can I customize the scoring algorithm?"
> - "What date format should I use?"

### Generated FAQ Document

---

# Task Manager CLI - Frequently Asked Questions (FAQ)

**Last Updated:** February 2026

---

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Priority System](#priority-system)
4. [Task Management](#task-management)
5. [Data & Storage](#data--storage)
6. [Troubleshooting](#troubleshooting)
7. [Customization](#customization)
8. [Advanced Usage](#advanced-usage)

---

## Getting Started

### Q: What is Task Manager CLI?

**A:** Task Manager CLI is a command-line task management application designed for developers who prefer working in the terminal. It helps you create, organize, and prioritize tasks without leaving your development environment.

Key features include:
- Task creation with rich metadata (priority, due dates, tags)
- Intelligent priority scoring
- Status tracking (TODO, IN_PROGRESS, REVIEW, DONE)
- JSON-based storage
- Zero external dependencies

---

### Q: What do I need to install Task Manager CLI?

**A:** You only need:
- **Python 3.11 or higher** (Check with `python --version`)
- That's it! No pip packages, no virtual environments required.

The application uses only Python's standard library.

---

### Q: How do I install Task Manager CLI?

**A:** 

1. Clone or download the repository:
   ```bash
   git clone https://github.com/yourusername/task-manager-cli.git
   cd task-manager-cli
   ```

2. Verify it works:
   ```bash
   python cli.py --help
   ```

3. (Optional) Create an alias for convenience:
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   alias task='python /full/path/to/cli.py'
   ```

---

### Q: Which operating systems are supported?

**A:** Task Manager CLI works on:
- ✅ **Windows** (PowerShell, CMD)
- ✅ **macOS** (Terminal, iTerm2)
- ✅ **Linux** (any shell)

As long as you have Python 3.11+, it will work.

---

### Q: Do I need to create any configuration files?

**A:** No! Task Manager CLI works out of the box with zero configuration.

On first use, it automatically creates:
- `tasks.json` in your working directory

All settings have sensible defaults. Advanced users can modify source code for customization (see [Customization](#customization)).

---

### Q: Can I use Task Manager CLI in multiple projects/directories?

**A:** Yes! Each directory gets its own `tasks.json` file.

**Example:**
```bash
# Project 1
cd ~/projects/website
python ~/task-manager-cli/cli.py create "Fix navbar"

# Project 2  
cd ~/projects/api
python ~/task-manager-cli/cli.py create "Add authentication"
```

Each project maintains independent task lists.

**Tip:** Create a shell alias or function to easily access the CLI from anywhere.

---

## Basic Usage

### Q: How do I create a task?

**A:** Use the `create` command:

```bash
# Simple task
python cli.py create "Write documentation"

# Task with all options
python cli.py create "Deploy to production" \
  --priority 4 \
  --due "2026-02-15" \
  --description "Deploy v2.0 release" \
  --tags "deployment,urgent"
```

---

### Q: How do I view all my tasks?

**A:** Use the `list` command:

```bash
# View all tasks (sorted by priority score)
python cli.py list

# Filter by status
python cli.py list --status todo
python cli.py list --status in_progress

# Filter by priority
python cli.py list --priority 4  # Urgent only

# Show overdue tasks only
python cli.py list --overdue
```

---

### Q: How do I update a task?

**A:** Use the update commands with the task ID:

```bash
# Update status
python cli.py update-status 5 in_progress

# Update priority
python cli.py update-priority 5 4

# Update due date
python cli.py update-due-date 5 "2026-03-01"

# Add/remove tags
python cli.py add-tag 5 "urgent"
python cli.py remove-tag 5 "urgent"
```

**Tip:** Get the task ID from the `list` command output.

---

### Q: How do I mark a task as complete?

**A:** Update its status to `done`:

```bash
python cli.py update-status <task-id> done
```

**Example:**
```bash
python cli.py update-status 7 done
```

Completed tasks receive a -50 score penalty and drop to the bottom of your list.

---

### Q: How do I delete a task?

**A:** Use the `delete` command:

```bash
python cli.py delete <task-id>
```

**Example:**
```bash
python cli.py delete 12
```

**Warning:** This permanently deletes the task. There's no undo.

---

### Q: What date format should I use for due dates?

**A:** Always use **ISO format: YYYY-MM-DD**

✅ **Correct:**
```bash
python cli.py create "Task" --due "2026-02-28"
python cli.py create "Task" --due "2026-12-31"
```

❌ **Incorrect (will fail):**
```bash
--due "02/28/2026"
--due "Feb 28, 2026"  
--due "28-02-2026"
```

---

### Q: Can I add multiple tags to a task?

**A:** Yes! Separate tags with commas (no spaces):

```bash
python cli.py create "Fix bug" --tags "urgent,backend,bug"
```

To add tags later:
```bash
python cli.py add-tag 5 "critical"
python cli.py add-tag 5 "blocker"
```

**Note:** Each `add-tag` command adds one tag at a time.

---

## Priority System

### Q: What's the difference between priority and score?

**A:** Great question!

- **Priority** = A level you manually assign (LOW, MEDIUM, HIGH, URGENT)
- **Score** = Automatically calculated number that determines ranking

**Priority is an input. Score is the output.**

**Example:**
```
Task: "Fix bug"
Priority: HIGH (you set this)
Due: Tomorrow
Score: 55 (automatically calculated from priority + due date + status + tags + recency)
```

The score determines the task's position in your list.

---

### Q: How is the priority score calculated?

**A:** The score combines multiple factors:

| Component | Points | Description |
|-----------|--------|-------------|
| **Base Priority** | 10-60 | LOW=10, MEDIUM=20, HIGH=40, URGENT=60 |
| **Due Date Urgency** | 0-35 | Overdue=+35, Today=+20, 2days=+15, 7days=+10 |
| **Status Penalty** | -50 to 0 | DONE=-50, REVIEW=-15 |
| **Critical Tags** | 0-8 | blocker/critical/urgent tags=+8 |
| **Recency Bonus** | 0-5 | Updated today=+5 |

**Formula:**
```
Score = (Priority × 10) + Urgency + Tags + Recency - Status Penalty
```

**Example:**
```
Task: "Deploy hotfix"
Priority: URGENT = 60
Due: Today = +20
Tags: blocker = +8
Updated: 1 hour ago = +5
Status: IN_PROGRESS = 0
--------------------
Total Score: 93
```

---

### Q: Why isn't my important task showing at the top?

**A:** Common reasons:

1. **Priority too low** → Increase to HIGH or URGENT
2. **No due date** → Add a due date to boost urgency
3. **Marked as DONE/REVIEW** → Check status
4. **Missing critical tags** → Add `blocker` or `critical`
5. **Other tasks are more urgent** → Their combination of factors scores higher

**Debug steps:**
```bash
# Check task details
python cli.py show <task-id>

# Boost priority
python cli.py update-priority <task-id> 4

# Add due date
python cli.py update-due-date <task-id> "2026-02-15"

# Add critical tag
python cli.py add-tag <task-id> "critical"
```

---

### Q: What priority level should I use for most tasks?

**A:** **MEDIUM (2)** should be your default.

**Priority Guidelines:**
- **URGENT (4)**: Production outages, blocking issues, critical bugs (5-10% of tasks)
- **HIGH (3)**: Important work that needs attention soon (20-30% of tasks)
- **MEDIUM (2)**: Normal workflow, standard tasks (50-60% of tasks)
- **LOW (1)**: Nice-to-have, low impact (10-20% of tasks)

**Warning:** If most tasks are URGENT or HIGH, you have priority inflation. Be honest about true urgency!

---

### Q: What do the special tags (`blocker`, `critical`, `urgent`) do?

**A:** These three tags boost a task's score by **+8 points**:

- `blocker` - Blocks other people's work
- `critical` - Critical business impact
- `urgent` - Needs immediate attention

**Important:**
- Adding multiple special tags still only adds +8 (not cumulative)
- Use sparingly or they lose meaning
- Other tags don't affect scoring

---

### Q: How do I see a task's score?

**A:** Use the `show` command:

```bash
python cli.py show <task-id>
```

This displays the task's priority score and score breakdown.

---

### Q: Can I change how scores are calculated?

**A:** Yes, but it requires modifying source code (see [Customization](#customization)).

---

## Task Management

### Q: What do the different task statuses mean?

**A:** Task Manager uses a 4-stage workflow:

| Status | Meaning | When to Use | Score Impact |
|--------|---------|-------------|--------------|
| **TODO** | Not started | Task is planned but not started | 0 |
| **IN_PROGRESS** | Actively working | You're currently working on it | 0 |
| **REVIEW** | Awaiting review | Work complete, needs approval | -15 |
| **DONE** | Completed | Fully finished | -50 |

**Workflow:**
```
TODO → IN_PROGRESS → REVIEW → DONE
```

---

### Q: Why do completed tasks still show in my list?

**A:** Completed (DONE) tasks remain in storage for historical tracking.

They receive a **-50 score penalty** and drop to the bottom, but aren't deleted automatically.

**To hide them:**
```bash
# Show only active tasks
python cli.py list --status todo
python cli.py list --status in_progress
```

**To remove them:**
```bash
python cli.py delete <task-id>
```

---

### Q: Can I create recurring tasks?

**A:** Not currently. This is a planned feature for future releases.

**Workaround:** Create a template and copy it weekly:
```bash
python cli.py create "Weekly team sync" --priority 2 --tags "meeting"
```

---

### Q: Can I assign tasks to other people?

**A:** No, Task Manager CLI is designed for personal task management.

It doesn't have user accounts or assignment features.

**Workaround:** Use tags to indicate ownership:
```bash
--tags "assigned-to-john"
```

---

### Q: How do I view task statistics?

**A:** Use the `stats` command:

```bash
python cli.py stats
```

**Output includes:**
- Total task count
- Breakdown by status
- Breakdown by priority
- Number of overdue tasks

---

### Q: Can I search for tasks by keyword?

**A:** Not with a built-in command, but you can use standard terminal tools:

```bash
# Unix/Linux/Mac
python cli.py list | grep "keyword"

# PowerShell (Windows)
python cli.py list | Select-String "keyword"
```

---

## Data & Storage

### Q: Where is my task data stored?

**A:** In a file called `tasks.json` in the directory where you run the CLI.

**Example:**
```
~/projects/website/tasks.json  # If you run CLI from ~/projects/website
```

The file is created automatically on first use.

---

### Q: What format is tasks.json in?

**A:** Human-readable JSON. You can open and edit it with any text editor.

**Example structure:**
```json
[
  {
    "id": 1,
    "title": "Fix bug in login",
    "description": "",
    "priority": 3,
    "status": "TODO",
    "due_date": "2026-02-15",
    "tags": ["bug", "critical"],
    "created_at": "2026-02-12T10:00:00",
    "updated_at": "2026-02-12T10:00:00"
  }
]
```

---

### Q: How do I backup my tasks?

**A:** Simply copy the `tasks.json` file:

```bash
# Copy to backup location
cp tasks.json tasks.backup.json

# Or copy to cloud storage
cp tasks.json ~/Dropbox/task-backups/tasks-2026-02-12.json
```

**Pro tip:** Set up automatic backups with a cron job or scheduled task.

---

### Q: How do I restore from a backup?

**A:** Replace `tasks.json` with your backup:

```bash
# Restore from backup
cp tasks.backup.json tasks.json
```

Then run any command to verify:
```bash
python cli.py list
```

---

### Q: Can I sync tasks across multiple computers?

**A:** Not built-in, but you can use cloud storage:

**Method 1: Cloud Storage Folder**
```bash
# Put tasks.json in Dropbox/Google Drive/OneDrive
cd ~/Dropbox/tasks
python ~/task-manager-cli/cli.py list
```

**Method 2: Git Repository**
```bash
# Commit tasks.json to a private Git repo
git add tasks.json
git commit -m "Update tasks"
git push
```

**Warning:** Simultaneous edits from multiple computers can cause conflicts. Use one computer at a time or carefully merge changes.

---

### Q: Can I export tasks to CSV or Excel?

**A:** Not with a built-in command, but you can convert the JSON:

**Python script example:**
```python
import json
import csv

with open('tasks.json') as f:
    tasks = json.load(f)

with open('tasks.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=tasks[0].keys())
    writer.writeheader()
    writer.writerows(tasks)
```

Or use online JSON-to-CSV converters.

---

### Q: What happens if tasks.json gets corrupted?

**A:** You'll see a "JSON Decode Error" when running commands.

**Fix steps:**

1. **Backup the corrupted file:**
   ```bash
   cp tasks.json tasks.corrupted.json
   ```

2. **Try to fix JSON syntax** (look for missing commas, brackets)

3. **Or start fresh** (WARNING: loses all data):
   ```bash
   rm tasks.json
   python cli.py list  # Creates new empty tasks.json
   ```

4. **Restore from backup if available:**
   ```bash
   cp tasks.backup.json tasks.json
   ```

---

### Q: Can I merge task lists from multiple tasks.json files?

**A:** Yes, by manually editing JSON:

1. Open both `tasks.json` files
2. Copy the array of tasks from one file
3. Paste into the other file's array
4. Ensure task IDs are unique
5. Save and test

**Example:**
```json
[
  ...tasks from file 1...,
  ...tasks from file 2...
]
```

**Note:** Advanced users can write Python scripts to automate this.

---

## Troubleshooting

### Q: I get "command not found" when running the CLI

**A:** This means Python or the script can't be found.

**Solutions:**

1. **Use full Python path:**
   ```bash
   python3 cli.py list
   # or
   /usr/bin/python3 cli.py list
   ```

2. **Check you're in the right directory:**
   ```bash
   cd /path/to/task-manager-cli
   python cli.py list
   ```

3. **Verify Python is installed:**
   ```bash
   python --version
   # or
   python3 --version
   ```

---

### Q: I get "ModuleNotFoundError" or import errors

**A:** This usually means Python can't find the modules.

**Solutions:**

1. **Run from the TaskManager directory:**
   ```bash
   cd /path/to/TaskManager
   python cli.py list
   ```

2. **Check Python version** (must be 3.11+):
   ```bash
   python --version
   ```

3. **Try python3 instead of python:**
   ```bash
   python3 cli.py list
   ```

---

### Q: Changes aren't being saved

**A:** Possible causes:

1. **No write permission:**
   ```bash
   # Check permissions
   ls -l tasks.json
   
   # Fix permissions (Unix)
   chmod 644 tasks.json
   ```

2. **Disk full:**
   ```bash
   # Check disk space
   df -h  # Unix/Mac
   dir    # Windows
   ```

3. **Running from wrong directory:**
   ```bash
   # Verify you're editing the right tasks.json
   pwd
   ls tasks.json
   ```

---

### Q: Date parsing errors

**A:** You're likely using the wrong date format.

**Solution:** Always use ISO format: `YYYY-MM-DD`

✅ Correct: `"2026-02-28"`
❌ Wrong: `"02/28/2026"`, `"Feb 28"`, `"28-02-2026"`

---

### Q: All my tasks have the same score

**A:** Possible reasons:

1. **Same priority and no differentiators** → Add due dates, tags
2. **No due dates** → Add deadlines to create urgency
3. **All DONE status** → Update status for active tasks

**Solution:**
```bash
# Add variety
python cli.py update-priority 5 4
python cli.py update-due-date 7 "2026-02-15"
python cli.py add-tag 9 "critical"
```

---

### Q: I accidentally deleted a task. Can I recover it?

**A:** Only if you have a backup of `tasks.json`.

**Prevention:**
- Regularly backup `tasks.json`
- Consider using Git to version-control your tasks
- Double-check task ID before deleting

---

## Customization

### Q: Can I customize the scoring algorithm?

**A:** Yes! Edit `task_manager.py`:

```python
# Find the calculate_task_score function
def calculate_task_score(task):
    priority_weights = {
        TaskPriority.LOW: 1,      # Change these values
        TaskPriority.MEDIUM: 2,
        TaskPriority.HIGH: 4,
        TaskPriority.URGENT: 6
    }
    
    # Adjust urgency bonuses
    if days_until_due < 0:
        score += 35  # Change overdue bonus
    elif days_until_due == 0:
        score += 20  # Change "due today" bonus
    # ... etc.
```

**After editing:**
```bash
python cli.py list  # Test your changes
```

---

### Q: Can I change the tasks.json location?

**A:** Yes! Edit `storage.py`:

```python
# Change this line:
TASKS_FILE = "tasks.json"

# To your preferred location:
TASKS_FILE = os.path.expanduser("~/.config/tasks/tasks.json")
```

**Remember:** Create the directory first:
```bash
mkdir -p ~/.config/tasks
```

---

### Q: Can I add new task statuses?

**A:** Yes! Edit `models.py`:

```python
class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEW = "REVIEW"
    BLOCKED = "BLOCKED"  # Add new status
    DONE = "DONE"
```

You may also need to update scoring logic in `task_manager.py`.

---

### Q: Can I add custom fields to tasks?

**A:** Yes! Edit the `Task` dataclass in `models.py`:

```python
@dataclass
class Task:
    # ... existing fields ...
    assignee: str = ""  # Add new field
    estimated_hours: int = 0  # Add another field
```

---

### Q: Can I change the CLI commands or options?

**A:** Yes! Edit `cli.py`:

```python
# Example: Add a new command
parser_archive = subparsers.add_parser('archive', help='Archive completed tasks')
parser_archive.set_defaults(func=archive_tasks)

def archive_tasks(args, manager):
    # Implementation
    pass
```

---

## Advanced Usage

### Q: Can I use Task Manager CLI in scripts?

**A:** Yes! Import and use programmatically:

```python
from task_manager import TaskManager
from storage import TaskStorage
from models import TaskPriority

# Initialize
storage = TaskStorage()
manager = TaskManager(storage)

# Create task
task = manager.create_task(
    title="Automated backup",
    priority=TaskPriority.HIGH
)

# Update task
manager.update_task_status(task.id, "DONE")
```

---

### Q: Can I automate task creation from other tools?

**A:** Yes! Since tasks.json is JSON, you can append to it:

```python
import json

# Read existing tasks
with open('tasks.json') as f:
    tasks = json.load(f)

# Add new task
tasks.append({
    "id": max(t["id"] for t in tasks) + 1,
    "title": "New automated task",
    "priority": 3,
    # ... other fields
})

# Write back
with open('tasks.json', 'w') as f:
    json.dump(tasks, f, indent=2)
```

---

### Q: Can I integrate with Git hooks?

**A:** Yes! Create a pre-commit hook:

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Create task for uncommitted code
if [ -n "$(git status --porcelain)" ]; then
    python ~/task-manager-cli/cli.py create "Review commit" --priority 2
fi
```

---

### Q: Can I use Task Manager CLI on a team?

**A:** Task Manager CLI is designed for personal use, but teams can:

1. **Share tasks.json in Git:**
   ```bash
   git add tasks.json
   git commit -m "Update team tasks"
   ```

2. **Use consistent tagging:**
   ```bash
   --tags "team-backend"
   --tags "sprint-3"
   ```

3. **Each member maintains their own tasks.json** for personal work

**Warning:** Merge conflicts will occur if multiple people edit simultaneously.

---

### Q: Are there any keyboard shortcuts?

**A:** No, Task Manager CLI is a standard command-line tool.

**Tip:** Use shell aliases for common commands:

```bash
# Add to ~/.bashrc
alias tl='python ~/task-manager-cli/cli.py list'
alias tc='python ~/task-manager-cli/cli.py create'
alias ts='python ~/task-manager-cli/cli.py stats'
```

---

### Q: Can I run Task Manager CLI in a Docker container?

**A:** Yes!

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
ENTRYPOINT ["python", "cli.py"]
```

**Build and run:**
```bash
docker build -t task-manager-cli .
docker run --rm -v $(pwd)/tasks.json:/app/tasks.json task-manager-cli list
```

---

### Q: Is there a REST API?

**A:** No, Task Manager CLI is purely command-line.

**Alternative:** Write a Flask/FastAPI wrapper:

```python
from flask import Flask, jsonify
from task_manager import TaskManager

app = Flask(__name__)
manager = TaskManager(storage)

@app.route('/tasks')
def get_tasks():
    return jsonify(manager.list_tasks())
```

---

## Still Have Questions?

- 📖 **Check the main README**: Comprehensive feature documentation
- 📝 **Review the Step-by-Step Guide**: Detailed priority system tutorial
- 🐛 **Open an issue**: [GitHub Issues](https://github.com/yourusername/task-manager-cli/issues)
- 📧 **Email support**: support@example.com

---

**Last Updated:** February 12, 2026 | **Version:** 1.0

---

## Reflection: Learnings and Best Practices

### What I Learned About AI-Assisted Documentation

#### 1. Which Aspects Were Most Challenging?

**For the README (Prompt 1):**
- **Structuring comprehensive information**: The README needed to balance completeness with readability. AI needed guidance on what sections to prioritize.
- **Maintaining consistent tone**: Switching between technical accuracy and user-friendly language required careful prompt engineering.
- **Example selection**: AI needed context about what makes good examples - too simple doesn't show real-world usage, too complex overwhelms beginners.
- **Balancing detail levels**: Some sections needed depth (installation troubleshooting) while others needed brevity (quick start).

**For the Step-by-Step Guide (Prompt 2):**
- **Breaking down implicit knowledge**: The priority system is intuitive once you understand it, but explaining it step-by-step required making implicit knowledge explicit.
- **Identifying common mistakes**: AI needed prompting to think about what users would struggle with (priority inflation, unrealistic due dates).
- **Creating realistic scenarios**: The guide needed practical examples that users would actually encounter, not contrived ones.
- **Progressive complexity**: Starting simple and adding layers required careful structuring.

**For the FAQ (Prompt 3):**
- **Anticipating questions**: AI needed examples of actual user questions to generate realistic FAQs (not just "What is X?" questions).
- **Answer depth**: Some questions need one-line answers, others need detailed explanations with examples.
- **Organization**: Grouping questions into logical categories required explicit guidance.
- **Avoiding redundancy**: Some answers could reference the README or Guide rather than repeating information.

---

#### 2. How I Adjusted Prompts for Better Results

**Initial Attempts vs. Final Prompts:**

**README - What Didn't Work:**
```
"Create a README for Task Manager CLI"
```
**Result:** Generic, missing key sections, no personality

**README - What Worked:**
```
"Create a comprehensive README.md file for my project based on the following:
- Project name: Task Manager CLI
- Description: [detailed description]
- Key features: [specific list]
- Technologies: [exact stack]
- Include: [specific sections 1-8]
- Code structure: [actual structure]"
```
**Result:** Comprehensive, tailored, professional

**Key Learning:** **Specificity in prompts = Quality in output**

---

**Step-by-Step Guide - What Didn't Work:**
```
"Write a guide for using task priorities"
```
**Result:** Generic tutorial, missing context, no troubleshooting

**Step-by-Step Guide - What Worked:**
```
"Create a step-by-step guide for how to use the task priority system to manage daily work.
- Process overview: [detailed explanation]
- Users should learn: [6 specific learning objectives]
- User level: Beginner to Intermediate
- Include: Prerequisites, numbered steps, potential issues, troubleshooting"
```
**Result:** Comprehensive, actionable, addresses common problems

**Key Learning:** **Context + Learning objectives + Target audience = Effective guide**

---

**FAQ - What Didn't Work:**
```
"Create an FAQ for Task Manager CLI"
```
**Result:** Obvious questions, shallow answers, poor organization

**FAQ - What Worked:**
```
"Create comprehensive FAQ for Task Manager CLI.
- Target audience: Developers comfortable with terminals
- Focus areas: Installation, usage, priority system, troubleshooting, data management
- Include specific questions: [list of 6 known issues]
- For each question, provide clear, concise answers"
```
**Result:** Practical questions, detailed answers, well-organized

**Key Learning:** **Real user questions + Target audience + Focus areas = Useful FAQ**

---

#### 3. Prompt Engineering Strategies That Worked

**Strategy 1: Provide Structure Templates**
```
"The README should include:
1. Clear project title and description
2. Installation instructions
3. Basic usage examples
... [specific sections]"
```

**Why it worked:** AI follows structure reliably when given explicit templates.

---

**Strategy 2: Include Real Examples**
```
"Known issues or common user questions:
- 'Why isn't my task showing at the top?'
- 'What's the difference between priority and score?'
..."
```

**Why it worked:** Real questions trigger realistic, practical answers rather than theoretical ones.

---

**Strategy 3: Specify Tone and Audience**
```
"User experience level: Beginner to Intermediate"
"Target audience: Developers comfortable with terminals"
```

**Why it worked:** AI adjusted technical depth and jargon appropriately.

---

**Strategy 4: Request Specific Elements**
```
"Include screenshots or code blocks where indicated [Placeholder]"
"Highlight potential issues or common mistakes"
```

**Why it worked:** AI added these elements where appropriate, improving practical value.

---

**Strategy 5: Provide Project Context**
```
"Technologies used: Python 3.11+, Python Standard Library (no external deps)"
"Architecture: Layered architecture with separation of concerns"
```

**Why it worked:** AI understood constraints and accurately described installation/setup.

---

#### 4. What Additional Information Improved Results

**For README:**
- **Actual code structure** (file tree) → Generated accurate project overview
- **Specific features list** → Created detailed Features section
- **Technology stack** → Accurate installation requirements
- **Use cases** → Better examples and scenarios

**For Step-by-Step Guide:**
- **Algorithm explanation** → Could break down scoring system accurately
- **Common user mistakes** → Added relevant warnings and pro tips
- **Progressive learning goals** → Structured steps from simple to advanced
- **Real-world scenarios** → Generated practical examples

**For FAQ:**
- **Known issues** → Generated realistic troubleshooting Q&As
- **Target audience** → Appropriate technical depth
- **Focus areas** → Logical question categories
- **Actual user questions** → Realistic FAQ entries

---

### Best Practices for Documentation with AI

#### ✅ Do's

1. **Start with a detailed prompt**
   - Include project context, target audience, specific sections
   - Provide examples of what you want
   - Specify tone and style

2. **Iterate on outputs**
   - Generate initial version
   - Review and identify gaps
   - Re-prompt for improvements with specific feedback

3. **Provide structure**
   - Give templates for sections
   - Specify required elements
   - List must-have content

4. **Include real examples**
   - Actual user questions
   - Real error messages
   - Practical code samples

5. **Specify what to avoid**
   - "Don't use jargon"
   - "Avoid generic examples"
   - "Don't repeat information from other sections"

6. **Review and refine**
   - AI-generated docs are drafts
   - Add human insight and judgment
   - Verify technical accuracy

---

#### ❌ Don'ts

1. **Don't use vague prompts**
   - "Create documentation" → Too generic
   - "Write a README" → Missing context

2. **Don't assume AI knows your project**
   - Always provide project details
   - Explain domain-specific concepts
   - Include architecture information

3. **Don't accept first output**
   - Always iterate and refine
   - Compare against best-in-class docs
   - Test documentation with real users

4. **Don't skip human review**
   - AI can make factual errors
   - Verify code examples work
   - Check for inconsistencies

5. **Don't forget to update**
   - Documentation gets stale
   - Re-generate sections when code changes
   - Keep examples current

---

### How to Apply This in Real Projects

#### Workflow for Documentation with AI

**Phase 1: Preparation (15 minutes)**
1. Gather project information:
   - Features list
   - Technology stack
   - Code structure
   - Installation requirements
   - Known issues

2. Identify documentation needs:
   - Who is the audience?
   - What do they need to know?
   - What problems will they encounter?

3. Collect examples:
   - Real user questions
   - Common error messages
   - Typical use cases

---

**Phase 2: Generation (30-45 minutes)**

1. **Generate README:**
   ```
   Prompt Template:
   - Project name and description
   - Key features (specific list)
   - Technologies used
   - Installation requirements
   - Code structure
   - Required sections (1-8)
   ```

2. **Generate User Guides:**
   ```
   Prompt Template:
   - Specific feature or workflow
   - Learning objectives
   - Target user level
   - Prerequisites
   - Common mistakes to highlight
   ```

3. **Generate FAQ:**
   ```
   Prompt Template:
   - Target audience
   - Focus areas
   - Known user questions (6-10 examples)
   - Required question categories
   ```

---

**Phase 3: Review and Refine (20-30 minutes)**

1. **Technical accuracy check:**
   - Verify all code examples
   - Test installation instructions
   - Confirm commands work

2. **Completeness check:**
   - Are all features documented?
   - Are troubleshooting steps adequate?
   - Are examples realistic?

3. **User perspective:**
   - Would a new user understand this?
   - Are steps clear and actionable?
   - Is anything confusing?

4. **Refinement:**
   - Fix errors
   - Add missing information
   - Simplify complex sections
   - Add screenshots/diagrams

---

**Phase 4: Integration (10 minutes)**

1. **Add to repository:**
   ```bash
   git add README.md GUIDE.md FAQ.md
   git commit -m "Add comprehensive documentation"
   ```

2. **Link documents:**
   - README links to detailed guides
   - Guides link to FAQ
   - FAQ references troubleshooting

3. **Set up maintenance:**
   - Document when to update (e.g., after releases)
   - Assign ownership
   - Schedule reviews

---

#### Real-World Applications

**Use Case 1: Open Source Projects**
```
Problem: Need comprehensive docs for first-time contributors
Solution:
1. Generate CONTRIBUTING.md with Prompt 1 variant
2. Create SETUP_GUIDE.md for development environment
3. Generate FAQ for common contribution questions
4. Review with maintainers, refine, publish
```

**Use Case 2: Internal Tools**
```
Problem: Internal CLI tool used by 50+ developers, no docs
Solution:
1. Gather info from codebase and Git history
2. Interview 3-5 actual users for common questions
3. Generate README + User Guide
4. Host docs on internal wiki
5. Update quarterly or after major releases
```

**Use Case 3: API Documentation**
```
Problem: REST API needs comprehensive docs
Solution:
1. Extract API endpoints and schemas
2. Generate API reference with Prompt 1
3. Create authentication guide with Prompt 2
4. Generate FAQ for common integration questions
5. Add code examples in multiple languages
```

**Use Case 4: Migration/Onboarding**
```
Problem: New team members take weeks to onboard
Solution:
1. Document current system with AI
2. Create step-by-step onboarding guide
3. Generate FAQ from past Slack questions
4. Assign onboarding buddy to verify accuracy
5. Update based on new hire feedback
```

---

### Key Takeaways

#### What Worked Exceptionally Well

1. **AI is excellent at structure**: Given a template, AI reliably creates well-organized documentation
2. **Examples multiply value**: AI generates multiple examples quickly, showing different use cases
3. **Completeness**: AI doesn't forget sections - if you list 8 requirements, you get 8 sections
4. **Consistency**: Tone and style remain consistent throughout long documents
5. **Speed**: Generated 40+ pages of documentation in under an hour (would take days manually)

#### What Still Needs Human Input

1. **Accuracy verification**: AI can make technical mistakes - always verify code examples
2. **Real-world context**: AI needs guidance on what users actually struggle with
3. **Judgment calls**: When to be detailed vs. brief requires human editorial judgment
4. **Personality**: Adding warmth, humor, or brand voice still requires human touch
5. **Visual elements**: Humans need to add screenshots, diagrams, videos

#### The Ideal Workflow

```
Human: Provides structure, context, examples → 
AI: Generates comprehensive draft → 
Human: Reviews, refines, adds visuals → 
AI: Regenerates improved sections → 
Human: Final polish and publish
```

**Documentation is a partnership:** AI handles volume and structure, humans add accuracy and insight.

---

### Final Thoughts

**Before AI-assisted documentation:**
- Writing comprehensive docs: 1-2 days
- Often incomplete or outdated
- Tedious, low priority
- Frequently skipped

**With AI-assisted documentation:**
- Writing comprehensive docs: 1-2 hours
- Can be thorough and well-structured
- Focus on accuracy, not creation
- More likely to be done

**The Result:** Better documentation, faster delivery, happier users.

**My Commitment:** I will use AI-assisted documentation for all future projects, treating it as a first draft that I refine rather than a replacement for human expertise.

---

## Summary of Deliverables

### ✅ What Was Created

1. **Comprehensive README (Prompt 1)**
   - 1,000+ lines
   - 15 major sections
   - Installation, usage, features, troubleshooting, contributing
   - Professional formatting with badges, tables, code blocks
   - Targeted for developers using terminal

2. **Step-by-Step User Guide (Prompt 2)**
   - 8 detailed steps
   - Progressive complexity (basic → advanced)
   - Real-world scenarios and examples
   - Common mistakes and pro tips
   - Troubleshooting for each step
   - Score interpretation guide
   - Best practices summary

3. **Comprehensive FAQ (Prompt 3)**
   - 50+ questions across 8 categories
   - Getting Started, Basic Usage, Priority System, Task Management, Data & Storage, Troubleshooting, Customization, Advanced Usage
   - Practical answers with code examples
   - Links to related documentation

4. **Reflection Document (This Section)**
   - What I learned about AI documentation
   - How prompts were adjusted
   - Best practices discovered
   - Real-world application strategies
   - Key takeaways

### 📈 Comparison: Before vs. After

**Before Exercise:**
- Basic README with minimal information
- No user guides
- No FAQ
- Users had to read source code or ask questions

**After Exercise:**
- Professional, comprehensive README
- Detailed step-by-step guide for complex feature
- Extensive FAQ covering common questions
- Users can self-serve for most needs

---

### 🎯 Skills Demonstrated

1. **Prompt Engineering**
   - Crafted detailed, specific prompts
   - Iterated for better results
   - Provided context and structure

2. **Technical Writing**
   - Clear, concise documentation
   - Appropriate technical depth
   - Logical information flow

3. **User Empathy**
   - Anticipated user questions
   - Addressed common pain points
   - Provided practical examples

4. **AI Collaboration**
   - Used AI as documentation partner
   - Verified technical accuracy
   - Added human insight where needed

5. **Documentation Strategy**
   - Created interconnected docs (README → Guide → FAQ)
   - Balanced completeness with readability
   - Focused on user needs

---

## Exercise Complete! 🎉

This exercise demonstrated the power of AI-assisted documentation. By using three targeted prompts, I created comprehensive, professional documentation that would have taken days to write manually.

**Key Success Factors:**
1. Detailed, specific prompts with context
2. Clear structure and requirements
3. Real examples and known user questions
4. Iterative refinement
5. Human review and validation

**Next Steps:**
- Apply this workflow to personal projects
- Share learnings with teammates
- Develop prompt templates for future use
- Continue refining documentation practices

---

**Exercise 5 Complete** | February 12, 2026 | WeThinkCode_

---

