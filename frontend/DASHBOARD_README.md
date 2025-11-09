# 📊 Telecom Complaints Dashboard - Complete Frontend

A comprehensive, interactive Streamlit dashboard for analyzing and categorizing telecom complaints. Perfect for hackathon demonstrations!

## ✨ Features

### 1. **Automatic Categorization**
- Automatically categorizes complaints into 7 categories:
  - Network/Service Problems
  - Billing and Charges
  - Device/Account Issues
  - Customer Support Experience
  - Plan/Service Features
  - App/Online Experience
  - Security and Privacy

### 2. **Interactive Bar Chart**
- Beautiful, color-coded bar chart showing complaint counts per category
- Hover to see business goals
- Click on categories to explore details

### 3. **Expandable Category Details**
When you select a category, you'll see:
- **Sample Complaint Texts**: Real examples from that category
- **Business Goal**: The strategic goal linked to that category
- **Product Manager Recommendations**: Actionable next steps and recommendations

### 4. **Sidebar Features**
- **📁 CSV Upload**: Upload new complaint files easily
- **🤖 AI Chatbot**: Ask questions about the dashboard and get PM recommendations
  - Requires OpenAI API key
  - Maintains chat history throughout the session
  - Provides context-aware responses

### 5. **Modern Design**
- Clean, professional interface
- Friendly color scheme
- Responsive layout
- Easy to navigate for hackathon judges

## 🚀 Quick Start

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the dashboard:**
```bash
streamlit run dashboard.py
```

The dashboard will open in your browser automatically!

### Using the Dashboard

1. **Upload a CSV file:**
   - Click "Upload CSV File" in the sidebar
   - Your CSV should have a column with complaint text (e.g., "Complaint Text")
   - The dashboard will automatically categorize all complaints

2. **Explore Categories:**
   - View the interactive bar chart
   - Select a category from the dropdown to see detailed information
   - Each category shows sample complaints, business goals, and PM recommendations

3. **Use the AI Chatbot:**
   - Enter your OpenAI API key in the sidebar
   - Ask questions like:
     - "What are the top 3 issues I should prioritize?"
     - "Give me recommendations for Network/Service Problems"
     - "What's the business goal for Billing complaints?"

## 📋 CSV Format

Your CSV file should have a column containing complaint text. The dashboard will automatically detect columns with names like:
- "Complaint Text"
- "complaint_text"
- "Complaint"
- "Text"

**Example CSV:**
```csv
Complaint Text
"I'm experiencing slow data speeds in my area"
"My bill was higher than expected this month"
"I can't log into the app"
```

## 🎯 For Hackathon Judges

This dashboard demonstrates:
- ✅ **Complete categorization system** with 7 categories
- ✅ **Interactive visualizations** with Plotly
- ✅ **User-friendly interface** with modern design
- ✅ **AI integration** for intelligent recommendations
- ✅ **Data upload capability** for real-time analysis
- ✅ **Product Manager insights** with actionable recommendations
- ✅ **Well-commented code** for easy understanding

## 🔧 Technical Details

- **Framework**: Streamlit
- **Visualization**: Plotly
- **AI**: OpenAI GPT-3.5-turbo (optional)
- **Data Processing**: Pandas
- **Categorization**: Keyword-based matching with priority ordering

## 📝 Notes

- The dashboard uses session state to maintain data and chat history
- All categorization happens automatically when you upload a CSV
- The AI chatbot requires an OpenAI API key (get one at https://platform.openai.com/)
- The dashboard is fully self-contained and doesn't require the backend modules

## 🎨 Customization

You can easily customize:
- Colors and styling in the CSS section
- Category keywords in the `CATEGORIES` dictionary
- PM recommendations for each category
- Chart appearance and layout

Enjoy analyzing complaints! 🚀

