from whitenoise import WhiteNoise

import app
"""app = app()"""

application = WhiteNoise(app)
application.add_files('static/', prefix='static/')