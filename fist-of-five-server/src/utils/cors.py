class CORSMiddleware:
    def __init__(self, app, allowed_origin="http://localhost:4200"):
        self.app = app
        self.allowed_origin = allowed_origin

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            headers.append(("Access-Control-Allow-Origin", self.allowed_origin))
            headers.append(('Access-Control-Allow-Credentials', 'true'))
            headers.append(("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"))
            headers.append(("Access-Control-Allow-Headers", "Content-Type"))
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)
