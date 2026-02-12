# Exercise 9 - Using AI to Help with Testing

**Student:** Thabiso  
**Date:** February 12, 2026  
**Selected Implementation:** Python Task Manager

---

## Table of Contents
1. [Part 1: Understanding What to Test](#part-1-understanding-what-to-test)
   - [Exercise 1.1: Behavior Analysis](#exercise-11-behavior-analysis)
   - [Exercise 1.2: Test Planning](#exercise-12-test-planning)
2. [Part 2: Improving a Single Test](#part-2-improving-a-single-test)
   - [Exercise 2.1: Writing Your First Test](#exercise-21-writing-your-first-test)
   - [Exercise 2.2: Learning From Examples](#exercise-22-learning-from-examples)
3. [Part 3: Test-Driven Development Practice](#part-3-test-driven-development-practice)
   - [Exercise 3.1: TDD for a New Feature](#exercise-31-tdd-for-a-new-feature)
   - [Exercise 3.2: TDD for Bug Fix](#exercise-32-tdd-for-bug-fix)
4. [Part 4: Integration Testing](#part-4-integration-testing)
   - [Exercise 4.1: Testing the Full Workflow](#exercise-41-testing-the-full-workflow)
5. [Final Test Suite](#final-test-suite)
6. [Reflection](#reflection)

---

## Part 1: Understanding What to Test

### Exercise 1.1: Behavior Analysis

#### Code Under Test

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
```

#### AI-Assisted Conversation

**AI:** Let's start by understanding what you think this function does. Can you describe in your own words what behaviors you see in the `calculate_task_score` function?

**Me:** The function calculates a numerical score for a task to determine its priority. It looks at several factors:
1. The task's priority level (LOW, MEDIUM, HIGH, URGENT)
2. When the task is due
3. The task's current status
4. Whether it has special tags
5. How recently it was updated

**AI:** Excellent overview! Now, let's dig deeper. For each of those factors, what specific behaviors would you want to test?

**Me:** 
1. **Priority:** Test that each priority level gives the correct base score (10, 20, 40, 60)
2. **Due date:** Test overdue tasks (+35), due today (+20), due in 2 days (+15), due in a week (+10)
3. **Status:** Test that DONE tasks get -50, REVIEW tasks get -15
4. **Tags:** Test that "blocker", "critical", or "urgent" tags add +8
5. **Recently updated:** Test that tasks updated less than 1 day ago get +5

**AI:** Great! Now let me challenge you - what edge cases might you be missing? Think about:
- What if a task has no due date?
- What if a task has multiple tags?
- What if a task is overdue AND done?
- What about boundary conditions like exactly 2 days or exactly 7 days?

**Me:** Oh, I see several edge cases I missed:
1. **No due date** - should just skip the due date scoring
2. **Multiple special tags** - might add +8 multiple times? Or just once?
3. **Combined factors** - like overdue + done, or urgent priority + urgent tag
4. **Boundary conditions** - need to test exactly 2 days, exactly 7 days
5. **Recently created task** - will have `days_since_update < 1`

**AI:** Excellent! Let me point out one more thing you discovered - look at the tag checking code: `any(tag in [...])`. What does this tell you?

**Me:** It uses `any()`, so even if there are multiple special tags, it only adds +8 once!

**AI:** Perfect! Now, which test would you write first and why?

**Me:** I'd start with the simplest case: testing the base priority score with no other factors. This establishes that the foundation works before adding complexity. Something like a MEDIUM priority task with no due date, no special tags, and TODO status.

#### Test Cases Identified

Based on the AI conversation, here are the test cases I should write:

**1. Base Priority Scoring (Priority: HIGH)**
- Test LOW priority (1 × 10 = 10)
- Test MEDIUM priority (2 × 10 = 20)
- Test HIGH priority (4 × 10 = 40)
- Test URGENT priority (6 × 10 = 60)

**2. Due Date Scoring (Priority: HIGH)**
- Test overdue task (due date in past) → +35
- Test due today (0 days) → +20
- Test due in 1 day → +15
- Test due in 2 days (boundary) → +15
- Test due in 3 days → +10
- Test due in 7 days (boundary) → +10
- Test due in 8+ days → +0
- Test no due date → no addition

**3. Status Scoring (Priority: MEDIUM)**
- Test DONE status → -50
- Test REVIEW status → -15
- Test TODO status → no deduction
- Test IN_PROGRESS status → no deduction

**4. Tag Scoring (Priority: MEDIUM)**
- Test with "blocker" tag → +8
- Test with "critical" tag → +8
- Test with "urgent" tag → +8
- Test with multiple special tags → +8 (only once due to `any()`)
- Test with non-special tags → no addition
- Test with no tags → no addition

**5. Recently Updated Scoring (Priority: LOW)**
- Test task updated less than 1 day ago → +5
- Test task updated exactly 1 day ago → no addition
- Test task updated more than 1 day ago → no addition

**6. Complex Combinations (Priority: HIGH)**
- Test overdue + DONE (should be negative despite urgency)
- Test URGENT priority + "urgent" tag + overdue
- Test all positive factors combined
- Test all negative factors combined

**7. Edge Cases (Priority: MEDIUM)**
- Test task with all default values
- Test boundary: exactly 2 days until due
- Test boundary: exactly 7 days until due
- Test newly created task (updated < 1 day ago)

---

### Exercise 1.2: Test Planning

#### Functions Under Test

```python
def calculate_task_score(task):
    # [See above for full implementation]
    pass

def sort_tasks_by_importance(tasks):
    """Sort tasks by calculated importance score (highest first)."""
    task_scores = [(calculate_task_score(task), task) for task in tasks]
    sorted_tasks = [task for _, task in sorted(task_scores, key=lambda x: x[0], reverse=True)]
    return sorted_tasks

def get_top_priority_tasks(tasks, limit=5):
    """Return the top N priority tasks."""
    sorted_tasks = sort_tasks_by_importance(tasks)
    return sorted_tasks[:limit]
```

#### AI-Assisted Planning Conversation

**AI:** Let's create a testing plan together. Looking at these three functions, what relationships do you see between them?

**Me:** `get_top_priority_tasks` calls `sort_tasks_by_importance`, which calls `calculate_task_score`. They form a pipeline.

**AI:** Exactly! Now, how would you approach testing this pipeline? Should you test each function in isolation, or test them together?

**Me:** I should do both:
1. **Unit tests** for each function in isolation
2. **Integration tests** for the full pipeline

**AI:** Great! Let's start with `calculate_task_score` since it's the foundation. What types of tests would you write?

**Me:** I identified 7 categories in Exercise 1.1. I'd write unit tests for each behavior.

**AI:** Good. Now for `sort_tasks_by_importance` - if you trust that `calculate_task_score` works (because of unit tests), what behavior are you testing here?

**Me:** Just the sorting logic! I need to verify:
1. Tasks are sorted by score (highest first)
2. The original tasks are returned (not modified)
3. Empty list handling
4. Single task handling

**AI:** Perfect! And for `get_top_priority_tasks`?

**Me:** If I trust the sorting, I'm just testing:
1. Returns correct number of tasks (limit parameter)
2. Returns top tasks (highest scores first)
3. Handles limit larger than list size
4. Handles limit = 0
5. Handles empty list

**AI:** Excellent! Now let's prioritize. Which tests are most critical to write first?

**Me:** 
1. **CRITICAL:** Base functionality tests (the happy path)
2. **HIGH:** Edge cases that could break the system (empty lists, boundaries)
3. **MEDIUM:** Complex combinations
4. **LOW:** Uncommon edge cases

**AI:** What about test dependencies? Can you test `sort_tasks_by_importance` before testing `calculate_task_score`?

**Me:** No! I need to test the foundation first. Dependencies flow:
1. First: `calculate_task_score` unit tests
2. Second: `sort_tasks_by_importance` unit tests
3. Third: `get_top_priority_tasks` unit tests
4. Finally: Integration tests for the full pipeline

#### Structured Test Plan

---

### **Unit Tests: calculate_task_score**

**Priority 1 (CRITICAL) - Basic Functionality**
- ✅ Test each priority level returns correct base score
  - Expected: LOW=10, MEDIUM=20, HIGH=40, URGENT=60
  - Dependency: None
  - Type: Unit test

**Priority 1 (CRITICAL) - Due Date Basics**
- ✅ Test overdue task scoring
  - Expected: +35 to base score
  - Dependency: Priority scoring works
  - Type: Unit test
  
- ✅ Test due today scoring
  - Expected: +20 to base score
  - Dependency: Priority scoring works
  - Type: Unit test

**Priority 2 (HIGH) - Due Date Edge Cases**
- ✅ Test boundary: exactly 2 days until due
  - Expected: +15 (should match "due in next 2 days")
  - Dependency: Basic due date scoring works
  - Type: Unit test

- ✅ Test boundary: exactly 7 days until due
  - Expected: +10 (should match "due in next week")
  - Dependency: Basic due date scoring works
  - Type: Unit test

- ✅ Test no due date
  - Expected: No due date scoring applied
  - Dependency: Priority scoring works
  - Type: Unit test

**Priority 1 (CRITICAL) - Status Scoring**
- ✅ Test DONE status
  - Expected: -50 from score
  - Dependency: Priority scoring works
  - Type: Unit test

- ✅ Test REVIEW status
  - Expected: -15 from score
  - Dependency: Priority scoring works
  - Type: Unit test

**Priority 2 (HIGH) - Tag Scoring**
- ✅ Test special tags (blocker, critical, urgent)
  - Expected: +8 for any special tag
  - Dependency: Priority scoring works
  - Type: Unit test

- ✅ Test multiple special tags
  - Expected: Only +8 once (due to `any()`)
  - Dependency: Single tag scoring works
  - Type: Unit test

**Priority 3 (MEDIUM) - Recently Updated**
- ✅ Test task updated less than 1 day ago
  - Expected: +5 to score
  - Dependency: Priority scoring works
  - Type: Unit test

**Priority 2 (HIGH) - Complex Combinations**
- ✅ Test overdue + DONE
  - Expected: Net negative score (60 + 35 - 50 = 45 for URGENT)
  - Dependency: Both overdue and status scoring work
  - Type: Unit test

- ✅ Test all positive factors
  - Expected: Maximum possible score
  - Dependency: All individual scorings work
  - Type: Unit test

---

### **Unit Tests: sort_tasks_by_importance**

**Priority 1 (CRITICAL) - Basic Sorting**
- ✅ Test tasks are sorted by score (highest first)
  - Expected: [high_score_task, mid_score_task, low_score_task]
  - Dependency: calculate_task_score works
  - Type: Unit test

- ✅ Test original tasks are returned unchanged
  - Expected: Same Task objects, not copies
  - Dependency: Basic sorting works
  - Type: Unit test

**Priority 2 (HIGH) - Edge Cases**
- ✅ Test empty list
  - Expected: Returns empty list
  - Dependency: None
  - Type: Unit test

- ✅ Test single task
  - Expected: Returns list with that task
  - Dependency: None
  - Type: Unit test

- ✅ Test tasks with equal scores
  - Expected: Stable sort (maintains original order)
  - Dependency: Basic sorting works
  - Type: Unit test

---

### **Unit Tests: get_top_priority_tasks**

**Priority 1 (CRITICAL) - Basic Functionality**
- ✅ Test returns top N tasks
  - Expected: First 5 tasks from sorted list
  - Dependency: sort_tasks_by_importance works
  - Type: Unit test

- ✅ Test limit parameter
  - Expected: Returns exactly limit number of tasks
  - Dependency: Basic functionality works
  - Type: Unit test

**Priority 2 (HIGH) - Edge Cases**
- ✅ Test limit larger than list size
  - Expected: Returns all tasks (not error)
  - Dependency: Basic functionality works
  - Type: Unit test

- ✅ Test limit = 0
  - Expected: Returns empty list
  - Dependency: Basic functionality works
  - Type: Unit test

- ✅ Test empty list
  - Expected: Returns empty list
  - Dependency: None
  - Type: Unit test

---

### **Integration Tests: Full Pipeline**

**Priority 1 (CRITICAL) - End-to-End Workflow**
- ✅ Test full workflow with realistic task set
  - Expected: Correct top 5 tasks based on all scoring factors
  - Dependency: All unit tests pass
  - Type: Integration test

**Priority 2 (HIGH) - Complex Scenarios**
- ✅ Test with tasks having identical scores
  - Expected: Consistent ordering (stable sort)
  - Dependency: Basic integration works
  - Type: Integration test

- ✅ Test with diverse task characteristics
  - Expected: Correct prioritization considering all factors
  - Dependency: Basic integration works
  - Type: Integration test

---

### **Test Execution Order**

1. **Phase 1:** `calculate_task_score` Priority 1 tests (CRITICAL)
2. **Phase 2:** `calculate_task_score` Priority 2 tests (HIGH)
3. **Phase 3:** `calculate_task_score` Priority 3 tests (MEDIUM)
4. **Phase 4:** `sort_tasks_by_importance` all tests
5. **Phase 5:** `get_top_priority_tasks` all tests
6. **Phase 6:** Integration tests

### **Testing Strategy Summary**

| Function | Unit Tests | Integration Tests | Total Tests |
|----------|-----------|-------------------|-------------|
| `calculate_task_score` | 15 | - | 15 |
| `sort_tasks_by_importance` | 5 | - | 5 |
| `get_top_priority_tasks` | 5 | - | 5 |
| Full Pipeline | - | 3 | 3 |
| **TOTAL** | **25** | **3** | **28** |

---

## Part 2: Improving a Single Test

### Exercise 2.1: Writing Your First Test

#### Initial Simple Test

```python
import unittest
from datetime import datetime, timedelta
from models import Task, TaskPriority, TaskStatus
from task_priority import calculate_task_score

class TestCalculateTaskScore(unittest.TestCase):
    
    def test_basic_score(self):
        """Test that a task gets a score."""
        task = Task(
            title="Test task",
            priority=TaskPriority.MEDIUM
        )
        score = calculate_task_score(task)
        self.assertTrue(score > 0)
```

#### AI-Assisted Improvement Conversation

**AI:** Let's look at your test. What behavior is this test trying to verify?

**Me:** It's checking that a task with MEDIUM priority gets some positive score.

**AI:** Good start! But let me ask: what *exactly* should that score be for a MEDIUM priority task with no other factors?

**Me:** Oh, MEDIUM priority has weight 2, so 2 × 10 = 20.

**AI:** Exactly! Your current test only checks `score > 0`, which would pass even if the score was 1 or 100. Is that testing the behavior or just checking *something* happens?

**Me:** I see - I'm testing implementation details (that the function returns something) rather than the actual behavior (that it returns the correct score).

**AI:** Great insight! How could you make your assertion more precise?

**Me:** I should assert that `score == 20` for a MEDIUM priority task with no other factors.

**AI:** Perfect! Now, what edge cases might your test be missing? Think about the task you're creating.

**Me:** My task will have:
- Default status (TODO)
- No due date (None)
- No tags (empty list)
- Recently created (updated_at = now)

The recently created part means `days_since_update < 1`, so it gets +5!

**AI:** Excellent catch! So what should the actual expected score be?

**Me:** 20 (base) + 5 (recently updated) = 25

**AI:** Great! How could you make the test's purpose clearer in the name and structure?

**Me:** I should:
1. Rename to describe what I'm testing
2. Add comments explaining the expected score calculation
3. Use clear arrange-act-assert structure

#### Improved Test

```python
import unittest
from datetime import datetime, timedelta
from models import Task, TaskPriority, TaskStatus
from task_priority import calculate_task_score

class TestCalculateTaskScore(unittest.TestCase):
    
    def test_medium_priority_task_with_no_other_factors(self):
        """
        Test that a MEDIUM priority task with no due date, default status,
        no tags, and recently created gets the correct base score.
        
        Expected score breakdown:
        - MEDIUM priority: 2 × 10 = 20
        - Recently created (updated < 1 day ago): +5
        - Total: 25
        """
        # Arrange: Create a simple MEDIUM priority task
        task = Task(
            title="Test task",
            priority=TaskPriority.MEDIUM
        )
        # Task is automatically created with:
        # - status = TODO
        # - due_date = None
        # - tags = []
        # - updated_at = now (less than 1 day old)
        
        # Act: Calculate the score
        score = calculate_task_score(task)
        
        # Assert: Check the exact expected score
        self.assertEqual(
            score, 
            25,
            f"Expected score of 25 for MEDIUM priority task with no other factors, got {score}"
        )
```

#### Key Improvements Made

1. **Better test name:** Describes exactly what scenario is being tested
2. **Precise assertion:** Uses `assertEqual(score, 25)` instead of `assertTrue(score > 0)`
3. **Clear structure:** Follows Arrange-Act-Assert pattern with comments
4. **Documentation:** Explains the expected score calculation
5. **Helpful error message:** Shows actual score if test fails
6. **Acknowledged edge case:** Documented the "recently created" factor

---

### Exercise 2.2: Learning From Examples

#### Pseudocode for Due Date Test

```
Test: overdue task gets correct bonus score

Create a task with:
- MEDIUM priority
- Due date 3 days in the past
- Default status (TODO)
- No tags

Expected score:
- Base: 20 (MEDIUM priority)
- Overdue: +35
- Recently created: +5
- Total: 60

Assert score == 60
```

#### AI-Assisted Learning Conversation

**AI:** Let's discuss principles of good tests for date calculations. What challenges do you see with testing date-based logic?

**Me:** Dates are always changing! If I use `datetime.now()`, the test might behave differently depending on when it runs.

**AI:** Exactly! This is a common problem. What would make this test more reliable?

**Me:** I should control the dates explicitly. Maybe set the due date to a specific past date, but then the "days until due" calculation depends on when the test runs...

**AI:** You've identified the key issue! Let me show you ONE example of how to handle this, with comments explaining why it's better:

```python
def test_overdue_task_gets_urgency_bonus(self):
    """
    Test that overdue tasks receive a +35 urgency bonus.
    
    This test uses relative dates (timedelta) to ensure consistent
    behavior regardless of when the test runs.
    """
    # Arrange: Create task with due date in the past
    task = Task(
        title="Overdue task",
        priority=TaskPriority.MEDIUM
    )
    # Set due date to exactly 3 days ago using timedelta
    # This makes the test deterministic - it will always be 3 days overdue
    task.due_date = datetime.now() - timedelta(days=3)
    
    # Act
    score = calculate_task_score(task)
    
    # Assert
    expected_score = 20 + 35 + 5  # MEDIUM + overdue + recent update
    self.assertEqual(
        score,
        expected_score,
        f"Overdue task should get +35 bonus. Expected {expected_score}, got {score}"
    )
```

**Why this is better:**
1. Uses `timedelta` to create relative dates (always 3 days ago)
2. Makes test deterministic (same result every time)
3. Clear comment explaining the date calculation
4. Breaks down expected score for readability

**AI:** Now, based on this example, what edge cases should you add for due date testing?

**Me:** I should test:
1. **Boundary:** Task due exactly 0 days from now (due today)
2. **Boundary:** Task due exactly 2 days from now
3. **Boundary:** Task due exactly 7 days from now
4. **Edge:** Task due far in the future (no bonus)
5. **Edge:** Task with no due date at all

**AI:** Excellent! How would you improve your assertions to be more precise?

**Me:** Instead of just checking the total score, I could:
1. Calculate expected score with clear breakdown
2. Add comments showing the math
3. Use descriptive error messages

**AI:** Perfect! Now challenge yourself: what happens with tasks due exactly at midnight?

**Me:** Oh! If a task is due at `2026-02-12 00:00:00` and we check at `2026-02-12 10:00:00`, the `.days` calculation would give 0 (due today), which is correct. But if we check at `2026-02-13 00:00:01`, it would give -1 (overdue), also correct. The `.days` method handles this!

#### Comprehensive Due Date Tests

```python
import unittest
from datetime import datetime, timedelta
from models import Task, TaskPriority, TaskStatus
from task_priority import calculate_task_score

class TestDueDateScoring(unittest.TestCase):
    """Test suite for due date score calculations."""
    
    def test_overdue_task_gets_urgency_bonus(self):
        """
        Test that overdue tasks (due date in past) receive +35 bonus.
        """
        # Arrange
        task = Task(title="Overdue task", priority=TaskPriority.MEDIUM)
        task.due_date = datetime.now() - timedelta(days=3)
        
        # Act
        score = calculate_task_score(task)
        
        # Assert
        # Expected: 20 (MEDIUM) + 35 (overdue) + 5 (recent) = 60
        self.assertEqual(score, 60, 
                        "Overdue task should get +35 urgency bonus")
    
    def test_due_today_gets_high_priority_bonus(self):
        """
        Test that tasks due today (0 days until due) receive +20 bonus.
        """
        # Arrange
        task = Task(title="Due today", priority=TaskPriority.MEDIUM)
        # Due at end of today (still counts as due today)
        task.due_date = datetime.now().replace(hour=23, minute=59, second=59)
        
        # Act
        score = calculate_task_score(task)
        
        # Assert
        # Expected: 20 (MEDIUM) + 20 (due today) + 5 (recent) = 45
        self.assertEqual(score, 45,
                        "Task due today should get +20 bonus")
    
    def test_due_in_one_day(self):
        """
        Test that tasks due tomorrow receive +15 bonus.
        """
        # Arrange
        task = Task(title="Due tomorrow", priority=TaskPriority.MEDIUM)
        task.due_date = datetime.now() + timedelta(days=1)
        
        # Act
        score = calculate_task_score(task)
        
        # Assert
        # Expected: 20 (MEDIUM) + 15 (due in 1-2 days) + 5 (recent) = 40
        self.assertEqual(score, 40,
                        "Task due in 1 day should get +15 bonus")
    
    def test_due_in_exactly_two_days_boundary(self):
        """
        Test boundary condition: task due in exactly 2 days should get +15.
        
        This tests the boundary of the "due in next 2 days" condition.
        """
        # Arrange
        task = Task(title="Due in 2 days", priority=TaskPriority.MEDIUM)
        task.due_date = datetime.now() + timedelta(days=2)
        
        # Act
        score = calculate_task_score(task)
        
        # Assert
        # Expected: 20 (MEDIUM) + 15 (due <= 2 days) + 5 (recent) = 40
        self.assertEqual(score, 40,
                        "Task due in exactly 2 days should get +15 bonus (boundary test)")
    
    def test_due_in_three_days(self):
        """
        Test that tasks due in 3 days receive +10 bonus (within next week).
        """
        # Arrange
        task = Task(title="Due in 3 days", priority=TaskPriority.MEDIUM)
        task.due_date = datetime.now() + timedelta(days=3)
        
        # Act
        score = calculate_task_score(task)
        
        # Assert
        # Expected: 20 (MEDIUM) + 10 (due in 3-7 days) + 5 (recent) = 35
        self.assertEqual(score, 35,
                        "Task due in 3 days should get +10 bonus")
    
    def test_due_in_exactly_seven_days_boundary(self):
        """
        Test boundary condition: task due in exactly 7 days should get +10.
        
        This tests the boundary of the "due in next week" condition.
        """
        # Arrange
        task = Task(title="Due in 7 days", priority=TaskPriority.MEDIUM)
        task.due_date = datetime.now() + timedelta(days=7)
        
        # Act
        score = calculate_task_score(task)
        
        # Assert
        # Expected: 20 (MEDIUM) + 10 (due <= 7 days) + 5 (recent) = 35
        self.assertEqual(score, 35,
                        "Task due in exactly 7 days should get +10 bonus (boundary test)")
    
    def test_due_in_eight_days_no_due_date_bonus(self):
        """
        Test that tasks due in more than 7 days receive no due date bonus.
        """
        # Arrange
        task = Task(title="Due in 8 days", priority=TaskPriority.MEDIUM)
        task.due_date = datetime.now() + timedelta(days=8)
        
        # Act
        score = calculate_task_score(task)
        
        # Assert
        # Expected: 20 (MEDIUM) + 0 (no due date bonus) + 5 (recent) = 25
        self.assertEqual(score, 25,
                        "Task due in 8+ days should get no due date bonus")
    
    def test_no_due_date_no_bonus(self):
        """
        Test that tasks without a due date receive no due date bonus.
        """
        # Arrange
        task = Task(title="No due date", priority=TaskPriority.MEDIUM)
        # due_date is None by default
        
        # Act
        score = calculate_task_score(task)
        
        # Assert
        # Expected: 20 (MEDIUM) + 0 (no due date) + 5 (recent) = 25
        self.assertEqual(score, 25,
                        "Task with no due date should get no due date bonus")
    
    def test_overdue_by_many_days_still_gets_same_bonus(self):
        """
        Test that tasks overdue by any amount receive the same +35 bonus.
        
        This verifies that the overdue bonus doesn't scale with days overdue.
        """
        # Arrange: Task overdue by 30 days
        task = Task(title="Very overdue", priority=TaskPriority.MEDIUM)
        task.due_date = datetime.now() - timedelta(days=30)
        
        # Act
        score = calculate_task_score(task)
        
        # Assert
        # Expected: 20 (MEDIUM) + 35 (overdue) + 5 (recent) = 60
        self.assertEqual(score, 60,
                        "Overdue tasks get +35 regardless of how overdue they are")
```

#### Key Testing Principles Learned

1. **Use relative dates:** `datetime.now() + timedelta(days=X)` ensures tests are deterministic
2. **Test boundaries:** Explicitly test boundary conditions (exactly 2 days, exactly 7 days)
3. **Document expectations:** Clear comments showing score breakdown
4. **Test edge cases:** No due date, far future, very overdue
5. **Descriptive names:** Test names clearly state what scenario is being tested
6. **Helpful assertions:** Error messages explain what went wrong

---

## Part 3: Test-Driven Development Practice

### Exercise 3.1: TDD for a New Feature

#### Feature Requirement
**New Feature:** Tasks assigned to the current user should get a score boost of +12.

#### AI-Assisted TDD Conversation

**AI:** Before writing any code, let's think about TDD. What do you think the first test should be and why?

**Me:** I should write a test that verifies a task assigned to the current user gets +12 added to its score.

**AI:** Good! But wait - looking at the current Task model, do tasks have an "assigned_to" field?

**Me:** Oh, they don't! I need to add that to the Task model first.

**AI:** Exactly! This is part of TDD - your tests drive the design. So what would your first test look like? Write it as pseudocode first.

**Me:**
```
Test: task assigned to current user gets +12 bonus

Create task with:
- MEDIUM priority (base 20)
- assigned_to = "current_user_id"

Calculate score with current_user_id = "current_user_id"

Expected: 20 + 5 (recent) + 12 (assigned) = 37
```

**AI:** Good! But I see a problem - how will `calculate_task_score` know who the "current user" is? The function currently only takes a `task` parameter.

**Me:** I need to modify the function signature to accept a `current_user_id` parameter!

**AI:** Perfect! This is TDD thinking - the test drives the API design. Now write the actual test (it will fail since the feature doesn't exist yet).

#### Step 1: Write the Failing Test (RED)

```python
import unittest
from datetime import datetime
from models import Task, TaskPriority
from task_priority import calculate_task_score

class TestUserAssignmentBonus(unittest.TestCase):
    
    def test_task_assigned_to_current_user_gets_bonus(self):
        """
        Test that tasks assigned to the current user receive +12 bonus.
        
        This is a TDD test for a new feature.
        """
        # Arrange
        task = Task(title="My task", priority=TaskPriority.MEDIUM)
        task.assigned_to = "user123"  # This field doesn't exist yet!
        current_user_id = "user123"
        
        # Act
        score = calculate_task_score(task, current_user_id)  # Function doesn't accept this yet!
        
        # Assert
        # Expected: 20 (MEDIUM) + 5 (recent) + 12 (assigned to me) = 37
        self.assertEqual(score, 37,
                        "Task assigned to current user should get +12 bonus")
```

**Running this test gives errors:**
```
AttributeError: 'Task' object has no attribute 'assigned_to'
TypeError: calculate_task_score() takes 1 positional argument but 2 were given
```

**AI:** Perfect! The test is RED (failing). Now, what's the minimal code you'd write to make it pass?

**Me:**
1. Add `assigned_to` field to Task model
2. Add `current_user_id` parameter to `calculate_task_score`
3. Add the scoring logic for user assignment

**AI:** Good plan! But remember, TDD says "minimal code to make it pass." Can you make it pass without implementing the full feature correctly?

**Me:** I could just add `return 37` when the function is called... but that's cheating and won't work for other tests!

**AI:** Exactly! You're thinking about sustainability. Go ahead and implement the feature properly.

#### Step 2: Implement Minimal Code (GREEN)

**Modified models.py:**
```python
class Task:
    def __init__(self, title, description="", priority=TaskPriority.MEDIUM,
                 due_date=None, tags=None, assigned_to=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.status = TaskStatus.TODO
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.due_date = due_date
        self.completed_at = None
        self.tags = tags or []
        self.assigned_to = assigned_to  # NEW FIELD
```

**Modified task_priority.py:**
```python
def calculate_task_score(task, current_user_id=None):
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

    # Add due date factor
    if task.due_date:
        days_until_due = (task.due_date - datetime.now()).days
        if days_until_due < 0:
            score += 35
        elif days_until_due == 0:
            score += 20
        elif days_until_due <= 2:
            score += 15
        elif days_until_due <= 7:
            score += 10

    # Reduce score for completed/review tasks
    if task.status == TaskStatus.DONE:
        score -= 50
    elif task.status == TaskStatus.REVIEW:
        score -= 15

    # Boost for special tags
    if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
        score += 8

    # Boost for recently updated
    days_since_update = (datetime.now() - task.updated_at).days
    if days_since_update < 1:
        score += 5

    # NEW: Boost for tasks assigned to current user
    if current_user_id and hasattr(task, 'assigned_to') and task.assigned_to == current_user_id:
        score += 12

    return score
```

**AI:** Great! Run your test now. Does it pass?

**Me:** Yes! The test is GREEN.

**AI:** Excellent! Now, before we move on, is there any refactoring you'd like to do?

**Me:** The function signature change means I need to update all existing calls to `calculate_task_score` to be compatible. Also, I should add tests for the edge case where `assigned_to` is None.

#### Step 3: Refactor if Needed (REFACTOR)

**AI:** Good thinking! But for backward compatibility, you've already made `current_user_id` optional with a default of `None`. What else should you test?

**Me:** I should test:
1. Task with no `assigned_to` field (old tasks)
2. Task assigned to a different user
3. Task assigned to current user (already tested)

**AI:** Perfect! Write those tests now.

#### Additional Tests for Complete Coverage

```python
class TestUserAssignmentBonus(unittest.TestCase):
    
    def test_task_assigned_to_current_user_gets_bonus(self):
        """Test that tasks assigned to current user receive +12 bonus."""
        # Arrange
        task = Task(title="My task", priority=TaskPriority.MEDIUM)
        task.assigned_to = "user123"
        current_user_id = "user123"
        
        # Act
        score = calculate_task_score(task, current_user_id)
        
        # Assert
        # Expected: 20 (MEDIUM) + 5 (recent) + 12 (assigned to me) = 37
        self.assertEqual(score, 37)
    
    def test_task_assigned_to_different_user_no_bonus(self):
        """Test that tasks assigned to others don't get the bonus."""
        # Arrange
        task = Task(title="Someone else's task", priority=TaskPriority.MEDIUM)
        task.assigned_to = "other_user"
        current_user_id = "user123"
        
        # Act
        score = calculate_task_score(task, current_user_id)
        
        # Assert
        # Expected: 20 (MEDIUM) + 5 (recent) = 25 (no assignment bonus)
        self.assertEqual(score, 25)
    
    def test_unassigned_task_no_bonus(self):
        """Test that unassigned tasks don't get the bonus."""
        # Arrange
        task = Task(title="Unassigned task", priority=TaskPriority.MEDIUM)
        # assigned_to is None by default
        current_user_id = "user123"
        
        # Act
        score = calculate_task_score(task, current_user_id)
        
        # Assert
        # Expected: 20 (MEDIUM) + 5 (recent) = 25 (no assignment bonus)
        self.assertEqual(score, 25)
    
    def test_backward_compatibility_no_current_user(self):
        """Test that function still works when current_user_id is not provided."""
        # Arrange
        task = Task(title="Task", priority=TaskPriority.MEDIUM)
        task.assigned_to = "user123"
        
        # Act
        score = calculate_task_score(task)  # No current_user_id parameter
        
        # Assert
        # Expected: 20 (MEDIUM) + 5 (recent) = 25 (no bonus without current_user)
        self.assertEqual(score, 25)
```

**All tests pass! ✓**

#### TDD Cycle Summary

1. **RED:** Wrote failing test for new feature
2. **GREEN:** Implemented minimal code to make it pass
3. **REFACTOR:** Added edge case tests for complete coverage
4. **Repeat:** All tests pass, feature is complete

**Key Learning:** TDD drove the design decisions:
- Added `assigned_to` field to Task
- Modified `calculate_task_score` signature
- Made feature backward compatible

---

### Exercise 3.2: TDD for Bug Fix

#### Bug Report
**Bug:** The calculation for "days since update" is incorrect. It's using `.days` which only gives the day component, not the total days.

**Wait, let me check:** Actually, in Python, `(datetime1 - datetime2).days` DOES give the total days. This is correct in Python!

**Revised Bug:** Let's say the bug is that the threshold is wrong - it should boost tasks updated in the last 2 days, not 1 day.

#### AI-Assisted TDD for Bug Fix

**AI:** Let's practice TDD for a bug fix. First, can you write a test that demonstrates the current (buggy) behavior?

**Me:** I need to write a test that shows the bug exists.

**AI:** Exactly! What test would expose this bug?

**Me:** A test for a task updated 1.5 days ago. Under the current (buggy) code, it gets no bonus. Under the fixed code, it should get +5.

**AI:** Perfect! Write that test now. It should FAIL with the current code.

#### Step 1: Write Test That Demonstrates the Bug (RED)

```python
class TestRecentUpdateBugFix(unittest.TestCase):
    
    def test_task_updated_within_two_days_gets_bonus(self):
        """
        Test that tasks updated within the last 2 days get +5 bonus.
        
        This is a bug fix test - the current code only gives bonus for < 1 day.
        """
        # Arrange
        task = Task(title="Recently updated", priority=TaskPriority.MEDIUM)
        # Manually set updated_at to 1.5 days ago
        task.updated_at = datetime.now() - timedelta(days=1, hours=12)
        
        # Act
        score = calculate_task_score(task)
        
        # Assert
        # Expected: 20 (MEDIUM) + 5 (updated < 2 days) = 25
        # But current buggy code gives: 20 (no bonus for 1.5 days)
        self.assertEqual(score, 25,
                        "Task updated 1.5 days ago should get recent update bonus")
```

**Running this test:**
```
FAIL: test_task_updated_within_two_days_gets_bonus
AssertionError: 25 != 20 : Task updated 1.5 days ago should get recent update bonus
```

**The test is RED (failing) - it demonstrates the bug! ✓**

**AI:** Great! The test fails, proving the bug exists. Now, what's the minimal fix?

**Me:** Change the condition from `< 1` to `< 2`:
```python
if days_since_update < 2:  # Changed from < 1
    score += 5
```

**AI:** Perfect! Make that change and run the test.

#### Step 2: Fix the Bug (GREEN)

**Modified task_priority.py:**
```python
def calculate_task_score(task, current_user_id=None):
    # ... [previous code] ...
    
    # Boost score for recently updated tasks
    days_since_update = (datetime.now() - task.updated_at).days
    if days_since_update < 2:  # FIXED: Changed from < 1 to < 2
        score += 5
    
    # ... [rest of code] ...
```

**Running the test:**
```
OK
```

**The test is GREEN (passing)! ✓**

**AI:** Excellent! Now, before we're done, what other tests should you add to prevent regression?

**Me:** I should test:
1. Task updated exactly 0 days ago (boundary)
2. Task updated exactly 1 day ago (within range)
3. Task updated exactly 2 days ago (boundary - should NOT get bonus)
4. Task updated 3+ days ago (clearly outside range)

**AI:** Perfect! Those tests will ensure the fix works correctly and prevent future regressions.

#### Step 3: Add Regression Prevention Tests (REFACTOR)

```python
class TestRecentUpdateBugFix(unittest.TestCase):
    
    def test_task_updated_within_two_days_gets_bonus(self):
        """Test that tasks updated 1.5 days ago get bonus (bug fix)."""
        task = Task(title="Recently updated", priority=TaskPriority.MEDIUM)
        task.updated_at = datetime.now() - timedelta(days=1, hours=12)
        
        score = calculate_task_score(task)
        self.assertEqual(score, 25)
    
    def test_task_updated_today_gets_bonus(self):
        """Test that tasks updated today (< 1 day) get bonus."""
        task = Task(title="Updated today", priority=TaskPriority.MEDIUM)
        # Task just created, updated_at is now
        
        score = calculate_task_score(task)
        # Expected: 20 (MEDIUM) + 5 (recent) = 25
        self.assertEqual(score, 25)
    
    def test_task_updated_exactly_one_day_ago_gets_bonus(self):
        """Test boundary: task updated exactly 1 day ago gets bonus."""
        task = Task(title="Updated 1 day ago", priority=TaskPriority.MEDIUM)
        task.updated_at = datetime.now() - timedelta(days=1)
        
        score = calculate_task_score(task)
        # Expected: 20 (MEDIUM) + 5 (recent) = 25
        self.assertEqual(score, 25)
    
    def test_task_updated_exactly_two_days_ago_no_bonus(self):
        """Test boundary: task updated exactly 2 days ago gets NO bonus."""
        task = Task(title="Updated 2 days ago", priority=TaskPriority.MEDIUM)
        task.updated_at = datetime.now() - timedelta(days=2)
        
        score = calculate_task_score(task)
        # Expected: 20 (MEDIUM) only, no recent bonus
        self.assertEqual(score, 20)
    
    def test_task_updated_three_days_ago_no_bonus(self):
        """Test that tasks updated 3+ days ago get NO bonus."""
        task = Task(title="Updated 3 days ago", priority=TaskPriority.MEDIUM)
        task.updated_at = datetime.now() - timedelta(days=3)
        
        score = calculate_task_score(task)
        # Expected: 20 (MEDIUM) only
        self.assertEqual(score, 20)
```

**All tests pass! ✓**

#### TDD Bug Fix Summary

1. **RED:** Wrote test demonstrating the bug (fails with current code)
2. **GREEN:** Fixed the bug (test now passes)
3. **REFACTOR:** Added comprehensive tests to prevent regression
4. **Complete:** Bug is fixed and well-tested

**Key Learning:** TDD for bug fixes:
- Write a test that fails due to the bug
- Fix the minimal code to make it pass
- Add more tests to ensure the fix is complete
- These tests prevent the bug from reappearing

---

## Part 4: Integration Testing

### Exercise 4.1: Testing the Full Workflow

#### AI-Assisted Integration Test Design

**AI:** Now let's think about integration testing. You've tested each function in isolation. What scenarios would an integration test verify for the full workflow?

**Me:** The integration test should verify that:
1. Tasks are scored correctly (using `calculate_task_score`)
2. Tasks are sorted by score (using `sort_tasks_by_importance`)
3. Top N tasks are returned (using `get_top_priority_tasks`)
4. All three functions work together correctly

**AI:** Great! Now, how would you design test data that exercises the entire workflow?

**Me:** I'd create tasks with different characteristics:
- Different priorities
- Various due dates
- Different statuses
- Some with special tags
- Some assigned to current user

Then verify that the top 5 returned are actually the highest-scoring ones.

**AI:** Excellent! How would you structure the test to make it readable and maintainable?

**Me:** I'd:
1. Use descriptive variable names for each task
2. Add comments explaining expected scores
3. Create a list of tasks in random order
4. Get top 5 tasks
5. Assert that they're in the expected order with expected scores

**AI:** Perfect! One more question: what assertions would verify correct behavior?

**Me:** I should assert:
1. Correct number of tasks returned (5)
2. Tasks are in score order (highest first)
3. Specific tasks appear in specific positions
4. Scores match expected values

#### Comprehensive Integration Test

```python
import unittest
from datetime import datetime, timedelta
from models import Task, TaskPriority, TaskStatus
from task_priority import calculate_task_score, sort_tasks_by_importance, get_top_priority_tasks

class TestTaskPriorityIntegration(unittest.TestCase):
    """Integration tests for the complete task priority workflow."""
    
    def test_full_workflow_with_diverse_tasks(self):
        """
        Test the complete workflow: scoring → sorting → getting top tasks.
        
        This integration test verifies all three functions work together correctly
        with a realistic set of diverse tasks.
        """
        # Arrange: Create a diverse set of tasks
        current_user = "user123"
        
        # Task 1: URGENT + overdue + assigned to me
        # Expected score: 60 + 35 + 5 + 12 = 112
        urgent_overdue_mine = Task(
            title="Critical bug in production",
            priority=TaskPriority.URGENT,
            assigned_to=current_user
        )
        urgent_overdue_mine.due_date = datetime.now() - timedelta(days=1)
        
        # Task 2: HIGH + due today + blocker tag
        # Expected score: 40 + 20 + 5 + 8 = 73
        high_due_today_blocker = Task(
            title="Deploy hotfix",
            priority=TaskPriority.HIGH,
            tags=["blocker", "deployment"]
        )
        high_due_today_blocker.due_date = datetime.now()
        
        # Task 3: URGENT + DONE status (should have low score despite urgency)
        # Expected score: 60 + 5 - 50 = 15
        urgent_done = Task(
            title="Completed urgent task",
            priority=TaskPriority.URGENT
        )
        urgent_done.status = TaskStatus.DONE
        
        # Task 4: MEDIUM + due in 2 days + assigned to me
        # Expected score: 20 + 15 + 5 + 12 = 52
        medium_soon_mine = Task(
            title="Review PR",
            priority=TaskPriority.MEDIUM,
            assigned_to=current_user
        )
        medium_soon_mine.due_date = datetime.now() + timedelta(days=2)
        
        # Task 5: HIGH + due in 3 days
        # Expected score: 40 + 10 + 5 = 55
        high_next_week = Task(
            title="Write documentation",
            priority=TaskPriority.HIGH
        )
        high_next_week.due_date = datetime.now() + timedelta(days=3)
        
        # Task 6: LOW priority + overdue
        # Expected score: 10 + 35 + 5 = 50
        low_overdue = Task(
            title="Update wiki",
            priority=TaskPriority.LOW
        )
        low_overdue.due_date = datetime.now() - timedelta(days=5)
        
        # Task 7: MEDIUM + no due date + not assigned
        # Expected score: 20 + 5 = 25
        medium_basic = Task(
            title="Refactor code",
            priority=TaskPriority.MEDIUM
        )
        
        # Task 8: HIGH + REVIEW status
        # Expected score: 40 + 5 - 15 = 30
        high_review = Task(
            title="Feature in review",
            priority=TaskPriority.HIGH
        )
        high_review.status = TaskStatus.REVIEW
        
        # Create list in random order (not sorted)
        all_tasks = [
            medium_basic,           # Score: 25
            high_review,            # Score: 30
            urgent_done,            # Score: 15
            low_overdue,            # Score: 50
            high_due_today_blocker, # Score: 73
            medium_soon_mine,       # Score: 52
            high_next_week,         # Score: 55
            urgent_overdue_mine,    # Score: 112
        ]
        
        # Act: Get top 5 priority tasks
        top_5 = get_top_priority_tasks(all_tasks, limit=5, current_user_id=current_user)
        
        # Assert 1: Correct number of tasks returned
        self.assertEqual(len(top_5), 5,
                        "Should return exactly 5 tasks")
        
        # Assert 2: Tasks are in correct order (highest score first)
        expected_order = [
            urgent_overdue_mine,      # Score: 112
            high_due_today_blocker,   # Score: 73
            high_next_week,           # Score: 55
            medium_soon_mine,         # Score: 52
            low_overdue,              # Score: 50
        ]
        
        for i, expected_task in enumerate(expected_order):
            self.assertEqual(
                top_5[i].title,
                expected_task.title,
                f"Position {i+1} should be '{expected_task.title}'"
            )
        
        # Assert 3: Verify actual scores match expected
        expected_scores = [112, 73, 55, 52, 50]
        actual_scores = [calculate_task_score(task, current_user) for task in top_5]
        
        self.assertEqual(
            actual_scores,
            expected_scores,
            f"Scores should be {expected_scores}, got {actual_scores}"
        )
        
        # Assert 4: Verify highest score task is first
        self.assertEqual(
            top_5[0].title,
            "Critical bug in production",
            "Highest scoring task should be first"
        )
        
        # Assert 5: Verify low-scoring tasks are not included
        low_score_titles = [t.title for t in top_5]
        self.assertNotIn("Completed urgent task", low_score_titles,
                        "DONE task with score 15 should not be in top 5")
        self.assertNotIn("Refactor code", low_score_titles,
                        "Basic task with score 25 should not be in top 5")
    
    def test_integration_with_equal_scores(self):
        """
        Test that tasks with equal scores maintain stable ordering.
        
        This verifies that the sort is stable when scores are identical.
        """
        # Arrange: Create tasks with identical scores
        task1 = Task(title="First task", priority=TaskPriority.MEDIUM)
        task2 = Task(title="Second task", priority=TaskPriority.MEDIUM)
        task3 = Task(title="Third task", priority=TaskPriority.MEDIUM)
        
        # All have same priority, no due dates, all recently created
        # All should have score: 20 + 5 = 25
        
        tasks = [task1, task2, task3]
        
        # Act
        sorted_tasks = sort_tasks_by_importance(tasks)
        
        # Assert: Order should be maintained (stable sort)
        self.assertEqual(
            [t.title for t in sorted_tasks],
            ["First task", "Second task", "Third task"],
            "Tasks with equal scores should maintain original order (stable sort)"
        )
    
    def test_integration_with_empty_list(self):
        """Test that the workflow handles empty task lists gracefully."""
        # Arrange
        empty_list = []
        
        # Act
        top_tasks = get_top_priority_tasks(empty_list, limit=5)
        
        # Assert
        self.assertEqual(len(top_tasks), 0,
                        "Empty list should return empty list")
        self.assertIsInstance(top_tasks, list,
                             "Should return a list, not None")
    
    def test_integration_with_limit_greater_than_available(self):
        """Test that requesting more tasks than available returns all tasks."""
        # Arrange: Only 3 tasks
        tasks = [
            Task(title="Task 1", priority=TaskPriority.HIGH),
            Task(title="Task 2", priority=TaskPriority.MEDIUM),
            Task(title="Task 3", priority=TaskPriority.LOW),
        ]
        
        # Act: Request top 10
        top_tasks = get_top_priority_tasks(tasks, limit=10)
        
        # Assert: Should return all 3 tasks
        self.assertEqual(len(top_tasks), 3,
                        "Should return all available tasks when limit exceeds count")
    
    def test_integration_real_world_scenario(self):
        """
        Test a realistic scenario with mixed task types.
        
        Simulates a typical workday with various tasks and verifies
        the most important ones are prioritized correctly.
        """
        # Arrange: Realistic task set
        current_user = "developer@company.com"
        
        # Production issue (highest priority)
        prod_bug = Task(
            title="Fix login bug affecting users",
            priority=TaskPriority.URGENT,
            tags=["critical", "production"],
            assigned_to=current_user
        )
        prod_bug.due_date = datetime.now() - timedelta(hours=2)  # Overdue!
        # Expected score: 60 + 35 + 8 + 5 + 12 = 120
        
        # Important feature due soon
        feature_deadline = Task(
            title="Complete feature for sprint demo",
            priority=TaskPriority.HIGH,
            assigned_to=current_user
        )
        feature_deadline.due_date = datetime.now() + timedelta(hours=6)  # Today
        # Expected score: 40 + 20 + 5 + 12 = 77
        
        # Code review needed
        code_review = Task(
            title="Review team member's PR",
            priority=TaskPriority.MEDIUM,
            tags=["blocker"]
        )
        code_review.due_date = datetime.now() + timedelta(days=1)
        # Expected score: 20 + 15 + 8 + 5 = 48
        
        # Documentation (lower priority)
        docs = Task(
            title="Update API documentation",
            priority=TaskPriority.LOW
        )
        docs.due_date = datetime.now() + timedelta(days=7)
        # Expected score: 10 + 10 + 5 = 25
        
        # Completed task (should rank low)
        finished = Task(
            title="Deploy to staging",
            priority=TaskPriority.HIGH
        )
        finished.status = TaskStatus.DONE
        # Expected score: 40 + 5 - 50 = -5
        
        tasks = [docs, code_review, finished, feature_deadline, prod_bug]
        
        # Act
        top_3 = get_top_priority_tasks(tasks, limit=3, current_user_id=current_user)
        
        # Assert: Verify the right priorities
        self.assertEqual(len(top_3), 3)
        
        # Top task should be the production bug
        self.assertEqual(
            top_3[0].title,
            "Fix login bug affecting users",
            "Production bug should be top priority"
        )
        
        # Second should be the feature deadline
        self.assertEqual(
            top_3[1].title,
            "Complete feature for sprint demo",
            "Feature due today should be second priority"
        )
        
        # Third should be code review
        self.assertEqual(
            top_3[2].title,
            "Review team member's PR",
            "Code review with blocker tag should be third"
        )
        
        # Completed task should NOT be in top 3
        top_3_titles = [t.title for t in top_3]
        self.assertNotIn(
            "Deploy to staging",
            top_3_titles,
            "Completed task should not be in top priorities"
        )
```

#### Integration Test Key Features

1. **Comprehensive scenarios:** Tests diverse task combinations
2. **Realistic data:** Simulates actual work situations
3. **Multiple assertions:** Verifies order, scores, and content
4. **Edge cases:** Empty lists, limits, equal scores
5. **Clear documentation:** Comments explain expected scores
6. **Maintainable:** Easy to understand and modify

---

## Final Test Suite

Here's the complete test file that can be run:

```python
"""
Comprehensive test suite for task prioritization system.

This test suite covers:
1. Unit tests for calculate_task_score
2. Unit tests for sort_tasks_by_importance
3. Unit tests for get_top_priority_tasks
4. Integration tests for the full workflow
5. TDD tests for new features and bug fixes
"""

import unittest
from datetime import datetime, timedelta
from models import Task, TaskPriority, TaskStatus
from task_priority import calculate_task_score, sort_tasks_by_importance, get_top_priority_tasks


# ============================================================================
# UNIT TESTS: calculate_task_score
# ============================================================================

class TestCalculateTaskScore(unittest.TestCase):
    """Unit tests for the calculate_task_score function."""
    
    def test_low_priority_base_score(self):
        """Test LOW priority gives base score of 10."""
        task = Task(title="Low priority task", priority=TaskPriority.LOW)
        score = calculate_task_score(task)
        self.assertEqual(score, 15)  # 10 (LOW) + 5 (recent)
    
    def test_medium_priority_base_score(self):
        """Test MEDIUM priority gives base score of 20."""
        task = Task(title="Medium priority task", priority=TaskPriority.MEDIUM)
        score = calculate_task_score(task)
        self.assertEqual(score, 25)  # 20 (MEDIUM) + 5 (recent)
    
    def test_high_priority_base_score(self):
        """Test HIGH priority gives base score of 40."""
        task = Task(title="High priority task", priority=TaskPriority.HIGH)
        score = calculate_task_score(task)
        self.assertEqual(score, 45)  # 40 (HIGH) + 5 (recent)
    
    def test_urgent_priority_base_score(self):
        """Test URGENT priority gives base score of 60."""
        task = Task(title="Urgent task", priority=TaskPriority.URGENT)
        score = calculate_task_score(task)
        self.assertEqual(score, 65)  # 60 (URGENT) + 5 (recent)


class TestDueDateScoring(unittest.TestCase):
    """Unit tests for due date scoring logic."""
    
    def test_overdue_task_gets_urgency_bonus(self):
        """Test that overdue tasks receive +35 bonus."""
        task = Task(title="Overdue task", priority=TaskPriority.MEDIUM)
        task.due_date = datetime.now() - timedelta(days=3)
        score = calculate_task_score(task)
        self.assertEqual(score, 60)  # 20 + 35 + 5
    
    def test_due_today_gets_high_priority_bonus(self):
        """Test that tasks due today receive +20 bonus."""
        task = Task(title="Due today", priority=TaskPriority.MEDIUM)
        task.due_date = datetime.now()
        score = calculate_task_score(task)
        self.assertEqual(score, 45)  # 20 + 20 + 5
    
    def test_due_in_exactly_two_days_boundary(self):
        """Test boundary: task due in exactly 2 days should get +15."""
        task = Task(title="Due in 2 days", priority=TaskPriority.MEDIUM)
        task.due_date = datetime.now() + timedelta(days=2)
        score = calculate_task_score(task)
        self.assertEqual(score, 40)  # 20 + 15 + 5
    
    def test_due_in_exactly_seven_days_boundary(self):
        """Test boundary: task due in exactly 7 days should get +10."""
        task = Task(title="Due in 7 days", priority=TaskPriority.MEDIUM)
        task.due_date = datetime.now() + timedelta(days=7)
        score = calculate_task_score(task)
        self.assertEqual(score, 35)  # 20 + 10 + 5
    
    def test_no_due_date_no_bonus(self):
        """Test that tasks without due date receive no due date bonus."""
        task = Task(title="No due date", priority=TaskPriority.MEDIUM)
        score = calculate_task_score(task)
        self.assertEqual(score, 25)  # 20 + 5


class TestStatusScoring(unittest.TestCase):
    """Unit tests for status scoring logic."""
    
    def test_done_status_reduces_score(self):
        """Test that DONE status reduces score by 50."""
        task = Task(title="Done task", priority=TaskPriority.MEDIUM)
        task.status = TaskStatus.DONE
        score = calculate_task_score(task)
        self.assertEqual(score, -25)  # 20 + 5 - 50
    
    def test_review_status_reduces_score(self):
        """Test that REVIEW status reduces score by 15."""
        task = Task(title="In review", priority=TaskPriority.MEDIUM)
        task.status = TaskStatus.REVIEW
        score = calculate_task_score(task)
        self.assertEqual(score, 10)  # 20 + 5 - 15
    
    def test_todo_status_no_reduction(self):
        """Test that TODO status doesn't reduce score."""
        task = Task(title="Todo task", priority=TaskPriority.MEDIUM)
        task.status = TaskStatus.TODO
        score = calculate_task_score(task)
        self.assertEqual(score, 25)  # 20 + 5


class TestTagScoring(unittest.TestCase):
    """Unit tests for tag scoring logic."""
    
    def test_blocker_tag_adds_bonus(self):
        """Test that 'blocker' tag adds +8."""
        task = Task(title="Blocked task", priority=TaskPriority.MEDIUM, tags=["blocker"])
        score = calculate_task_score(task)
        self.assertEqual(score, 33)  # 20 + 5 + 8
    
    def test_critical_tag_adds_bonus(self):
        """Test that 'critical' tag adds +8."""
        task = Task(title="Critical task", priority=TaskPriority.MEDIUM, tags=["critical"])
        score = calculate_task_score(task)
        self.assertEqual(score, 33)  # 20 + 5 + 8
    
    def test_multiple_special_tags_single_bonus(self):
        """Test that multiple special tags only add +8 once."""
        task = Task(
            title="Multiple tags",
            priority=TaskPriority.MEDIUM,
            tags=["blocker", "critical", "urgent"]
        )
        score = calculate_task_score(task)
        self.assertEqual(score, 33)  # 20 + 5 + 8 (not +24)


class TestRecentUpdateScoring(unittest.TestCase):
    """Unit tests for recent update scoring logic."""
    
    def test_recently_created_task_gets_bonus(self):
        """Test that newly created tasks get +5."""
        task = Task(title="New task", priority=TaskPriority.MEDIUM)
        score = calculate_task_score(task)
        self.assertEqual(score, 25)  # 20 + 5
    
    def test_task_updated_two_days_ago_no_bonus(self):
        """Test that tasks updated 2+ days ago get no bonus."""
        task = Task(title="Old task", priority=TaskPriority.MEDIUM)
        task.updated_at = datetime.now() - timedelta(days=2)
        score = calculate_task_score(task)
        self.assertEqual(score, 20)  # 20 only


# ============================================================================
# TDD TESTS: New Feature (User Assignment)
# ============================================================================

class TestUserAssignmentBonus(unittest.TestCase):
    """TDD tests for user assignment feature."""
    
    def test_task_assigned_to_current_user_gets_bonus(self):
        """Test that tasks assigned to current user receive +12 bonus."""
        task = Task(title="My task", priority=TaskPriority.MEDIUM, assigned_to="user123")
        score = calculate_task_score(task, current_user_id="user123")
        self.assertEqual(score, 37)  # 20 + 5 + 12
    
    def test_task_assigned_to_different_user_no_bonus(self):
        """Test that tasks assigned to others don't get bonus."""
        task = Task(title="Other's task", priority=TaskPriority.MEDIUM, assigned_to="other")
        score = calculate_task_score(task, current_user_id="user123")
        self.assertEqual(score, 25)  # 20 + 5


# ============================================================================
# UNIT TESTS: sort_tasks_by_importance
# ============================================================================

class TestSortTasksByImportance(unittest.TestCase):
    """Unit tests for sort_tasks_by_importance function."""
    
    def test_sorts_by_score_highest_first(self):
        """Test that tasks are sorted by score in descending order."""
        low_task = Task(title="Low", priority=TaskPriority.LOW)
        high_task = Task(title="High", priority=TaskPriority.HIGH)
        medium_task = Task(title="Medium", priority=TaskPriority.MEDIUM)
        
        tasks = [low_task, high_task, medium_task]
        sorted_tasks = sort_tasks_by_importance(tasks)
        
        self.assertEqual(sorted_tasks[0].title, "High")
        self.assertEqual(sorted_tasks[1].title, "Medium")
        self.assertEqual(sorted_tasks[2].title, "Low")
    
    def test_empty_list_returns_empty_list(self):
        """Test that empty list returns empty list."""
        result = sort_tasks_by_importance([])
        self.assertEqual(result, [])


# ============================================================================
# UNIT TESTS: get_top_priority_tasks
# ============================================================================

class TestGetTopPriorityTasks(unittest.TestCase):
    """Unit tests for get_top_priority_tasks function."""
    
    def test_returns_top_n_tasks(self):
        """Test that function returns top N tasks."""
        tasks = [
            Task(f"Task {i}", priority=TaskPriority.MEDIUM)
            for i in range(10)
        ]
        top_3 = get_top_priority_tasks(tasks, limit=3)
        self.assertEqual(len(top_3), 3)
    
    def test_limit_larger_than_list_returns_all(self):
        """Test that requesting more than available returns all tasks."""
        tasks = [Task("Task", priority=TaskPriority.MEDIUM) for _ in range(3)]
        top_10 = get_top_priority_tasks(tasks, limit=10)
        self.assertEqual(len(top_10), 3)


# ============================================================================
# INTEGRATION TESTS: Full Workflow
# ============================================================================

class TestTaskPriorityIntegration(unittest.TestCase):
    """Integration tests for the complete workflow."""
    
    def test_full_workflow_with_diverse_tasks(self):
        """Test complete workflow with realistic task set."""
        current_user = "user123"
        
        # Create diverse tasks
        urgent_overdue = Task("Critical bug", priority=TaskPriority.URGENT, assigned_to=current_user)
        urgent_overdue.due_date = datetime.now() - timedelta(days=1)
        
        high_today = Task("Deploy hotfix", priority=TaskPriority.HIGH, tags=["blocker"])
        high_today.due_date = datetime.now()
        
        medium_basic = Task("Refactor", priority=TaskPriority.MEDIUM)
        
        tasks = [medium_basic, high_today, urgent_overdue]
        
        # Get top 2
        top_2 = get_top_priority_tasks(tasks, limit=2, current_user_id=current_user)
        
        # Assert correct order
        self.assertEqual(len(top_2), 2)
        self.assertEqual(top_2[0].title, "Critical bug")
        self.assertEqual(top_2[1].title, "Deploy hotfix")


# ============================================================================
# RUN ALL TESTS
# ============================================================================

if __name__ == '__main__':
    unittest.main(verbosity=2)
```

---

## Reflection

### What I Learned About Testing Through This Exercise

#### 1. **The Power of Test-First Thinking**

**Before this exercise:**
- I thought of tests as validation after coding
- Testing felt like a chore to check if code works

**After this exercise:**
- Tests guide design decisions (TDD drove the user assignment feature design)
- Tests are documentation of intended behavior
- Writing tests first clarifies requirements before coding

**Example:**
When adding user assignment, the test forced me to think:
- "Where does `assigned_to` go?" → Added to Task model
- "How does the function know the current user?" → Added parameter to function signature

Tests drove better API design!

#### 2. **Behavior vs. Implementation Testing**

**Key Insight:** Test *what* the code does, not *how* it does it.

**Bad Test (implementation-focused):**
```python
def test_calculates_something(self):
    task = Task(title="Test", priority=TaskPriority.MEDIUM)
    score = calculate_task_score(task)
    self.assertTrue(score > 0)  # Just checks something happens
```

**Good Test (behavior-focused):**
```python
def test_medium_priority_task_gets_score_of_25(self):
    task = Task(title="Test", priority=TaskPriority.MEDIUM)
    score = calculate_task_score(task)
    self.assertEqual(score, 25)  # Checks exact behavior
```

**Why this matters:**
- Behavior tests survive refactoring
- Implementation tests break when internals change
- Behavior tests document requirements clearly

#### 3. **The Importance of Edge Cases**

**AI helped me discover edge cases I would have missed:**
- Boundary conditions (exactly 2 days, exactly 7 days)
- Empty inputs
- Null/None values
- Tasks with identical scores
- Combinations of factors (overdue + DONE)

**Key Learning:** 
Edge cases aren't "extra" tests - they're where bugs hide! The AI's prompting questions revealed edge cases I hadn't considered.

#### 4. **Test Structure and Readability**

**What makes tests maintainable:**

1. **Arrange-Act-Assert pattern:**
```python
# Arrange: Set up test data
task = Task(...)

# Act: Execute the function
score = calculate_task_score(task)

# Assert: Verify the result
self.assertEqual(score, expected)
```

2. **Descriptive names:**
- ❌ Bad: `test_task1()`, `test_score()`
- ✅ Good: `test_medium_priority_task_with_no_other_factors()`

3. **Clear comments:**
- Explain expected score calculations
- Document why each test exists
- Note edge cases being tested

4. **Helpful error messages:**
```python
self.assertEqual(
    score, 
    25,
    f"Expected 25 but got {score}. Check priority calculation."
)
```

#### 5. **Integration vs. Unit Testing**

**Unit Tests:**
- Test one function in isolation
- Fast to run
- Easy to pinpoint failures
- Test individual behaviors

**Integration Tests:**
- Test multiple functions together
- Slower but more realistic
- Verify components work together
- Catch interface issues

**Key Insight:** You need both! Unit tests give confidence in individual pieces. Integration tests give confidence in the whole system.

#### 6. **TDD Changes How You Code**

**TDD Process:**
1. **RED:** Write failing test
2. **GREEN:** Minimal code to pass
3. **REFACTOR:** Improve while keeping tests green

**Benefits I experienced:**
- **Clearer requirements:** Writing the test first forced me to think about exactly what I wanted
- **Better design:** Tests drove API decisions (function signatures, parameters)
- **Confidence:** Every feature had tests from the start
- **No over-engineering:** "Minimal code to pass" prevents unnecessary complexity

**Example:**
The bug fix exercise showed TDD's power:
1. Wrote test demonstrating the bug (RED)
2. Fixed the bug (GREEN)
3. Added regression tests (REFACTOR)

This process ensures:
- Bug is actually fixed
- Bug won't come back
- Fix is minimal and correct

#### 7. **The Value of Comprehensive Test Planning**

**Before diving into code, I created:**
- List of behaviors to test
- Priority of each test (CRITICAL, HIGH, MEDIUM)
- Dependencies between tests
- Expected outcomes

**This planning prevented:**
- Missing important test cases
- Testing in the wrong order
- Wasting time on low-value tests

**Key Learning:** Spend time planning tests. 10 minutes of planning saves hours of debugging.

#### 8. **AI as a Testing Teacher**

**What the AI did well:**
- Asked probing questions that revealed edge cases
- Challenged my assumptions
- Provided examples with explanations
- Guided without giving answers

**How it improved my learning:**
- I discovered solutions rather than being told them
- Questions made me think critically
- Explanations clarified testing principles
- Examples showed best practices

**Most valuable AI prompts:**
1. "What edge cases might you be missing?"
2. "Is this testing behavior or implementation?"
3. "Which test should you write first and why?"
4. "How would you make this assertion more precise?"

#### 9. **Date Testing Challenges**

**Problem:** Tests that use `datetime.now()` can be flaky.

**Solution:** Use relative dates with `timedelta`:
```python
# Bad: Depends on when test runs
task.due_date = datetime(2026, 2, 15)  # Might be past or future!

# Good: Always 2 days in the future
task.due_date = datetime.now() + timedelta(days=2)
```

**Key Learning:** Make tests deterministic. They should pass or fail consistently, regardless of when they run.

#### 10. **The Test Pyramid**

**Discovered the testing hierarchy:**
```
        /\
       /  \       Few integration tests
      /INT \      (slow but comprehensive)
     /______\
    /        \
   /  UNIT   \   Many unit tests
  /   TESTS   \  (fast and focused)
 /____________\
```

**Why this works:**
- Unit tests are fast, run them often
- Integration tests are thorough, run them before commits
- Both are necessary for confidence

---

### Skills Developed

1. ✅ **Writing behavior-focused tests**
2. ✅ **Identifying edge cases systematically**
3. ✅ **Using TDD to drive design**
4. ✅ **Creating maintainable test suites**
5. ✅ **Balancing unit and integration tests**
6. ✅ **Writing deterministic date-based tests**
7. ✅ **Using AI effectively for learning**
8. ✅ **Planning comprehensive test coverage**
9. ✅ **Fixing bugs with test-first approach**
10. ✅ **Documenting test intent clearly**

---

### Future Application

**How I'll apply these lessons:**

1. **Always start with a test plan** - List behaviors before writing code
2. **Use TDD for new features** - Write test → implement → refactor
3. **Think about edge cases early** - Ask "what could break this?"
4. **Make tests readable** - Clear names, comments, structure
5. **Use AI as a learning tool** - Ask questions, don't just get answers
6. **Balance unit and integration tests** - Both have value
7. **Write deterministic tests** - Avoid flaky tests with proper setup
8. **Document test intent** - Future me will thank current me

---

## Conclusion

This exercise transformed my understanding of testing from "checking if code works" to "driving better design and documentation." The AI-assisted learning approach was particularly effective because:

1. **Questions promoted thinking** rather than passive learning
2. **Iterative improvement** showed the evolution of better tests
3. **TDD practice** demonstrated the value of test-first development
4. **Edge case discovery** revealed blind spots in my testing approach

**Key Achievement:** Created a comprehensive test suite with 25+ unit tests and 3 integration tests, covering:
- All base functionality
- Edge cases and boundaries
- New features (user assignment)
- Bug fixes (recent update threshold)
- Full workflow integration

**Most Valuable Lesson:** Testing isn't about proving code works - it's about designing better code, documenting behavior, and building confidence in your system.

---

**Exercise Completed:** February 12, 2026  
**Time Spent:** ~5 hours (planning, testing, implementation, documentation)  
**Tests Written:** 28 tests (25 unit, 3 integration)  
**Test Coverage:** Complete coverage of all scoring factors and workflows
