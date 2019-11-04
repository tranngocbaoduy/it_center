from flask import Flask, render_template
from flask_mongoengine import *
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from it_center.config import Config
# from flask_dance.contrib.twitter import make_twiiter_blueprint, twitter
# from flask_cors import CORS, cross_origin

db = MongoEngine() 
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'danger'
# twitter_blueprint = make_twiiter_blueprint(api_key='', api_secret='')

mail = Mail()
 
def create_app(config_class=Config):
    app = Flask(__name__)
    
    app.config.from_object(Config) 
    # CORS(app, supports_credentials=True)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from it_center.users.routes import users  
    from it_center.main.routes import main 
    from it_center.student.routes import student 
    from it_center.teacher.routes import teacher      
    from it_center.educate.routes import educate  
    from it_center.staff.routes import staff  
    

    app.register_blueprint(users) 
    app.register_blueprint(main)   
    app.register_blueprint(student) 
    app.register_blueprint(teacher)
    app.register_blueprint(educate) 
    app.register_blueprint(staff)
 
    @app.errorhandler(404)
    def error404(error):
        print(error)
        return render_template('error.html', error="404" ,title="PAGE NOT FOUND !!!"),404 

    @app.errorhandler(403)
    def error403(error):
        return render_template('error.html', error="403" ,title="METHOD IS NOT ALLOW !!!"),403
    
    @app.errorhandler(405)
    def error405(error):
        print(error)
        return render_template('error.html', error="405" ,title="METHOD IS NOT ALLOW !!!"),405

    @app.errorhandler(500)
    def error500(error):
        return render_template('error.html', error="500" ,title="ERROR !!!"),500

    return app