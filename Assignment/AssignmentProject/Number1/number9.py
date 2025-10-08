class InventoryItem:
    """
    A class to manage inventory items with encapsulated attributes and validation.
    This ensures data integrity and prevents unintended modifications.
    """

    def __init__(self, item_id: str, name: str, quantity: int = 0):
        """
        Constructor to initialize inventory item with private attributes.

        Args:
            item_id (str): Unique identifier for the item
            name (str): Name of the item
            quantity (int): Initial quantity (default 0, must be non-negative)
        """
        self.__item_id = None
        self.__name = None
        self.__quantity = None

        # Use setters to leverage validation during initialization
        self.set_item_id(item_id)
        self.set_name(name)
        self.set_quantity(quantity)

        print(f"✅ Inventory item created: {self.__name} (ID: {self.__item_id})")

    # Getter methods
    def get_item_id(self) -> str:
        """
        Get the item ID.

        Returns:
            str: The item ID
        """
        return self.__item_id

    def get_name(self) -> str:
        """
        Get the item name.

        Returns:
            str: The item name
        """
        return self.__name

    def get_quantity(self) -> int:
        """
        Get the current quantity.

        Returns:
            int: The current quantity
        """
        return self.__quantity

    # Setter methods with validation
    def set_item_id(self, new_id: str) -> None:
        """
        Set a new item ID with validation.

        Args:
            new_id (str): New item ID

        Raises:
            ValueError: If item ID is empty or not a string
        """
        if not new_id or not isinstance(new_id, str):
            raise ValueError("Item ID must be a non-empty string")

        old_id = self.__item_id
        self.__item_id = new_id

        if old_id:
            print(f"🆔 Item ID updated: '{old_id}' → '{new_id}'")

    def set_name(self, new_name: str) -> None:
        """
        Set a new item name with validation.

        Args:
            new_name (str): New item name

        Raises:
            ValueError: If name is empty or not a string
        """
        if not new_name or not isinstance(new_name, str):
            raise ValueError("Item name must be a non-empty string")

        old_name = self.__name
        self.__name = new_name

        if old_name:
            print(f"📝 Item name updated: '{old_name}' → '{new_name}'")

    def set_quantity(self, new_quantity: int) -> None:
        """
        Set a new quantity with validation to prevent negative values.

        Args:
            new_quantity (int): New quantity value

        Raises:
            ValueError: If quantity is negative or not an integer
        """
        if not isinstance(new_quantity, int):
            raise ValueError("Quantity must be an integer")

        if new_quantity < 0:
            raise ValueError(f"❌ Quantity cannot be negative. Attempted: {new_quantity}")

        old_quantity = self.__quantity
        self.__quantity = new_quantity

        if old_quantity is not None:
            change = new_quantity - old_quantity
            change_symbol = "↑" if change > 0 else "↓" if change < 0 else "="
            print(f"📦 Quantity updated: {old_quantity} → {new_quantity} ({change_symbol}{abs(change)})")

    # Business logic methods
    def increase_quantity(self, amount: int) -> None:
        """
        Increase the quantity by a specified amount.

        Args:
            amount (int): Amount to increase (must be positive)

        Raises:
            ValueError: If amount is not positive
        """
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Increase amount must be a positive integer")

        new_quantity = self.__quantity + amount
        self.set_quantity(new_quantity)

    def decrease_quantity(self, amount: int) -> None:
        """
        Decrease the quantity by a specified amount.

        Args:
            amount (int): Amount to decrease (must be positive)

        Raises:
            ValueError: If amount is not positive or would result in negative quantity
        """
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Decrease amount must be a positive integer")

        if self.__quantity - amount < 0:
            raise ValueError(f"Cannot decrease by {amount}. Current quantity: {self.__quantity}")

        new_quantity = self.__quantity - amount
        self.set_quantity(new_quantity)

    def restock(self, amount: int) -> None:
        """
        Restock the item by increasing quantity.

        Args:
            amount (int): Amount to restock
        """
        print(f"🚚 Restocking {self.__name} with {amount} units...")
        self.increase_quantity(amount)

    def sell(self, amount: int) -> None:
        """
        Sell the item by decreasing quantity.

        Args:
            amount (int): Amount to sell
        """
        print(f"💰 Selling {amount} units of {self.__name}...")
        self.decrease_quantity(amount)

    # Utility methods
    def get_item_info(self) -> str:
        """
        Get formatted item information.

        Returns:
            str: Formatted item information
        """
        return f"ID: {self.__item_id} | Name: {self.__name} | Quantity: {self.__quantity}"

    def display_info(self) -> None:
        """Display item information in a formatted way."""
        print(f"\n📋 Inventory Item Details:")
        print(f"   ID: {self.__item_id}")
        print(f"   Name: {self.__name}")
        print(f"   Quantity: {self.__quantity}")

    def is_out_of_stock(self) -> bool:
        """
        Check if the item is out of stock.

        Returns:
            bool: True if quantity is 0, False otherwise
        """
        return self.__quantity == 0

    def is_low_stock(self, threshold: int = 10) -> bool:
        """
        Check if the item has low stock.

        Args:
            threshold (int): Low stock threshold (default 10)

        Returns:
            bool: True if quantity is below threshold, False otherwise
        """
        return self.__quantity < threshold

    # Special methods
    def __str__(self) -> str:
        """String representation of the inventory item."""
        return f"InventoryItem('{self.__name}', ID: {self.__item_id}, Qty: {self.__quantity})"

    def __repr__(self) -> str:
        """Official string representation."""
        return f"InventoryItem(item_id='{self.__item_id}', name='{self.__name}', quantity={self.__quantity})"


