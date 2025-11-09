"""
Telecom Complaints Analytics Dashboard
Professional analytics platform for complaint data insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from backend.backend import ComplaintBackend

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="BridgeLens - Customer Satisfaction Analytics",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# =============================================================================
# CUSTOM STYLING - COHESIVE COLOR SCHEME
# =============================================================================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
/* Color Palette - ScaleAI Inspired */
:root {
    --primary: #6366f1;
    --secondary: #8b5cf6;
    --accent: #a78bfa;
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --bg-main: #0f172a;
    --bg-card: #1e293b;
    --bg-sidebar: #1e293b;
    --border: #334155;
}

/* Global Styles */
* {
    box-sizing: border-box;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    color: var(--text-primary);
    background-color: var(--bg-main) !important;
}

/* Main Container */
.main .block-container {
    background-color: var(--bg-main);
    padding: 2rem;
}

/* Typography - NO GRADIENTS, CONSISTENT SIZING */
h1 {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--border);
}

h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
}

/* Sidebar - ScaleAI Style */
section[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: var(--text-primary);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 1.5rem;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary);
}

/* Metric Cards */
.metric-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.2s ease;
}

.metric-card:hover {
    border-color: var(--primary);
    box-shadow: 0 4px 6px rgba(99, 102, 241, 0.3);
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 0.5rem;
}

.metric-label {
    color: var(--text-secondary);
    font-size: 0.875rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Buttons */
.stButton > button {
    background-color: var(--primary);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.625rem 1.25rem;
    font-weight: 600;
    font-size: 0.875rem;
    transition: all 0.2s ease;
    width: 100%;
}

.stButton > button:hover {
    background-color: #4f46e5;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4);
}

/* Selectbox & Multiselect */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background-color: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text-primary);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background-color: var(--bg-card);
    padding: 0.5rem;
    border-radius: 8px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--text-secondary);
    border-radius: 6px;
    padding: 0.75rem 1.5rem;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background-color: var(--primary);
    color: white;
}

/* Dataframe */
.dataframe {
    background-color: var(--bg-main);
    border: 1px solid var(--border);
    border-radius: 8px;
}

/* Dividers */
hr {
    border: none;
    height: 1px;
    background-color: var(--border);
    margin: 2rem 0;
}

/* Info Boxes */
.stInfo {
    background-color: rgba(99, 102, 241, 0.1);
    border-left: 4px solid var(--primary);
    border-radius: 6px;
    color: var(--text-primary);
}

/* Footer */
footer {
    display: none;
}

[data-testid="stDecoration"] {
    display: none;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-card);
}

::-webkit-scrollbar-thumb {
    background: var(--accent);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary);
}

/* Loading Spinner */
.stSpinner > div {
    border-color: var(--primary) transparent transparent transparent;
}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'overview'

# =============================================================================
# DATA LOADING
# =============================================================================
@st.cache_data(ttl=3600)
def load_backend_data():
    """Load and process backend data with caching."""
    with st.spinner("Loading analytics..."):
        backend = ComplaintBackend()
        backend.load_data(['data/dataset1.csv', 'data/dataset2.csv'])
        backend.process_data()
    return backend

backend = load_backend_data()
categorized_data = backend.get_categorized_data()
chart_data = backend.get_chart_data()
priority_df = backend.get_priority_ranking()
summary_stats = backend.get_summary_stats()
goal_mapping = backend.get_business_goal_mapping()

# =============================================================================
# SIDEBAR CONTROLS
# =============================================================================
with st.sidebar:
    # App Branding
    st.markdown("""
        <div style="padding: 1.5rem 0; border-bottom: 2px solid var(--border); margin-bottom: 2rem;">
            <h1 style="font-size: 1.75rem; font-weight: 700; color: var(--primary); margin-bottom: 0.5rem; text-align: center;">BridgeLens</h1>
            <p style="font-size: 0.875rem; color: var(--text-secondary); text-align: center; font-style: italic; margin: 0;">Customer satisfaction to product perfection</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## Navigation")
    
    view_options = {
        "Overview": "overview",
        "Analytics": "analytics",
        "Priority Matrix": "priority",
        "Category Details": "categories",
        "Business Goals": "goals"
    }
    
    selected_view = st.radio(
        "Select View",
        options=list(view_options.keys()),
        label_visibility="collapsed"
    )
    st.session_state.current_view = view_options[selected_view]
    
    st.markdown("---")
    st.markdown("## Filters")
    
    all_categories = chart_data['categories']
    
    # Simple multiselect dropdown for categories - starts with none selected
    selected_categories = st.multiselect(
        "Select Categories",
        options=all_categories,
        default=None,
        help="Choose which categories to include in the analysis"
    )
    
    if not selected_categories:
        selected_categories = all_categories
        st.info("Showing all categories")
    
    st.markdown("---")
    
    # Export Options
    st.markdown("## Export Data")
    if st.button("Download Priority Report", use_container_width=True):
        csv = priority_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="priority_report.csv",
            mime="text/csv",
            use_container_width=True
)

