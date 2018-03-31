from uuid import uuid4
from functools import wraps

from flask import url_for, redirect, request
from flask import g, session
from werkzeug.local import LocalProxy

from authlib.client.apps import register_apps
from authlib.flask.oauth2 import ResourceProtector, current_token

from hana.core import db
from .core import oauth, authorization_server
from .models import User, Client, Token, ClientCredentialsGrant


SESSION_ID = 'sid'


def login(user, permanent=True):
    session[SESSION_ID] = user.id
    session.permanent = permanent
    g.current_user = user


def logout():
    if SESSION_ID in session:
        del session[SESSION_ID]


def generate_token():
    return uuid4().hex + uuid4().hex


def get_current_user():
    user = getattr(g, 'current_user', None)
    if user:
        return user

    sid = session.get(SESSION_ID)
    if not sid:
        return None

    user = User.query.get(sid)
    if not user:
        logout()
        return None

    g.current_user = user
    return user


current_user = LocalProxy(get_current_user)


def require_login(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user:
            url = url_for('auth.login', next=request.path)
            return redirect(url)

        return f(*args, **kwargs)

    return decorated


from authlib.flask.oauth2.sqla import (
    create_query_client_func,
    create_save_token_func
)
from authlib.flask.oauth2.sqla import create_bearer_token_validator

query_client = create_query_client_func(db.session, Client)
save_token = create_save_token_func(db.session, Token)

BearerTokenValidator = create_bearer_token_validator(db.session, Token)
ResourceProtector.register_token_validator(BearerTokenValidator())

require_oauth = ResourceProtector()

def require_auth(f):
    @wraps(f)
    def _(*args, **kwargs):
        if SESSION_ID not in session:
            url = url_for('auth.login', next=request.path)
            return redirect(url)
        return f(*args, **kwargs)
    return _

def init_app(app):
    oauth.init_app(app)
    register_apps(oauth, ['github'])

    authorization_server.init_app(
        app, query_client=query_client, save_token=save_token
    )
    authorization_server.register_grant_endpoint(ClientCredentialsGrant)

    from .controllers import auth

    app.register_blueprint(auth)
