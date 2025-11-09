"""
Data Loader Module
Handles loading and preprocessing of telecom complaints CSV files.
Supports multiple CSV formats and structures.
"""

import pandas as pd
from typing import Union, Optional, List
import os


class DataLoader:
    """Handles loading and preprocessing of complaint CSV files."""
    
    def __init__(self):
        self.complaint_column = None
    
    def load_csv(self, file_path: str) -> pd.DataFrame:
        """
        Load a CSV file and auto-detect the complaint column.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            DataFrame with standardized column names
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Auto-detect complaint column
        self.complaint_column = self._detect_complaint_column(df)
        
        # Standardize column name
        if self.complaint_column and self.complaint_column != 'complaint_text':
            df = df.rename(columns={self.complaint_column: 'complaint_text'})
        
        return df
    
    def _detect_complaint_column(self, df: pd.DataFrame) -> Optional[str]:
        """
        Auto-detect the complaint text column from common names.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Name of the complaint column or None
        """
        # Common column name variations
        common_names = [
            'Customer Complaint',
            'Complaint Text',
            'Complaint',
            'Text',
            'Description',
            'Issue',
            'Message',
            'complaint_text'
        ]
        
        # Check if any common name exists (case-insensitive)
        df_columns_lower = [col.lower() for col in df.columns]
        
        for name in common_names:
            if name in df.columns:
                return name
            # Case-insensitive check
            if name.lower() in df_columns_lower:
                idx = df_columns_lower.index(name.lower())
                return df.columns[idx]
        
        # If single column or first column looks like text, use it
        if len(df.columns) == 1:
            return df.columns[0]
        
        # If no header or can't detect, return None (will raise error)
        return None
    
    def load_multiple_csvs(self, file_paths: List[str]) -> pd.DataFrame:
        """
        Load multiple CSV files and combine them into a single DataFrame.
        
        Args:
            file_paths: List of paths to CSV files
            
        Returns:
            Combined DataFrame with all complaints
        """
        dataframes = []
        
        for file_path in file_paths:
            df = self.load_csv(file_path)
            # Add source file column for tracking
            df['source_file'] = os.path.basename(file_path)
            dataframes.append(df)
        
        # Combine all dataframes
        combined_df = pd.concat(dataframes, ignore_index=True)
        
        return combined_df
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the loaded data (clean, remove nulls, etc.).
        
        Args:
            df: DataFrame with complaint data
            
        Returns:
            Cleaned DataFrame
        """
        df_clean = df.copy()
        
        # Remove rows with null complaint text
        if 'complaint_text' in df_clean.columns:
            df_clean = df_clean[df_clean['complaint_text'].notna()]
            df_clean = df_clean[df_clean['complaint_text'].str.strip() != '']
        
        # Reset index
        df_clean = df_clean.reset_index(drop=True)
        
        return df_clean

