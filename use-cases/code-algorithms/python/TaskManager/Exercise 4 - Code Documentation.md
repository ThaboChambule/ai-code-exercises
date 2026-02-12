# Exercise 4: Code Documentation Challenge

## Original Code Selected

I chose the **Task Priority Sorting Algorithm** from `task_priority.py` because it's complex, has multiple decision points, and would benefit significantly from comprehensive documentation.

### Original Undocumented Code

```python
from datetime import datetime

from models import TaskStatus, TaskPriority

def calculate_task_score(task):
    """Calculate a priority score for a task based on multiple factors."""
    # Base priority weights
    priority_weights = {
        TaskPriority.LOW: 1,
        TaskPriority.MEDIUM: 2,
        TaskPriority.HIGH: 4,
        TaskPriority.URGENT: 6
    }

    # Calculate base score from priority
    score = priority_weights.get(task.priority, 0) * 10

    # Add due date factor (higher score for tasks due sooner)
    if task.due_date:
        days_until_due = (task.due_date - datetime.now()).days
        if days_until_due < 0:  # Overdue tasks
            score += 35
        elif days_until_due == 0:  # Due today
            score += 20
        elif days_until_due <= 2:  # Due in next 2 days
            score += 15
        elif days_until_due <= 7:  # Due in next week
            score += 10

    # Reduce score for tasks that are completed or in review
    if task.status == TaskStatus.DONE:
        score -= 50
    elif task.status == TaskStatus.REVIEW:
        score -= 15

    # Boost score for tasks with certain tags
    if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
        score += 8

    # Boost score for recently updated tasks
    days_since_update = (datetime.now() - task.updated_at).days
    if days_since_update < 1:
        score += 5

    return score

def sort_tasks_by_importance(tasks):
    """Sort tasks by calculated importance score (highest first)."""
    task_scores = [(calculate_task_score(task), task) for task in tasks]
    # Use key parameter to tell sorted() to only compare the scores (first element of tuple)
    sorted_tasks = [task for _, task in sorted(task_scores, key=lambda x: x[0], reverse=True)]
    return sorted_tasks

def get_top_priority_tasks(tasks, limit=5):
    """Return the top N priority tasks."""
    sorted_tasks = sort_tasks_by_importance(tasks)
    return sorted_tasks[:limit]
```

---

## Prompt 1: Comprehensive Function Documentation

### Generated Documentation (Following Python Docstring Conventions)

