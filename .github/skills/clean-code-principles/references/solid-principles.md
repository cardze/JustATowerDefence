# SOLID Principles Reference

Comprehensive guide to SOLID principles with examples and applications.

## Overview

SOLID is an acronym for five design principles that make software designs more understandable, flexible, and maintainable:

- **S**ingle Responsibility Principle
- **O**pen/Closed Principle
- **L**iskov Substitution Principle
- **I**nterface Segregation Principle
- **D**ependency Inversion Principle

## Single Responsibility Principle (SRP)

### Definition
A class should have one, and only one, reason to change.

### Explanation
Each class should have only one job or responsibility. If a class has multiple responsibilities, changes to one responsibility may affect the class's ability to fulfill its other responsibilities.

### How to Identify Violations
- Class has multiple unrelated methods
- Changes to different features require changing the same class
- Class name contains "And" or "Manager"
- Difficult to name the class precisely

### Bad Example

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def save_to_database(self):
        # Database logic here
        pass
    
    def send_email(self):
        # Email sending logic here
        pass
    
    def generate_report(self):
        # Report generation logic here
        pass
```

**Problems:**
- User class handles data, persistence, email, and reporting
- Changes to email system affect User class
- Changes to database affect User class
- Difficult to test in isolation

### Good Example

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    def save(self, user):
        # Database logic here
        pass

class EmailService:
    def send_email(self, user):
        # Email sending logic here
        pass

class UserReportGenerator:
    def generate_report(self, user):
        # Report generation logic here
        pass
```

**Benefits:**
- Each class has one reason to change
- Easy to test independently
- Can swap implementations easily
- Clear, focused responsibilities

### When to Apply
- When a class is doing too much
- When unit testing requires mocking multiple dependencies
- When the same class changes for different features
- When team members work on different features but touch the same class

## Open/Closed Principle (OCP)

### Definition
Software entities should be open for extension but closed for modification.

### Explanation
You should be able to add new functionality without changing existing code. This is typically achieved through abstraction and polymorphism.

### How to Identify Violations
- Adding new features requires modifying existing classes
- Long switch/if-else statements checking types
- Conditional logic scattered throughout codebase
- Fear of breaking existing code when adding features

### Bad Example

```python
class PaymentProcessor:
    def process_payment(self, payment_type, amount):
        if payment_type == "credit_card":
            # Credit card logic
            print(f"Processing credit card payment: ${amount}")
        elif payment_type == "paypal":
            # PayPal logic
            print(f"Processing PayPal payment: ${amount}")
        elif payment_type == "bitcoin":
            # Bitcoin logic
            print(f"Processing Bitcoin payment: ${amount}")
        # Need to modify this class for each new payment type!
```

**Problems:**
- Must modify existing code for each new payment type
- Risk of breaking existing payment methods
- Violates SRP (knows about all payment types)
- Difficult to test individual payment types

### Good Example

```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCardPayment(PaymentMethod):
    def process_payment(self, amount):
        print(f"Processing credit card payment: ${amount}")

class PayPalPayment(PaymentMethod):
    def process_payment(self, amount):
        print(f"Processing PayPal payment: ${amount}")

class BitcoinPayment(PaymentMethod):
    def process_payment(self, amount):
        print(f"Processing Bitcoin payment: ${amount}")

class PaymentProcessor:
    def process(self, payment_method: PaymentMethod, amount):
        payment_method.process_payment(amount)

# Adding new payment type requires NO changes to existing code
class ApplePayPayment(PaymentMethod):
    def process_payment(self, amount):
        print(f"Processing Apple Pay payment: ${amount}")
```

**Benefits:**
- New payment types don't modify existing code
- Each payment type is independently testable
- No risk of breaking existing payment methods
- Easy to add new types

### When to Apply
- When you have conditional logic based on type
- When you anticipate new variations of behavior
- When you find yourself modifying core classes for new features
- When implementing plugin architectures

## Liskov Substitution Principle (LSP)

### Definition
Objects of a superclass should be replaceable with objects of a subclass without breaking the application.

### Explanation
Derived classes must be substitutable for their base classes. This means a subclass should override parent methods in a way that doesn't break functionality from the client's perspective.

### How to Identify Violations
- Subclass throws exceptions in overridden methods
- Subclass returns different types than parent
- Subclass requires different preconditions
- Subclass has weaker postconditions
- Client needs to check types before calling methods

### Bad Example

```python
class Bird:
    def fly(self):
        print("Flying")

class Sparrow(Bird):
    def fly(self):
        print("Sparrow flying")

class Penguin(Bird):
    def fly(self):
        raise Exception("Penguins can't fly!")

# Client code breaks with substitution
def make_bird_fly(bird: Bird):
    bird.fly()  # Breaks if bird is a Penguin!

sparrow = Sparrow()
penguin = Penguin()
make_bird_fly(sparrow)  # OK
make_bird_fly(penguin)  # Exception!
```

