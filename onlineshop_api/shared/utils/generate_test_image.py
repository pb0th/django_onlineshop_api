from PIL import Image
import io
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime 

def generate_test_image():
    test_image_prefix = "unit_testing_image_"
    # Create a valid in-memory image
    image = Image.new('RGB', (100, 100), color='red')
    image_io = io.BytesIO()
    image.save(image_io, format='JPEG')
    image_io.seek(0)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_image = SimpleUploadedFile(
            name=f'{test_image_prefix}_{timestamp}_test_image.jpg',
            content=image_io.read(),
            content_type='image/jpeg'
    )
    return test_image