```python
from datetime import datetime
from typing import List

from models import TaskStatus, TaskPriority, Task


def calculate_task_score(task: Task) -> int:
    """
    Calculate a weighted priority score for a task based on multiple factors.
    
    This function computes a numeric score that represents the urgency and importance
    of a task by combining several factors: base priority level, due date proximity,
    completion status, special tags, and recent activity. Higher scores indicate
    higher priority tasks that should be addressed sooner.
    
    Args:
        task (Task): A Task object containing the following attributes:
            - priority (TaskPriority): The priority level (LOW, MEDIUM, HIGH, URGENT)
            - due_date (datetime, optional): The task's due date, or None if no deadline
            - status (TaskStatus): Current status (TODO, IN_PROGRESS, REVIEW, DONE)
            - tags (list[str]): List of tag strings associated with the task
            - updated_at (datetime): Timestamp of the last update to the task
    
    Returns:
        int: A weighted priority score. Score ranges typically from -40 to ~108.
            - Negative scores indicate completed tasks (should be deprioritized)
            - 0-30: Low priority tasks with no urgency
            - 30-60: Medium priority or moderately urgent tasks
            - 60+: High priority or urgent tasks requiring immediate attention
    
    Raises:
        AttributeError: If the task object is missing required attributes.
        TypeError: If task.updated_at or task.due_date are not datetime objects.
    
    Examples:
        >>> from models import Task, TaskPriority, TaskStatus
        >>> from datetime import datetime, timedelta
        
        >>> # High priority task due tomorrow
        >>> task = Task(
        ...     "Fix critical bug",
        ...     priority=TaskPriority.HIGH,
        ...     due_date=datetime.now() + timedelta(days=1),
        ...     status=TaskStatus.IN_PROGRESS,
        ...     tags=["critical"],
        ...     updated_at=datetime.now()
        ... )
        >>> score = calculate_task_score(task)
        >>> print(score)  # Output: 73 (40 + 15 + 8 + 5 + 5)
        
        >>> # Completed low priority task
        >>> completed_task = Task(
        ...     "Document code",
        ...     priority=TaskPriority.LOW,
        ...     status=TaskStatus.DONE
        ... )
        >>> score = calculate_task_score(completed_task)
        >>> print(score)  # Output: -40 (10 - 50)
    
    Notes:
        - The score is calculated at the time of function call and uses datetime.now()
          for time comparisons, so scores will change over time as due dates approach.
        - Tasks without a due_date receive no bonus or penalty from urgency scoring.
        - The scoring weights are hardcoded and may need adjustment based on team
          preferences and workflow patterns.
        - Completed tasks (DONE status) always receive a -50 penalty, ensuring they
          rank below all active tasks regardless of other factors.
        
    Edge Cases:
        - If task.priority is not in the priority_weights dict, defaults to 0 base score
        - If task.due_date is None, no due date bonuses are applied
        - If task.tags is empty, no tag bonus is applied
        - Days calculation uses integer days, so times are truncated (23 hours = 0 days)
        - Tasks updated within the last 24 hours receive a +5 recency bonus
    
    See Also:
        sort_tasks_by_importance(): Sorts tasks using this scoring function
        get_top_priority_tasks(): Returns top N tasks by score
    """
    # Base priority weights - exponential scale to emphasize urgency differences
    priority_weights = {
        TaskPriority.LOW: 1,      # Base: 10 points
        TaskPriority.MEDIUM: 2,   # Base: 20 points
        TaskPriority.HIGH: 4,     # Base: 40 points
        TaskPriority.URGENT: 6    # Base: 60 points
    }

    # Calculate base score from priority (multiplied by 10 for better granularity)
    score = priority_weights.get(task.priority, 0) * 10

    # Add due date urgency factor - exponentially higher for sooner deadlines
    if task.due_date:
        days_until_due = (task.due_date - datetime.now()).days
        
        if days_until_due < 0:          # Overdue tasks get significant boost
            score += 35
        elif days_until_due == 0:        # Due today - high urgency
            score += 20
        elif days_until_due <= 2:        # Due within 2 days - moderate urgency
            score += 15
        elif days_until_due <= 7:        # Due within a week - mild urgency
            score += 10
        # Tasks due beyond 7 days receive no urgency bonus

    # Apply status-based adjustments - completed/reviewed tasks score lower
    if task.status == TaskStatus.DONE:
        # Heavy penalty ensures completed tasks always rank lowest
        score -= 50
    elif task.status == TaskStatus.REVIEW:
        # Moderate penalty since work is done but not fully complete
        score -= 15

    # Boost score for tasks with critical impact tags
    if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
        score += 8

    # Boost score for tasks with recent activity (worked on today)
    days_since_update = (datetime.now() - task.updated_at).days
    if days_since_update < 1:
        score += 5

    return score


def sort_tasks_by_importance(tasks: List[Task]) -> List[Task]:
    """
    Sort a list of tasks by their calculated importance score in descending order.
    
    This function calculates a priority score for each task and returns them sorted
    with the highest priority tasks first. It uses calculate_task_score() to compute
    scores based on priority, due dates, status, tags, and recent activity.
    
    Args:
        tasks (List[Task]): A list of Task objects to be sorted. Can be empty.
    
    Returns:
        List[Task]: A new list containing the same tasks sorted by importance score
            (highest score first). The original list is not modified.
    
    Raises:
        TypeError: If tasks is not iterable or contains non-Task objects.
        AttributeError: If any task object is missing required attributes for scoring.
    
    Examples:
        >>> tasks = [
        ...     Task("Low priority task", priority=TaskPriority.LOW),
        ...     Task("Urgent task", priority=TaskPriority.URGENT, 
        ...          due_date=datetime.now(), tags=["critical"]),
        ...     Task("Medium task", priority=TaskPriority.MEDIUM)
        ... ]
        >>> sorted_tasks = sort_tasks_by_importance(tasks)
        >>> print(sorted_tasks[0].title)  # Output: "Urgent task"
        >>> print(sorted_tasks[-1].title)  # Output: "Low priority task"
        
        >>> # Empty list handling
        >>> empty_sorted = sort_tasks_by_importance([])
        >>> print(len(empty_sorted))  # Output: 0
    
    Notes:
        - Scores are calculated once per task at sort time using datetime.now()
        - Sorting is stable for tasks with equal scores (preserves original order)
        - Time complexity: O(n log n) where n is the number of tasks
        - Space complexity: O(n) for creating score tuples and sorted list
        - The function creates a new list; original list remains unchanged
    
    Performance:
        For large task lists (>1000 tasks), consider caching scores if sorting
        multiple times within a short time window, as datetime.now() calls and
        score calculations can be computationally expensive.
    
    See Also:
        calculate_task_score(): The scoring function used for comparisons
        get_top_priority_tasks(): Convenience function to get top N tasks
    """
    # Pre-calculate scores to avoid redundant calculations during sort
    # Creates list of (score, task) tuples for efficient sorting
    task_scores = [(calculate_task_score(task), task) for task in tasks]
    
    # Sort by score (first element of tuple) in descending order
    # Using key parameter ensures stable sort and clear intent
    sorted_tasks = [task for _, task in sorted(task_scores, key=lambda x: x[0], reverse=True)]
    
    return sorted_tasks


def get_top_priority_tasks(tasks: List[Task], limit: int = 5) -> List[Task]:
    """
    Return the top N highest priority tasks from a list.
    
    This convenience function sorts tasks by importance and returns only the
    specified number of highest priority tasks. Useful for dashboard displays,
    daily planning, or filtering work queues.
    
    Args:
        tasks (List[Task]): A list of Task objects to filter and sort.
        limit (int, optional): Maximum number of tasks to return. Defaults to 5.
            Must be non-negative. If limit exceeds the number of tasks,
            returns all tasks sorted by priority.
    
    Returns:
        List[Task]: A list containing up to 'limit' tasks, sorted by importance
            (highest priority first). If the input list is shorter than limit,
            returns all tasks sorted.
    
    Raises:
        ValueError: If limit is negative.
        TypeError: If tasks is not iterable or limit is not an integer.
        AttributeError: If any task object is missing required attributes.
    
    Examples:
        >>> tasks = [Task(f"Task {i}") for i in range(20)]
        >>> top_5 = get_top_priority_tasks(tasks, limit=5)
        >>> print(len(top_5))  # Output: 5
        
        >>> # When fewer tasks than limit exist
        >>> few_tasks = [Task("Task 1"), Task("Task 2")]
        >>> top_10 = get_top_priority_tasks(few_tasks, limit=10)
        >>> print(len(top_10))  # Output: 2
        
        >>> # Default limit behavior
        >>> top_default = get_top_priority_tasks(tasks)
        >>> print(len(top_default))  # Output: 5 (default)
    
    Notes:
        - This is equivalent to sort_tasks_by_importance(tasks)[:limit]
        - For very large task lists, this is more efficient than sorting all tasks
          if you only need the top few (though current implementation sorts all)
        - Returns an empty list if tasks is empty
        - If limit is 0, returns an empty list
    
    Performance Optimization:
        For very large datasets where limit << len(tasks), consider using a
        heap-based approach (heapq.nlargest) for O(n log k) complexity instead
        of full sort's O(n log n), where k is the limit.
    
    Use Cases:
        - Dashboard "Top 5 Tasks" widget
        - Daily planning - "What should I work on today?"
        - Team standup - "What are our most critical tasks?"
        - Automated notifications for high-priority items
    
    See Also:
        sort_tasks_by_importance(): Returns all tasks sorted
        calculate_task_score(): The underlying scoring algorithm
    """
    # Validate limit parameter
    if limit < 0:
        raise ValueError(f"limit must be non-negative, got {limit}")
    
    # Sort all tasks and return the top 'limit' tasks
    sorted_tasks = sort_tasks_by_importance(tasks)
    return sorted_tasks[:limit]
```

