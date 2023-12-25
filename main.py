from app import app
from app.configs import routes
from app.libs import constants

routes.init(app)

if __name__ == "__main__":
    app.run(debug=constants.PYTHON_ENV == "development", port=constants.PORT)
