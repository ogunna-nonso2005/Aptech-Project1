class Employee:
    """
    A class to manage employee records efficiently.
    Demonstrates key OOP concepts: encapsulation, constructors, methods, and static fields.
    """

    # Static field to count the number of employees
    _employee_count = 0

    def __init__(self, employee_id: int, name: str, department: str):
        """
        Constructor for initializing employee attributes.

        Args:
            employee_id (int): Unique identifier for the employee
            name (str): Full name of the employee
            department (str): Department where the employee works
        """
        self._employee_id = employee_id
        self._name = name
        self._department = department

        # Increment the static employee count
        Employee._employee_count += 1

        print(f"Employee #{employee_id} created: {name} from {department}")

    # Getter and Setter methods for name
    def get_name(self) -> str:
        """Getter method for employee name."""
        return self._name

    def set_name(self, new_name: str) -> None:
        """
        Setter method for employee name with validation.

        Args:
            new_name (str): New name for the employee
        """
        if not new_name or not isinstance(new_name, str):
            raise ValueError("Name must be a non-empty string")

        old_name = self._name
        self._name = new_name
        print(f"Employee #{self._employee_id}: Name updated from '{old_name}' to '{new_name}'")

    # Getter and Setter methods for department
    def get_department(self) -> str:
        """Getter method for employee department."""
        return self._department

    def set_department(self, new_department: str) -> None:
        """
        Setter method for employee department with validation.

        Args:
            new_department (str): New department for the employee
        """
        if not new_department or not isinstance(new_department, str):
            raise ValueError("Department must be a non-empty string")

        old_department = self._department
        self._department = new_department
        print(f"Employee #{self._employee_id}: Department updated from '{old_department}' to '{new_department}'")

    # Getter for employee_id (read-only property)
    def get_employee_id(self) -> int:
        """Getter method for employee ID (read-only)."""
        return self._employee_id

    # Additional methods for employee management
    def get_employee_info(self) -> str:
        """
        Returns formatted string with complete employee information.

        Returns:
            str: Formatted employee information
        """
        return (f"Employee ID: {self._employee_id}, "
                f"Name: {self._name}, "
                f"Department: {self._department}")

    def display_employee_info(self) -> None:
        """Displays employee information in a formatted way."""
        print(f"\n📋 Employee Information:")
        print(f"   ID: {self._employee_id}")
        print(f"   Name: {self._name}")
        print(f"   Department: {self._department}")

    # Class method to get total employee count
    @classmethod
    def get_employee_count(cls) -> int:
        """
        Class method to get the total number of employees created.

        Returns:
            int: Total employee count
        """
        return cls._employee_count

    @classmethod
    def display_employee_count(cls) -> None:
        """Displays the total number of employees."""
        print(f"\n👥 Total Employees: {cls._employee_count}")

    # Static method for company information
    @staticmethod
    def get_company_info() -> str:
        """
        Static method that returns company information.
        This method doesn't depend on any instance or class data.

        Returns:
            str: Company information
        """
        return "Welcome to Our Company - Employee Management System v1.0"

    # Special methods for better object representation
    def __str__(self) -> str:
        """String representation of the Employee object."""
        return f"Employee({self._employee_id}: {self._name} - {self._department})"

    def __repr__(self) -> str:
        """Official string representation of the Employee object."""
        return f"Employee(employee_id={self._employee_id}, name='{self._name}', department='{self._department}')"

    # Destructor to demonstrate garbage collection
    def __del__(self):
        """
        Destructor method that is called when the object is about to be destroyed.
        Decrements the employee count and prints a message.
        """
        Employee._employee_count -= 1
        print(f"🗑️  Employee #{self._employee_id} ({self._name}) is being destroyed. "
              f"Remaining employees: {Employee._employee_count}")