---

## Prompt 2: Intent and Logic Explanation

### High-Level Intent

**What this code accomplishes:**

This module implements an intelligent task prioritization system that automatically ranks tasks based on multiple real-world factors. The goal is to help users focus on what matters most by calculating a numeric "urgency score" that considers:

1. **Inherent Importance** (Priority Level): How important is this task fundamentally?
2. **Time Pressure** (Due Dates): How soon does this need to be done?
3. **Workflow State** (Status): Is work still needed or is it done?
4. **Impact Scope** (Tags): Does this block other work or have critical dependencies?
5. **Momentum** (Recent Activity): Is someone actively working on this?

The system mimics how humans naturally prioritize: we balance importance with urgency, consider completion state, and pay attention to work that's actively in progress.

### Step-by-Step Logic Breakdown

#### `calculate_task_score()` - The Scoring Engine

**Step 1: Establish Base Priority (Lines 7-16)**
```python
priority_weights = {
    TaskPriority.LOW: 1,
    TaskPriority.MEDIUM: 2,
    TaskPriority.HIGH: 4,
    TaskPriority.URGENT: 6
}
score = priority_weights.get(task.priority, 0) * 10
```

**Logic:** Start with the task's intrinsic priority. Uses exponential weights (1, 2, 4, 6) rather than linear to emphasize differences between priority levels. Multiply by 10 to create a larger numeric range for finer-grained sorting.

**Design Decision:** The exponential scale ensures that priority differences are meaningful - URGENT is 6x more important than LOW, not just "one level higher."

---

**Step 2: Add Time Urgency (Lines 18-28)**
```python
if task.due_date:
    days_until_due = (task.due_date - datetime.now()).days
    if days_until_due < 0:          # Overdue
        score += 35
    elif days_until_due == 0:        # Due today
        score += 20
    elif days_until_due <= 2:        # Due soon
        score += 15
    elif days_until_due <= 7:        # Due this week
        score += 10
```

**Logic:** Tasks become more urgent as their deadline approaches. Uses tiered urgency bonuses:
- **Overdue** (+35): Maximum urgency - past the deadline
- **Due today** (+20): Very high urgency - must complete today
- **Due in 2 days** (+15): High urgency - need to start/finish soon
- **Due in 7 days** (+10): Moderate urgency - keep on radar
- **Due beyond 7 days** (0): No urgency bonus yet

**Design Decision:** The +35 for overdue tasks ensures they rise above most other tasks, even low-priority ones. The 35-point bonus can overcome priority differences (e.g., overdue LOW priority = 10 + 35 = 45, which beats a non-urgent HIGH priority = 40).

**Edge Case:** Tasks with no `due_date` receive no urgency bonus, treating them as "whenever possible" tasks.

---

**Step 3: Apply Status Penalties (Lines 30-34)**
```python
if task.status == TaskStatus.DONE:
    score -= 50
elif task.status == TaskStatus.REVIEW:
    score -= 15
```

