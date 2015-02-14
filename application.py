import os

import app as application

env = os.getenv('FLASK_CONFIG')

if env is None:
    env = 'dev'

app = application.create_app(env)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
