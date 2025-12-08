from django.core.exceptions import ValidationError
import os


def validate_file_size(value):
    """Validate file size is under 5MB"""
    max_size = 5 * 1024 * 1024  # 5MB
    if value.size > max_size:
        raise ValidationError(f'File size must be under 5MB. Current size: {value.size / (1024*1024):.2f}MB')


def validate_document_extension(value):
    """Validate file has allowed extension"""
    allowed_extensions = ['.pdf', '.doc', '.docx']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(f'File type not allowed. Allowed types: {", ".join(allowed_extensions)}')
