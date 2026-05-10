from pathlib import Path

APP_NAME = "Kitap Atlası"
TURKEY_CENTER = (39.9, 32.8)
DEFAULT_ZOOM = 6

DATA_URL = "https://raw.githubusercontent.com/your-user/your-repo/main/data/books.json"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CACHE_FILE = DATA_DIR / "cached_books.json"
