from app import app, routes, constants

routes.init(app)

if __name__ == "__main__":
    app.run(debug=constants.PYTHON_ENV == "development", port=constants.PORT)
