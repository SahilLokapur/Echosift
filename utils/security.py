def check_redirects(response):
    if len(response.history) > 3:
        return False, "Too many redirects (possible honeypot)"
    return True, "Safe"

def detect_rate_limit(status_code):
    return status_code in [429, 403]
