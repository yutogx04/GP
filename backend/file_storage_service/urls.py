from django.urls import path
from .views import UploadFileView, FileListView

app_name = "file_storage_service"

urlpatterns = [
    path("upload/", UploadFileView.as_view(), name="upload-file"),
    path("", FileListView.as_view(), name="list-files"),
]
