import time
import functools
from typing import Any, Callable, Dict, List


class TimerDecorator:
    """
    A class-based decorator that measures and logs the execution times of functions.
    This helps identify performance bottlenecks in the application.
    """

    def __init__(self, func: Callable = None, *, verbose: bool = True, store_results: bool = True):
        """
        Initialize the TimerDecorator.

        Args:
            func (Callable): The function to be decorated (for direct usage)
            verbose (bool): Whether to print timing information immediately
            store_results (bool): Whether to store timing data for later analysis
        """
        self.verbose = verbose
        self.store_results = store_results
        self.timing_data: Dict[str, List[float]] = {}

        if func is not None:
            self.__call__ = functools.wraps(func)(self._create_wrapper(func))

    def __call__(self, func: Callable = None) -> Callable:
        """
        Make the class callable so it can be used as a decorator.

        Args:
            func (Callable): The function to be decorated

        Returns:
            Callable: The wrapped function
        """
        if func is None:
            # Called with parameters: @TimerDecorator(verbose=True)
            return lambda f: TimerDecorator(f, verbose=self.verbose, store_results=self.store_results)

        # Called directly: @TimerDecorator
        return self._create_wrapper(func)

    def _create_wrapper(self, func: Callable) -> Callable:
        """
        Create the wrapper function that adds timing functionality.

        Args:
            func (Callable): The original function to wrap

        Returns:
            Callable: The wrapped function with timing
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Record start time
            start_time = time.perf_counter()

            try:
                # Execute the original function
                result = func(*args, **kwargs)
                return result
            finally:
                # Calculate elapsed time (always executed, even if function fails)
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time

                # Store timing data
                if self.store_results:
                    if func.__name__ not in self.timing_data:
                        self.timing_data[func.__name__] = []
                    self.timing_data[func.__name__].append(elapsed_time)

                # Print timing information if verbose mode is enabled
                if self.verbose:
                    self._print_timing_info(func.__name__, elapsed_time, args, kwargs)

        return wrapper

    def _print_timing_info(self, func_name: str, elapsed_time: float, args: tuple, kwargs: dict) -> None:
        """
        Print formatted timing information.

        Args:
            func_name (str): Name of the executed function
            elapsed_time (float): Execution time in seconds
            args (tuple): Function arguments
            kwargs (dict): Function keyword arguments
        """
        # Format arguments for display
        args_str = ", ".join([str(arg) for arg in args])
        kwargs_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))

        print(f"⏱️  {func_name}({all_args}) executed in {elapsed_time:.6f} seconds")

    def get_stats(self, func_name: str = None) -> Dict[str, Any]:
        """
        Get statistics for timing data.

        Args:
            func_name (str): Specific function name, or None for all functions

        Returns:
            Dict[str, Any]: Statistics including count, average, min, max times
        """
        if not self.timing_data:
            return {}

        if func_name:
            if func_name not in self.timing_data:
                return {}
            times = self.timing_data[func_name]
            return {
                'function': func_name,
                'call_count': len(times),
                'total_time': sum(times),
                'average_time': sum(times) / len(times),
                'min_time': min(times),
                'max_time': max(times),
                'all_times': times
            }
        else:
            # Return stats for all functions
            all_stats = {}
            for name, times in self.timing_data.items():
                all_stats[name] = {
                    'call_count': len(times),
                    'total_time': sum(times),
                    'average_time': sum(times) / len(times),
                    'min_time': min(times),
                    'max_time': max(times)
                }
            return all_stats

    def reset_stats(self, func_name: str = None) -> None:
        """
        Reset timing data for specific function or all functions.

        Args:
            func_name (str): Specific function name, or None for all functions
        """
        if func_name:
            if func_name in self.timing_data:
                del self.timing_data[func_name]
        else:
            self.timing_data.clear()


# Demonstration with time-consuming functions

# Create an instance of the decorator for reuse
performance_timer = TimerDecorator(verbose=True, store_results=True)


# Method 1: Using the decorator as a class instance
@performance_timer
def factorial_recursive(n: int) -> int:
    """
    Calculate factorial using recursion - can be slow for large numbers.
    """
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)


# Method 2: Using the decorator class directly
@TimerDecorator
def factorial_iterative(n: int) -> int:
    """
    Calculate factorial using iteration - more efficient than recursion.
    """
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


# Method 3: Using decorator with parameters
@TimerDecorator(verbose=True, store_results=True)
def fibonacci_recursive(n: int) -> int:
    """
    Calculate Fibonacci number using recursion - very slow for larger numbers.
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


# Method 4: More efficient Fibonacci implementation
@TimerDecorator
def fibonacci_iterative(n: int) -> int:
    """
    Calculate Fibonacci number using iteration - much faster than recursion.
    """
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


# Method 5: Simulate database query or API call
@TimerDecorator
def simulated_api_call(duration: float) -> str:
    """
    Simulate a time-consuming API call or database query.
    """
    time.sleep(duration)
    return f"API response after {duration} seconds"


# Method 6: Matrix multiplication simulation
@TimerDecorator
def matrix_operations(size: int) -> List[List[int]]:
    """
    Simulate matrix operations with given size.
    """
    # Create sample matrices
    matrix = [[i * j for j in range(size)] for i in range(size)]

    # Simulate some computation
    result = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] += matrix[i][k] * matrix[k][j]

    return result


