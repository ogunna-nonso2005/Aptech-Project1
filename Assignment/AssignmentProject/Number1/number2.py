def suggest_activity(precipitation, temperature, wind_speed):
    """
    Recommends activities based on current weather conditions.

    Args:
        precipitation (float): Precipitation in mm/h
        temperature (float): Temperature in Celsius
        wind_speed (float): Wind speed in km/h

    Returns:
        str: Recommended activity
    """

    # Set Boolean variables based on weather thresholds
    is_raining = precipitation > 0  # True if there's any precipitation
    is_cold = temperature < 15  # True if temperature below 15°C (considered cold)
    is_windy = wind_speed > 20  # True if wind speed exceeds 20 km/h

    print(f"Weather Conditions: Precipitation={precipitation}mm/h, "
          f"Temperature={temperature}°C, Wind Speed={wind_speed}km/h")
    print(f"Status: Raining={is_raining}, Cold={is_cold}, Windy={is_windy}")

    # Decision-making logic for activity recommendations
    if is_raining:
        # Rainy conditions - recommend indoor activities
        if is_cold:
            return "Recommendation: Visit a museum or art gallery - perfect for a cold, rainy day!"
        else:
            return "Recommendation: Go to an indoor swimming pool or shopping mall - rainy but not too cold!"

    elif is_windy:
        # Windy but not rainy - consider temperature for outdoor activities
        if is_cold:
            return "Recommendation: Try indoor rock climbing - too windy and cold for most outdoor activities!"
        else:
            return "Recommendation: Go flying a kite at the park - windy conditions are perfect for kite flying!"

    elif is_cold:
        # Cold but not rainy or windy - suitable for certain outdoor activities
        return "Recommendation: Go for a brisk hike - cold weather is great for energetic outdoor exercise!"

    else:
        # Perfect weather conditions - no rain, not cold, not windy
        return "Recommendation: Perfect for a picnic in the park or outdoor sports - enjoy the great weather!"


def demonstrate_activity_suggestions():
    """Demonstrate the function with various weather scenarios"""

    print("=== WEATHER ACTIVITY RECOMMENDATION SYSTEM ===\n")

    # Test Case 1: Perfect weather
    print("Test 1 - Perfect Weather:")
    print(suggest_activity(0, 25, 10))  # No rain, warm, light breeze
    print("\n" + "-" * 50 + "\n")

    # Test Case 2: Rainy and cold
    print("Test 2 - Rainy and Cold:")
    print(suggest_activity(5, 10, 15))  # Rainy, cold, moderate wind
    print("\n" + "-" * 50 + "\n")

    # Test Case 3: Windy but warm
    print("Test 3 - Windy but Warm:")
    print(suggest_activity(0, 22, 25))  # No rain, warm, windy
    print("\n" + "-" * 50 + "\n")

    # Test Case 4: Cold but dry
    print("Test 4 - Cold but Dry:")
    print(suggest_activity(0, 12, 15))  # No rain, cold, light wind
    print("\n" + "-" * 50 + "\n")

    # Test Case 5: Light rain but warm
    print("Test 5 - Light Rain but Warm:")
    print(suggest_activity(2, 20, 10))  # Light rain, warm, light wind
    print("\n" + "-" * 50 + "\n")

    # Test Case 6: Very windy and cold
    print("Test 6 - Very Windy and Cold:")
    print(suggest_activity(0, 8, 30))  # No rain, very cold, very windy


# Additional utility function for interactive testing
def interactive_weather_check():
    """Allow users to input their own weather conditions"""
    print("\n=== INTERACTIVE WEATHER CHECK ===")
    try:
        precip = float(input("Enter precipitation (mm/h): "))
        temp = float(input("Enter temperature (°C): "))
        wind = float(input("Enter wind speed (km/h): "))

        print("\n" + "=" * 50)
        print(suggest_activity(precip, temp, wind))
        print("=" * 50)

    except ValueError:
        print("Please enter valid numerical values!")


# Execute the demonstration
if __name__ == "__main__":
    demonstrate_activity_suggestions()

    # Uncomment the line below for interactive testing
    # interactive_weather_check()