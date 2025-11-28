from rest_framework import serializers
from .models import StoredFile

class StoredFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoredFile
        fields = ("id", "uploader", "file", "mime_type", "size", "tags", "created_at")
        read_only_fields = ("uploader", "size", "created_at")

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["uploader"] = request.user
        return super().create(validated_data)
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["file_url"] = instance.file.url
        return representation