# =============================================================================
# HEADER
# =============================================================================
st.markdown("# Telecom Complaints Analytics")
st.markdown("**Professional insights for data-driven decision making**")

# =============================================================================
# MAIN CONTENT AREA
# =============================================================================

# OVERVIEW TAB
if st.session_state.current_view == 'overview':
    st.markdown("## Executive Summary")
    
    # Key Metrics
    metric_cols = st.columns(4)
    metrics = [
        ("Total Complaints", summary_stats['total_complaints'], f"{summary_stats['total_complaints']:,}"),
        ("Categories", summary_stats['total_categories'], str(summary_stats['total_categories'])),
        ("Top Category", priority_df.iloc[0]['category'] if len(priority_df) > 0 else "N/A", priority_df.iloc[0]['category'] if len(priority_df) > 0 else "N/A"),
        ("Top Count", priority_df.iloc[0]['count'] if len(priority_df) > 0 else 0, f"{priority_df.iloc[0]['count']:,}" if len(priority_df) > 0 else "0")
    ]
    
    for col, (label, value, display) in zip(metric_cols, metrics):
        with col:
            # Special handling for Top Category - smaller font size
            if label == "Top Category":
                st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 1.25rem; font-weight: 700; color: var(--primary); margin-bottom: 0.5rem;">{display}</div>
                        <div class="metric-label">{label}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{display}</div>
                        <div class="metric-label">{label}</div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Category Distribution Chart
    st.markdown("## Category Distribution")

    filtered_chart_data = {
        'categories': [cat for cat in chart_data['categories'] if cat in selected_categories],
        'counts': [chart_data['counts'][i] for i, cat in enumerate(chart_data['categories']) if cat in selected_categories],
        'business_goals': [chart_data['business_goals'][i] for i, cat in enumerate(chart_data['categories']) if cat in selected_categories]
    }

    chart_df = pd.DataFrame({
        'Category': filtered_chart_data['categories'],
        'Count': filtered_chart_data['counts'],
        'Business Goal': filtered_chart_data['business_goals']
    })

    # Create bar chart with ScaleAI colors
    fig = px.bar(
        chart_df,
        x='Category',
        y='Count',
        color='Count',
        color_continuous_scale=['#334155', '#6366f1', '#8b5cf6'],
        hover_data=['Business Goal'],
        text='Count',
        height=500
    )
    
    fig.update_traces(
        textposition="outside",
        marker_line_color='#1e293b',
        marker_line_width=1,
        textfont=dict(color='#f8fafc')
    )
    
    fig.update_layout(
        plot_bgcolor="#0f172a",
        paper_bgcolor="#0f172a",
        font=dict(color="#f8fafc", family="Inter", size=12),
        xaxis=dict(
            gridcolor="#334155",
            title=dict(font=dict(size=14, color="#cbd5e1")),
            tickfont=dict(color="#cbd5e1")
        ),
        yaxis=dict(
            gridcolor="#334155",
            title=dict(font=dict(size=14, color="#cbd5e1")),
            tickfont=dict(color="#cbd5e1")
        ),
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=40),
        coloraxis_colorbar=dict(
            title=dict(text="Count", font=dict(color="#cbd5e1")),
            tickfont=dict(color="#cbd5e1")
        )
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})

