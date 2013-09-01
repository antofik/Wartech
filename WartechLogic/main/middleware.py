from django.conf import settings


class CooklessMiddleware(object):
    def process_request(self, request):
        if settings.SESSION_COOKIE_NAME not in request.COOKIES:
            if request.method == "GET" and settings.SESSION_COOKIE_NAME in request.GET:
                request.COOKIES[settings.SESSION_COOKIE_NAME] = request.GET[settings.SESSION_COOKIE_NAME]
            elif request.method == "POST" and settings.SESSION_COOKIE_NAME in request.POST:
                request.COOKIES[settings.SESSION_COOKIE_NAME] = request.POST[settings.SESSION_COOKIE_NAME]
