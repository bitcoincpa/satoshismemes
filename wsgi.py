from whitenoise import WhiteNoise

from app import app
app = app()

"""application = WhiteNoise(app)
application.add_files('static/', prefix='static/')"""