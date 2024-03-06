from flask import Flask
from routes import client_routes, serverExampleRoutes

app = Flask(__name__)

app.register_blueprint(client_routes.client_bp)
app.register_blueprint(serverExampleRoutes.serverExample_bp)

if __name__ == '__main__':
    app.run(debug=True)