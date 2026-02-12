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