**Problems:**
- Penguin violates contract established by Bird
- Client must check type before calling fly()
- Not all Birds can fly, bad abstraction

### Good Example

```python
class Bird:
    def move(self):
        pass

class FlyingBird(Bird):
    def fly(self):
        print("Flying")
    
    def move(self):
        self.fly()

class Sparrow(FlyingBird):
    def fly(self):
        print("Sparrow flying")

class Penguin(Bird):
    def swim(self):
        print("Swimming")
    
    def move(self):
        self.swim()

# Client code works with any Bird
def make_bird_move(bird: Bird):
    bird.move()  # Always works!

sparrow = Sparrow()
penguin = Penguin()
make_bird_move(sparrow)  # Flies
make_bird_move(penguin)  # Swims
```

**Benefits:**
- All subtypes fulfill parent contract
- No type checking needed in client code
- Polymorphism works correctly
- Better abstraction hierarchy

### Contract Rules
- **Preconditions** cannot be strengthened in subtype
- **Postconditions** cannot be weakened in subtype
- **Invariants** must be preserved
- **History constraint**: subclass shouldn't allow state changes that base class doesn't allow

### When to Apply
- When designing inheritance hierarchies
- When overriding methods in subclasses
- When you find yourself checking types
- When exceptions are thrown from overridden methods

## Interface Segregation Principle (ISP)

### Definition
Clients should not be forced to depend on interfaces they don't use.

### Explanation
Many specific interfaces are better than one general-purpose interface. Classes should not be forced to implement methods they don't need.

### How to Identify Violations
- Interface has many unrelated methods
- Implementing classes throw NotImplementedError or leave methods empty
- Different clients use different parts of the interface
- Interface changes affect classes that don't use changed methods

### Bad Example

```python
from abc import ABC, abstractmethod

class Worker(ABC):
    @abstractmethod
    def work(self):
        pass
    
    @abstractmethod
    def eat(self):
        pass
    
    @abstractmethod
    def sleep(self):
        pass

class HumanWorker(Worker):
    def work(self):
        print("Human working")
    
    def eat(self):
        print("Human eating")
    
    def sleep(self):
        print("Human sleeping")

class RobotWorker(Worker):
    def work(self):
        print("Robot working")
    
    def eat(self):
        raise NotImplementedError("Robots don't eat")
    
    def sleep(self):
        raise NotImplementedError("Robots don't sleep")
```

**Problems:**
- RobotWorker forced to implement methods it doesn't need
- Violations throw exceptions
- Interface too broad for all use cases

### Good Example

```python
from abc import ABC, abstractmethod

class Workable(ABC):
    @abstractmethod
    def work(self):
        pass

class Eatable(ABC):
    @abstractmethod
    def eat(self):
        pass

class Sleepable(ABC):
    @abstractmethod
    def sleep(self):
        pass

class HumanWorker(Workable, Eatable, Sleepable):
    def work(self):
        print("Human working")
    
    def eat(self):
        print("Human eating")
    
    def sleep(self):
        print("Human sleeping")

class RobotWorker(Workable):
    def work(self):
        print("Robot working")
    
    # No need to implement eat() or sleep()
```

**Benefits:**
- Classes only implement what they need
- Smaller, focused interfaces
- Changes don't affect unrelated classes
- Better composition possibilities

### When to Apply
- When interface has many unrelated methods
- When different clients use different subsets of interface
- When implementing classes leave methods empty
- When designing APIs or plugin systems

## Dependency Inversion Principle (DIP)

### Definition
1. High-level modules should not depend on low-level modules. Both should depend on abstractions.
2. Abstractions should not depend on details. Details should depend on abstractions.

### Explanation
Depend on abstractions (interfaces) rather than concrete implementations. This reduces coupling and makes the system more flexible.

### How to Identify Violations
- High-level classes directly instantiate low-level classes
- Hard to swap implementations
- Difficult to test because of hard dependencies
- Changes to low-level classes break high-level classes

### Bad Example

```python
class MySQLDatabase:
    def save(self, data):
        print(f"Saving {data} to MySQL")

class UserService:
    def __init__(self):
        self.database = MySQLDatabase()  # Direct dependency!
    
    def save_user(self, user):
        self.database.save(user)

# Hard to test without MySQL
# Hard to switch to PostgreSQL
# UserService depends on concrete implementation
```

**Problems:**
- UserService tightly coupled to MySQLDatabase
- Cannot test without MySQL
- Cannot switch database without changing UserService
- High-level depends on low-level

### Good Example

