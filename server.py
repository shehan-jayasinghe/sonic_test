from sanic import Sanic, response
from sanic.response import json
import asyncio

app = Sanic("MyApp")

# Middleware
@app.middleware('request')
async def print_request(request):
    print(f"Received request: {request.url}")

@app.middleware('response')
async def add_custom_header(request, response):
    response.headers["X-Custom-Header"] = "My Custom Header"

# Listeners
@app.listener('before_server_start')
async def before_start(app, loop):
    print("Server is starting...")

@app.listener('after_server_stop')
async def after_stop(app, loop):
    print("Server has stopped.")

# Handlers
@app.route("/")
async def handle_request(request):
    return json({"message": "Hello, world!"})

@app.route("/hello/<name>")
async def handle_greeting(request, name):
    return json({"message": f"Hello, {name}!"})

@app.route("/set_cookie")
async def set_cookie(request):
    response = json({"message": "Cookie set"})
    response.cookies["my_cookie"] = "cookie_value"
    return response

@app.route("/get_cookie")
async def get_cookie(request):
    cookie_value = request.cookies.get("my_cookie", "No cookie found")
    return json({"cookie_value": cookie_value})

@app.route("/background_task")
async def handle_background_task(request):
    app.add_task(background_task())
    return json({"message": "Background task started"})

async def background_task():
    print("Background task running...")
    await asyncio.sleep(5)
    print("Background task complete!")

# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)