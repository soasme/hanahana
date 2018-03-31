from flask import Flask, url_for, redirect

def create_app(config):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_envvar(config)

    from hana.core import db
    db.init_app(app)

    from hana.auth.app import init_app as init_auth
    init_auth(app)

    from hana.spa.app import init_app as init_spa
    init_spa(app)

    @app.before_first_request
    def start_instance():
        import hana.auth.models
        import hana.hana.models
        db.create_all()

    @app.route('/')
    def index():
        return redirect(url_for('spa.index'))

    return app
