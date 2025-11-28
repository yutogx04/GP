from rest_framework import generics, permissions
from .models import StoredFile
from .serializers import StoredFileSerializer

class UploadFileView(generics.CreateAPIView):
    queryset = StoredFile.objects.all()
    serializer_class = StoredFileSerializer
    permission_classes = [permissions.IsAuthenticated]

class FileListView(generics.ListAPIView):
    queryset = StoredFile.objects.all()
    serializer_class = StoredFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return StoredFile.objects.filter(uploader=self.request.user).order_by("-created_at")