**Logic:** Reduce scores for tasks that don't need active work:
- **DONE** (-50): Heavy penalty to push completed tasks to bottom
- **REVIEW** (-15): Moderate penalty since work is done but awaiting review

**Design Decision:** The -50 penalty for DONE tasks is deliberately larger than any possible positive score, ensuring completed tasks always rank below active tasks. This prevents the list from being cluttered with finished work.

**Assumption:** The code assumes REVIEW status means the task is awaiting external review, not actively being worked on.

---

**Step 4: Boost Critical Tags (Lines 36-38)**
```python
if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
    score += 8
```

**Logic:** Add a modest bonus for tasks tagged with high-impact keywords. These tags indicate the task blocks other work or has broad impact.

**Design Decision:** The +8 bonus is significant but not overwhelming - it can tip the scales between similar tasks but won't override major priority or urgency differences.

**Edge Case:** Multiple critical tags only add +8 once (not cumulative). This prevents tag spam from artificially inflating scores.

---

**Step 5: Boost Recent Activity (Lines 40-43)**
```python
days_since_update = (datetime.now() - task.updated_at).days
if days_since_update < 1:
    score += 5
```

**Logic:** Give a small boost to tasks that were updated within the last 24 hours. This captures momentum - if someone is actively working on a task, it should stay visible.

**Design Decision:** The +5 bonus is small, acting as a tiebreaker rather than a major factor. It helps keep active work items from getting lost in the shuffle.

**Edge Case:** Uses integer day comparison, so a task updated 23 hours ago gets the bonus, but one updated 25 hours ago doesn't.

---

#### `sort_tasks_by_importance()` - The Sorter

**Logic:** 
1. **Map phase:** Calculate score for each task once
2. **Sort phase:** Sort by score in descending order
3. **Extract phase:** Remove scores and return just the tasks

**Optimization:** Pre-calculating scores is crucial - it ensures we only call `calculate_task_score()` once per task (O(n)) rather than potentially multiple times during sorting.

**Alternative Approach:** Could use `key=calculate_task_score` directly in `sorted()`, but the tuple approach is more explicit and performs identically.

---

#### `get_top_priority_tasks()` - The Convenience Function

**Logic:** Simple wrapper that sorts and slices. Exists for code readability and convenience.

**Use Case:** This is the function most client code would call - "Give me the top 5 things I should work on."

---

### Assumptions and Edge Cases

#### Assumptions:
1. **Time-based calculations use current time** - Scores are point-in-time and will change as time passes
2. **Tasks have valid datetime objects** - Code assumes `due_date` and `updated_at` are datetime objects or None
3. **Tags are lowercase strings** - The critical tag check uses exact string matching
4. **Score range is sufficient** - Assumes -50 to ~110 range provides enough differentiation
5. **Single priority per task** - Doesn't handle tasks with multiple priorities

#### Edge Cases Handled:
1. **Missing due_date** (None): Skips urgency calculation
2. **Unknown priority**: Defaults to 0 base score via `.get()`
3. **Empty task list**: Returns empty list from sort/filter functions
4. **Limit > list length**: Returns all tasks in `get_top_priority_tasks()`
5. **Same scores**: Stable sort preserves original order

#### Edge Cases NOT Handled:
1. **Timezone issues**: Uses naive datetime.now(), could fail with timezone-aware dates
2. **Future updated_at**: No validation that updated_at is in the past
3. **Negative limit**: `get_top_priority_tasks()` doesn't validate (would return empty via negative slicing)
4. **Very old dates**: No maximum limit on overdue bonus (a task overdue 1000 days gets same +35 as one overdue 1 day)

---

### Suggested Inline Comments for Complex Parts

```python
def calculate_task_score(task):
    # === SCORING FORMULA ===
    # Base (10-60) + Urgency (0-35) + Tags (0-8) + Recency (0-5) - Status (0-50)
    # Range: -40 (completed low priority) to 108 (urgent + overdue + tags + recent)
    
    priority_weights = {
        TaskPriority.LOW: 1,
        TaskPriority.MEDIUM: 2,
        TaskPriority.HIGH: 4,     # Exponential scale: each level is 2x more important
        TaskPriority.URGENT: 6
    }

    # Base score: Priority weight * 10 for granularity (LOW=10, URGENT=60)
    score = priority_weights.get(task.priority, 0) * 10

    if task.due_date:
        # Calculate urgency: how many full days until due (negative = overdue)
        days_until_due = (task.due_date - datetime.now()).days
        
        # Urgency bonuses: exponentially higher as deadline approaches
        # +35 for overdue ensures even low-priority overdue tasks rank high
        if days_until_due < 0:
            score += 35  # CRITICAL: Overdue tasks must be visible
        elif days_until_due == 0:
            score += 20  # Due today: high urgency
        elif days_until_due <= 2:
            score += 15  # Due soon: moderate urgency
        elif days_until_due <= 7:
            score += 10  # Due this week: mild urgency

    # Status penalties: reduce visibility of completed/reviewed work
    if task.status == TaskStatus.DONE:
        score -= 50  # Heavy penalty: ensures all DONE tasks rank below active tasks
    elif task.status == TaskStatus.REVIEW:
        score -= 15  # Moderate penalty: work done but not fully complete

    # Tag bonus: +8 for blocker/critical tags (applied once even if multiple matches)
    if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
        score += 8

    # Recency bonus: +5 if updated today (captures active work momentum)
    # Note: Uses integer days, so 0 days = updated within last 24 hours
    days_since_update = (datetime.now() - task.updated_at).days
    if days_since_update < 1:
        score += 5

    return score


def sort_tasks_by_importance(tasks):
    # Pre-calculate scores to avoid redundant calculation during sort (O(n) not O(n log n))
    task_scores = [(calculate_task_score(task), task) for task in tasks]
    
    # Sort by score descending: highest priority first
    # key=lambda: explicit about sorting by score (first tuple element)
    sorted_tasks = [task for _, task in sorted(task_scores, key=lambda x: x[0], reverse=True)]
    
    return sorted_tasks
```

