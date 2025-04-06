from middleware.before_request import auth_middleware
from config.settings import create_app

app = create_app("config.local")

auth_middleware(app)  # Register middleware


