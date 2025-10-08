import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SerializationError(Exception):
    """Custom exception for serialization errors."""
    pass


class DeserializationError(Exception):
    """Custom exception for deserialization errors."""
    pass


class UserProfile:
    """
    Represents a user profile with validation and serialization capabilities.
    """

    def __init__(self, name: str, age: int, email: str, preferences: Dict[str, Any] = None):
        """
        Initialize a user profile with validation.

        Args:
            name (str): User's full name
            age (int): User's age (must be between 0 and 150)
            email (str): User's email address
            preferences (Dict): User preferences dictionary
        """
        self._validate_name(name)
        self._validate_age(age)
        self._validate_email(email)

        self.name = name
        self.age = age
        self.email = email
        self.preferences = preferences or {}
        self.created_at = datetime.now().isoformat()
        self.last_updated = self.created_at

    def _validate_name(self, name: str) -> None:
        """Validate the name field."""
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if not name.strip():
            raise ValueError("Name cannot be empty")
        if len(name) > 100:
            raise ValueError("Name too long (max 100 characters)")

    def _validate_age(self, age: int) -> None:
        """Validate the age field."""
        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
        if age < 0 or age > 150:
            raise ValueError("Age must be between 0 and 150")

    def _validate_email(self, email: str) -> None:
        """Basic email validation."""
        if not isinstance(email, str):
            raise ValueError("Email must be a string")
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email format")

    def update_preferences(self, new_preferences: Dict[str, Any]) -> None:
        """Update user preferences with validation."""
        if not isinstance(new_preferences, dict):
            raise ValueError("Preferences must be a dictionary")

        # Validate preference values (basic check)
        for key, value in new_preferences.items():
            if not isinstance(key, str):
                raise ValueError("Preference keys must be strings")
            # Ensure value is JSON serializable
            try:
                json.dumps(value)
            except (TypeError, ValueError) as e:
                raise ValueError(f"Preference value for '{key}' is not JSON serializable: {e}")

        self.preferences.update(new_preferences)
        self.last_updated = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert user profile to dictionary for serialization."""
        return {
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'preferences': self.preferences,
            'created_at': self.created_at,
            'last_updated': self.last_updated,
            '_version': '1.0'  # Schema version for compatibility
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        """Create UserProfile from dictionary with validation."""
        try:
            # Check required fields
            required_fields = ['name', 'age', 'email']
            for field in required_fields:
                if field not in data:
                    raise DeserializationError(f"Missing required field: {field}")

            # Create profile instance
            profile = cls(
                name=data['name'],
                age=data['age'],
                email=data['email'],
                preferences=data.get('preferences', {})
            )

            # Restore metadata if available
            if 'created_at' in data:
                profile.created_at = data['created_at']
            if 'last_updated' in data:
                profile.last_updated = data['last_updated']

            return profile

        except (ValueError, TypeError) as e:
            raise DeserializationError(f"Invalid data in dictionary: {e}")

    def __str__(self) -> str:
        return f"UserProfile(name='{self.name}', age={self.age}, email='{self.email}')"

    def __repr__(self) -> str:
        return f"UserProfile(name='{self.name}', age={self.age}, email='{self.email}', preferences={self.preferences})"


def serialize_user_profile(profile: UserProfile, filename: Optional[str] = None) -> str:
    """
    Serialize a UserProfile object to JSON format with comprehensive error handling.

    Args:
        profile (UserProfile): The user profile object to serialize
        filename (str, optional): If provided, save to file

    Returns:
        str: JSON string representation of the profile

    Raises:
        SerializationError: If serialization fails due to various reasons
    """
    try:
        # Step 1: Convert to dictionary
        logger.info(f"Starting serialization for user: {profile.name}")
        profile_dict = profile.to_dict()

        # Step 2: Serialize to JSON with additional validation
        json_data = json.dumps(profile_dict, indent=2, ensure_ascii=False, default=_json_serializer)

        # Step 3: Validate the JSON can be parsed back (round-trip validation)
        try:
            parsed_back = json.loads(json_data)
            if parsed_back['name'] != profile.name:  # Basic integrity check
                raise SerializationError("Data integrity check failed during serialization")
        except (KeyError, json.JSONDecodeError) as e:
            raise SerializationError(f"Serialization integrity check failed: {e}")

        # Step 4: Save to file if filename provided
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(json_data)
                logger.info(f"Profile successfully saved to: {filename}")
            except IOError as e:
                raise SerializationError(f"Failed to write to file '{filename}': {e}")
            except PermissionError as e:
                raise SerializationError(f"Permission denied writing to file '{filename}': {e}")

        logger.info(f"Successfully serialized profile for: {profile.name}")
        return json_data

    except (TypeError, ValueError) as e:
        error_msg = f"Data type error during serialization: {e}"
        logger.error(error_msg)
        raise SerializationError(error_msg)

    except AttributeError as e:
        error_msg = f"Invalid object structure during serialization: {e}"
        logger.error(error_msg)
        raise SerializationError(error_msg)

    except Exception as e:
        error_msg = f"Unexpected error during serialization: {e}"
        logger.error(error_msg)
        raise SerializationError(error_msg)


def deserialize_user_profile(json_data: str, filename: Optional[str] = None) -> UserProfile:
    """
    Deserialize JSON data back into a UserProfile object with comprehensive error handling.

    Args:
        json_data (str): JSON string to deserialize (optional if filename provided)
        filename (str, optional): File to read JSON data from

    Returns:
        UserProfile: Reconstructed UserProfile object

    Raises:
        DeserializationError: If deserialization fails due to various reasons
    """
    try:
        # Step 1: Get JSON data from file or direct input
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    json_data = f.read()
                logger.info(f"Successfully read data from: {filename}")
            except FileNotFoundError:
                raise DeserializationError(f"File not found: {filename}")
            except IOError as e:
                raise DeserializationError(f"Error reading file '{filename}': {e}")
            except PermissionError as e:
                raise DeserializationError(f"Permission denied reading file '{filename}': {e}")

        if not json_data:
            raise DeserializationError("No JSON data provided for deserialization")

        # Step 2: Parse JSON with schema validation
        try:
            parsed_data = json.loads(json_data)
        except json.JSONDecodeError as e:
            raise DeserializationError(f"Invalid JSON format: {e}")

        # Step 3: Validate basic structure
        if not isinstance(parsed_data, dict):
            raise DeserializationError("JSON data must represent a dictionary")

        # Step 4: Check schema version for compatibility
        version = parsed_data.get('_version', '1.0')
        if version != '1.0':
            logger.warning(f"Loading data with different schema version: {version}")

        # Step 5: Create UserProfile from dictionary
        profile = UserProfile.from_dict(parsed_data)

        logger.info(f"Successfully deserialized profile for: {profile.name}")
        return profile

    except KeyError as e:
        error_msg = f"Missing required field in JSON data: {e}"
        logger.error(error_msg)
        raise DeserializationError(error_msg)

    except ValueError as e:
        error_msg = f"Data validation error during deserialization: {e}"
        logger.error(error_msg)
        raise DeserializationError(error_msg)

    except Exception as e:
        error_msg = f"Unexpected error during deserialization: {e}"
        logger.error(error_msg)
        raise DeserializationError(error_msg)


def _json_serializer(obj: Any) -> Any:
    """
    Custom JSON serializer for handling non-serializable objects.

    Args:
        obj: Object to serialize

    Returns:
        Serializable representation of the object

    Raises:
        TypeError: If object cannot be serialized
    """
    if isinstance(obj, (datetime,)):
        return obj.isoformat()
    elif hasattr(obj, '__dict__'):
        return obj.__dict__
    else:
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def backup_deserialization_attempt(json_data: str) -> Optional[UserProfile]:
    """
    Attempt a backup deserialization with relaxed rules for corrupted data recovery.

    Args:
        json_data (str): Potentially corrupted JSON data

    Returns:
        Optional[UserProfile]: Profile if recoverable, None otherwise
    """
    try:
        logger.warning("Attempting backup deserialization for corrupted data")

        # Try to parse with relaxed error handling
        parsed_data = json.loads(json_data)

        # Extract fields with fallbacks
        name = parsed_data.get('name', 'Unknown User')
        age = parsed_data.get('age', 0)
        email = parsed_data.get('email', 'unknown@example.com')
        preferences = parsed_data.get('preferences', {})

        # Create basic profile (bypassing some validations)
        profile = UserProfile(
            name=str(name) if name else 'Unknown User',
            age=int(age) if isinstance(age, (int, float, str)) and str(age).isdigit() else 0,
            email=str(email) if email else 'unknown@example.com',
            preferences=preferences if isinstance(preferences, dict) else {}
        )

        logger.info(f"Backup deserialization successful for: {profile.name}")
        return profile

    except Exception as e:
        logger.error(f"Backup deserialization failed: {e}")
        return None


def demonstrate_serialization_deserialization():
    """
    Comprehensive demonstration of serialization and deserialization with various scenarios.
    """
    print("=" * 70)
    print("USER PROFILE SERIALIZATION/DESERIALIZATION DEMONSTRATION")
    print("=" * 70)

    # Create sample user profiles
    users = [
        UserProfile("Alice Johnson", 28, "alice@example.com", {"theme": "dark", "notifications": True}),
        UserProfile("Bob Smith", 35, "bob.smith@company.com", {"language": "en", "timezone": "UTC"}),
        UserProfile("Carol Davis", 42, "carol.davis@email.org", {"newsletter": False, "auto_save": True})
    ]

    print("\n1. SUCCESSFUL SERIALIZATION AND DESERIALIZATION")
    print("-" * 50)

    for i, user in enumerate(users, 1):
        try:
            print(f"\nProcessing user {i}: {user.name}")

            # Serialize
            json_output = serialize_user_profile(user, f"user_profile_{i}.json")
            print(f"✅ Serialization successful")
            print(f"   JSON preview: {json_output[:100]}...")

            # Deserialize
            restored_user = deserialize_user_profile(filename=f"user_profile_{i}.json")
            print(f"✅ Deserialization successful")
            print(f"   Restored: {restored_user}")

        except (SerializationError, DeserializationError) as e:
            print(f"❌ Error: {e}")

    print("\n2. ERROR HANDLING DEMONSTRATION")
    print("-" * 50)

    # Test various error scenarios
    error_scenarios = [
        ("Invalid data types", lambda: UserProfile("Test", "not_an_integer", "invalid_email")),
        ("Missing required fields", lambda: deserialize_user_profile('{"name": "Partial"}')),
        ("Invalid JSON format", lambda: deserialize_user_profile('{"invalid: json}')),
        ("File not found", lambda: deserialize_user_profile(filename="nonexistent_file.json")),
        ("Non-serializable preferences",
         lambda: UserProfile("Test", 25, "test@example.com", {"complex_obj": object()})),
    ]

    for scenario_name, test_func in error_scenarios:
        try:
            print(f"\nTesting: {scenario_name}")
            result = test_func()
            print(f"❌ UNEXPECTED: Should have raised an error!")
        except (SerializationError, DeserializationError, ValueError) as e:
            print(f"✅ Correctly handled: {e}")

    print("\n3. DATA CORRUPTION RECOVERY ATTEMPT")
    print("-" * 50)

    # Test backup deserialization with corrupted data
    corrupted_data = '{"name": "John", "age": "invalid", "email": "john@example.com", "preferences": {}}'

    print("Attempting to recover from corrupted data...")
    recovered_profile = backup_deserialization_attempt(corrupted_data)

    if recovered_profile:
        print(f"✅ Recovery successful: {recovered_profile}")
    else:
        print("❌ Recovery failed")

    print("\n4. COMPREHENSIVE DATA INTEGRITY CHECK")
    print("-" * 50)

    # Test round-trip integrity
    original_user = UserProfile("Integrity Test", 30, "test@example.com", {"setting": "value"})

    try:
        # Serialize and deserialize
        json_data = serialize_user_profile(original_user)
        restored_user = deserialize_user_profile(json_data)

        # Verify data integrity
        integrity_checks = [
            ("Name matches", original_user.name == restored_user.name),
            ("Age matches", original_user.age == restored_user.age),
            ("Email matches", original_user.email == restored_user.email),
            ("Preferences match", original_user.preferences == restored_user.preferences),
        ]

        for check_name, check_result in integrity_checks:
            status = "✅" if check_result else "❌"
            print(f"{status} {check_name}: {check_result}")

        if all(check[1] for check in integrity_checks):
            print("🎉 All integrity checks passed! Data round-trip successful.")
        else:
            print("⚠️  Some integrity checks failed!")

    except Exception as e:
        print(f"❌ Integrity test failed: {e}")


def explain_error_handling_mechanisms():
    """
    Explain the importance of each error handling mechanism in real-world applications.
    """
    print("\n" + "=" * 70)
    print("ERROR HANDLING MECHANISMS EXPLANATION")
    print("=" * 70)

    explanation = """
    IMPORTANCE OF ERROR HANDLING IN REAL-WORLD APPLICATIONS:

    1. DATA TYPE VALIDATION (Serialization):
       • Prevents: Invalid data types causing serialization failures
       • Real-world impact: Prevents application crashes when saving user data
       • Example: Ensuring age is integer, not string "twenty-five"

    2. JSON DECODE ERROR HANDLING (Deserialization):
       • Prevents: Corrupted or malformed JSON files from crashing the app
       • Real-world impact: Allows graceful recovery from file corruption
       • Example: Network interruptions during file transfer

    3. REQUIRED FIELD VALIDATION (Deserialization):
       • Prevents: Incomplete data from creating invalid user objects
       • Real-world impact: Maintains data consistency across system
       • Example: Schema evolution without breaking existing data

    4. FILE I/O ERROR HANDLING:
       • Prevents: Permission issues, disk full, or missing files from causing crashes
       • Real-world impact: Application remains stable under various system conditions
       • Example: User without write permissions can still use the app

    5. SCHEMA VERSION COMPATIBILITY:
       • Prevents: Version mismatches from breaking data loading
       • Real-world impact: Smooth upgrades and backward compatibility
       • Example: Old data files work with new application versions

    6. CUSTOM EXCEPTION HIERARCHY:
       • Enables: Specific error handling for different failure types
       • Real-world impact: Better user feedback and recovery strategies
       • Example: Different messages for file not found vs data corruption

    7. BACKUP DESERIALIZATION:
       • Provides: Last-resort data recovery from partially corrupted files
       • Real-world impact: Data loss prevention in critical situations
       • Example: Recovering user preferences from damaged config files

    8. LOGGING AND MONITORING:
       • Enables: Debugging and monitoring in production environments
       • Real-world impact: Faster issue identification and resolution
       • Example: Tracking serialization failures across user base

    WHY THIS MATTERS:
    • User Experience: Prevents confusing crashes and data loss
    • Data Integrity: Ensures consistent and reliable data storage
    • Maintainability: Clear error paths make debugging easier
    • Scalability: Robust error handling supports larger deployments
    • Compliance: Proper data handling meets regulatory requirements
    """

    print(explanation)


if __name__ == "__main__":
    # Run the demonstration
    demonstrate_serialization_deserialization()

    # Explain error handling mechanisms
    explain_error_handling_mechanisms()

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)