def demonstrate_timer_decorator():
    """
    Demonstrate the TimerDecorator with various time-consuming functions.
    """
    print("=" * 70)
    print("TIMER DECORATOR DEMONSTRATION")
    print("Performance Analytics for Python Functions")
    print("=" * 70)

    print("\n1. FACTORIAL CALCULATIONS")
    print("-" * 40)

    # Test factorial functions
    numbers = [5, 10, 15, 20]

    for n in numbers:
        print(f"\nCalculating factorial of {n}:")
        result_recursive = factorial_recursive(n)
        result_iterative = factorial_iterative(n)
        print(f"Results: recursive={result_recursive}, iterative={result_iterative}")

    print("\n2. FIBONACCI SEQUENCE CALCULATIONS")
    print("-" * 40)

    # Test Fibonacci functions (with smaller numbers due to recursion slowness)
    fib_numbers = [5, 10, 15, 20, 25]

    for n in fib_numbers:
        print(f"\nCalculating Fibonacci({n}):")
        if n <= 20:  # Recursive is too slow for larger numbers
            result_fib_recursive = fibonacci_recursive(n)
            print(f"Recursive result: {result_fib_recursive}")

        result_fib_iterative = fibonacci_iterative(n)
        print(f"Iterative result: {result_fib_iterative}")

    print("\n3. SIMULATED API CALLS")
    print("-" * 40)

    # Test simulated API calls
    durations = [0.5, 1.0, 0.3]
    for duration in durations:
        response = simulated_api_call(duration)
        print(f"Response: {response}")

    print("\n4. MATRIX OPERATIONS")
    print("-" * 40)

    # Test matrix operations with different sizes
    sizes = [50, 100]
    for size in sizes:
        print(f"\nPerforming matrix operations with size {size}x{size}:")
        matrix_operations(size)
        print(f"Completed matrix operations for size {size}")

    print("\n" + "=" * 70)
    print("PERFORMANCE STATISTICS SUMMARY")
    print("=" * 70)

    # Display comprehensive statistics
    stats = performance_timer.get_stats()
    for func_name, func_stats in stats.items():
        print(f"\n📊 {func_name.upper()}:")
        print(f"   Call Count: {func_stats['call_count']}")
        print(f"   Total Time: {func_stats['total_time']:.6f}s")
        print(f"   Average Time: {func_stats['average_time']:.6f}s")
        print(f"   Min Time: {func_stats['min_time']:.6f}s")
        print(f"   Max Time: {func_stats['max_time']:.6f}s")

    # Compare recursive vs iterative performance
    print("\n" + "=" * 70)
    print("PERFORMANCE COMPARISON: RECURSIVE VS ITERATIVE")
    print("=" * 70)

    recursive_stats = performance_timer.get_stats('factorial_recursive')
    iterative_stats = performance_timer.get_stats('factorial_iterative')

    if recursive_stats and iterative_stats:
        recursive_avg = recursive_stats['average_time']
        iterative_avg = iterative_stats['average_time']
        speedup = recursive_avg / iterative_avg if iterative_avg > 0 else float('inf')

        print(f"\nFactorial Performance Comparison:")
        print(f"  Recursive Average: {recursive_avg:.6f}s")
        print(f"  Iterative Average: {iterative_avg:.6f}s")
        print(f"  Speedup Factor: {speedup:.2f}x")

        if speedup > 1:
            print(f"  ✅ Iterative is {speedup:.2f}x faster than recursive")
        else:
            print(f"  ⚠️  Recursive is {1 / speedup:.2f}x faster than iterative")


def advanced_usage_example():
    """
    Demonstrate advanced usage patterns of the TimerDecorator.
    """
    print("\n" + "=" * 70)
    print("ADVANCED USAGE EXAMPLES")
    print("=" * 70)

    # Create a dedicated timer for a specific module
    module_timer = TimerDecorator(verbose=False, store_results=True)

    @module_timer
    def data_processing_operation(data_size: int) -> List[int]:
        """Simulate data processing operation."""
        time.sleep(0.1 * (data_size / 1000))
        return list(range(data_size))

    @module_timer
    def file_operation(file_size_mb: int) -> str:
        """Simulate file operation."""
        time.sleep(0.05 * file_size_mb)
        return f"Processed {file_size_mb}MB file"

    # Run multiple operations
    print("\nRunning data processing operations...")
    for size in [1000, 5000, 10000]:
        data_processing_operation(size)

    print("Running file operations...")
    for size in [10, 50, 100]:
        file_operation(size)

    # Get detailed statistics
    module_stats = module_timer.get_stats()
    print(f"\nModule Performance Statistics:")
    for func_name, stats in module_stats.items():
        print(f"  {func_name}: {stats['call_count']} calls, avg: {stats['average_time']:.4f}s")


if __name__ == "__main__":
    # Run the main demonstration
    demonstrate_timer_decorator()

    # Run advanced usage examples
    advanced_usage_example()

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print(" Class-based decorator with proper initialization")
    print(" Accurate execution time measurement")
    print(" Multiple usage patterns (direct, with parameters)")
    print(" Comprehensive timing data storage and statistics")
    print(" Performance comparison between different algorithms")
    print(" Robust error handling (timing works even if function fails)")