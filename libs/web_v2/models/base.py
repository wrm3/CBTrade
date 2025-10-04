# Base Model Class for Clean Data Access
from libs.db_mysql.cbtrade.db_main import cbtrade_db as db
from datetime import datetime, timezone, date, timedelta
from typing import List, Dict, Optional, Any, Union


class BaseModel:
    """Base model providing clean data access patterns"""
    
    @staticmethod
    def execute_query(sql: str, title: str = None) -> List[Dict[str, Any]]:
        """Execute a query and return clean results"""
        try:
            results = db.seld(sql)
            return results if results else []
        except Exception as e:
            print(f"Query Error ({title}): {e}")
            print(f"SQL: {sql}")
            return []
    
    @staticmethod
    def get_date_range(period: str) -> tuple[date, date]:
        """Get date range for common periods"""
        today = date.today()
        
        if period == 'today':
            return today, today
        elif period == 'yesterday':
            yesterday = today - timedelta(days=1)
            return yesterday, yesterday
        elif period == 'week':
            # Start of current week (Monday)
            start_of_week = today - timedelta(days=today.weekday())
            return start_of_week, today
        elif period == 'month':
            # Start of current month
            start_of_month = today.replace(day=1)
            return start_of_month, today
        elif period == 'year':
            # Start of current year
            start_of_year = today.replace(month=1, day=1)
            return start_of_year, today
        elif period == 'last_7_days':
            start_date = today - timedelta(days=7)
            return start_date, today
        elif period == 'last_30_days':
            start_date = today - timedelta(days=30)
            return start_date, today
        else:
            return today, today
    
    @staticmethod
    def format_currency(amount: Union[float, int, None]) -> str:
        """Format currency values consistently"""
        if amount is None:
            return "$0.00"
        try:
            return f"${float(amount):,.2f}"
        except (ValueError, TypeError):
            return "$0.00"
    
    @staticmethod
    def format_percentage(pct: Union[float, int, None], decimals: int = 2) -> str:
        """Format percentage values consistently"""
        if pct is None:
            return "0.00%"
        try:
            return f"{float(pct):.{decimals}f}%"
        except (ValueError, TypeError):
            return "0.00%"
    
    @staticmethod
    def get_color_class(value: Union[float, int, None]) -> str:
        """Get CSS class for positive/negative values"""
        if value is None or value == 0:
            return "neutral"
        return "positive" if float(value) > 0 else "negative"