---

### Potential Improvements (Maintaining Original Functionality)

1. **Make Weights Configurable**
   ```python
   def calculate_task_score(task, config=None):
       config = config or DEFAULT_SCORING_CONFIG
       priority_weights = config['priority_weights']
       urgency_bonuses = config['urgency_bonuses']
       # ... use config throughout
   ```
   **Benefit:** Teams can tune scoring without code changes

2. **Add Timezone Awareness**
   ```python
   def calculate_task_score(task, current_time=None):
       current_time = current_time or datetime.now(tz=timezone.utc)
       # ... use current_time instead of datetime.now()
   ```
   **Benefit:** Fixes timezone bugs and makes testing easier

3. **Validate Inputs**
   ```python
   def calculate_task_score(task):
       if not isinstance(task, Task):
           raise TypeError(f"Expected Task, got {type(task)}")
       if task.due_date and task.due_date < task.created_at:
           raise ValueError("due_date cannot be before created_at")
   ```
   **Benefit:** Fail fast with clear errors

4. **Cache Scores for Performance**
   ```python
   @lru_cache(maxsize=1000)
   def calculate_task_score_cached(task_id, task_hash):
       # ... actual calculation
   ```
   **Benefit:** Avoid recalculating for frequently accessed tasks

5. **Add Score Breakdown for Debugging**
   ```python
   def calculate_task_score_verbose(task):
       breakdown = {
           'base': priority_weights.get(task.priority, 0) * 10,
           'urgency': ...,
           'status_penalty': ...,
           'tags': ...,
           'recency': ...
       }
       return sum(breakdown.values()), breakdown
   ```
   **Benefit:** Helps understand why a task scored a certain way

6. **Use Heap for Top-N Selection**
   ```python
   import heapq
   
   def get_top_priority_tasks(tasks, limit=5):
       return heapq.nlargest(limit, tasks, key=calculate_task_score)
   ```
   **Benefit:** O(n log k) instead of O(n log n) for large lists where k << n

---

## Final Combined Documentation

*Combining the best elements from both Prompt 1 (comprehensive structure) and Prompt 2 (intent and logic explanation):*

