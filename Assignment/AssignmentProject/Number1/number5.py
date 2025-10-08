def add_session(schedule, session_detail):
    """
    Adds a new study session to the schedule list.

    Args:
        schedule (list): The current list of study sessions
        session_detail (str): The details of the study session to add

    Returns:
        list: The updated schedule with the new session appended
    """
    # Input validation
    if not isinstance(schedule, list):
        raise TypeError("Schedule must be a list")

    if not session_detail or not isinstance(session_detail, str):
        raise ValueError("Session detail must be a non-empty string")

    # Append the session to the schedule
    schedule.append(session_detail)
    return schedule


def display_schedule(schedule, title="Current Study Schedule"):
    """
    Displays the current study schedule in a formatted way.

    Args:
        schedule (list): The list of study sessions
        title (str): The title for the display
    """
    print(f"\n{title}")
    print("=" * 50)

    if not schedule:
        print("No study sessions scheduled yet.")
        return

    for i, session in enumerate(schedule, 1):
        print(f"{i}. {session}")

    print(f"Total sessions: {len(schedule)}")
    print("=" * 50)


def demonstrate_basic_functionality():
    """
    Demonstrates the basic functionality of adding sessions to an empty list.
    """
    print("=== BASIC FUNCTIONALITY DEMONSTRATION ===")

    # Start with an empty list
    study_schedule = []
    display_schedule(study_schedule, "Initial Empty Schedule")

    # Sequentially add different study sessions
    sessions_to_add = [
        "Mathematics - Chapter 5: Calculus",
        "Physics - Quantum Mechanics Review",
        "Computer Science - Python Programming Practice",
        "History - World War II Analysis",
        "Chemistry - Organic Compounds Study"
    ]

    for session in sessions_to_add:
        add_session(study_schedule, session)
        display_schedule(study_schedule, f"After adding: '{session}'")

    return study_schedule


def test_with_various_inputs():
    """
    Tests the add_session function with various types of inputs and edge cases.
    """
    print("\n" + "=" * 60)
    print("=== COMPREHENSIVE TESTING WITH VARIOUS INPUTS ===")
    print("=" * 60)

    # Test 1: Normal operation with mixed subjects
    print("\n--- Test 1: Mixed Subjects ---")
    mixed_schedule = []
    mixed_sessions = [
        "English Literature - Shakespeare Analysis",
        "Biology - Cell Structure Revision",
        "Mathematics - Linear Algebra Problems"
    ]

    for session in mixed_sessions:
        add_session(mixed_schedule, session)

    display_schedule(mixed_schedule, "Mixed Subjects Schedule")

    # Test 2: Adding sessions with time specifications
    print("\n--- Test 2: Sessions with Time Specifications ---")
    timed_schedule = []
    timed_sessions = [
        "Morning: Physics - 2 hours problem solving",
        "Afternoon: Chemistry Lab Report Writing",
        "Evening: Mathematics Revision - 7:00 PM to 9:00 PM"
    ]

    for session in timed_sessions:
        add_session(timed_schedule, session)
        print(f"Added: '{session}'")

    display_schedule(timed_schedule, "Timed Study Schedule")

    # Test 3: Progressive building of a weekly schedule
    print("\n--- Test 3: Building Weekly Schedule ---")
    weekly_schedule = []

    days_sessions = [
        "Monday: Calculus and Algebra",
        "Tuesday: Physics and Chemistry",
        "Wednesday: Programming Projects",
        "Thursday: History and Literature",
        "Friday: Review and Practice Tests",
        "Saturday: Group Study Session",
        "Sunday: Relaxation and Light Reading"
    ]

    for day_session in days_sessions:
        add_session(weekly_schedule, day_session)

    display_schedule(weekly_schedule, "Complete Weekly Study Schedule")

    return mixed_schedule, timed_schedule, weekly_schedule


