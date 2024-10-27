import os

from app import create_app
#from flask import Flask

from flasgger import Swagger

app = create_app()
#app = Flask(__name__)

swagger = Swagger(app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)