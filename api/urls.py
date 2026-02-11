from django.urls import path
from api.views.rag_views import AskView
from api.views.system_views import SystemStatusView, HealthCheckView

urlpatterns = [
    path("v1/ask", AskView.as_view()),
    path("v1/system/status", SystemStatusView.as_view()),
    path("v1/system/health-check", HealthCheckView.as_view()),
]


app_name = "api"
