def generate_file_upload_path(instance, filename, folder='uploads'):
    """Generate a reusable file path for uploaded files."""
    model_name = instance.__class__.__name__.lower()
    return f'{folder}/{model_name}/{filename}'
