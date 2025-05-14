from time import time
from collections import defaultdict
import random

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = defaultdict(list)

    def allow(self, user_id: int) -> bool:
        now = time()
        self.requests[user_id] = [t for t in self.requests[user_id] if now - t < self.time_window]
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        self.requests[user_id].append(now)
        return True

    @staticmethod
    async def random_delay(min_delay: float = 1.0, max_delay: float = 3.0):
        await asyncio.sleep(random.uniform(min_delay, max_delay))