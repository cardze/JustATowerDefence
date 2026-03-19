---
name: clean-code-principles
description: 'Analyze and improve code quality based on Clean Code principles by Robert C. Martin. Use when asked to review code quality, refactor for readability, check naming conventions, reduce complexity, improve function design, remove code smells, or ensure SOLID principles. Supports all programming languages with language-specific best practices.'
---

# Clean Code Principles

A comprehensive skill for writing and checking code that follows Clean Code principles. This skill helps you analyze existing code, suggest improvements, and write new code that is readable, maintainable, and follows industry best practices.

## When to Use This Skill

- User asks to "check code quality", "review for clean code", or "improve code readability"
- User wants to refactor messy or complex code
- User mentions "code smells", "technical debt", or "maintainability"
- User asks about naming conventions, function size, or code organization
- User wants to apply SOLID principles or design patterns
- User asks to "make this code cleaner" or "simplify this function"
- During code review or before committing code

## Prerequisites

- Code to analyze (existing file or code snippet)
- Understanding of the programming language being used
- Context about the code's purpose and requirements

## Core Clean Code Principles

### 1. Meaningful Names
- **Variables**: Use descriptive names that reveal intent
- **Functions**: Use verb phrases that describe what they do
- **Classes**: Use noun phrases that describe what they represent
- **Avoid**: Single letters (except loop counters), abbreviations, encodings

### 2. Functions
- **Single Responsibility**: Each function does one thing well
- **Small Size**: Ideally 5-15 lines, maximum 20-30 lines
- **Few Parameters**: 0-3 parameters ideal, avoid flag arguments
- **No Side Effects**: Function does what its name says, nothing more
- **Command-Query Separation**: Functions either do something or return something, not both

### 3. Comments
- **Self-Documenting Code**: Code should explain itself through clear names
- **When to Comment**: Explain WHY, not WHAT
- **Avoid**: Redundant comments, commented-out code, misleading comments
- **Good Uses**: Legal comments, warnings, TODOs, clarification of complex logic

### 4. Formatting
- **Consistent Style**: Follow language conventions and team standards
- **Vertical Formatting**: Related code stays together, blank lines separate concepts
- **Horizontal Formatting**: Keep lines short (80-120 characters)
- **Indentation**: Consistent and meaningful

### 5. Error Handling
- **Use Exceptions**: Not return codes
- **Don't Return Null**: Return empty objects or throw exceptions
- **Provide Context**: Error messages should be informative
- **Define Exception Classes**: Based on caller's needs

### 6. SOLID Principles
- **S**ingle Responsibility Principle: One reason to change
- **O**pen/Closed Principle: Open for extension, closed for modification
- **L**iskov Substitution Principle: Subtypes must be substitutable
- **I**nterface Segregation Principle: Many specific interfaces over one general
- **D**ependency Inversion Principle: Depend on abstractions, not concretions

## Step-by-Step Code Review Workflow

### Step 1: Initial Assessment
1. Read through the code to understand its purpose
2. Identify the main responsibilities and components
3. Note initial observations about complexity and structure

### Step 2: Check Names
1. Review all variable names for clarity and intent
2. Check function names follow verb-noun patterns
3. Ensure class names are nouns describing their role
4. Look for magic numbers that should be named constants
5. Replace ambiguous abbreviations with full words

### Step 3: Analyze Functions
1. Measure function length (lines of code)
2. Count parameters (flag for >3 parameters)
3. Check for single responsibility violations
4. Identify functions with side effects
5. Look for deeply nested code (>3 levels)

### Step 4: Review Structure
1. Check for proper separation of concerns
2. Identify code duplication (DRY violations)
3. Review class and module organization
4. Check for proper abstraction levels
5. Verify SOLID principle adherence

### Step 5: Examine Error Handling
1. Check for proper exception usage
2. Identify null returns that should throw or return empty
3. Review error messages for clarity
4. Ensure resources are properly cleaned up

### Step 6: Provide Recommendations
1. Prioritize issues by severity (critical, major, minor)
2. Provide specific, actionable refactoring suggestions
3. Show before/after examples for key improvements
4. Explain the benefits of each change

## Common Code Smells and Solutions

| Code Smell | Description | Solution |
|------------|-------------|----------|
| **Long Method** | Function >30 lines | Extract smaller functions |
| **Long Parameter List** | >3 parameters | Use parameter objects or builder pattern |
| **Duplicated Code** | Copy-pasted logic | Extract to shared function/class |
| **Large Class** | Class doing too much | Split into smaller, focused classes |
| **Feature Envy** | Method uses another class more than its own | Move method to the envied class |
| **Data Clumps** | Same group of data together | Create a class for the group |
| **Primitive Obsession** | Using primitives instead of objects | Create value objects |
| **Switch Statements** | Complex switch/if-else chains | Use polymorphism or strategy pattern |
| **Lazy Class** | Class that doesn't do enough | Inline or remove |
| **Speculative Generality** | Code for future that may not come | Remove until needed (YAGNI) |
| **Temporary Field** | Fields only used sometimes | Extract to parameter or new class |
| **Message Chains** | a.getB().getC().getD() | Apply Law of Demeter, add delegation |
| **Middle Man** | Class that only delegates | Remove or add value |
| **Comments** | Explaining what code does | Refactor code to be self-explanatory |

