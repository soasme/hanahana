def init_app(app):
    from .core import spa
    from . import controllers
    app.register_blueprint(spa)
