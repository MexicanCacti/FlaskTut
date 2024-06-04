import os

from flask import Flask

def create_app(test_config =None):
    #create & config app
    app = Flask(__name__, instance_relative_config=True) 
    app.config.from_mapping(
        SECRET_KEY='123',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        #load instance config when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load test config if passed in
        app.config.from_mapping(test_config)
    
    #ensure instnace folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # define the page
    @app.route('/hello')
    def hello():
        return "Sup, World!"
    return app