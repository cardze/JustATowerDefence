# Code Smells Reference Guide

A comprehensive catalog of code smells and how to recognize them.

## Bloaters

Code that has grown so large it's hard to work with.

### Long Method
**Symptoms:**
- Method exceeds 30 lines
- Multiple levels of nested loops/conditionals
- Difficult to understand at a glance

**Detection:**
- Count lines of code in method
- Check cyclomatic complexity > 10
- If you need to scroll to see the whole method, it's probably too long

**Refactoring:**
- Extract Method: Break into smaller methods
- Replace Temp with Query: Convert temporary variables to methods
- Introduce Parameter Object: Group related parameters

### Large Class
**Symptoms:**
- Class with many instance variables
- Class with many methods
- Class doing multiple unrelated things

**Detection:**
- Count methods (> 20 is suspicious)
- Count instance variables (> 10 is suspicious)
- Check if class name is vague (Manager, Helper, Util)

**Refactoring:**
- Extract Class: Split functionality
- Extract Subclass: Move specialized behavior
- Extract Interface: Define clear contracts

### Primitive Obsession
**Symptoms:**
- Using primitives instead of small objects for simple tasks
- Using string constants for field names
- Using arrays for complex data structures

**Detection:**
- Money represented as number
- Phone numbers as strings
- Date ranges as two separate dates

**Refactoring:**
- Replace Data Value with Object
- Replace Type Code with Class
- Extract Class for related primitives

### Long Parameter List
**Symptoms:**
- Method with more than 3-4 parameters
- Parameters that are always passed together
- Boolean flags as parameters

**Detection:**
- Count parameters
- Check for parameter groups
- Look for flag arguments

**Refactoring:**
- Replace Parameter with Method Call
- Preserve Whole Object
- Introduce Parameter Object

### Data Clumps
**Symptoms:**
- Same group of variables appearing together
- Multiple methods with same parameter groups
- Related fields in classes

**Detection:**
- Delete one variable from group - do others lose meaning?
- Same field names across multiple classes

**Refactoring:**
- Extract Class for the clump
- Introduce Parameter Object
- Preserve Whole Object

## Object-Orientation Abusers

Incomplete or incorrect application of OOP principles.

### Switch Statements
**Symptoms:**
- Complex switch/case or if-else chains
- Same switch logic duplicated in multiple places
- Switch on type codes

**Detection:**
- Long switch statements
- Multiple switches on same variable
- New cases require editing multiple places

**Refactoring:**
- Replace Type Code with Subclasses
- Replace Conditional with Polymorphism
- Replace Parameter with Explicit Methods

### Temporary Field
**Symptoms:**
- Instance variables used only in certain circumstances
- Fields that are null most of the time
- Fields set in one method, used in another

**Detection:**
- Check for null checks on instance variables
- Fields only valid during certain operations

**Refactoring:**
- Extract Class with those fields
- Replace Method with Method Object

### Refused Bequest
**Symptoms:**
- Subclass uses only some inherited methods
- Subclass overrides inherited methods with empty or exception-throwing implementations
- Subclass doesn't fit the "is-a" relationship

**Detection:**
- Check if subclass redefines methods to do nothing
- Unused inherited methods

**Refactoring:**
- Replace Inheritance with Delegation
- Extract Superclass for common functionality

### Alternative Classes with Different Interfaces
**Symptoms:**
- Classes doing similar things but with different method names
- Duplicate functionality across classes
- Different interfaces for same concept

**Detection:**
- Similar method bodies
- Same responsibility, different names

**Refactoring:**
- Rename Method to make interfaces consistent
- Move Method to consolidate functionality
- Extract Superclass for common interface

## Change Preventers

Code that makes changes difficult.

### Divergent Change
**Symptoms:**
- One class changed for many different reasons
- Making one type of change requires touching multiple methods
- Class changes for unrelated features

**Detection:**
- "If I need to add X, I have to change this class"
- "If I need to change Y, I also change this class"
- Multiple reasons to modify class

