import hashlib
import time

from shared import cache
from config import cfg
from core import log


class RateLimiter:
    def __init__(self, max_attempts=5, window_seconds=300):
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds

    def _normalize_identifier(self, identifier):
        # Normalize and hash the identifier to ensure consistency and privacy
        normalized = identifier.strip().lower()
        return hashlib.sha256(normalized.encode()).hexdigest()

    def _get_attempts_cache_key(self, identifier):
        normalized_identifier = self._normalize_identifier(identifier)
        return f"{cfg.application}:rate_limit:{normalized_identifier}"

    def is_allowed_attempt(self, identifier):
        cache_key = self._get_attempts_cache_key(identifier)
        attempts = cache.get(cache_key) or []
        current_time = time.time()
        attempts = [
            attempt
            for attempt in attempts
            if current_time - attempt < self.window_seconds
        ]

        if len(attempts) >= self.max_attempts:
            log.warning(f"Rate limit exceeded for {identifier}")
            return False
        return True

    def record_failed_attempt(self, identifier):
        cache_key = self._get_attempts_cache_key(identifier)
        attempts = cache.get(cache_key) or []

        attempts.append(time.time())
        try:
            cache.set(cache_key, attempts, timeout=self.window_seconds)
        except Exception as e:
            log.error(f"Failed to record rate limit attempt for {identifier}: {e}")


# Initialize a single instance of RateLimiter
rate_limiter = RateLimiter()
