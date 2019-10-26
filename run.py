from app import app
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
     app.run(debug=True, port=app.config['PORT'], host='0.0.0.0')