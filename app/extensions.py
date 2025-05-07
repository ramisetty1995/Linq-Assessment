from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
limiter = Limiter(key_func=get_remote_address)

# Retry for Outbound Requests
retry_strategy = Retry(
    total=3,                # Total no of retries
    backoff_factor=1,       # backoff factor (1, 2, 4 seconds)
    status_forcelist=[500, 502, 503, 504],  # HTTP status codes to retry
)
adapter = HTTPAdapter(max_retries=retry_strategy)

# HTTP Session with Retry and Timeout
session = requests.Session()
session.mount("http://", adapter)
session.mount("https://", adapter)