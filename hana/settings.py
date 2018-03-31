import os


DEBUG = bool(int(os.environ.get('DEBUG')))
SECRET_KEY = os.environ['SECRET_KEY']
OAUTH2_ACCESS_TOKEN_GENERATOR = 'hana.auth.app.generate_token'
OAUTH2_REFRESH_TOKEN_GENERATOR = 'hana.auth.app.generate_token'
GITHUB_CLIENT_ID = os.environ['GITHUB_CLIENT_ID']
GITHUB_CLIENT_SECRET = os.environ['GITHUB_CLIENT_SECRET']
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or os.environ['SQLALCHEMY_DATABASE_URI']
ALLOWED_USERS = [u for u in os.environ.get('HANA_ALLOWED_USERS').split() if u]
