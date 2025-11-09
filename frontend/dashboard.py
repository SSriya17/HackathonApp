"""
Complete Streamlit Dashboard for Telecom Complaints Analysis
This is a comprehensive, interactive dashboard with all requested features:
- Automatic categorization into 7 categories
- Interactive bar chart with clickable categories
- Expandable sections showing sample complaints, business goals, and PM recommendations
- Sidebar with CSV upload and AI chatbot
- Modern, visually appealing design
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objects import Figure
from typing import Dict, List, Optional, Tuple
import os
from io import StringIO

# Try to import OpenAI - support both old and new API
try:
    from openai import OpenAI
    OPENAI_NEW_API = True
except ImportError:
    try:
        import openai
        OPENAI_NEW_API = False
    except ImportError:
        OPENAI_NEW_API = None

# ============================================================================
# PAGE CONFIGURATION - Modern and friendly design
# ============================================================================
st.set_page_config(
    page_title="Telecom Complaints Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS FOR MODERN STYLING
# ============================================================================
st.markdown("""
    <style>
    /* Main title styling */
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Category card styling */
    .category-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    /* Metric cards */
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
    }
    
    /* Chat message styling */
    .user-message {
        background-color: #e3f2fd;
        padding: 0.75rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .bot-message {
        background-color: #f5f5f5;
        padding: 0.75rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
    }
    
    .stButton>button:hover {
        background-color: #1565c0;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# CATEGORIZATION LOGIC - 7 Categories with Keywords
# ============================================================================
CATEGORIES = {
    'Network/Service Problems': {
        'keywords': ['network', 'signal', 'outage', 'call drop', 'slow data', 'no service', 'connection', 'coverage'],
        'business_goal': 'Improve Network Quality',
        'pm_recommendation': """**Product Manager Action Items:**
1. **Network Infrastructure Audit**: Conduct a comprehensive review of network coverage maps and identify dead zones
2. **Real-time Monitoring**: Implement advanced network monitoring tools to detect and resolve outages faster
3. **Customer Communication**: Set up automated alerts for network issues and estimated resolution times
4. **Quality Metrics**: Track call drop rates, data speeds, and service availability by region
5. **Infrastructure Investment**: Prioritize network upgrades in high-complaint areas"""
    },
    'Billing and Charges': {
        'keywords': ['bill', 'charge', 'overcharged', 'fee', 'refund', 'payment issues', 'billing', 'cost'],
        'business_goal': 'Improve Billing Transparency',
        'pm_recommendation': """**Product Manager Action Items:**
1. **Bill Clarity Initiative**: Redesign bills with clear line-item breakdowns and explanations
2. **Proactive Notifications**: Send alerts before charges are applied, especially for unexpected fees
3. **Self-Service Portal**: Enable easy bill dispute and refund requests through the app
4. **Billing Analytics**: Identify patterns in billing complaints (specific fees, plan types, regions)
5. **Customer Education**: Create clear guides explaining common charges and how to avoid them"""
    },
    'Device/Account Issues': {
        'keywords': ['device', 'phone', 'sim', 'account locked', 'phone not received', 'upgrade', 'trade-ins', 'account'],
        'business_goal': 'Streamline Device/Account Management',
        'pm_recommendation': """**Product Manager Action Items:**
1. **Account Unlock Automation**: Reduce account lock times with automated verification processes
2. **Device Tracking**: Implement real-time shipment tracking for device orders
3. **Self-Service Tools**: Build in-app features for SIM activation, device upgrades, and account management
4. **Inventory Management**: Improve coordination between sales, inventory, and shipping teams
5. **Customer Onboarding**: Create smoother device setup and account activation workflows"""
    },
    'Customer Support Experience': {
        'keywords': ['support', 'agent', 'customer service', 'rudeness', 'slow response', 'credit', 'promo', 'unresolved case'],
        'business_goal': 'Enhance Customer Support',
        'pm_recommendation': """**Product Manager Action Items:**
1. **Agent Training Program**: Implement comprehensive training on empathy, problem-solving, and product knowledge
2. **Response Time SLA**: Set and monitor strict response time targets (e.g., < 2 hours for urgent issues)
3. **Case Management System**: Upgrade to a unified system that tracks cases from start to resolution
4. **Empowerment Tools**: Give agents more authority to issue credits, refunds, and resolve issues without escalation
5. **Customer Feedback Loop**: Implement post-interaction surveys and use feedback to improve training"""
    },
    'Plan/Service Features': {
        'keywords': ['plan', 'feature', 'throttling', 'eligibility', 'upgrade', 'downgrade', 'service'],
        'business_goal': 'Optimize Service Offerings',
        'pm_recommendation': """**Product Manager Action Items:**
1. **Plan Comparison Tool**: Build an interactive tool helping customers choose the right plan
2. **Feature Transparency**: Clearly communicate data limits, throttling policies, and feature availability
3. **Flexible Plans**: Introduce more flexible options for customers to upgrade/downgrade easily
4. **Usage Analytics**: Provide customers with detailed usage insights to optimize their plan choice
5. **Eligibility Automation**: Streamline eligibility checks for upgrades and special offers"""
    },
    'App/Online Experience': {
        'keywords': ['app', 'online', 'website', 'login', 'crash', 'bug', 'payment (in app)', 'digital'],
        'business_goal': 'Improve Digital Experience',
        'pm_recommendation': """**Product Manager Action Items:**
1. **Performance Optimization**: Reduce app load times and fix crashes through comprehensive testing
2. **User Experience Audit**: Conduct usability testing and redesign confusing flows
3. **Bug Tracking System**: Implement robust error tracking and prioritize fixes based on user impact
4. **Mobile-First Design**: Ensure all features work seamlessly on mobile devices
5. **Accessibility**: Ensure app meets WCAG standards for users with disabilities"""
    },
    'Security and Privacy': {
        'keywords': ['security', 'privacy', 'hack', 'fraud', 'leak', 'unauthorized access', 'breach'],
        'business_goal': 'Strengthen Security Measures',
        'pm_recommendation': """**Product Manager Action Items:**
1. **Security Audit**: Conduct comprehensive security review of all systems and data handling
2. **Multi-Factor Authentication**: Mandate MFA for all account access and sensitive operations
3. **Fraud Detection**: Implement AI-powered fraud detection and real-time alerts
4. **Privacy Controls**: Give customers granular control over data sharing and privacy settings
5. **Incident Response Plan**: Establish clear protocols for security incidents and customer communication"""
    }
}

def categorize_complaint(complaint_text: str) -> Tuple[str, str]:
    """
    Categorize a single complaint into one of the 7 categories.
    
    Args:
        complaint_text: The complaint text to categorize
        
    Returns:
        Tuple of (category_name, business_goal)
    """
    if pd.isna(complaint_text) or not complaint_text:
        return ('Uncategorized', 'Review Manually')
    
    text_lower = str(complaint_text).lower()
    
    # Check categories in priority order (most specific first)
    # Security and Privacy (most critical)
    for keyword in CATEGORIES['Security and Privacy']['keywords']:
        if keyword in text_lower:
            return ('Security and Privacy', CATEGORIES['Security and Privacy']['business_goal'])
    
    # App/Online Experience (specific context)
    for keyword in CATEGORIES['App/Online Experience']['keywords']:
        if keyword in text_lower:
            return ('App/Online Experience', CATEGORIES['App/Online Experience']['business_goal'])
    
    # Network/Service Problems
    for keyword in CATEGORIES['Network/Service Problems']['keywords']:
        if keyword in text_lower:
            return ('Network/Service Problems', CATEGORIES['Network/Service Problems']['business_goal'])
    
    # Billing and Charges
    for keyword in CATEGORIES['Billing and Charges']['keywords']:
        if keyword in text_lower:
            return ('Billing and Charges', CATEGORIES['Billing and Charges']['business_goal'])
    
    # Device/Account Issues
    for keyword in CATEGORIES['Device/Account Issues']['keywords']:
        if keyword in text_lower:
            return ('Device/Account Issues', CATEGORIES['Device/Account Issues']['business_goal'])
    
    # Customer Support Experience
    for keyword in CATEGORIES['Customer Support Experience']['keywords']:
        if keyword in text_lower:
            return ('Customer Support Experience', CATEGORIES['Customer Support Experience']['business_goal'])
    
    # Plan/Service Features
    for keyword in CATEGORIES['Plan/Service Features']['keywords']:
        if keyword in text_lower:
            return ('Plan/Service Features', CATEGORIES['Plan/Service Features']['business_goal'])
    
    # Default to uncategorized
    return ('Uncategorized', 'Review Manually')

def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process a DataFrame and add category and business_goal columns.
    
    Args:
        df: DataFrame with complaint data (must have 'Complaint Text' column)
        
    Returns:
        DataFrame with added 'category' and 'business_goal' columns
    """
    # Handle different possible column names
    complaint_col = None
    for col in df.columns:
        if 'complaint' in col.lower() or 'text' in col.lower():
            complaint_col = col
            break
    
    if complaint_col is None:
        st.error("❌ Could not find complaint text column. Please ensure your CSV has a column named 'Complaint Text' or similar.")
        return df
    
    # Create copies of the columns we need
    df = df.copy()
    df['category'] = df[complaint_col].apply(categorize_complaint).apply(lambda x: x[0])
    df['business_goal'] = df[complaint_col].apply(categorize_complaint).apply(lambda x: x[1])
    df['complaint_text'] = df[complaint_col]
    
    return df

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================
if 'data' not in st.session_state:
    st.session_state.data = None
if 'categorized_data' not in st.session_state:
    st.session_state.categorized_data = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

# ============================================================================
# SIDEBAR - Upload CSV and Chatbot
# ============================================================================
st.sidebar.title("⚙️ Dashboard Controls")

# CSV Upload Section
st.sidebar.markdown("---")
st.sidebar.header("📁 Upload CSV File")
uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file", 
    type=['csv'],
    help="Upload a CSV file with complaint data. Must include a 'Complaint Text' column."
)

if uploaded_file is not None:
    try:
        # Read the uploaded file
        df = pd.read_csv(uploaded_file)
        
        # Process and categorize
        with st.sidebar.spinner("🔄 Processing and categorizing complaints..."):
            categorized_df = process_dataframe(df)
            st.session_state.data = df
            st.session_state.categorized_data = categorized_df
        
        st.sidebar.success(f"✅ Successfully loaded {len(df)} complaints!")
        st.sidebar.info(f"📊 Found {len(categorized_df['category'].unique())} categories")
        
    except Exception as e:
        st.sidebar.error(f"❌ Error loading file: {str(e)}")

# AI Chatbot Section
st.sidebar.markdown("---")
st.sidebar.header("🤖 AI Assistant")

# OpenAI API Key Input
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password",
    help="Enter your OpenAI API key to enable the AI chatbot",
    value=st.session_state.get('openai_key', '')
)

if openai_api_key:
    st.session_state.openai_key = openai_api_key
    # Initialize OpenAI client based on API version
    if OPENAI_NEW_API:
        openai_client = OpenAI(api_key=openai_api_key)
    elif OPENAI_NEW_API is False:
        openai.api_key = openai_api_key
        openai_client = None
    else:
        openai_client = None
        st.sidebar.warning("⚠️ OpenAI library not installed. Install with: pip install openai")
else:
    openai_client = None

# Chat Interface
st.sidebar.markdown("**Ask me about the dashboard or get PM recommendations!**")

# Display chat history
chat_container = st.sidebar.container()
with chat_container:
    for i, message in enumerate(st.session_state.chat_history):
        if message['role'] == 'user':
            st.sidebar.markdown(f"**You:** {message['content']}")
        else:
            st.sidebar.markdown(f"**AI:** {message['content']}")

# Chat input
user_question = st.sidebar.text_input("Type your question here:", key="chat_input")

if st.sidebar.button("💬 Send", key="send_button"):
    if user_question and openai_api_key:
        if openai_client is None and OPENAI_NEW_API is None:
            st.sidebar.error("❌ OpenAI library not installed. Please install with: pip install openai")
        else:
            try:
                # Prepare context about the dashboard
                context = "You are an AI assistant helping Product Managers analyze telecom complaints. "
                if st.session_state.categorized_data is not None:
                    total = len(st.session_state.categorized_data)
                    category_counts = st.session_state.categorized_data['category'].value_counts().to_dict()
                    context += f"Current dashboard shows {total} complaints across {len(category_counts)} categories. "
                    context += f"Category breakdown: {category_counts}. "
                
                # Prepare messages
                messages = [
                    {"role": "system", "content": context + "Provide helpful, actionable advice for Product Managers."},
                    *[{"role": msg['role'], "content": msg['content']} for msg in st.session_state.chat_history],
                    {"role": "user", "content": user_question}
                ]
                
                # Call OpenAI API (support both old and new API)
                if OPENAI_NEW_API and openai_client:
                    response = openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        max_tokens=300,
                        temperature=0.7
                    )
                    ai_response = response.choices[0].message.content
                elif not OPENAI_NEW_API:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        max_tokens=300,
                        temperature=0.7
                    )
                    ai_response = response.choices[0].message.content
                else:
                    ai_response = "OpenAI API not properly configured."
                
                # Add to chat history
                st.session_state.chat_history.append({"role": "user", "content": user_question})
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                
                # Clear input and rerun
                st.rerun()
                
            except Exception as e:
                st.sidebar.error(f"❌ Error: {str(e)}")
    elif not openai_api_key:
        st.sidebar.warning("⚠️ Please enter your OpenAI API key first")
    elif not user_question:
        st.sidebar.warning("⚠️ Please enter a question")

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun()

# ============================================================================
# MAIN DASHBOARD CONTENT
# ============================================================================

# Title and Header
st.markdown('<h1 class="main-title">📊 Telecom Complaints Dashboard</h1>', unsafe_allow_html=True)
st.markdown("### Analyze and prioritize telecom complaints to drive product improvements")

# Check if data is loaded
if st.session_state.categorized_data is None:
    st.info("👆 **Please upload a CSV file using the sidebar to get started!**")
    st.markdown("""
    ### 📋 Expected CSV Format:
    - Your CSV should contain a column with complaint text (e.g., "Complaint Text")
    - The dashboard will automatically categorize each complaint into one of 7 categories
    - Once uploaded, you'll see interactive charts and detailed insights
    """)
    st.stop()

# Get the categorized data
df = st.session_state.categorized_data

# ============================================================================
# SUMMARY METRICS
# ============================================================================
st.markdown("---")
st.header("📈 Overview Metrics")

# Calculate summary statistics
total_complaints = len(df)
category_counts = df['category'].value_counts()
total_categories = len(category_counts)
top_category = category_counts.index[0] if len(category_counts) > 0 else "N/A"
top_category_count = category_counts.iloc[0] if len(category_counts) > 0 else 0

# Display metrics in columns
col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Total Complaints", f"{total_complaints:,}")
col2.metric("🏷️ Categories Found", total_categories)
col3.metric("🔝 Top Category", top_category)
col4.metric("📈 Top Category Count", f"{top_category_count:,}")

# ============================================================================
# INTERACTIVE BAR CHART
# ============================================================================
st.markdown("---")
st.header("📊 Complaints by Category - Interactive Chart")

# Prepare chart data
chart_data = []
for category in CATEGORIES.keys():
    count = len(df[df['category'] == category])
    if count > 0:  # Only include categories with complaints
        chart_data.append({
            'Category': category,
            'Count': count,
            'Business Goal': CATEGORIES[category]['business_goal']
        })

if chart_data:
    chart_df = pd.DataFrame(chart_data)
    
    # Create interactive bar chart with Plotly
    fig = px.bar(
        chart_df,
        x='Category',
        y='Count',
        color='Count',
        color_continuous_scale='Viridis',
        title='Click on any bar to see detailed information',
        hover_data=['Business Goal'],
        text='Count',
        labels={'Count': 'Number of Complaints', 'Category': 'Complaint Category'}
    )
    
    # Customize the chart appearance
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5,
        hovertemplate='<b>%{x}</b><br>Count: %{y}<br>Business Goal: %{customdata[0]}<extra></extra>'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        title_font_size=16
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True, key="main_chart")
    
    # Category selector based on chart interaction
    st.markdown("### 🎯 Select a Category to Explore")
    st.markdown("💡 **Tip:** Hover over the bars to see business goals. Select a category below to view detailed information, sample complaints, and PM recommendations.")
    
    # Highlight the selected category in the selector
    selected_category = st.selectbox(
        "Choose a category to see detailed information:",
        options=chart_df['Category'].tolist(),
        key="category_selector",
        index=0 if st.session_state.selected_category not in chart_df['Category'].tolist() else chart_df['Category'].tolist().index(st.session_state.selected_category) if st.session_state.selected_category else 0
    )
    
    # Visual indicator for selected category
    if selected_category:
        selected_count = chart_df[chart_df['Category'] == selected_category]['Count'].iloc[0]
        st.info(f"📌 **Selected:** {selected_category} ({selected_count} complaints) - Scroll down to see detailed information!")
    
    # Update session state
    st.session_state.selected_category = selected_category
    
else:
    st.warning("⚠️ No categorized complaints found. Please check your data.")

# ============================================================================
# EXPANDABLE CATEGORY DETAILS SECTION
# ============================================================================
if st.session_state.selected_category:
    st.markdown("---")
    st.header(f"🔍 Detailed View: {st.session_state.selected_category}")
    
    # Filter data for selected category
    category_df = df[df['category'] == st.session_state.selected_category]
    
    # Display category information in an expandable container
    with st.expander(f"📋 View Details for {st.session_state.selected_category}", expanded=True):
        # Business Goal
        st.subheader("🎯 Business Goal")
        business_goal = CATEGORIES[st.session_state.selected_category]['business_goal']
        st.info(f"**{business_goal}**")
        
        # Statistics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Complaints in Category", len(category_df))
        with col2:
            percentage = (len(category_df) / total_complaints * 100) if total_complaints > 0 else 0
            st.metric("Percentage of Total", f"{percentage:.1f}%")
        
        # Sample Complaints
        st.subheader("📝 Sample Complaints")
        st.markdown("Here are some example complaints from this category:")
        
        # Get sample complaints (up to 10)
        sample_complaints = category_df['complaint_text'].head(10).tolist()
        
        for idx, complaint in enumerate(sample_complaints, 1):
            st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 5px; margin: 0.5rem 0; border-left: 4px solid #1f77b4;">
                <strong>Complaint #{idx}:</strong><br>
                {complaint}
            </div>
            """, unsafe_allow_html=True)
        
        # Product Manager Recommendations
        st.subheader("💡 Product Manager Recommendations")
        pm_rec = CATEGORIES[st.session_state.selected_category]['pm_recommendation']
        st.markdown(pm_rec)
        
        # Action Items Summary
        st.markdown("---")
        st.markdown("### ✅ Quick Action Summary")
        st.success(f"""
        **Priority Actions for {st.session_state.selected_category}:**
        1. Review the {len(category_df)} complaints in this category
        2. Focus on the business goal: **{business_goal}**
        3. Implement the PM recommendations above
        4. Track improvements and measure impact
        """)

# ============================================================================
# ADDITIONAL INSIGHTS SECTION
# ============================================================================
st.markdown("---")
st.header("📊 Additional Insights")

# Category Distribution Pie Chart
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Category Distribution")
    if len(chart_data) > 0:
        pie_fig = px.pie(
            chart_df,
            values='Count',
            names='Category',
            title='Complaint Distribution by Category',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        pie_fig.update_traces(textposition='inside', textinfo='percent+label')
        pie_fig.update_layout(height=400)
        st.plotly_chart(pie_fig, use_container_width=True)

with col2:
    st.subheader("🎯 Business Goals Overview")
    # Create a summary of business goals
    goal_summary = []
    for category in CATEGORIES.keys():
        count = len(df[df['category'] == category])
        if count > 0:
            goal_summary.append({
                'Business Goal': CATEGORIES[category]['business_goal'],
                'Category': category,
                'Complaint Count': count
            })
    
    if goal_summary:
        goal_df = pd.DataFrame(goal_summary)
        st.dataframe(
            goal_df,
            use_container_width=True,
            hide_index=True
        )

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>📊 Telecom Complaints Dashboard</strong></p>
    <p>Powered by Streamlit | Designed for Product Managers</p>
    <p>Upload CSV files, explore categories, and get AI-powered insights!</p>
</div>
""", unsafe_allow_html=True)

