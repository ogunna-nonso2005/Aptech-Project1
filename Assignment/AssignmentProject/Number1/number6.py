def update_metrics(marketing_data, channel, new_data):
    """
    Updates metrics for a specific marketing channel by merging new data with existing metrics.

    Args:
        marketing_data (dict): The main dictionary containing all marketing channels data
        channel (str): The specific marketing channel to update
        new_data (dict): Dictionary containing metric updates (e.g., {'clicks': 50, 'impressions': 1000})

    Returns:
        dict: The updated marketing_data dictionary
    """
    # Input validation
    if not isinstance(marketing_data, dict):
        raise TypeError("marketing_data must be a dictionary")

    if not isinstance(new_data, dict):
        raise TypeError("new_data must be a dictionary")

    if not channel or not isinstance(channel, str):
        raise ValueError("channel must be a non-empty string")

    # If channel doesn't exist, create it with the new_data
    if channel not in marketing_data:
        marketing_data[channel] = new_data.copy()
        print(f"✓ Created new channel '{channel}' with data: {new_data}")
        return marketing_data

    # If channel exists, merge the new_data with existing metrics
    existing_metrics = marketing_data[channel]

    for metric, value in new_data.items():
        if metric in existing_metrics:
            # Update existing metric (you can choose to replace or add)
            print(f"✓ Updated '{channel}' - {metric}: {existing_metrics[metric]} → {value}")
            existing_metrics[metric] = value
        else:
            # Add new metric
            existing_metrics[metric] = value
            print(f"✓ Added new metric to '{channel}': {metric} = {value}")

    return marketing_data


def summarize_metrics(marketing_data):
    """
    Calculates total clicks and impressions across all marketing channels.

    Args:
        marketing_data (dict): The main dictionary containing all marketing channels data

    Returns:
        dict: A summary dictionary with total clicks, impressions, and other aggregated metrics
    """
    # Input validation
    if not isinstance(marketing_data, dict):
        raise TypeError("marketing_data must be a dictionary")

    # Initialize summary dictionary
    summary = {
        'total_clicks': 0,
        'total_impressions': 0,
        'total_conversions': 0,
        'channels_analyzed': 0,
        'metrics_found': set()
    }

    # Traverse through all channels and aggregate metrics
    for channel, metrics in marketing_data.items():
        if not isinstance(metrics, dict):
            print(f"⚠ Warning: Channel '{channel}' has invalid metrics format")
            continue

        summary['channels_analyzed'] += 1

        # Aggregate each metric
        for metric, value in metrics.items():
            summary['metrics_found'].add(metric)

            # Only sum numeric values
            if isinstance(value, (int, float)):
                if metric == 'clicks':
                    summary['total_clicks'] += value
                elif metric == 'impressions':
                    summary['total_impressions'] += value
                elif metric == 'conversions':
                    summary['total_conversions'] += value
                else:
                    # For any other numeric metrics, create dynamic totals
                    total_key = f'total_{metric}'
                    if total_key not in summary:
                        summary[total_key] = 0
                    summary[total_key] += value

    # Calculate derived metrics
    if summary['total_impressions'] > 0:
        summary['overall_ctr'] = (summary['total_clicks'] / summary['total_impressions']) * 100
    else:
        summary['overall_ctr'] = 0

    if summary['total_clicks'] > 0:
        summary['overall_conversion_rate'] = (summary['total_conversions'] / summary['total_clicks']) * 100
    else:
        summary['overall_conversion_rate'] = 0

    return summary


def display_marketing_data(marketing_data, title="Marketing Analytics Data"):
    """
    Displays the marketing data in a formatted way.

    Args:
        marketing_data (dict): The marketing data dictionary
        title (str): Display title
    """
    print(f"\n{title}")
    print("=" * 70)

    if not marketing_data:
        print("No marketing data available.")
        return

    for channel, metrics in marketing_data.items():
        print(f"\n📊 {channel.upper()}:")
        for metric, value in metrics.items():
            print(f"   • {metric}: {value:,}")

    print("=" * 70)


def display_summary(summary):
    """
    Displays the summary metrics in a formatted way.

    Args:
        summary (dict): The summary dictionary from summarize_metrics
    """
    print(f"\n📈 MARKETING PERFORMANCE SUMMARY")
    print("=" * 50)

    # Display core metrics
    core_metrics = ['total_clicks', 'total_impressions', 'total_conversions']
    for metric in core_metrics:
        if metric in summary:
            value = summary[metric]
            formatted_name = metric.replace('_', ' ').title()
            print(f"{formatted_name}: {value:,}")

    # Display calculated metrics
    print(f"\n📊 Performance Ratios:")
    if 'overall_ctr' in summary:
        print(f"Click-Through Rate (CTR): {summary['overall_ctr']:.2f}%")
    if 'overall_conversion_rate' in summary:
        print(f"Conversion Rate: {summary['overall_conversion_rate']:.2f}%")

    # Display additional information
    print(f"\n📋 Analysis Details:")
    print(f"Channels Analyzed: {summary['channels_analyzed']}")
    print(f"Metrics Tracked: {', '.join(sorted(summary['metrics_found']))}")

    # Display any additional totals
    additional_totals = [k for k in summary.keys() if k.startswith('total_') and k not in core_metrics]
    if additional_totals:
        print(f"\n➕ Additional Metrics:")
        for metric in additional_totals:
            formatted_name = metric.replace('total_', '').replace('_', ' ').title()
            print(f"{formatted_name}: {summary[metric]:,}")

    print("=" * 50)