**Refactoring:**
- Extract Class for each responsibility
- Single Responsibility Principle
- Separate concerns

### Shotgun Surgery
**Symptoms:**
- Single change requires many small changes to many classes
- Related functionality scattered across codebase
- Change ripples through system

**Detection:**
- Making one change touches 5+ classes
- Similar changes needed in multiple places
- Related code far apart

**Refactoring:**
- Move Method to bring code together
- Move Field to consolidate data
- Inline Class if too fragmented

### Parallel Inheritance Hierarchies
**Symptoms:**
- Creating subclass in one hierarchy requires creating subclass in another
- Two hierarchies with similar structure
- Prefixes/names mirror each other

**Detection:**
- ClassA and ClassAHandler
- Manager and ManagerFactory parallel structure

**Refactoring:**
- Move Method to eliminate one hierarchy
- Move Field to consolidate

## Dispensables

Code that can be removed without consequences.

### Comments
**Symptoms:**
- Comments explaining what code does
- Comments that restate the code
- Commented-out code left in
- Obsolete comments

**Detection:**
- Comment longer than code it describes
- Comment stating the obvious
- Dead code commented out

**Refactoring:**
- Extract Method with explanatory name
- Rename Method to be self-documenting
- Delete commented-out code
- Replace comment with assertion if it's a constraint

### Duplicate Code
**Symptoms:**
- Same code structure in two or more places
- Copy-pasted code
- Similar algorithms with slight variations

**Detection:**
- Exact same lines in multiple places
- Similar code structure
- Same logic, different variable names

**Refactoring:**
- Extract Method for duplicates in same class
- Pull Up Method for duplicates in subclasses
- Form Template Method for similar algorithms
- Extract Class for duplicates across classes

### Lazy Class
**Symptoms:**
- Class that doesn't do enough to justify existence
- Class with only one or two methods
- Class that's just a wrapper

**Detection:**
- Tiny classes
- Classes that forward all calls
- Classes created "just in case"

**Refactoring:**
- Inline Class if too small
- Collapse Hierarchy if subclass isn't doing enough

### Data Class
**Symptoms:**
- Class with only fields and getters/setters
- No behavior, only data
- Other classes manipulate its data

**Detection:**
- Only has public fields or getters/setters
- No methods that operate on data
- All logic about data is elsewhere

**Refactoring:**
- Move Method to bring behavior to data
- Encapsulate Field
- Hide getters/setters for collections

### Dead Code
**Symptoms:**
- Unused variables, parameters, fields
- Methods never called
- Code after return statement
- Unreachable conditional branches

**Detection:**
- IDE marks as unused
- Coverage tools show never executed
- Can't find callers

**Refactoring:**
- Delete it
- Remove unused parameters
- Delete unreachable code

### Speculative Generality
**Symptoms:**
- Code for functionality that might be needed someday
- Overly flexible design with no current use
- Hooks and parameters "for future use"

**Detection:**
- Unused parameters
- Abstract classes with one subclass
- Methods never called
- "We might need this someday"