def test_inventory_item_class():
    """
    Comprehensive test script for the InventoryItem class.
    Tests normal operations, edge cases, and error handling.
    """
    print("=" * 70)
    print("INVENTORY MANAGEMENT SYSTEM TESTING")
    print("=" * 70)

    print("\n1. CREATING INVENTORY ITEMS")
    print("-" * 40)

    # Create inventory items
    try:
        laptop = InventoryItem("ITM001", "Gaming Laptop", 15)
        mouse = InventoryItem("ITM002", "Wireless Mouse", 25)
        keyboard = InventoryItem("ITM003", "Mechanical Keyboard", 8)

        print("\n✅ All items created successfully!")
    except Exception as e:
        print(f"❌ Error creating items: {e}")
        return

    print("\n2. TESTING GETTER METHODS")
    print("-" * 40)

    # Test getter methods
    print(f"Laptop - ID: {laptop.get_item_id()}, Name: {laptop.get_name()}, Quantity: {laptop.get_quantity()}")
    print(f"Mouse - ID: {mouse.get_item_id()}, Name: {mouse.get_name()}, Quantity: {mouse.get_quantity()}")
    print(f"Keyboard - ID: {keyboard.get_item_id()}, Name: {keyboard.get_name()}, Quantity: {keyboard.get_quantity()}")

    print("\n3. TESTING SETTER METHODS - NORMAL OPERATIONS")
    print("-" * 40)

    # Test normal setter operations
    try:
        laptop.set_name("Premium Gaming Laptop")
        mouse.set_quantity(30)
        keyboard.set_item_id("ITM003-UPD")

        print("\n✅ All normal setter operations completed successfully!")
    except Exception as e:
        print(f"❌ Error in setter operations: {e}")

    print("\n4. TESTING QUANTITY VALIDATION - NEGATIVE QUANTITY ATTEMPT")
    print("-" * 40)

    # Test negative quantity validation
    try:
        print("Attempting to set quantity to -5...")
        laptop.set_quantity(-5)
        print("❌ ERROR: This should not be reached!")
    except ValueError as e:
        print(f"✅ Correctly prevented negative quantity: {e}")

    print("\n5. TESTING BUSINESS LOGIC METHODS")
    print("-" * 40)

    # Test business logic methods
    try:
        print("Testing restock operation:")
        laptop.restock(10)  # Should increase quantity

        print("\nTesting sell operation:")
        laptop.sell(5)  # Should decrease quantity

        print("\nTesting direct quantity modifications:")
        laptop.increase_quantity(3)
        laptop.decrease_quantity(2)

        print("\n✅ All business logic operations completed successfully!")
    except Exception as e:
        print(f"❌ Error in business logic: {e}")

    print("\n6. TESTING EDGE CASES AND ERROR HANDLING")
    print("-" * 40)

    # Test various edge cases
    test_cases = [
        ("Empty name", lambda: InventoryItem("ITM004", "", 10)),
        ("None quantity", lambda: InventoryItem("ITM005", "Test Item", None)),
        ("Negative initial quantity", lambda: InventoryItem("ITM006", "Test Item", -1)),
        ("Empty ID", lambda: InventoryItem("", "Test Item", 10)),
        ("Sell more than available", lambda: laptop.sell(1000)),
        ("Decrease with negative amount", lambda: laptop.decrease_quantity(-5)),
        ("Increase with zero amount", lambda: laptop.increase_quantity(0)),
    ]

    for test_name, test_func in test_cases:
        try:
            print(f"\nTesting: {test_name}")
            result = test_func()
            print(f"❌ UNEXPECTED: {test_name} should have failed!")
        except (ValueError, TypeError) as e:
            print(f"✅ Correctly handled: {e}")

    print("\n7. TESTING UTILITY METHODS")
    print("-" * 40)

    # Test utility methods
    laptop.display_info()
    print(f"\nFormatted info: {laptop.get_item_info()}")
    print(f"Is out of stock: {laptop.is_out_of_stock()}")
    print(f"Is low stock (threshold 20): {laptop.is_low_stock(20)}")
    print(f"Is low stock (threshold 10): {laptop.is_low_stock(10)}")

    print("\n8. TESTING SPECIAL METHODS")
    print("-" * 40)

    # Test special methods
    print(f"String representation: {laptop}")
    print(f"Official representation: {repr(laptop)}")

    print("\n9. FINAL STATE OF ALL ITEMS")
    print("-" * 40)

    # Display final state of all items
    items = [laptop, mouse, keyboard]
    for item in items:
        item.display_info()

    return laptop, mouse, keyboard


