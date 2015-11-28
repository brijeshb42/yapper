"""Create application instance using application factory."""
import os

import yapper as application

env = os.getenv('FLASK_CONFIG')

if env is None or env not in ["test", "prod"]:
    env = "dev"

app = application.create_app(env)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