## Language-Specific Considerations

### Python
- Follow PEP 8 style guide
- Use snake_case for functions/variables
- Use descriptive names over abbreviated ones
- Prefer list comprehensions for simple transformations
- Use context managers (with statements) for resources
- Type hints for function signatures

### JavaScript/TypeScript
- Follow ESLint standard or Airbnb style guide
- Use camelCase for variables/functions
- Use const/let, never var
- Prefer arrow functions for callbacks
- Use async/await over promise chains
- TypeScript: Avoid 'any', use proper types

### Java
- Follow Oracle Java conventions
- Use PascalCase for classes, camelCase for methods
- Keep classes focused and cohesive
- Use interfaces for abstractions
- Prefer composition over inheritance
- Use dependency injection

### C#
- Follow Microsoft C# conventions
- Use PascalCase for public members
- Use LINQ for data transformations
- Async methods should end with Async
- Use properties instead of getters/setters

## Refactoring Techniques

### Extract Method
Break large methods into smaller, named functions

```python
# Before
def process_order(order):
    total = 0
    for item in order.items:
        total += item.price * item.quantity
    discount = total * 0.1 if total > 100 else 0
    tax = (total - discount) * 0.08
    return total - discount + tax

# After
def process_order(order):
    subtotal = calculate_subtotal(order.items)
    discount = calculate_discount(subtotal)
    tax = calculate_tax(subtotal - discount)
    return subtotal - discount + tax

def calculate_subtotal(items):
    return sum(item.price * item.quantity for item in items)

def calculate_discount(subtotal):
    return subtotal * 0.1 if subtotal > 100 else 0

def calculate_tax(amount):
    return amount * 0.08
```

### Replace Magic Numbers
Use named constants for clarity

```python
# Before
if age >= 18:
    can_vote = True

# After
VOTING_AGE = 18
if age >= VOTING_AGE:
    can_vote = True
```

### Replace Conditional with Polymorphism
Use inheritance/interfaces for type-specific behavior

```python
# Before
def calculate_pay(employee):
    if employee.type == "HOURLY":
        return employee.hours * employee.rate
    elif employee.type == "SALARIED":
        return employee.salary / 12
    elif employee.type == "COMMISSIONED":
        return employee.base + employee.sales * employee.commission

# After
class HourlyEmployee:
    def calculate_pay(self):
        return self.hours * self.rate

class SalariedEmployee:
    def calculate_pay(self):
        return self.salary / 12

class CommissionedEmployee:
    def calculate_pay(self):
        return self.base + self.sales * self.commission
```

## Automated Checks

When reviewing code, check for:

1. **Complexity Metrics**
   - Cyclomatic complexity (< 10 per function)
   - Cognitive complexity (< 15 per function)
   - Nesting depth (< 4 levels)

2. **Size Metrics**
   - Lines per function (< 30)
   - Parameters per function (< 4)
   - Lines per file (< 500)
   - Methods per class (< 20)

3. **Naming Conventions**
   - Variables: descriptive, no single letters (except i, j in loops)
   - Functions: verb phrases
   - Classes: noun phrases
   - Constants: UPPER_CASE

4. **Documentation**
   - Public APIs have docstrings/comments
   - Complex algorithms are explained
   - No commented-out code

## Output Format

When providing clean code feedback, use this structure:

```markdown
## Clean Code Analysis

### Overall Assessment
[Brief summary of code quality: Excellent/Good/Needs Improvement/Poor]

### Critical Issues
1. [Issue with severity and location]
   - **Problem**: [What's wrong]
   - **Impact**: [Why it matters]
   - **Solution**: [How to fix]

### Major Improvements
1. [Improvement opportunity]
   - **Current**: [Code snippet or description]
   - **Suggested**: [Improved version]
   - **Benefit**: [Why this is better]

### Minor Suggestions
- [Quick wins and polish items]

### Positive Aspects
- [What's already done well]
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Code is legacy/can't change | Suggest incremental improvements, focus on new code |
| Performance concerns with clean code | Profile first, clean code is usually fast enough |
| Team disagrees on style | Adopt automated formatter (Black, Prettier, etc.) |
| Too many issues to fix | Prioritize by severity, fix incrementally |
| Code works, why change it? | Explain maintenance costs, bug risk, onboarding time |

## Best Practices Summary

✅ **DO:**
- Write code for humans first, computers second
- Use meaningful, searchable names
- Keep functions small and focused
- Follow the principle of least surprise
- Write tests for clean code confidence
- Refactor continuously, not in big batches

❌ **DON'T:**
- Sacrifice clarity for brevity
- Optimize prematurely
- Add comments that restate the code
- Leave TODO comments indefinitely
- Mix abstraction levels in one function
- Ignore language idioms and conventions

## References

- **Book**: "Clean Code: A Handbook of Agile Software Craftsmanship" by Robert C. Martin
- **Book**: "Refactoring: Improving the Design of Existing Code" by Martin Fowler
- **Principles**: SOLID, DRY (Don't Repeat Yourself), YAGNI (You Aren't Gonna Need It), KISS (Keep It Simple, Stupid)
- **Law of Demeter**: Objects should only talk to their immediate neighbors
- **Boy Scout Rule**: Leave code cleaner than you found it
