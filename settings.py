import os

BASE_API_URL = str(os.getenv("BASE_API_URL", "https://baas-dev.buildai.company/api/"))
HASH_CODES = str(os.getenv("HASH_CODES", "n8HgfIAGLskbEfZr"))  # Fetch as string, not list
