import threading

_thread_local = threading.local()

def get_current_request():
    """Retourne la requête en cours depuis le thread local."""
    return getattr(_thread_local, 'request', None)

class CurrentRequestMiddleware:
    """Stocke la requête actuelle dans le thread local pour être accessible ailleurs."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_local.request = request
        response = self.get_response(request)
        return response