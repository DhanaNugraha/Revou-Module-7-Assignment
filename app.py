from auth.before_request import register_auth_middleware
from config.settings import create_app

app = create_app("config.local")

register_auth_middleware(app)  # Register middleware


