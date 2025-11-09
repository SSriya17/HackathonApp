"""
Example usage of the Complaint Backend
This file demonstrates how to use the backend in your Streamlit dashboard.
"""

from backend.backend import ComplaintBackend

# Example 1: Basic usage
def example_basic():
    """Basic usage example."""
    # Initialize backend
    backend = ComplaintBackend()
    
    # Load data from one or more CSV files
    backend.load_data([
        'data/dataset1.csv',
        'data/dataset2.csv'
    ])
    
    # Process and categorize data
    backend.process_data()
    
    # Get chart data for visualization
    chart_data = backend.get_chart_data()
    print("Categories:", chart_data['categories'])
    print("Counts:", chart_data['counts'])
    print("Business Goals:", chart_data['business_goals'])
    
    # Get priority ranking for Product Managers
    priority_df = backend.get_priority_ranking()
    print("\nPriority Ranking:")
    print(priority_df)
    
    # Get summary statistics
    stats = backend.get_summary_stats()
    print("\nSummary Statistics:")
    print(f"Total Complaints: {stats['total_complaints']}")
    print(f"Total Categories: {stats['total_categories']}")


# Example 2: Quick initialization
def example_quick():
    """Quick initialization example."""
    from backend.backend import create_backend
    
    # Create backend with data loaded in one step
    backend = create_backend([
        'data/dataset1.csv',
        'data/dataset2.csv'
    ])
    
    # Get category counts
    category_counts = backend.get_category_counts()
    print(category_counts)


# Example 3: Streamlit integration
def example_streamlit():
    """Example of how to use in Streamlit."""
    import streamlit as st
    
    # Initialize backend (use st.cache_data for performance)
    @st.cache_data
    def load_complaint_data():
        backend = ComplaintBackend()
        backend.load_data([
            'data/dataset1.csv',
            'data/dataset2.csv'
        ])
        backend.process_data()
        return backend
    
    # Load data
    backend = load_complaint_data()
    
    # Get chart data
    chart_data = backend.get_chart_data()
    
    # Display bar chart (example)
    # st.bar_chart(
    #     pd.DataFrame({
    #         'Category': chart_data['categories'],
    #         'Count': chart_data['counts']
    #     })
    # )
    
    # Display priority ranking
    priority_df = backend.get_priority_ranking()
    st.dataframe(priority_df)


if __name__ == '__main__':
    print("Running basic example...")
    example_basic()