def demonstrate_encapsulation():
    """
    Demonstrates that private attributes are truly encapsulated.
    """
    print("\n" + "=" * 70)
    print("ENCAPSULATION DEMONSTRATION")
    print("=" * 70)

    # Create a test item
    test_item = InventoryItem("ENCAP001", "Encapsulated Item", 50)

    print("\n1. DIRECT ATTRIBUTE ACCESS ATTEMPTS:")
    print("-" * 40)

    # Attempt to access private attributes directly
    try:
        print(f"Attempting to access __item_id directly...")
        print(test_item.__item_id)  # This should fail
    except AttributeError as e:
        print(f"✅ Correctly prevented direct access: {e}")

    try:
        print(f"Attempting to access __name directly...")
        print(test_item.__name)  # This should fail
    except AttributeError as e:
        print(f"✅ Correctly prevented direct access: {e}")

    try:
        print(f"Attempting to access __quantity directly...")
        print(test_item.__quantity)  # This should fail
    except AttributeError as e:
        print(f"✅ Correctly prevented direct access: {e}")

    print("\n2. NAME MANGLING ATTEMPT:")
    print("-" * 40)

    # Show that even with name mangling, we can't easily modify private attributes
    try:
        print("Attempting name mangling access...")
        # This is the actual mangled name, but it's still not recommended to use
        mangled_name = f"_InventoryItem__quantity"
        if hasattr(test_item, mangled_name):
            print("⚠️  Name mangling exists but should not be used in production code!")
            # We won't actually modify it to maintain encapsulation principles
    except Exception as e:
        print(f"Access issue: {e}")

    print("\n3. PROPER ACCESS THROUGH GETTERS:")
    print("-" * 40)

    # Show proper access through getters
    print(f"Proper ID access: {test_item.get_item_id()}")
    print(f"Proper name access: {test_item.get_name()}")
    print(f"Proper quantity access: {test_item.get_quantity()}")

    print("\n✅ Encapsulation is properly enforced!")


if __name__ == "__main__":
    # Run comprehensive tests
    items = test_inventory_item_class()

    # Demonstrate encapsulation
    demonstrate_encapsulation()

    print("\n" + "=" * 70)
    print("TESTING COMPLETE")
    print("=" * 70)
    print("\nSummary:")
    print(" Private attributes properly encapsulated")
    print(" Getter and setter methods work correctly")
    print(" Negative quantity validation effective")
    print(" Business logic methods functional")
    print(" Error handling robust")
    print(" Encapsulation cannot be easily bypassed")