```python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass

class MySQLDatabase(Database):
    def save(self, data):
        print(f"Saving {data} to MySQL")

class PostgreSQLDatabase(Database):
    def save(self, data):
        print(f"Saving {data} to PostgreSQL")

class MockDatabase(Database):
    def save(self, data):
        print(f"Mock saving {data}")

class UserService:
    def __init__(self, database: Database):
        self.database = database  # Depend on abstraction!
    
    def save_user(self, user):
        self.database.save(user)

# Easy to test with mock
test_service = UserService(MockDatabase())

# Easy to switch implementations
mysql_service = UserService(MySQLDatabase())
postgres_service = UserService(PostgreSQLDatabase())
```

**Benefits:**
- UserService doesn't know about concrete databases
- Easy to test with mocks
- Easy to swap implementations
- Both layers depend on abstraction
- Lower coupling

### Dependency Injection Patterns

#### Constructor Injection (Recommended)
```python
class Service:
    def __init__(self, dependency: Abstraction):
        self.dependency = dependency
```

#### Setter Injection
```python
class Service:
    def set_dependency(self, dependency: Abstraction):
        self.dependency = dependency
```

#### Method Injection
```python
class Service:
    def do_something(self, dependency: Abstraction):
        dependency.execute()
```

### When to Apply
- When creating reusable components
- When you need to test classes in isolation
- When you want to swap implementations easily
- When designing plugin architectures
- Always in high-level business logic

## Applying SOLID Together

### Example: E-commerce Order System

```python
from abc import ABC, abstractmethod
from typing import List

# SRP: Each class has one responsibility

class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

class Order:
    def __init__(self, products: List[Product]):
        self.products = products
    
    def get_total(self) -> float:
        return sum(p.price for p in self.products)

# ISP: Focused interfaces
class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class NotificationService(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass

# OCP: Open for extension
class CreditCardPayment(PaymentMethod):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing ${amount} via credit card")
        return True

class PayPalPayment(PaymentMethod):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing ${amount} via PayPal")
        return True

# OCP: Can add new notification types without changing existing code
class EmailNotification(NotificationService):
    def send(self, message: str) -> None:
        print(f"Sending email: {message}")

class SMSNotification(NotificationService):
    def send(self, message: str) -> None:
        print(f"Sending SMS: {message}")

# SRP: Only handles order processing logic
# DIP: Depends on abstractions, not concrete classes
class OrderProcessor:
    def __init__(self, payment: PaymentMethod, notification: NotificationService):
        self.payment = payment
        self.notification = notification
    
    def process_order(self, order: Order) -> bool:
        total = order.get_total()
        
        if self.payment.process_payment(total):
            self.notification.send(f"Order processed successfully: ${total}")
            return True
        else:
            self.notification.send("Payment failed")
            return False

# Usage - easy to configure and test
processor = OrderProcessor(
    payment=CreditCardPayment(),
    notification=EmailNotification()
)

order = Order([
    Product("Book", 10.00),
    Product("Pen", 2.00)
])

processor.process_order(order)
```

## Benefits of SOLID

1. **Maintainability**: Easier to understand and modify code
2. **Testability**: Classes can be tested in isolation
3. **Flexibility**: Easy to extend and modify behavior
4. **Reusability**: Components can be reused in different contexts
5. **Scalability**: System can grow without becoming unwieldy
6. **Reduced Coupling**: Classes are less dependent on each other
7. **Better Design**: Forces you to think about responsibilities

## Common Mistakes

### Over-Engineering
Don't apply SOLID when you don't need it:
- Simple scripts don't need interfaces
- Prototypes can be messier
- Apply incrementally as code grows

### Interface Explosion
Don't create too many tiny interfaces:
- Balance between ISP and practical grouping
- Related methods can share an interface

### Abstraction for Everything
Don't abstract things that won't change:
- Some dependencies are stable (standard library)
- Focus on volatile dependencies

### Ignoring Performance
SOLID can add overhead:
- Profile before optimizing
- Most applications benefit more from maintainability
- Optimize hot paths if needed

## Checklist

### Single Responsibility
- [ ] Each class has one clear purpose
- [ ] Class name describes its single responsibility
- [ ] Changes to different features don't affect same class

### Open/Closed
- [ ] New features don't require modifying existing code
- [ ] Behavior extended through inheritance/composition
- [ ] No type checking in business logic

### Liskov Substitution
- [ ] Subclasses can replace parent classes
- [ ] Overridden methods don't throw unexpected exceptions
- [ ] Subclasses don't violate parent contracts

### Interface Segregation
- [ ] Interfaces are focused and cohesive
- [ ] No methods throw NotImplementedError
- [ ] Clients depend only on methods they use

### Dependency Inversion
- [ ] High-level modules depend on abstractions
- [ ] Dependencies injected, not created internally
- [ ] Easy to mock dependencies for testing

## Further Reading

- "Clean Architecture" by Robert C. Martin
- "Design Patterns" by Gang of Four
- "Refactoring" by Martin Fowler
- "Dependency Injection in .NET" by Mark Seemann