def edge_case_testing():
    """
    Tests edge cases and error handling.
    """
    print("\n" + "=" * 60)
    print("=== EDGE CASE AND ERROR HANDLING TESTING ===")
    print("=" * 60)

    # Test with empty string (should raise error)
    print("\n--- Testing Error Handling ---")
    try:
        test_schedule = []
        add_session(test_schedule, "")  # This should raise ValueError
    except ValueError as e:
        print(f"✓ Correctly caught error: {e}")

    # Test with non-list schedule (should raise error)
    try:
        add_session("not_a_list", "Some session")  # This should raise TypeError
    except TypeError as e:
        print(f"✓ Correctly caught error: {e}")

    # Test with very long session description
    print("\n--- Testing Long Session Description ---")
    long_schedule = []
    long_description = "Advanced Mathematics: Multivariable Calculus, Differential Equations, and Complex Analysis with practical applications in Physics and Engineering"
    add_session(long_schedule, long_description)
    display_schedule(long_schedule, "Schedule with Long Description")

    # Test adding duplicate sessions (should work fine)
    print("\n--- Testing Duplicate Sessions ---")
    duplicate_schedule = []
    add_session(duplicate_schedule, "Python Programming")
    add_session(duplicate_schedule, "Python Programming")  # Duplicate
    add_session(duplicate_schedule, "Data Structures")
    display_schedule(duplicate_schedule, "Schedule with Duplicate Sessions")


def interactive_demo():
    """
    Provides an interactive demonstration where users can add their own sessions.
    """
    print("\n" + "=" * 60)
    print("=== INTERACTIVE DEMONSTRATION ===")
    print("=" * 60)

    interactive_schedule = []

    print("\nWelcome to the Study Planner Interactive Demo!")
    print("You can add your own study sessions to the schedule.")
    print("Type 'done' when you're finished adding sessions.\n")

    while True:
        session_input = input("Enter a study session: ").strip()

        if session_input.lower() == 'done':
            break

        if not session_input:
            print("Please enter a valid session description.")
            continue

        try:
            add_session(interactive_schedule, session_input)
            print(f"✓ Added: '{session_input}'")
            print(f"Total sessions so far: {len(interactive_schedule)}\n")
        except (ValueError, TypeError) as e:
            print(f"Error: {e}\n")

    if interactive_schedule:
        display_schedule(interactive_schedule, "Your Final Study Schedule")
    else:
        print("\nNo sessions were added to the schedule.")


def performance_demonstration():
    """
    Demonstrates the function's performance with a large number of sessions.
    """
    print("\n" + "=" * 60)
    print("=== PERFORMANCE DEMONSTRATION ===")
    print("=" * 60)

    large_schedule = []
    num_sessions = 10  # Reduced for demonstration purposes

    print(f"\nAdding {num_sessions} study sessions dynamically...")

    for i in range(1, num_sessions + 1):
        session = f"Study Session #{i}: Topic Review and Practice"
        add_session(large_schedule, session)

        # Show progress for every 2 sessions
        if i % 2 == 0:
            print(f"Progress: {i}/{num_sessions} sessions added")

    print(f"\n✓ Successfully added {len(large_schedule)} sessions!")
    print(f"First 3 sessions: {large_schedule[:3]}")
    print(f"Last 3 sessions: {large_schedule[-3:]}")
    print(f"Total schedule size: {len(large_schedule)} sessions")


# Main execution
if __name__ == "__main__":
    # Run all demonstrations
    print("STUDY PLANNER APPLICATION - SESSION MANAGEMENT")
    print("=" * 60)

    # Basic functionality
    final_schedule = demonstrate_basic_functionality()

    # Various input tests
    mixed, timed, weekly = test_with_various_inputs()

    # Edge case testing
    edge_case_testing()

    # Performance demonstration
    performance_demonstration()

    # Interactive demo (uncomment to use)
    # interactive_demo()

    print("\n" + "=" * 60)
    print("=== DEMONSTRATION COMPLETE ===")
    print("=" * 60)
    print("\nKey Features Demonstrated:")
    print("✓ Dynamic list expansion without overwriting existing data")
    print("✓ Sequential addition of study sessions")
    print("✓ Real-time schedule display after each addition")
    print("✓ Input validation and error handling")
    print("✓ Support for various session formats and types")