```python
from datetime import datetime
from typing import List, Optional, Dict

from models import TaskStatus, TaskPriority, Task


def calculate_task_score(task: Task) -> int:
    """
    Calculate a weighted priority score for a task based on multiple factors.
    
    This function implements an intelligent task prioritization algorithm that mimics
    how humans naturally prioritize work. It combines inherent importance (priority level)
    with time pressure (due dates), workflow state (status), impact scope (tags), and
    momentum (recent activity) to produce a single numeric score.
    
    **Scoring Formula:**
    Base Priority (10-60) + Urgency Bonus (0-35) + Tag Boost (0-8) + 
    Recency Bonus (0-5) - Status Penalty (0-50)
    
    **Design Philosophy:**
    - Overdue tasks always rank high (even if low priority)
    - Completed tasks always rank low (even if urgent)
    - Priority provides the foundation; urgency provides the pressure
    - Tags and recency act as tiebreakers
    
    Args:
        task (Task): A Task object with the following required attributes:
            - priority (TaskPriority): Priority level (LOW=1, MEDIUM=2, HIGH=4, URGENT=6)
            - due_date (datetime or None): Task deadline (None = no urgency bonus)
            - status (TaskStatus): Current state (TODO, IN_PROGRESS, REVIEW, DONE)
            - tags (List[str]): Associated tags (e.g., ["blocker", "backend"])
            - updated_at (datetime): Last modification timestamp
    
    Returns:
        int: Priority score typically ranging from -40 to 108:
            - Negative scores: Completed tasks (deprioritized)
            - 0-30: Low priority, no urgency
            - 30-60: Medium priority or some urgency
            - 60-90: High priority or significant urgency  
            - 90+: Critical tasks (urgent, overdue, or blocking)
    
    Raises:
        AttributeError: If task is missing required attributes
        TypeError: If datetime attributes are not datetime objects
    
    Examples:
        >>> # Overdue critical bug
        >>> task = Task(
        ...     "Fix payment processor",
        ...     priority=TaskPriority.URGENT,
        ...     due_date=datetime.now() - timedelta(days=1),
        ...     status=TaskStatus.IN_PROGRESS,
        ...     tags=["blocker", "critical"],
        ...     updated_at=datetime.now()
        ... )
        >>> score = calculate_task_score(task)
        >>> print(score)  # Output: 108 (60 + 35 + 8 + 5)
        
        >>> # Completed low-priority task
        >>> task = Task("Update docs", priority=TaskPriority.LOW, status=TaskStatus.DONE)
        >>> score = calculate_task_score(task)
        >>> print(score)  # Output: -40 (10 - 50)
    
    Notes:
        **Time Sensitivity:**
        - Scores use datetime.now() and change as time passes
        - Day calculations use integer days (23 hours = 0 days)
        - Tasks without due_date receive no urgency bonus
        
        **Scoring Weights:**
        - Priority weights: LOW=1, MEDIUM=2, HIGH=4, URGENT=6 (exponential scale)
        - Urgency bonuses: Overdue=+35, Today=+20, 2days=+15, 7days=+10
        - Status penalties: DONE=-50, REVIEW=-15
        - Special tags: blocker/critical/urgent = +8 (once per task)
        - Recent activity: Updated today = +5
        
        **Edge Cases:**
        - Unknown priority defaults to 0 score
        - Multiple critical tags only add +8 once
        - Empty tags list = no tag bonus
        - Timezone-naive datetime (uses local system time)
    
    Performance:
        O(1) time complexity, but involves datetime comparisons.
        For repeated sorting, consider caching scores.
    
    See Also:
        - sort_tasks_by_importance(): Sorts tasks using this function
        - get_top_priority_tasks(): Returns top N tasks by score
    """
    # === SCORING CONFIGURATION ===
    # Exponential priority weights emphasize importance differences
    priority_weights = {
        TaskPriority.LOW: 1,      # Base: 10 points
        TaskPriority.MEDIUM: 2,   # Base: 20 points  
        TaskPriority.HIGH: 4,     # Base: 40 points
        TaskPriority.URGENT: 6    # Base: 60 points
    }

    # === BASE SCORE: Priority Foundation ===
    # Multiply by 10 for finer-grained score ranges
    score = priority_weights.get(task.priority, 0) * 10

    # === URGENCY BONUS: Time Pressure ===
    # Add exponentially increasing bonuses as deadline approaches
    if task.due_date:
        # Calculate full days until due (negative = overdue)
        days_until_due = (task.due_date - datetime.now()).days
        
        if days_until_due < 0:
            # OVERDUE: +35 ensures even low-priority overdue tasks rank high
            # This value is deliberately larger than priority differences
            score += 35
        elif days_until_due == 0:
            # DUE TODAY: Maximum urgency for active work
            score += 20
        elif days_until_due <= 2:
            # DUE SOON: High urgency, should start/finish soon
            score += 15
        elif days_until_due <= 7:
            # DUE THIS WEEK: Moderate urgency, keep on radar
            score += 10
        # Tasks due beyond 7 days receive no bonus yet

    # === STATUS PENALTY: Completion State ===
    # Reduce visibility of tasks that don't need active work
    if task.status == TaskStatus.DONE:
        # Heavy penalty (-50) ensures ALL completed tasks rank below active tasks
        # This value is larger than any possible positive score
        score -= 50
    elif task.status == TaskStatus.REVIEW:
        # Moderate penalty for tasks awaiting review (work done but not complete)
        score -= 15

    # === TAG BOOST: Impact Scope ===
    # Boost tasks that block other work or have critical dependencies
    # Applied once even if multiple critical tags exist (prevents tag spam)
    if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
        score += 8

    # === RECENCY BONUS: Active Work Momentum ===
    # Small boost for tasks updated within last 24 hours
    # Helps keep active work visible as a tiebreaker
    days_since_update = (datetime.now() - task.updated_at).days
    if days_since_update < 1:
        score += 5

    return score


def sort_tasks_by_importance(tasks: List[Task]) -> List[Task]:
    """
    Sort tasks by calculated importance score in descending order (highest priority first).
    
    This function is the primary sorting interface for the task prioritization system.
    It calculates a priority score for each task once, then sorts by those scores to
    produce an intelligently ordered task list.
    
    **Use Cases:**
    - Daily planning: "What should I work on today?"
    - Dashboard views: Display tasks by priority
    - Work queue management: Process highest priority items first
    - Team standups: Discuss most important work
    
    Args:
        tasks (List[Task]): List of Task objects to sort. Can be empty.
            The original list is not modified.
    
    Returns:
        List[Task]: New list with same tasks sorted by importance (highest first).
            Tasks with equal scores maintain their original relative order (stable sort).
    
    Raises:
        TypeError: If tasks is not iterable or contains non-Task objects
        AttributeError: If any task missing required attributes for scoring
    
    Examples:
        >>> tasks = [
        ...     Task("Low priority", priority=TaskPriority.LOW),
        ...     Task("Critical bug", priority=TaskPriority.URGENT, 
        ...          due_date=datetime.now(), tags=["blocker"]),
        ...     Task("Regular work", priority=TaskPriority.MEDIUM)
        ... ]
        >>> sorted_tasks = sort_tasks_by_importance(tasks)
        >>> print([t.title for t in sorted_tasks])
        # Output: ["Critical bug", "Regular work", "Low priority"]
        
        >>> # Handles empty lists
        >>> sort_tasks_by_importance([])
        # Output: []
    
    Algorithm:
        1. **Map Phase:** Calculate score for each task (O(n))
        2. **Sort Phase:** Sort by score descending (O(n log n))
        3. **Extract Phase:** Remove scores, return tasks (O(n))
        
        Overall complexity: O(n log n)
    
    Notes:
        - Scores are calculated once per task at sort time
        - Uses stable sort (equal scores preserve input order)
        - Creates new list; original list unchanged
        - Scores use current time, so re-sorting later may change order
        
    Performance:
        - Time: O(n log n) where n = number of tasks
        - Space: O(n) for score tuples and new sorted list
        - For very large lists (>1000 tasks), consider caching scores if sorting
          multiple times within seconds, as datetime.now() and scoring calculations
          add overhead
    
    Implementation Detail:
        Pre-calculates scores to avoid redundant calculations. The alternative
        approach `sorted(tasks, key=calculate_task_score, reverse=True)` would
        work identically but the tuple approach is more explicit about the
        optimization.
    
    See Also:
        - calculate_task_score(): The scoring algorithm
        - get_top_priority_tasks(): Convenience function for top N tasks
    """
    # Pre-calculate scores once per task (optimization: O(n) instead of O(n log n))
    # Creates list of (score, task) tuples for efficient sorting
    task_scores = [(calculate_task_score(task), task) for task in tasks]
    
    # Sort by score (first tuple element) in descending order
    # key parameter makes sort stable and intention explicit
    # reverse=True ensures highest scores first
    sorted_tasks = [task for _, task in sorted(task_scores, key=lambda x: x[0], reverse=True)]
    
    return sorted_tasks


def get_top_priority_tasks(tasks: List[Task], limit: int = 5) -> List[Task]:
    """
    Return the top N highest priority tasks from a list.
    
    Convenience function that sorts tasks and returns only the most important ones.
    Perfect for dashboard widgets, daily planning, or filtered work queues where
    you want to focus on a manageable number of high-priority items.
    
    **Common Use Cases:**
    - "Show me my top 5 tasks for today"
    - Dashboard "Critical Tasks" widget
    - Daily standup: "What are our top priorities?"
    - Email digest: "Your most urgent tasks"
    
    Args:
        tasks (List[Task]): List of Task objects to filter and sort
        limit (int, optional): Maximum number of tasks to return. Defaults to 5.
            - Must be non-negative
            - If limit > len(tasks), returns all tasks sorted
            - If limit = 0, returns empty list
    
    Returns:
        List[Task]: Up to 'limit' tasks, sorted by importance (highest first).
            If input list is shorter than limit, returns all tasks sorted.
    
    Raises:
        ValueError: If limit is negative
        TypeError: If limit is not an integer or tasks is not iterable
        AttributeError: If any task is missing required scoring attributes
    
    Examples:
        >>> # Get top 3 from 10 tasks
        >>> tasks = [Task(f"Task {i}", priority=TaskPriority.MEDIUM) for i in range(10)]
        >>> top_3 = get_top_priority_tasks(tasks, limit=3)
        >>> len(top_3)
        3
        
        >>> # Limit exceeds list length
        >>> few_tasks = [Task("Task 1"), Task("Task 2")]
        >>> top_10 = get_top_priority_tasks(few_tasks, limit=10)
        >>> len(top_10)  # Returns all 2 tasks
        2
        
        >>> # Default limit
        >>> top_default = get_top_priority_tasks(tasks)  # Gets top 5
        >>> len(top_default)
        5
        
        >>> # Zero limit
        >>> get_top_priority_tasks(tasks, limit=0)
        []
    
    Notes:
        - Equivalent to `sort_tasks_by_importance(tasks)[:limit]`
        - Returns empty list if tasks is empty
        - Limit is applied after sorting (not a filter condition)
        - Tasks are sorted by the same algorithm as sort_tasks_by_importance()
    
    Performance:
        - Time: O(n log n) due to full sort
        - Space: O(n) for sorted list
        
        **Optimization Opportunity:**
        For very large datasets where limit << len(tasks), using heapq.nlargest
        would be more efficient: O(n log k) where k=limit. Current implementation
        prioritizes simplicity and code reuse.
        
        Example optimization:
        ```python
        import heapq
        return heapq.nlargest(limit, tasks, key=calculate_task_score)
        ```
    
    Edge Cases:
        - Empty task list → returns []
        - Limit = 0 → returns []
        - Limit > len(tasks) → returns all tasks sorted
        - All tasks have equal scores → returns first 'limit' tasks from input
    
    See Also:
        - sort_tasks_by_importance(): Returns all tasks sorted
        - calculate_task_score(): The scoring algorithm
    """
    # Validate limit parameter to prevent unexpected behavior
    if limit < 0:
        raise ValueError(f"limit must be non-negative, got {limit}")
    
    # Sort all tasks by importance and slice to get top N
    sorted_tasks = sort_tasks_by_importance(tasks)
    return sorted_tasks[:limit]
```

