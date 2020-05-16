# from flask_blog import app
from flask_blog import create_app

if __name__ == "__main__":
    app = create_app()
#    app = create_app('flask_blog.config')
    app.run()