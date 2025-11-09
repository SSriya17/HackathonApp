"""
Main Backend Service
Provides a unified interface for loading, categorizing, and processing complaint data.
This is the main file to import in your Streamlit dashboard.
"""

import pandas as pd
from typing import List, Dict, Optional, Union
import os

from .data_loader import DataLoader
from .categorizer import ComplaintCategorizer
from .data_processor import DataProcessor


class ComplaintBackend:
    """
    Main backend service for telecom complaints dashboard.
    
    Usage:
        backend = ComplaintBackend()
        backend.load_data(['path/to/dataset1.csv', 'path/to/dataset2.csv'])
        chart_data = backend.get_chart_data()
        priority_df = backend.get_priority_ranking()
    """
    
    def __init__(self):
        """Initialize the backend with all required components."""
        self.data_loader = DataLoader()
        self.categorizer = ComplaintCategorizer()
        self.processor = DataProcessor()
        self.data = None
        self.categorized_data = None
    
    def load_data(self, file_paths: Union[str, List[str]]) -> pd.DataFrame:
        """
        Load complaint data from CSV file(s).
        
        Args:
            file_paths: Single file path or list of file paths
            
        Returns:
            Loaded and preprocessed DataFrame
        """
        # Convert single path to list
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        
        # Load data
        self.data = self.data_loader.load_multiple_csvs(file_paths)
        
        # Preprocess
        self.data = self.data_loader.preprocess_data(self.data)
        
        return self.data
    
    def categorize_data(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Categorize complaints in the loaded data.
        
        Args:
            df: Optional DataFrame to categorize. If None, uses self.data
            
        Returns:
            DataFrame with added 'category' and 'business_goal' columns
        """
        if df is None:
            if self.data is None:
                raise ValueError("No data loaded. Call load_data() first.")
            df = self.data
        
        # Categorize
        self.categorized_data = self.categorizer.categorize_dataframe(df)
        
        return self.categorized_data
    
    def process_data(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Process and categorize data in one step.
        
        Args:
            df: Optional DataFrame to process. If None, uses self.data
            
        Returns:
            Categorized DataFrame
        """
        if df is None:
            if self.data is None:
                raise ValueError("No data loaded. Call load_data() first.")
            df = self.data
        
        # Categorize if not already done
        if self.categorized_data is None or df is not self.categorized_data:
            self.categorized_data = self.categorize_data(df)
        
        return self.categorized_data
    
    def get_chart_data(self, df: Optional[pd.DataFrame] = None) -> Dict:
        """
        Get data formatted for bar chart visualization.
        
        Args:
            df: Optional categorized DataFrame. If None, uses self.categorized_data
            
        Returns:
            Dictionary with 'categories', 'counts', and 'business_goals' lists
        """
        if df is None:
            if self.categorized_data is None:
                self.process_data()
            df = self.categorized_data
        
        return self.processor.get_chart_data(df)
    
    def get_category_counts(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Get count of complaints per category.
        
        Args:
            df: Optional categorized DataFrame. If None, uses self.categorized_data
            
        Returns:
            DataFrame with category and count columns
        """
        if df is None:
            if self.categorized_data is None:
                self.process_data()
            df = self.categorized_data
        
        return self.processor.get_category_counts(df)
    
    def get_priority_ranking(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Get prioritized ranking of categories for Product Managers.
        
        Args:
            df: Optional categorized DataFrame. If None, uses self.categorized_data
            
        Returns:
            DataFrame with priority_rank, category, count, and business_goal
        """
        if df is None:
            if self.categorized_data is None:
                self.process_data()
            df = self.categorized_data
        
        return self.processor.get_priority_ranking(df)
    
    def get_summary_stats(self, df: Optional[pd.DataFrame] = None) -> Dict:
        """
        Get summary statistics about the complaints.
        
        Args:
            df: Optional categorized DataFrame. If None, uses self.categorized_data
            
        Returns:
            Dictionary with summary statistics
        """
        if df is None:
            if self.categorized_data is None:
                self.process_data()
            df = self.categorized_data
        
        return self.processor.get_summary_stats(df)
    
    def get_business_goal_mapping(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Get mapping of categories to business goals.
        
        Args:
            df: Optional categorized DataFrame. If None, uses self.categorized_data
            
        Returns:
            DataFrame with category, business_goal, and count
        """
        if df is None:
            if self.categorized_data is None:
                self.process_data()
            df = self.categorized_data
        
        return self.processor.get_category_business_goal_mapping(df)
    
    def filter_by_category(self, category: str, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Filter complaints by category.
        
        Args:
            category: Category name to filter by
            df: Optional categorized DataFrame. If None, uses self.categorized_data
            
        Returns:
            Filtered DataFrame
        """
        if df is None:
            if self.categorized_data is None:
                self.process_data()
            df = self.categorized_data
        
        return self.processor.filter_by_category(df, category)
    
    def filter_by_business_goal(self, business_goal: str, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Filter complaints by business goal.
        
        Args:
            business_goal: Business goal to filter by
            df: Optional categorized DataFrame. If None, uses self.categorized_data
            
        Returns:
            Filtered DataFrame
        """
        if df is None:
            if self.categorized_data is None:
                self.process_data()
            df = self.categorized_data
        
        return self.processor.filter_by_business_goal(df, business_goal)
    
    def get_raw_data(self) -> Optional[pd.DataFrame]:
        """
        Get the raw loaded data (before categorization).
        
        Returns:
            Raw DataFrame or None if no data loaded
        """
        return self.data
    
    def get_categorized_data(self) -> Optional[pd.DataFrame]:
        """
        Get the categorized data.
        
        Returns:
            Categorized DataFrame or None if not processed
        """
        return self.categorized_data


# Convenience function for quick usage
def create_backend(file_paths: Union[str, List[str]]) -> ComplaintBackend:
    """
    Create and initialize a backend with data loaded.
    
    Args:
        file_paths: Single file path or list of file paths
        
    Returns:
        Initialized ComplaintBackend instance
    """
    backend = ComplaintBackend()
    backend.load_data(file_paths)
    backend.process_data()
    return backend

