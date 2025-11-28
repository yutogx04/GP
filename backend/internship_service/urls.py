from django.urls import path
from .views import CreateStageView, StudentStagesListView, StageDetailView, FinishStageView, CancelStageView

app_name = "internship_service"

urlpatterns = [
    path("create/", CreateStageView.as_view(), name="create-stage"),
    path("me/", StudentStagesListView.as_view(), name="student-stages"),
    path("<int:pk>/", StageDetailView.as_view(), name="stage-detail"),
    path("<int:pk>/finish/", FinishStageView.as_view(), name="stage-finish"),
    path("<int:pk>/cancel/", CancelStageView.as_view(), name="stage-cancel"),
]