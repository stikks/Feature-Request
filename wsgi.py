# # use to retrieve environment variable
import os

# import flask app
from app import app

# run application
if __name__ == '__main__':
    port = os.getenv('FLASK_PORT', 5000)
    app.run(port=port, host='0.0.0.0')
