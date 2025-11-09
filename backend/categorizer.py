"""
Categorizer Module
Categorizes telecom complaints into 7 predefined categories using keyword matching.
"""

import pandas as pd
from typing import Dict, List


class ComplaintCategorizer:
    """Categorizes complaints using keyword-based matching."""
    
    def __init__(self):
        """Initialize with category definitions and business goals."""
        self.categories = {
            'Network/Service': {
                'keywords': [
                    'network', 'signal', 'outage', 'call drop', 'dropped call', 
                    'slow data', 'no service', 'service drop', 'connection', 
                    'coverage', 'speed', 'internet speed', 'data speed', 
                    'throttling', 'disconnect', 'disconnected', 'unavailable',
                    'down', 'offline', 'not working', 'poor service', 
                    'service quality', 'latency', 'lag', 'buffering'
                ],
                'business_goal': 'Improve Network Quality and Reliability'
            },
            'Billing/Charges': {
                'keywords': [
                    'bill', 'billing', 'charge', 'charged', 'overcharge', 
                    'overcharged', 'fee', 'fees', 'refund', 'payment', 
                    'cost', 'price', 'pricing', 'double charge', 'unauthorized charge',
                    'wrong charge', 'incorrect bill', 'billing error', 
                    'monthly bill', 'invoice', 'statement', 'money', 'cost'
                ],
                'business_goal': 'Improve Billing Transparency and Accuracy'
            },
            'Device/Account': {
                'keywords': [
                    'device', 'phone', 'sim', 'sim card', 'account', 
                    'account locked', 'locked account', 'phone not received', 
                    'device not received', 'upgrade device', 'trade-in', 
                    'trade in', 'activation', 'activate', 'device issue',
                    'phone issue', 'hardware', 'equipment', 'account access',
                    'cannot access', 'account problem', 'device problem'
                ],
                'business_goal': 'Streamline Device and Account Management'
            },
            'Customer Support': {
                'keywords': [
                    'support', 'agent', 'customer service', 'service rep', 
                    'representative', 'rude', 'rudeness', 'slow response', 
                    'response time', 'wait time', 'hold time', 'escalate', 
                    'escalation', 'unhelpful', 'not helpful', 'poor service',
                    'service quality', 'customer care', 'help', 'assistance',
                    'unresolved', 'not resolved', 'no solution', 'no help'
                ],
                'business_goal': 'Enhance Customer Support Experience'
            },
            'Plan/Features': {
                'keywords': [
                    'plan', 'feature', 'features', 'upgrade plan', 'downgrade',
                    'plan change', 'service plan', 'data plan', 'usage cap',
                    'data cap', 'limit', 'limits', 'promo', 'promotion', 
                    'promotional', 'offer', 'deal', 'eligibility', 'qualify',
                    'new feature', 'feature not working', 'plan feature',
                    'service feature', 'subscription', 'package'
                ],
                'business_goal': 'Optimize Service Plans and Features'
            },
            'App/Online': {
                'keywords': [
                    'app', 'application', 'online', 'website', 'web', 
                    'login', 'log in', 'crash', 'crashes', 'bug', 'bugs',
                    'error', 'not working', 'broken', 'freeze', 'frozen',
                    'slow', 'loading', 'interface', 'ui', 'user interface',
                    'mobile app', 'web portal', 'online portal', 'digital',
                    'platform', 'system', 'software'
                ],
                'business_goal': 'Improve Digital and Online Experience'
            },
            'Security/Privacy': {
                'keywords': [
                    'security', 'privacy', 'hack', 'hacked', 'breach', 
                    'data breach', 'leak', 'leaked', 'unauthorized access',
                    'fraud', 'fraudulent', 'scam', 'phishing', 'identity theft',
                    'personal information', 'data exposed', 'privacy violation',
                    'security issue', 'security problem', 'compromised',
                    'stolen', 'theft', 'unauthorized', 'suspicious'
                ],
                'business_goal': 'Strengthen Security and Privacy Measures'
            }
        }
    
    def categorize_complaint(self, complaint_text: str) -> Dict[str, str]:
        """
        Categorize a single complaint based on keyword matching.
        
        Args:
            complaint_text: The complaint text to categorize
            
        Returns:
            Dictionary with 'category' and 'business_goal' keys
        """
        if pd.isna(complaint_text) or not str(complaint_text).strip():
            return {
                'category': 'Uncategorized',
                'business_goal': 'Review Manually'
            }
        
        # Convert to lowercase for case-insensitive matching
        text_lower = str(complaint_text).lower()
        
        # Track matches with priority (more specific categories first)
        matches = {}
        
        # Check Security/Privacy first (highest priority)
        if self._has_keywords(text_lower, self.categories['Security/Privacy']['keywords']):
            return {
                'category': 'Security/Privacy',
                'business_goal': self.categories['Security/Privacy']['business_goal']
            }
        
        # Check App/Online (specific context)
        if self._has_keywords(text_lower, self.categories['App/Online']['keywords']):
            return {
                'category': 'App/Online',
                'business_goal': self.categories['App/Online']['business_goal']
            }
        
        # Check Network/Service
        if self._has_keywords(text_lower, self.categories['Network/Service']['keywords']):
            return {
                'category': 'Network/Service',
                'business_goal': self.categories['Network/Service']['business_goal']
            }
        
        # Check Billing/Charges
        if self._has_keywords(text_lower, self.categories['Billing/Charges']['keywords']):
            return {
                'category': 'Billing/Charges',
                'business_goal': self.categories['Billing/Charges']['business_goal']
            }
        
        # Check Customer Support
        if self._has_keywords(text_lower, self.categories['Customer Support']['keywords']):
            return {
                'category': 'Customer Support',
                'business_goal': self.categories['Customer Support']['business_goal']
            }
        
        # Check Plan/Features
        if self._has_keywords(text_lower, self.categories['Plan/Features']['keywords']):
            return {
                'category': 'Plan/Features',
                'business_goal': self.categories['Plan/Features']['business_goal']
            }
        
        # Check Device/Account
        if self._has_keywords(text_lower, self.categories['Device/Account']['keywords']):
            return {
                'category': 'Device/Account',
                'business_goal': self.categories['Device/Account']['business_goal']
            }
        
        # No match found
        return {
            'category': 'Uncategorized',
            'business_goal': 'Review Manually'
        }
    
    def _has_keywords(self, text: str, keywords: List[str]) -> bool:
        """
        Check if any keyword appears in the text.
        
        Args:
            text: Text to search in (lowercase)
            keywords: List of keywords to search for
            
        Returns:
            True if any keyword is found, False otherwise
        """
        for keyword in keywords:
            if keyword in text:
                return True
        return False
    
    def categorize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Categorize all complaints in a DataFrame.
        
        Args:
            df: DataFrame with 'complaint_text' column
            
        Returns:
            DataFrame with added 'category' and 'business_goal' columns
        """
        if 'complaint_text' not in df.columns:
            raise ValueError("DataFrame must have 'complaint_text' column")
        
        df_categorized = df.copy()
        
        # Apply categorization
        categorization_results = df_categorized['complaint_text'].apply(
            lambda x: self.categorize_complaint(x)
        )
        
        # Extract category and business_goal
        df_categorized['category'] = categorization_results.apply(lambda x: x['category'])
        df_categorized['business_goal'] = categorization_results.apply(lambda x: x['business_goal'])
        
        return df_categorized

