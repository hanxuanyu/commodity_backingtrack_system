from application import app


@app.errorhandler(404)
def error404(e):
    return "404 not found"
