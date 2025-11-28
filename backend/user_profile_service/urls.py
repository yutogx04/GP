from django.urls import path
from .views import MyProfileView, UploadPieceView, ListMyPiecesView

app_name = "user_profile_service"

urlpatterns = [
    path("me/", MyProfileView.as_view(), name="my-profile"),
    path("pieces/upload/", UploadPieceView.as_view(), name="upload-piece"),
    path("pieces/", ListMyPiecesView.as_view(), name="list-pieces"),
]