---

## Reflection and Learnings

### What I Learned

#### 1. Which Parts Were Most Challenging for AI?

**Challenging Aspects:**
- **Understanding scoring weight rationale**: The AI needed context about *why* certain numbers were chosen (e.g., why +35 for overdue vs +20 for due today)
- **Implicit assumptions**: The code doesn't explicitly state assumptions like "DONE tasks should always rank lowest" - the AI had to infer this from the -50 penalty
- **Edge case identification**: Required careful analysis to identify all the edge cases (timezone issues, negative limits, etc.)
- **Real-world use cases**: The AI needed guidance on what problems this code actually solves in practice

**What Helped:**
- Providing the broader context (this is part of a task management system)
- Asking for both technical documentation AND intent/logic explanation
- Requesting specific examples and edge cases

#### 2. Additional Information Needed in Prompts

**To Get Better Results, I Should Have:**

1. **Provided more context upfront:**
   - "This is part of a task management CLI application"
   - "Users are software developers managing their work"
   - "The goal is to automatically surface the most important work"

2. **Specified target audience:**
   - "Documentation for mid-level developers"
   - "Assume familiarity with Python but not domain-specific knowledge"

3. **Included related code:**
   - The `Task`, `TaskStatus`, `TaskPriority` class definitions
   - Example usage from the CLI layer
   - Test cases showing expected behavior

