# =============================================================================
# ORIGINAL REGULAR FUNCTIONS (BEFORE CONVERSION)
# =============================================================================

def calculate_percentage(part, whole):
    """Calculate percentage: (part/whole) * 100"""
    return (part / whole) * 100 if whole != 0 else 0


def validate_positive_number(number):
    """Validate if a number is positive"""
    return number > 0


def extract_field(record, field_name):
    """Extract a specific field from a data record dictionary"""
    return record.get(field_name, None)


# =============================================================================
# LAMBDA FUNCTION CONVERSIONS
# =============================================================================

# 1. Percentage calculation lambda
# Syntax: lambda arguments: expression
calculate_percentage_lambda = lambda part, whole: (part / whole) * 100 if whole != 0 else 0

# 2. Positive number validation lambda
validate_positive_lambda = lambda number: number > 0

# 3. Field extraction lambda (curried version for better usability)
extract_field_lambda = lambda field_name: lambda record: record.get(field_name, None)


# =============================================================================
# DEMONSTRATION AND USAGE EXAMPLES
# =============================================================================

def demonstrate_lambda_usage():
    """Demonstrate various ways to use the lambda functions"""

    print("=== FINANCIAL ANALYTICS LAMBDA FUNCTIONS DEMONSTRATION ===\n")

    # Sample financial data
    financial_records = [
        {'ticker': 'AAPL', 'price': 150.25, 'volume': 1000000, 'change': 2.5},
        {'ticker': 'GOOGL', 'price': 2750.80, 'volume': 500000, 'change': -1.2},
        {'ticker': 'MSFT', 'price': 305.45, 'volume': 750000, 'change': 0.8},
        {'ticker': 'TSLA', 'price': 210.30, 'volume': 1200000, 'change': 5.7},
        {'ticker': 'AMZN', 'price': 3250.75, 'volume': 300000, 'change': -0.5}
    ]

    stock_prices = [150.25, 2750.80, 305.45, 210.30, 3250.75]
    trading_volumes = [1000000, 500000, 750000, 1200000, 300000]
    portfolio_values = [5000, -2500, 10000, 7500, 0]

    # =========================================================================
    # 1. USING LAMBDA FUNCTIONS DIRECTLY
    # =========================================================================
    print("1. DIRECT LAMBDA FUNCTION CALLS:")
    print(f"Percentage (25 of 200): {calculate_percentage_lambda(25, 200):.1f}%")
    print(f"Is 150 positive? {validate_positive_lambda(150)}")
    print(f"Is -50 positive? {validate_positive_lambda(-50)}")

    # Create specialized extractors using currying
    extract_price = extract_field_lambda('price')
    extract_ticker = extract_field_lambda('ticker')

    print(f"Extracted price: {extract_price(financial_records[0])}")
    print(f"Extracted ticker: {extract_ticker(financial_records[1])}")
    print("\n" + "-" * 60 + "\n")

    # =========================================================================
    # 2. USING LAMBDA FUNCTIONS IN LIST COMPREHENSIONS
    # =========================================================================
    print("2. LAMBDA FUNCTIONS IN LIST COMPREHENSIONS:")

    # Calculate percentages of each stock price relative to maximum price
    max_price = max(stock_prices)
    price_percentages = [calculate_percentage_lambda(price, max_price) for price in stock_prices]
    print(f"Price percentages of max: {[f'{p:.1f}%' for p in price_percentages]}")

    # Filter and validate positive portfolio values
    valid_portfolios = [value for value in portfolio_values if validate_positive_lambda(value)]
    print(f"Valid (positive) portfolios: {valid_portfolios}")

    # Extract all tickers using list comprehension
    all_tickers = [extract_field_lambda('ticker')(record) for record in financial_records]
    print(f"All stock tickers: {all_tickers}")
    print("\n" + "-" * 60 + "\n")

    # =========================================================================
    # 3. USING LAMBDA FUNCTIONS WITH MAP()
    # =========================================================================
    print("3. LAMBDA FUNCTIONS WITH MAP():")

    # Calculate daily returns as percentages (assuming previous close was 95% of current)
    previous_closes = [price * 0.95 for price in stock_prices]
    returns = list(map(
        lambda current, prev: calculate_percentage_lambda(current - prev, prev),
        stock_prices, previous_closes
    ))
    print(f"Daily returns: {[f'{r:+.2f}%' for r in returns]}")

    # Format prices with currency symbol
    formatted_prices = list(map(lambda price: f"${price:.2f}", stock_prices))
    print(f"Formatted prices: {formatted_prices}")

    # Extract all volume data
    volumes = list(map(extract_field_lambda('volume'), financial_records))
    print(f"Trading volumes: {volumes}")
    print("\n" + "-" * 60 + "\n")

    # =========================================================================
    # 4. USING LAMBDA FUNCTIONS WITH FILTER()
    # =========================================================================
    print("4. LAMBDA FUNCTIONS WITH FILTER():")

    # Filter stocks with positive price change
    gainers = list(filter(
        lambda record: validate_positive_lambda(record['change']),
        financial_records
    ))
    print(f"Stocks with positive change: {[r['ticker'] for r in gainers]}")

    # Filter high-volume stocks (volume > 700,000)
    high_volume_stocks = list(filter(
        lambda record: validate_positive_lambda(record['volume'] - 700000),
        financial_records
    ))
    print(f"High volume stocks: {[r['ticker'] for r in high_volume_stocks]}")

    # Filter valid financial records (all required fields present)
    required_fields = ['ticker', 'price', 'volume']
    valid_records = list(filter(
        lambda record: all(extract_field_lambda(field)(record) for field in required_fields),
        financial_records
    ))
    print(f"Valid records count: {len(valid_records)}")
    print("\n" + "-" * 60 + "\n")

    # =========================================================================
    # 5. ADVANCED USAGE: COMBINING MAP AND FILTER
    # =========================================================================
    print("5. COMBINING MAP AND FILTER:")

    # Calculate price-to-volume ratio for high volume stocks only
    high_volume_ratios = list(map(
        lambda record: record['price'] / record['volume'],
        filter(lambda record: record['volume'] > 600000, financial_records)
    ))
    print(f"Price/Volume ratios for high volume stocks: {[f'{r:.6f}' for r in high_volume_ratios]}")

    # Get percentage changes only for stocks with valid data
    valid_changes = list(map(
        extract_field_lambda('change'),
        filter(lambda record: record.get('change') is not None, financial_records)
    ))
    print(f"Valid price changes: {valid_changes}")