def demonstrate_functionality():
    """
    Demonstrates the update_metrics and summarize_metrics functions with sample data.
    """
    print("MARKETING ANALYTICS PLATFORM")
    print("=" * 60)

    # Sample initial marketing data
    marketing_data = {
        'google_ads': {
            'clicks': 1500,
            'impressions': 50000,
            'conversions': 75,
            'cost': 3000
        },
        'facebook_ads': {
            'clicks': 800,
            'impressions': 25000,
            'conversions': 40,
            'cost': 1200
        },
        'email_marketing': {
            'clicks': 1200,
            'impressions': 15000,
            'conversions': 60,
            'opens': 8000
        }
    }

    # Display initial data
    display_marketing_data(marketing_data, "INITIAL MARKETING DATA")

    # Demonstrate update_metrics function
    print("\n" + "=" * 60)
    print("UPDATING MARKETING METRICS")
    print("=" * 60)

    # Update existing metrics for google_ads
    print("\n1. Updating existing metrics for 'google_ads':")
    update_metrics(marketing_data, 'google_ads', {'clicks': 1600, 'conversions': 80})

    # Add new metrics to facebook_ads
    print("\n2. Adding new metrics to 'facebook_ads':")
    update_metrics(marketing_data, 'facebook_ads', {'engagement': 450, 'shares': 120})

    # Create a new channel
    print("\n3. Creating new channel 'instagram_ads':")
    update_metrics(marketing_data, 'instagram_ads', {
        'clicks': 300,
        'impressions': 8000,
        'conversions': 15,
        'cost': 600
    })

    # Display updated data
    display_marketing_data(marketing_data, "UPDATED MARKETING DATA")

    # Demonstrate summarize_metrics function
    print("\n" + "=" * 60)
    print("SUMMARIZING METRICS ACROSS ALL CHANNELS")
    print("=" * 60)

    summary = summarize_metrics(marketing_data)
    display_summary(summary)

    return marketing_data, summary


def advanced_demonstration():
    """
    Shows more advanced usage scenarios and edge cases.
    """
    print("\n" + "=" * 60)
    print("ADVANCED DEMONSTRATION")
    print("=" * 60)

    # Create a fresh dataset for advanced demo
    advanced_data = {
        'search_ads': {
            'clicks': 2000,
            'impressions': 75000,
            'conversions': 100,
            'cost': 5000
        },
        'social_media': {
            'clicks': 1500,
            'impressions': 45000,
            'engagement': 1200
        }
    }

    display_marketing_data(advanced_data, "ADVANCED DEMONSTRATION DATA")

    # Batch updates
    print("\n📝 BATCH UPDATES:")
    updates = [
        ('search_ads', {'clicks': 2100, 'conversions': 110}),
        ('social_media', {'impressions': 48000, 'shares': 300}),
        ('content_marketing', {'clicks': 800, 'impressions': 12000, 'conversions': 25})
    ]

    for channel, new_data in updates:
        print(f"\nUpdating {channel}:")
        update_metrics(advanced_data, channel, new_data)

    display_marketing_data(advanced_data, "DATA AFTER BATCH UPDATES")

    # Final summary
    final_summary = summarize_metrics(advanced_data)
    display_summary(final_summary)


def error_handling_demonstration():
    """
    Demonstrates error handling and edge cases.
    """
    print("\n" + "=" * 60)
    print("ERROR HANDLING DEMONSTRATION")
    print("=" * 60)

    test_data = {'test_channel': {'clicks': 100}}

    try:
        # Invalid marketing_data type
        update_metrics("not_a_dict", "channel", {"clicks": 100})
    except TypeError as e:
        print(f"✓ Correctly handled error: {e}")

    try:
        # Invalid new_data type
        update_metrics(test_data, "channel", "not_a_dict")
    except TypeError as e:
        print(f"✓ Correctly handled error: {e}")

    try:
        # Empty channel name
        update_metrics(test_data, "", {"clicks": 100})
    except ValueError as e:
        print(f"✓ Correctly handled error: {e}")


# Main execution
if __name__ == "__main__":
    # Run main demonstration
    final_data, main_summary = demonstrate_functionality()

    # Run advanced demonstration
    advanced_demonstration()

    # Run error handling demonstration
    error_handling_demonstration()

    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("\nKey Features Implemented:")
    print("✓ update_metrics: Intelligently merges new data with existing channel metrics")
    print("✓ summarize_metrics: Calculates totals across all nested dictionaries")
    print("✓ Handles dynamic metric types and new channels")
    print("✓ Comprehensive error handling and input validation")
    print("✓ Formatted display for better readability")