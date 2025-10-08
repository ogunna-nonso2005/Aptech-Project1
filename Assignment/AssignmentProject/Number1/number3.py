class Book:
    """
    A class to represent a book in the inventory system.

    Attributes:
        title (str): The title of the book
        author (str): The author of the book
        price (float): The price of the book
        stock_quantity (int): The number of copies in stock
    """

    def __init__(self, title, author, price, stock_quantity):
        """
        Initialize a new Book instance.

        Args:
            title (str): Book title
            author (str): Book author
            price (float): Book price
            stock_quantity (int): Initial stock quantity
        """
        self.title = title
        self.author = author
        self.price = price
        self.stock_quantity = stock_quantity

    def update_stock(self, new_quantity):
        """
        Update the stock quantity of the book.

        Args:
            new_quantity (int): New stock quantity
        """
        self.stock_quantity = new_quantity

    def display_info(self):
        """Display the book's information in a formatted way."""
        return f"Title: {self.title:<20} | Author: {self.author:<15} | Price: ${self.price:>6.2f} | Stock: {self.stock_quantity:>3}"


class BookstoreInventory:
    """
    A class to manage the bookstore's inventory of books.

    Attributes:
        books (list): List of Book objects in the inventory
    """

    def __init__(self):
        """Initialize an empty inventory."""
        self.books = []

    def add_new_book(self, title, author, price, stock_quantity):
        """
        Add a new book to the inventory.

        Args:
            title (str): Book title
            author (str): Book author
            price (float): Book price
            stock_quantity (int): Initial stock quantity

        Returns:
            str: Confirmation message
        """
        # Input validation
        if not title or not author:
            return "Error: Title and author cannot be empty."

        if price < 0:
            return "Error: Price cannot be negative."

        if stock_quantity < 0:
            return "Error: Stock quantity cannot be negative."

        # Check if book already exists
        for book in self.books:
            if book.title.lower() == title.lower() and book.author.lower() == author.lower():
                return f"Error: '{title}' by {author} already exists in inventory."

        # Create new book and add to inventory
        new_book = Book(title, author, price, stock_quantity)
        self.books.append(new_book)
        return f"Successfully added '{title}' by {author} to inventory."

    def update_stock(self, title, author, new_quantity):
        """
        Update the stock quantity of an existing book.

        Args:
            title (str): Book title
            author (str): Book author
            new_quantity (int): New stock quantity

        Returns:
            str: Confirmation message
        """
        # Input validation
        if new_quantity < 0:
            return "Error: Stock quantity cannot be negative."

        # Find the book and update its stock
        for book in self.books:
            if book.title.lower() == title.lower() and book.author.lower() == author.lower():
                book.update_stock(new_quantity)
                return f"Successfully updated stock for '{title}' by {author} to {new_quantity}."

        return f"Error: Book '{title}' by {author} not found in inventory."

    def display_all_books(self):
        """
        Display details of all books in the inventory.

        Returns:
            str: Formatted string with all books' information or empty message
        """
        if not self.books:
            return "No books in inventory."

        # Create header and book list
        header = "=" * 80
        title_header = "BOOKSTORE INVENTORY"
        column_header = f"{'Title':<20} | {'Author':<15} | {'Price':>8} | {'Stock':>5}"

        result = [header, title_header.center(80), header, column_header, "-" * 80]

        # Add each book's information
        for book in self.books:
            result.append(book.display_info())

        result.append(header)
        result.append(f"Total books in inventory: {len(self.books)}")

        return "\n".join(result)

    def find_book(self, title, author):
        """
        Helper function to find a specific book in inventory.

        Args:
            title (str): Book title
            author (str): Book author

        Returns:
            Book or None: Book object if found, None otherwise
        """
        for book in self.books:
            if book.title.lower() == title.lower() and book.author.lower() == author.lower():
                return book
        return None


def main():
    """
    Main function to demonstrate the bookstore inventory system.
    """
    # Create bookstore inventory
    bookstore = BookstoreInventory()

    print("=== BOOKSTORE INVENTORY MANAGEMENT SYSTEM ===\n")

    # Demonstration: Adding new books
    print("1. ADDING NEW BOOKS:")
    print(bookstore.add_new_book("The Great Gatsby", "F. Scott Fitzgerald", 12.99, 15))
    print(bookstore.add_new_book("To Kill a Mockingbird", "Harper Lee", 14.50, 8))
    print(bookstore.add_new_book("1984", "George Orwell", 10.99, 12))
    print(bookstore.add_new_book("Pride and Prejudice", "Jane Austen", 9.99, 20))

    # Try to add duplicate book
    print(bookstore.add_new_book("1984", "George Orwell", 11.99, 5))

    print("\n" + "=" * 50 + "\n")

    # Demonstration: Display all books
    print("2. CURRENT INVENTORY:")
    print(bookstore.display_all_books())

    print("\n" + "=" * 50 + "\n")

    # Demonstration: Updating stock
    print("3. UPDATING STOCK:")
    print(bookstore.update_stock("The Great Gatsby", "F. Scott Fitzgerald", 10))
    print(bookstore.update_stock("1984", "George Orwell", 20))

    # Try to update non-existent book
    print(bookstore.update_stock("Unknown Book", "Unknown Author", 5))

    print("\n" + "=" * 50 + "\n")

    # Demonstration: Display updated inventory
    print("4. UPDATED INVENTORY:")
    print(bookstore.display_all_books())


# Interactive menu for user input
def interactive_menu():
    """
    Provides an interactive menu for the bookstore staff to use the system.
    """
    bookstore = BookstoreInventory()

    while True:
        print("\n=== BOOKSTORE INVENTORY MENU ===")
        print("1. Add New Book")
        print("2. Update Stock Quantity")
        print("3. Display All Books")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == '1':
            print("\n--- Add New Book ---")
            title = input("Enter book title: ").strip()
            author = input("Enter author: ").strip()
            try:
                price = float(input("Enter price: $"))
                stock = int(input("Enter stock quantity: "))
                result = bookstore.add_new_book(title, author, price, stock)
                print(f"\n{result}")
            except ValueError:
                print("Error: Please enter valid numbers for price and stock.")

        elif choice == '2':
            print("\n--- Update Stock ---")
            title = input("Enter book title: ").strip()
            author = input("Enter author: ").strip()
            try:
                new_stock = int(input("Enter new stock quantity: "))
                result = bookstore.update_stock(title, author, new_stock)
                print(f"\n{result}")
            except ValueError:
                print("Error: Please enter a valid number for stock quantity.")

        elif choice == '3':
            print(f"\n{bookstore.display_all_books()}")

        elif choice == '4':
            print("Thank you for using the Bookstore Inventory System!")
            break

        else:
            print("Invalid choice. Please enter a number between 1-4.")


if __name__ == "__main__":
    # Run the demonstration
    main()

    # Uncomment the line below to run the interactive menu
    # interactive_menu()