**Refactoring:**
- Collapse Hierarchy if not needed
- Inline Class
- Remove unused parameters
- Apply YAGNI (You Aren't Gonna Need It)

## Couplers

Excessive coupling between classes.

### Feature Envy
**Symptoms:**
- Method uses data/methods from another class more than its own
- Method prefers foreign class over its owner
- Heavy communication with other class

**Detection:**
- Count calls to other classes vs own class
- Method accesses other class's data repeatedly
- Method would be more at home elsewhere

**Refactoring:**
- Move Method to the envied class
- Extract Method and move the extracted part
- If method uses features of several classes, move to most-used

### Inappropriate Intimacy
**Symptoms:**
- Classes too familiar with each other's private parts
- Classes spending too much time together
- Excessive bidirectional dependencies

**Detection:**
- One class uses internal fields/methods of another
- Two classes deeply intertwined
- Circular dependencies

**Refactoring:**
- Move Method/Move Field to separate
- Extract Class for common functionality
- Replace Bidirectional Association with Unidirectional
- Replace Delegation with Inheritance (or vice versa)

### Message Chains
**Symptoms:**
- Client asks object for another object to ask for another object
- Long chains of getX().getY().getZ()
- Violations of Law of Demeter

**Detection:**
- Multiple chained method calls
- Code like a.getB().getC().doSomething()
- Client knows about object structure

**Refactoring:**
- Hide Delegate: Add method to intermediate object
- Extract Method then Move Method
- Delegate to closer objects

### Middle Man
**Symptoms:**
- Class whose only purpose is delegation
- Most methods just forward to another class
- Class adds no value, just passes requests

**Detection:**
- More than half of methods delegate
- Thin wrapper around another class

**Refactoring:**
- Remove Middle Man: Let client call directly
- Inline Method for simple delegation
- Replace Delegation with Inheritance if appropriate

## Severity Guide

### Critical (Fix Immediately)
- Security vulnerabilities from poor code structure
- Memory leaks or resource management issues
- Race conditions from poor separation
- Code that makes bugs likely

### High (Fix Soon)
- Long methods (> 50 lines)
- Large classes (> 500 lines)
- Deep nesting (> 4 levels)
- High cyclomatic complexity (> 15)
- Duplicate code in critical paths

### Medium (Refactor When Touching)
- Long methods (30-50 lines)
- Magic numbers
- Poor naming
- Medium complexity (10-15)
- Feature envy
- Data clumps

### Low (Nice to Have)
- Short methods that could be shorter
- Minor naming improvements
- Formatting inconsistencies
- Comments that could be code
- Lazy classes

## Detection Strategies

### Manual Review
1. Read through code slowly
2. Question every line: "Could this be simpler?"
3. Look for patterns that appear multiple times
4. Check if names reveal intent
5. Measure method/class size manually

### Automated Tools
- **Linters**: ESLint, Pylint, RuboCop, etc.
- **Complexity**: McCabe complexity, cognitive complexity
- **Coverage**: Identify dead code
- **Duplication**: PMD, CPD, Simian
- **Metrics**: SonarQube, Code Climate

### Code Review Checklist
- [ ] Functions < 30 lines
- [ ] Classes < 500 lines
- [ ] Parameters < 4
- [ ] Nesting depth < 4
- [ ] Cyclomatic complexity < 10
- [ ] No duplicate code blocks
- [ ] No commented-out code
- [ ] Names reveal intent
- [ ] No magic numbers
- [ ] Single responsibility per unit

## Quick Reference: Smell → Refactoring

| Smell | Primary Refactoring |
|-------|---------------------|
| Long Method | Extract Method |
| Large Class | Extract Class |
| Primitive Obsession | Replace Data Value with Object |
| Long Parameter List | Introduce Parameter Object |
| Data Clumps | Extract Class |
| Switch Statements | Replace Conditional with Polymorphism |
| Temporary Field | Extract Class |
| Refused Bequest | Replace Inheritance with Delegation |
| Alternative Classes | Rename Method + Move Method |
| Divergent Change | Extract Class |
| Shotgun Surgery | Move Method + Move Field |
| Feature Envy | Move Method |
| Inappropriate Intimacy | Move Method/Field + Extract Class |
| Message Chains | Hide Delegate |
| Middle Man | Remove Middle Man |
| Duplicate Code | Extract Method + Pull Up Method |
| Dead Code | Delete |
| Speculative Generality | Collapse Hierarchy + Inline Class |
| Comments | Rename Method + Extract Method |

## Remember

- Not all smells need immediate fixing
- Prioritize based on change frequency and bug risk
- Fix when you touch the code (Boy Scout Rule)
- Use automated tools to catch common smells
- Balance clean code with pragmatism
- Sometimes legacy code should be left alone
- Always have tests before refactoring
