from flaskapp import create_app
from flaskapp.config import DevelopmentConfig

app = create_app(DevelopmentConfig)


# If we do not want to set all enviroment variables to run the server.
# We can wirte this code and run server using python command:
# python flaskblog.py
if __name__ == '__main__':
    app.run(debug=True)
