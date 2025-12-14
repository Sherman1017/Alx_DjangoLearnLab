class SecurityHeadersMiddleware:
    """
    Custom middleware to add security headers to responses.
    This provides basic Content Security Policy (CSP) and other security headers.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Content Security Policy (CSP) headers
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' https://trusted.cdn.com; "
            "style-src 'self' 'unsafe-inline' https://trusted.cdn.com; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://trusted.cdn.com; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        
        # Other security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
