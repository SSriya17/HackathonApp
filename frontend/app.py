"""
Streamlit Dashboard for Telecom Complaints
This is a complete example Streamlit app using the backend.
Copy this to your HackathonApp-main folder and customize as needed.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from backend.backend import ComplaintBackend

# Page configuration
st.set_page_config(
    page_title="Telecom Complaints Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Telecom Complaints Dashboard")
st.markdown("Categorize and analyze telecom complaints to help Product Managers prioritize improvements")

# Load data with caching
@st.cache_data
def load_complaint_data():
    """Load and process complaint data."""
    try:
        backend = ComplaintBackend()
        backend.load_data([
            'data/dataset1.csv',
            'data/dataset2.csv'
        ])
        backend.process_data()
        return backend
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Load data
with st.spinner("Loading and processing complaints..."):
    backend = load_complaint_data()

if backend is None:
    st.stop()

# Get data
categorized_data = backend.get_categorized_data()
chart_data = backend.get_chart_data()
priority_df = backend.get_priority_ranking()
summary_stats = backend.get_summary_stats()

# Sidebar filters
st.sidebar.header("Filters")
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=chart_data['categories'],
    default=chart_data['categories']
)

# Filter data based on selection
if selected_categories:
    filtered_data = categorized_data[categorized_data['category'].isin(selected_categories)]
else:
    filtered_data = categorized_data

# Main metrics
st.header("📈 Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Complaints", summary_stats['total_complaints'])
col2.metric("Categories", summary_stats['total_categories'])
col3.metric("Top Category", priority_df.iloc[0]['category'] if len(priority_df) > 0 else "N/A")
col4.metric("Top Category Count", priority_df.iloc[0]['count'] if len(priority_df) > 0 else 0)

# Bar Chart
st.header("📊 Complaints by Category")
if selected_categories:
    # Filter chart data
    filtered_chart_data = {
        'categories': [cat for cat in chart_data['categories'] if cat in selected_categories],
        'counts': [chart_data['counts'][i] for i, cat in enumerate(chart_data['categories']) if cat in selected_categories],
        'business_goals': [chart_data['business_goals'][i] for i, cat in enumerate(chart_data['categories']) if cat in selected_categories]
    }
else:
    filtered_chart_data = chart_data

# Create bar chart with Plotly
chart_df = pd.DataFrame({
    'Category': filtered_chart_data['categories'],
    'Count': filtered_chart_data['counts'],
    'Business Goal': filtered_chart_data['business_goals']
})

fig = px.bar(
    chart_df,
    x='Category',
    y='Count',
    color='Count',
    color_continuous_scale='Blues',
    title='Complaint Count by Category',
    hover_data=['Business Goal'],
    text='Count'
)
fig.update_traces(texttemplate='%{text}', textposition='outside')
fig.update_layout(
    xaxis_tickangle=-45,
    height=500,
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)

# Priority Ranking Table
st.header("🎯 Priority Ranking for Product Managers")
st.markdown("**Ranked by complaint count - highest priority issues at the top**")

# Display priority table
priority_display = priority_df.copy()
priority_display = priority_display[priority_display['category'].isin(selected_categories)] if selected_categories else priority_display

st.dataframe(
    priority_display,
    use_container_width=True,
    hide_index=True
)

# Business Goals Summary
st.header("🎯 Business Goals Linked to Categories")
st.markdown("Each category is linked to a business goal to help prioritize improvements")

goal_mapping = backend.get_business_goal_mapping()
if selected_categories:
    goal_mapping = goal_mapping[goal_mapping['category'].isin(selected_categories)]

st.dataframe(
    goal_mapping,
    use_container_width=True,
    hide_index=True
)

# Category Details
st.header("📋 Category Breakdown")
selected_category = st.selectbox(
    "Select a category to view details",
    options=chart_data['categories']
)

if selected_category:
    category_data = backend.filter_by_category(selected_category)
    st.subheader(f"Complaints in {selected_category}")
    st.write(f"**Total:** {len(category_data)} complaints")
    st.write(f"**Business Goal:** {category_data.iloc[0]['business_goal'] if len(category_data) > 0 else 'N/A'}")
    
    # Show sample complaints
    if 'complaint_text' in category_data.columns:
        st.subheader("Sample Complaints")
        sample_complaints = category_data['complaint_text'].head(10)
        for idx, complaint in enumerate(sample_complaints, 1):
            st.write(f"{idx}. {complaint}")

# Footer
st.markdown("---")
st.markdown("**Dashboard created for Product Managers to prioritize improvements based on complaint analysis**")

