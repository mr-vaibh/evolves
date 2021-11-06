from django.core.exceptions import ValidationError
import os

def validate_video_size(value):
    filesize= value.size
    
    if filesize > 52428800:
        raise ValidationError(f"The maximum file size that can be uploaded is 50MB")
    else:
        return value


def validate_video_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4', '.mov', '.avi', '.wmv', '.mkv', '.webm']
    if not ext.lower() in valid_extensions:
        raise ValidationError(f'Unsupported file extension. Choose in {valid_extensions}')