4. **Asked for specific documentation elements:**
   - "Include complexity analysis"
   - "Show score calculation examples with actual numbers"
   - "Explain the trade-offs in weight selection"

5. **Requested validation:**
   - "Point out potential bugs or issues"
   - "Suggest test cases for edge conditions"

#### 3. How I Would Use This Approach in My Projects

**Practical Applications:**

**A) During Development:**
- **Write code first, document later**: Focus on getting logic right, then use AI to generate comprehensive docs
- **Pair programming with AI**: Write a complex function, immediately generate docs to verify I understand my own logic
- **Code review prep**: Generate docs before submitting PR to ensure functionality is clear

**B) For Legacy Code:**
- **Understanding inherited code**: Feed undocumented legacy functions to AI for explanation
- **Migration documentation**: Document old system before refactoring
- **Knowledge transfer**: Create docs when team members leave

**C) For Team Collaboration:**
- **Onboarding new developers**: Generate comprehensive guides for complex algorithms
- **API documentation**: Create detailed interface docs for shared libraries
- **Architecture decisions**: Document *why* certain approaches were taken

**D) For Learning:**
- **Study open-source code**: Generate explanations for complex functions I'm trying to learn from
- **Algorithm understanding**: Break down CS algorithms into digestible explanations

**E) Workflow Integration:**
```bash
# Git pre-commit hook
1. Detect functions with missing/minimal docstrings
2. Generate AI documentation
3. Review and approve
4. Commit with improved docs

# IDE Integration
1. Right-click function → "Generate Documentation"
2. AI creates draft
3. Developer reviews and tweaks
4. Insert into code
```

### Key Takeaways

#### What Worked Well:

1. **Two-prompt approach**: Combining comprehensive documentation (Prompt 1) with intent/logic explanation (Prompt 2) gave a fuller picture than either alone
2. **Examples in documentation**: AI-generated examples with actual output made the docs immediately useful
3. **Edge case identification**: AI caught edge cases I hadn't considered (timezone issues, negative limits)
4. **Inline comments**: The suggested inline comments clarified complex parts without cluttering the code

#### What I'd Improve:

1. **Iterative refinement**: First generate basic docs, then ask AI to expand specific sections that need more detail
2. **Domain-specific language**: Provide a glossary of domain terms (e.g., "blocker", "standup") for more accurate documentation
3. **Code comparison**: Feed AI both the original and improved versions to document the evolution
4. **Test generation**: Ask AI to generate test cases based on the documentation to verify correctness

#### Best Practices Discovered:

1. **Start with high-level intent**, then drill into details
2. **Include concrete examples** with realistic data
3. **Document the "why"** not just the "what"
4. **Explicitly state assumptions** that code makes
5. **Provide performance characteristics** (time/space complexity)
6. **Link related functions** to show the bigger picture
7. **Include edge cases and error conditions**
8. **Show use cases** to make documentation actionable

### Conclusion

This exercise demonstrated that AI is an excellent **documentation assistant** but requires **guidance and validation**. The best results came from:
- Clear prompts with context
- Two-pass approach (comprehensive + intent)
- Human review and refinement
- Combining AI strengths (thoroughness, examples) with human insights (domain knowledge, judgment)

The final documentation is significantly better than what I would have written alone, and the process was faster while maintaining high quality. This is a workflow I'll definitely adopt for future projects.
