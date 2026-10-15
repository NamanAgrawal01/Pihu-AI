app_instance = None


def set_app(app):
    global app_instance
    app_instance = app


def get_app():
    return app_instance