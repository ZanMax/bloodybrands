DEVELOPER_MODE = True
PROJECT_NAME = "BLOODYBRANDS API"
PROJECT_DESCRIPTION = "Detect company which support war"
PROJECT_VERSION = "1.0"
API_PATH = "/api"
BACKEND_CORS_ORIGINS = ["*"]
ALLOW_METHODS = ['*']
ALLOW_HEADERS = ['*']
DB_HOST = "stoprusdb-do-user-148972-0.b.db.ondigitalocean.com"
DB_PORT = "25060"
DB_NAME = "bloodybrands"
DB_USER = "bloodybrands"
DB_PASS = "znKPkaGmCjujVr4n"
SQLALCHEMY_DATABASE_URI = (
    f"mysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)