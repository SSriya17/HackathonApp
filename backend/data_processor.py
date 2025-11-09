"""
Data Processor Module
Processes categorized complaint data for analytics and visualization.
"""

import pandas as pd
from typing import Dict, List, Tuple
import numpy as np


class DataProcessor:
    """Processes complaint data for analytics and chart generation."""
    
    def __init__(self):
        """Initialize the data processor."""
        self.category_order = [
            'Network/Service',
            'Billing/Charges',
            'Device/Account',
            'Customer Support',
            'Plan/Features',
            'App/Online',
            'Security/Privacy',
            'Uncategorized'
        ]
    
    def get_category_counts(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get count of complaints per category.
        
        Args:
            df: DataFrame with 'category' column
            
        Returns:
            DataFrame with category counts sorted by count (descending)
        """
        if 'category' not in df.columns:
            raise ValueError("DataFrame must have 'category' column")
        
        counts = df['category'].value_counts().reset_index()
        counts.columns = ['category', 'count']
        
        # Sort by predefined order, then by count
        counts['order'] = counts['category'].apply(
            lambda x: self.category_order.index(x) if x in self.category_order else 999
        )
        counts = counts.sort_values(['order', 'count'], ascending=[True, False])
        counts = counts.drop('order', axis=1)
        
        return counts
    
    def get_business_goal_counts(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get count of complaints per business goal.
        
        Args:
            df: DataFrame with 'business_goal' column
            
        Returns:
            DataFrame with business goal counts
        """
        if 'business_goal' not in df.columns:
            raise ValueError("DataFrame must have 'business_goal' column")
        
        counts = df['business_goal'].value_counts().reset_index()
        counts.columns = ['business_goal', 'count']
        counts = counts.sort_values('count', ascending=False)
        
        return counts
    
    def get_category_business_goal_mapping(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get mapping of categories to business goals with counts.
        
        Args:
            df: DataFrame with 'category' and 'business_goal' columns
            
        Returns:
            DataFrame with category, business_goal, and count
        """
        if 'category' not in df.columns or 'business_goal' not in df.columns:
            raise ValueError("DataFrame must have 'category' and 'business_goal' columns")
        
        mapping = df.groupby(['category', 'business_goal']).size().reset_index(name='count')
        mapping = mapping.sort_values('count', ascending=False)
        
        return mapping
    
    def get_priority_ranking(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get prioritized list of categories based on complaint counts.
        
        Args:
            df: DataFrame with categorized complaints
            
        Returns:
            DataFrame with category, count, business_goal, and priority rank
        """
        category_counts = self.get_category_counts(df)
        
        # Merge with business goals
        if 'business_goal' in df.columns:
            business_goals = df[['category', 'business_goal']].drop_duplicates()
            priority_df = category_counts.merge(business_goals, on='category', how='left')
        else:
            priority_df = category_counts.copy()
            priority_df['business_goal'] = 'N/A'
        
        # Add priority rank
        priority_df['priority_rank'] = range(1, len(priority_df) + 1)
        
        # Reorder columns
        priority_df = priority_df[['priority_rank', 'category', 'count', 'business_goal']]
        
        return priority_df
    
    def get_summary_stats(self, df: pd.DataFrame) -> Dict:
        """
        Get summary statistics about the complaints.
        
        Args:
            df: DataFrame with categorized complaints
            
        Returns:
            Dictionary with summary statistics
        """
        stats = {
            'total_complaints': len(df),
            'total_categories': df['category'].nunique() if 'category' in df.columns else 0,
            'categories': {}
        }
        
        if 'category' in df.columns:
            category_counts = self.get_category_counts(df)
            for _, row in category_counts.iterrows():
                stats['categories'][row['category']] = {
                    'count': int(row['count']),
                    'percentage': round((row['count'] / stats['total_complaints']) * 100, 2)
                }
        
        return stats
    
    def get_chart_data(self, df: pd.DataFrame) -> Dict:
        """
        Get formatted data ready for chart visualization.
        
        Args:
            df: DataFrame with categorized complaints
            
        Returns:
            Dictionary with chart-ready data
        """
        category_counts = self.get_category_counts(df)
        
        chart_data = {
            'categories': category_counts['category'].tolist(),
            'counts': category_counts['count'].tolist(),
            'business_goals': []
        }
        
        # Get business goals for each category
        if 'business_goal' in df.columns:
            category_goals = df[['category', 'business_goal']].drop_duplicates()
            goal_dict = dict(zip(category_goals['category'], category_goals['business_goal']))
            chart_data['business_goals'] = [
                goal_dict.get(cat, 'N/A') for cat in chart_data['categories']
            ]
        
        return chart_data
    
    def filter_by_category(self, df: pd.DataFrame, category: str) -> pd.DataFrame:
        """
        Filter complaints by category.
        
        Args:
            df: DataFrame with categorized complaints
            category: Category name to filter by
            
        Returns:
            Filtered DataFrame
        """
        if 'category' not in df.columns:
            raise ValueError("DataFrame must have 'category' column")
        
        return df[df['category'] == category].copy()
    
    def filter_by_business_goal(self, df: pd.DataFrame, business_goal: str) -> pd.DataFrame:
        """
        Filter complaints by business goal.
        
        Args:
            df: DataFrame with categorized complaints
            business_goal: Business goal to filter by
            
        Returns:
            Filtered DataFrame
        """
        if 'business_goal' not in df.columns:
            raise ValueError("DataFrame must have 'business_goal' column")
        
        return df[df['business_goal'] == business_goal].copy()