# =============================================================================
# PERFORMANCE COMPARISON DEMONSTRATION
# =============================================================================

def performance_comparison():
    """Compare lambda vs regular function performance (conceptual)"""
    print("\n=== PERFORMANCE CONSIDERATIONS ===")
    print("Lambda functions offer:")
    print("• Reduced overhead for simple operations")
    print("• Inline definition eliminates function call lookup")
    print("• Better performance in tight loops with map()/filter()")
    print("• Cleaner code for simple transformations")
    print("\nBest suited for:")
    print("• Simple, single-expression operations")
    print("• Use within map(), filter(), sorted()")
    print("• Callbacks and short-lived operations")


# =============================================================================
# ALTERNATIVE INLINE LAMBDA USAGE
# =============================================================================

def demonstrate_inline_lambdas():
    """Show inline lambda usage without variable assignment"""

    print("\n=== INLINE LAMBDA USAGE ===")

    data = [10, 25, 40, 15, 30]

    # Inline lambda with map
    squared = list(map(lambda x: x ** 2, data))
    print(f"Squared values: {squared}")

    # Inline lambda with filter
    above_20 = list(filter(lambda x: x > 20, data))
    print(f"Values above 20: {above_20}")

    # Inline lambda with sorted
    records = [{'value': 15}, {'value': 5}, {'value': 25}]
    sorted_records = sorted(records, key=lambda x: x['value'])
    print(f"Sorted records: {sorted_records}")


if __name__ == "__main__":
    demonstrate_lambda_usage()
    performance_comparison()
    demonstrate_inline_lambdas()