# ANALYTICS TAB
elif st.session_state.current_view == 'analytics':
    st.markdown("## Advanced Analytics")
    
    # Prepare filtered data for analytics
    filtered_chart_data = {
        'categories': [cat for cat in chart_data['categories'] if cat in selected_categories],
        'counts': [chart_data['counts'][i] for i, cat in enumerate(chart_data['categories']) if cat in selected_categories],
        'business_goals': [chart_data['business_goals'][i] for i, cat in enumerate(chart_data['categories']) if cat in selected_categories]
    }
    
    chart_df = pd.DataFrame({
        'Category': filtered_chart_data['categories'],
        'Count': filtered_chart_data['counts'],
        'Business Goal': filtered_chart_data['business_goals']
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie Chart
        st.markdown("### Distribution by Category")
        st.markdown("**💡 Tip:** Click on any category in the legend to filter the chart. Click again to show all categories.", unsafe_allow_html=True)
        
        pie_df = pd.DataFrame({
            'Category': filtered_chart_data['categories'],
            'Count': filtered_chart_data['counts']
        })
        
        # Use ScaleAI color palette
        colors = ['#6366f1', '#8b5cf6', '#a78bfa', '#c084fc', '#d946ef', '#ec4899', '#f472b6']
        
        fig_pie = px.pie(
            pie_df,
            values='Count',
            names='Category',
            hole=0.4,
            color_discrete_sequence=colors[:len(pie_df)]
        )
        
        fig_pie.update_layout(
            plot_bgcolor="#0f172a",
            paper_bgcolor="#0f172a",
            font=dict(color="#f8fafc", family="Inter", size=12),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05,
                font=dict(color="#cbd5e1", size=11),
                itemwidth=30,
                bgcolor="rgba(0,0,0,0)",
                bordercolor="rgba(0,0,0,0)"
            ),
            margin=dict(l=20, r=120, t=20, b=20)
        )
        
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': True})
    
    with col2:
        # Statistics Summary
        st.markdown("### Statistical Summary")
        
        stats_data = {
            'Metric': ['Mean', 'Median', 'Std Dev', 'Min', 'Max'],
            'Value': [
                chart_df['Count'].mean(),
                chart_df['Count'].median(),
                chart_df['Count'].std(),
                chart_df['Count'].min(),
                chart_df['Count'].max()
            ]
        }
        
        stats_df = pd.DataFrame(stats_data)
        stats_df['Value'] = stats_df['Value'].round(2)
        
        st.dataframe(
            stats_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Metric": st.column_config.TextColumn("Metric", width="medium"),
                "Value": st.column_config.NumberColumn("Value", format="%.2f")
            }
        )
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("### Quick Actions")
        if st.button("Refresh Analysis", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        if st.button("Generate Report", use_container_width=True):
            st.success("Report generation initiated")

# PRIORITY MATRIX TAB
elif st.session_state.current_view == 'priority':
    st.markdown("## Priority Ranking Matrix")
    st.markdown("**Actionable insights ranked by complaint volume**")
    
    filtered_priority = priority_df[priority_df['category'].isin(selected_categories)].copy()
    
    if len(filtered_priority) > 0:
        # Enhanced Priority Table
        st.dataframe(
            filtered_priority,
            use_container_width=True,
            hide_index=True,
            column_config={
                "category": st.column_config.TextColumn("Category", width="medium"),
                "count": st.column_config.NumberColumn("Count", format="%d"),
                "business_goal": st.column_config.TextColumn("Business Goal", width="large")
            }
        )
        
        # Priority Visualization
        st.markdown("### Priority Visualization")
        
        fig_priority = px.bar(
            filtered_priority,
            x='count',
            y='category',
            orientation='h',
            color='count',
            color_continuous_scale=['#334155', '#6366f1', '#8b5cf6'],
            text='count',
            height=max(400, len(filtered_priority) * 50)
        )
        
        fig_priority.update_traces(textposition="outside", textfont=dict(color='#f8fafc'))
        fig_priority.update_layout(
            plot_bgcolor="#0f172a",
            paper_bgcolor="#0f172a",
            font=dict(color="#f8fafc", family="Inter", size=12),
            xaxis=dict(
                title=dict(text="Complaint Count", font=dict(color="#cbd5e1")),
                gridcolor="#334155",
                tickfont=dict(color="#cbd5e1")
            ),
            yaxis=dict(
                title="",
                gridcolor="#334155",
                tickfont=dict(color="#cbd5e1")
            ),
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20),
            coloraxis_colorbar=dict(
                title=dict(text="Count", font=dict(color="#cbd5e1")),
                tickfont=dict(color="#cbd5e1")
            )
        )
        
        st.plotly_chart(fig_priority, use_container_width=True, config={
            'displayModeBar': True,
            'modeBarButtonsToRemove': [],
            'doubleClick': 'reset',
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'priority_visualization',
                'height': 500,
                'width': 700,
                'scale': 1
            }
        })
        st.caption("💡 Tip: Press the autoscale button to reset the zoom and go back to the default view.")
    else:
        st.info("No data available for selected categories")

