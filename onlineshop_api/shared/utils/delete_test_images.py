import os
from django.conf import settings


def delete_test_images(path):
    test_image_prefix = "unit_testing_image_"
    uploads_dir = os.path.join(settings.MEDIA_ROOT, path)
    # Check if the directory exists
    if os.path.exists(uploads_dir):
        # Iterate over all files in the directory
        for filename in os.listdir(uploads_dir):
            if filename.startswith(test_image_prefix):
                # Construct the full file path
                file_path = os.path.join(uploads_dir, filename)
                # Delete the file
                os.remove(file_path)

            # Optionally remove the directory if it's empty after deletion
        if not os.listdir(uploads_dir):
            os.rmdir(uploads_dir)