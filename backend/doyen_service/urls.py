from django.urls import path
from .views import AssignmentOverrideCreateView

app_name = "doyen_service"

urlpatterns = [
    path("overrides/", AssignmentOverrideCreateView.as_view(), name="assignment-override"),
]
