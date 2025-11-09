# Telecom Complaints Backend

A complete backend system for categorizing and analyzing telecom complaints. This backend loads CSV files, categorizes complaints into 7 predefined categories using keyword matching, and provides data for visualization and prioritization.

## Files Structure

```
backend/
├── __init__.py              # Package initialization
├── backend.py               # Main backend service (import this in Streamlit)
├── data_loader.py           # Handles CSV loading and preprocessing
├── categorizer.py           # Categorizes complaints using keyword matching
├── data_processor.py        # Processes data for analytics and charts
├── requirements.txt         # Python dependencies
├── example_usage.py         # Usage examples
└── README.md                # This file
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage in Streamlit

```python
import streamlit as st
import pandas as pd
from backend.backend import ComplaintBackend

# Initialize backend
@st.cache_data
def load_data():
    backend = ComplaintBackend()
    backend.load_data([
        'data/dataset1.csv',
        'data/dataset2.csv'
    ])
    backend.process_data()
    return backend

# Load data
backend = load_data()

# Get chart data for bar chart
chart_data = backend.get_chart_data()

# Create bar chart
chart_df = pd.DataFrame({
    'Category': chart_data['categories'],
    'Count': chart_data['counts']
})

st.bar_chart(chart_df.set_index('Category'))

# Display priority ranking
priority_df = backend.get_priority_ranking()
st.dataframe(priority_df)
```

## API Reference

### ComplaintBackend

Main backend class that provides a unified interface.

#### Methods

- `load_data(file_paths)`: Load CSV file(s)
  - `file_paths`: Single path (str) or list of paths
  
- `categorize_data(df=None)`: Categorize complaints
  - Returns DataFrame with 'category' and 'business_goal' columns
  
- `process_data(df=None)`: Load, categorize, and process in one step
  
- `get_chart_data(df=None)`: Get data formatted for bar charts
  - Returns dict with 'categories', 'counts', 'business_goals'
  
- `get_category_counts(df=None)`: Get count per category
  - Returns DataFrame with 'category' and 'count' columns
  
- `get_priority_ranking(df=None)`: Get prioritized ranking for PMs
  - Returns DataFrame with 'priority_rank', 'category', 'count', 'business_goal'
  
- `get_summary_stats(df=None)`: Get summary statistics
  - Returns dict with total complaints, categories, and percentages
  
- `get_business_goal_mapping(df=None)`: Get category to business goal mapping
  
- `filter_by_category(category, df=None)`: Filter by category
  
- `filter_by_business_goal(business_goal, df=None)`: Filter by business goal

## Categories

The backend categorizes complaints into these 7 categories:

1. **Network/Service** → Business Goal: "Improve Network Quality and Reliability"
2. **Billing/Charges** → Business Goal: "Improve Billing Transparency and Accuracy"
3. **Device/Account** → Business Goal: "Streamline Device and Account Management"
4. **Customer Support** → Business Goal: "Enhance Customer Support Experience"
5. **Plan/Features** → Business Goal: "Optimize Service Plans and Features"
6. **App/Online** → Business Goal: "Improve Digital and Online Experience"
7. **Security/Privacy** → Business Goal: "Strengthen Security and Privacy Measures"

## CSV Format Support

The backend automatically detects complaint columns from common names:
- "Customer Complaint"
- "Complaint Text"
- "Complaint"
- "Text"
- "Description"
- "Issue"
- "Message"

If your CSV has a single column or no header, it will use the first column.

## Example Output

### Chart Data
```python
{
    'categories': ['Network/Service', 'Billing/Charges', ...],
    'counts': [150, 120, ...],
    'business_goals': ['Improve Network Quality...', 'Improve Billing...', ...]
}
```

### Priority Ranking DataFrame
```
   priority_rank          category  count                    business_goal
0              1   Network/Service    150  Improve Network Quality and...
1              2    Billing/Charges    120  Improve Billing Transparency...
...
```

## Notes

- The backend uses keyword matching for categorization (case-insensitive)
- Priority is determined by complaint count (highest count = highest priority)
- All data processing is cached-friendly for Streamlit performance

