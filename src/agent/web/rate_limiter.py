from typing import Dict, Optional
from datetime import datetime, timedelta
import time
from dataclasses import dataclass
import logging

@dataclass
class RateLimit:
    calls: int
    period: timedelta
    
class RateLimiter:
    def __init__(self):
        self.limits: Dict[str, RateLimit] = {
            "weather": RateLimit(60, timedelta(minutes=60)),  # 60 calls per hour
            "news": RateLimit(100, timedelta(minutes=60)),    # 100 calls per hour
            "wikipedia": RateLimit(200, timedelta(minutes=60)) # 200 calls per hour
        }
        self.call_history: Dict[str, list] = {}
        self.logger = logging.getLogger(__name__)
        
    def check_rate_limit(self, api_name: str) -> bool:
        """Check if we can make another API call"""
        if api_name not in self.limits:
            return True
            
        limit = self.limits[api_name]
        now = datetime.now()
        
        # Initialize history if needed
        if api_name not in self.call_history:
            self.call_history[api_name] = []
            
        # Clean old history
        self.call_history[api_name] = [
            ts for ts in self.call_history[api_name] 
            if now - ts < limit.period
        ]
        
        # Check if we're under the limit
        return len(self.call_history[api_name]) < limit.calls
        
    def add_call(self, api_name: str):
        """Record an API call"""
        if api_name in self.limits:
            self.call_history.setdefault(api_name, []).append(datetime.now())
            
    def wait_if_needed(self, api_name: str) -> Optional[float]:
        """Wait if we're over rate limit, return wait time if we had to wait"""
        if not self.check_rate_limit(api_name):
            # Calculate wait time
            limit = self.limits[api_name]
            oldest_call = min(self.call_history[api_name])
            now = datetime.now()
            wait_time = (oldest_call + limit.period - now).total_seconds()
            
            if wait_time > 0:
                self.logger.warning(f"Rate limit hit for {api_name}, waiting {wait_time:.1f}s")
                time.sleep(wait_time)
                return wait_time
                
        return None 