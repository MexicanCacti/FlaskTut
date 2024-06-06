import os

from flask import Flask

def create_app(test_config =None): #factory fun to create & config instance of Flask app
    #create & config app
    app = Flask(__name__, instance_relative_config=True)
    #__name__ :name of current module (root path of app)
    #instance_relative_config=True: config files relative to instance folder 
    app.config.from_mapping( # sets default config values
        SECRET_KEY='dev', # secret key to kepp data safe (used by Flask & Ext)
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'), #Specifies path to SQLite database, app.instance_path path to instance folder
    )

    if test_config is None:
        #load instance config when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load test config if passed in
        app.config.from_mapping(test_config)
    
    #ensure instance folder exists
    try:
        os.makedirs(app.instance_path) # ensures instance folder exists, create if necesary
    except OSError: #if exists will raise error, will make sure to ignore
        pass
    
    # define the page
    @app.route('/hello') #defines route for URL path '/hello'
    def hello():
        return "Sup, World!"

    from . import db #imports db module from current package
    db.init_app(app) #calls init_app function from db module.
    
    from . import auth
    app.register_blueprint(auth.py)

    return app  # return app isntance cereated & config'd by create_app func