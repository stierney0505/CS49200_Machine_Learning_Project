import os
import sys

from flask import Flask
from routes import client_routes, serverExampleRoutes
# import logging, ngrok
# from dotenv import load_dotenv

# load_dotenv()

app = Flask(__name__)
# Initialize our ngrok settings into Flask
# app.config.from_mapping(
#     BASE_URL="http://localhost:5000",
#     USE_NGROK=os.environ.get("USE_NGROK") == "True"
# )

# if app.config["USE_NGROK"] and os.environ.get("NGROK_AUTHTOKEN"):
#     # pyngrok will only be installed, and should only ever be initialized, in a dev environment
#     from pyngrok import ngrok

#     # Get the dev server port (defaults to 5000 for Flask, can be overridden with `--port`
#     # when starting the server
#     port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "5000"

#     # Open a ngrok tunnel to the dev server
#     public_url = ngrok.connect(port).public_url
#     print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{port}\"")

#     # Update any base URLs or webhooks to use the public ngrok URL
#     app.config["BASE_URL"] = public_url
#     # init_webhooks(public_url)

# # ... Initialize Blueprints and the rest of our app
@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


app.register_blueprint(client_routes.client_bp)
app.register_blueprint(serverExampleRoutes.serverExample_bp)




if __name__ == '__main__':
    app.run(debug=True)