def demonstrate_employee_class():
    """
    Demonstrates the functionality of the Employee class.
    """
    print("=" * 70)
    print("EMPLOYEE MANAGEMENT SYSTEM DEMONSTRATION")
    print("=" * 70)

    print(f"\n{Employee.get_company_info()}")

    print("\n1. CREATING EMPLOYEES")
    print("-" * 40)

    # Create employee instances
    emp1 = Employee(101, "Alice Johnson", "Engineering")
    emp2 = Employee(102, "Bob Smith", "Marketing")
    emp3 = Employee(103, "Carol Davis", "Human Resources")

    # Display current employee count
    Employee.display_employee_count()

    print("\n2. USING GETTER AND SETTER METHODS")
    print("-" * 40)

    # Demonstrate getter methods
    print(f"\nEmployee 1 Info:")
    print(f"  ID: {emp1.get_employee_id()}")
    print(f"  Name: {emp1.get_name()}")
    print(f"  Department: {emp1.get_department()}")

    # Demonstrate setter methods
    emp1.set_name("Alice Brown")  # Name change due to marriage
    emp2.set_department("Sales")  # Department transfer

    print("\n3. EMPLOYEE INFORMATION DISPLAY")
    print("-" * 40)

    # Display all employee information
    emp1.display_employee_info()
    emp2.display_employee_info()
    emp3.display_employee_info()

    print("\n4. USING SPECIAL METHODS")
    print("-" * 40)

    # Demonstrate __str__ and __repr__
    print(f"String representation: {emp1}")
    print(f"Official representation: {repr(emp1)}")

    # Get complete employee info
    print(f"\nComplete info for emp2: {emp2.get_employee_info()}")

    print("\n5. GARBAGE COLLECTION DEMONSTRATION")
    print("-" * 40)

    # Create temporary employees to demonstrate garbage collection
    print("Creating temporary employees...")
    temp_emp1 = Employee(201, "Temp Employee 1", "IT")
    temp_emp2 = Employee(202, "Temp Employee 2", "Finance")

    Employee.display_employee_count()

    print("\nDeleting temporary employees...")
    del temp_emp1  # Explicitly delete object
    del temp_emp2  # Explicitly delete object

    # Force garbage collection to see immediate results
    import gc
    gc.collect()

    Employee.display_employee_count()

    return emp1, emp2, emp3


def advanced_employee_operations():
    """
    Demonstrates advanced operations and error handling.
    """
    print("\n" + "=" * 70)
    print("ADVANCED OPERATIONS AND ERROR HANDLING")
    print("=" * 70)

    # Create a new employee for advanced demonstration
    emp = Employee(301, "David Wilson", "Operations")

    print("\n1. ERROR HANDLING IN SETTER METHODS")
    print("-" * 40)

    try:
        emp.set_name("")  # This should raise ValueError
    except ValueError as e:
        print(f"✓ Correctly caught error: {e}")

    try:
        emp.set_department(123)  # This should raise ValueError
    except ValueError as e:
        print(f"✓ Correctly caught error: {e}")

    print("\n2. MULTIPLE UPDATES")
    print("-" * 40)

    # Demonstrate multiple updates
    emp.set_name("David Wilson Jr.")
    emp.set_department("Senior Operations")

    print("\n3. FINAL STATE")
    print("-" * 40)
    emp.display_employee_info()

    return emp


# Explanation of Python's Garbage Collection for Employee Class
def explain_garbage_collection():
    """
    Provides a detailed explanation of how Python's garbage collection
    manages instances of the Employee class.
    """
    print("\n" + "=" * 70)
    print("PYTHON GARBAGE COLLECTION EXPLANATION")
    print("=" * 70)

    explanation = """
    How Python's Garbage Collection Manages Employee Class Instances:

    1. REFERENCE COUNTING (Primary Mechanism):
       • Each Employee object has a reference count tracking how many references point to it
       • When reference count drops to 0, object is immediately eligible for deletion
       • Examples of reference count changes:
         - emp = Employee(101, "John", "IT")  # ref count = 1
         - emp2 = emp                         # ref count = 2  
         - del emp                            # ref count = 1
         - del emp2                           # ref count = 0 → Object destroyed

    2. DESTRUCTOR EXECUTION (__del__ method):
       • When an Employee object's reference count reaches 0, __del__ is called
       • Our __del__ method:
         - Decrements the static _employee_count
         - Prints destruction message
         - Helps track object lifecycle

    3. GARBAGE COLLECTOR (GC) for Circular References:
       • Python's GC detects and collects circular references
       • Example circular reference:
         emp1.manager = emp2
         emp2.subordinate = emp1
       • Even if external references are gone, GC breaks these cycles

    4. MEMORY MANAGEMENT:
       • Employee objects are stored in heap memory
       • When destroyed, memory is returned to Python's memory manager
       • Python may reuse memory for new objects

    5. MANUAL GARBAGE COLLECTION:
       • Can force collection: import gc; gc.collect()
       • Useful for immediate cleanup in performance-critical applications

    Key Points for Employee Class:
    • Static _employee_count provides real-time tracking of active objects
    • __del__ method ensures proper cleanup when objects are destroyed
    • Getter/setter methods don't affect garbage collection
    • Objects are automatically cleaned up when they go out of scope
    """

    print(explanation)


if __name__ == "__main__":
    # Run the main demonstration
    employees = demonstrate_employee_class()

    # Run advanced operations
    advanced_emp = advanced_employee_operations()

    # Explain garbage collection
    explain_garbage_collection()

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)

    # Final employee count
    Employee.display_employee_count()

    print("\nCleaning up remaining employees...")
    # Explicitly delete remaining objects to demonstrate garbage collection
    for emp in employees:
        del emp

    # Force final garbage collection
    import gc

    gc.collect()

    print(f"Final employee count: {Employee.get_employee_count()}")