# CATEGORY DETAILS TAB
elif st.session_state.current_view == 'categories':
    st.markdown("## Category Deep Dive")
    
    selected_category = st.selectbox(
        "Select Category",
        options=chart_data['categories'],
        help="Choose a category to view detailed breakdown"
    )
    
    if selected_category:
        category_data = backend.filter_by_category(selected_category)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            # Display Total Complaints with box like Category and Business Goal - same structure
            st.markdown(f"""
                <div style="padding: 1rem; background: #1e293b; border-radius: 8px; border: 1px solid #334155;">
                    <div style="font-size: 0.875rem; color: #cbd5e1; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em;">Total Complaints</div>
                    <div style="font-size: 1rem; color: #6366f1; font-weight: 600; word-wrap: break-word; line-height: 1.4;">{len(category_data):,}</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            # Display category with proper wrapping
            st.markdown(f"""
                <div style="padding: 1rem; background: #1e293b; border-radius: 8px; border: 1px solid #334155;">
                    <div style="font-size: 0.875rem; color: #cbd5e1; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em;">Category</div>
                    <div style="font-size: 1rem; color: #f8fafc; font-weight: 600; word-wrap: break-word; line-height: 1.4;">{selected_category}</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            business_goal = category_data.iloc[0]['business_goal'] if len(category_data) > 0 else "N/A"
            st.markdown(f"""
                <div style="padding: 1rem; background: #1e293b; border-radius: 8px; border: 1px solid #334155;">
                    <div style="font-size: 0.875rem; color: #cbd5e1; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em;">Business Goal</div>
                    <div style="font-size: 0.9rem; color: #f8fafc; font-weight: 500; word-wrap: break-word; line-height: 1.4;">{business_goal}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if 'complaint_text' in category_data.columns:
            st.markdown("### Sample Complaints")
            
            with st.expander("View Complaints", expanded=True):
                for idx, complaint in enumerate(category_data['complaint_text'].head(20), 1):
                    st.markdown(f"""
                        <div style="padding: 1rem; margin: 0.5rem 0; background: #1e293b; border-radius: 8px; border-left: 3px solid #6366f1; color: #f8fafc;">
                            <strong style="color: #6366f1;">#{idx}</strong> <span style="color: #f8fafc;">{complaint}</span>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Complaint text not available in dataset")

# BUSINESS GOALS TAB
elif st.session_state.current_view == 'goals':
    st.markdown("## Business Goals Mapping")
    st.markdown("**Strategic alignment between categories and business objectives**")
    
    filtered_goals = goal_mapping[goal_mapping['category'].isin(selected_categories)].copy()
    
    st.dataframe(
        filtered_goals,
        use_container_width=True,
        hide_index=True,
        column_config={
            "category": st.column_config.TextColumn("Category", width="medium"),
            "business_goal": st.column_config.TextColumn("Business Goal", width="large")
        }
    )
    
    st.markdown("---")
    
    # Goal Summary
    st.markdown("### Goal Distribution")
    goal_counts = filtered_goals['business_goal'].value_counts()
    
    fig_goals = px.bar(
        x=goal_counts.index,
        y=goal_counts.values,
        labels={'x': 'Business Goal', 'y': 'Category Count'},
        color=goal_counts.values,
        color_continuous_scale=['#334155', '#6366f1', '#8b5cf6']
    )
    
    fig_goals.update_layout(
        plot_bgcolor="#0f172a",
        paper_bgcolor="#0f172a",
        font=dict(color="#f8fafc", family="Inter", size=12),
        xaxis=dict(gridcolor="#334155", tickfont=dict(color="#cbd5e1")),
        yaxis=dict(
            gridcolor="#334155",
            title=dict(font=dict(color="#cbd5e1")),
            tickfont=dict(color="#cbd5e1")
        ),
        showlegend=False,
        height=400,
        coloraxis_colorbar=dict(
            title=dict(text="Count", font=dict(color="#cbd5e1")),
            tickfont=dict(color="#cbd5e1")
        )
    )
    
    st.plotly_chart(fig_goals, use_container_width=True)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.875rem; padding: 2rem 0;">
    Telecom Complaints Analytics Platform | Built with Streamlit
</div>
""", unsafe_allow_html=True)
