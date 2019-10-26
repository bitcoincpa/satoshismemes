from whitenoise import WhiteNoise

from app import app


application = WhiteNoise(app)
application.add_files('app/static/', prefix='app/static/')