Module plugins.auth.rate_limiter
================================

Classes
-------

`RateLimiter(max_attempts=5, window_seconds=300)`
:   

    ### Methods

    `is_allowed_attempt(self, identifier)`
    :

    `record_failed_attempt(self, identifier)`
    :