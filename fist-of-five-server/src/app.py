import importlib
import os.path

from flask import Blueprint, Flask
from infrastructure import db, SQLALCHEMY_DATABASE_URI


def register_blueprints(app, package_name="exposition"):
    """
    Recursively registers all blueprints found in the given package.
    It expects each module (except __init__.py) to have an attribute 'blueprint'
    that is an instance of Flask's Blueprint.
    """
    # Get absolute path to the package
    package_path = os.path.join(os.path.dirname(__file__), package_name)
    # Walk through the package directory
    for root, dirs, files in os.walk(package_path):
        for filename in files:
            if filename.endswith(".py") and filename != "__init__.py":
                # Construct the full file path
                file_path = os.path.join(root, filename)
                # Determine module name relative to the src folder
                rel_path = os.path.relpath(file_path, os.path.dirname(__file__))
                module_name = rel_path.replace(os.path.sep, ".")[:-3]  # remove '.py'
                module = importlib.import_module(module_name)
                if hasattr(module, "blueprint"):
                    bp = getattr(module, "blueprint")
                    if isinstance(bp, Blueprint):
                        app.register_blueprint(bp)


def create_app():
    app = Flask(__name__)

    # Set up database configuration from the infrastructure layer.
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    register_blueprints(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)