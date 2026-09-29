from django.http import HttpResponse, JsonResponse
from django.urls import path


def home(request):
    return HttpResponse(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>MES</title>
        </head>
        <body>
            <h1>Manufacturing Execution System</h1>
            <p>MES is running.</p>
            <p>Django foundation: OK</p>
        </body>
        </html>
        """
    )


def health_check(request):
    return JsonResponse(
        {
            "status": "ok",
            "service": "MES",
        }
    )


urlpatterns = [
    path("", home, name="home"),
    path("admin/", __import__("django.contrib.admin").contrib.admin.site.urls),
    path("health/", health_check, name="health"),
]
