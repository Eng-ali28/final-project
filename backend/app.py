from flask import Flask, Response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import videoprocess as vp
from flask_cors import CORS
import os

# init flask app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# CORS 
CORS(app)

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir , 'db.sqlite')

# init db
db = SQLAlchemy(app)
# init ma
ma = Marshmallow(app)

# System Class/Model
class System(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    video_path = db.Column(db.String())
    first_distance = db.Column(db.Float)
    second_distance = db.Column(db.Float)
    isStop = db.Column(db.String())
    # screen_shot_images = db.relationship('ScreenShotImages', backref='system')

    def __init__(self, video_path, first_distance, second_distance, isStop ):
        self.video_path = video_path
        self.first_distance = first_distance
        self.second_distance = second_distance
        self.isStop = isStop

# System schema
class SystemSchema(ma.Schema):
    class Meta:
        fields = ('id' , 'video_path' , 'first_distance', 'second_distance', 'isStop')

# init schema
system_schema = SystemSchema()
systems_schema = SystemSchema(many=True)

# screen shot images
# class ScreenShotImages(db.Model):
#     id = db.Column(db.Integer , primary_key=True)
#     path = db.Column(db.String())
#     # system_id = db.Column(db.Integer, db.ForeignKey('system.id'))

#     def __init__(self, path):
#         self.path = path

# # System schema
# class ScreenShotImageSchema(ma.Schema):
#     class Meta:
#         fields = ('id' , 'path')

# # init schema
# screen_shot_image_schema = ScreenShotImageSchema()
# screen_shot_images_schema = ScreenShotImageSchema(many=True)

# create system
# @app.route("/system", methods=['POST'])
# def createSystem():
#     video_path = request.json['video_path']
#     first_distance = request.json['first_distance']
#     second_distance = request.json['second_distance']

#     new_system = System(video_path, first_distance, second_distance)

#     db.session.add(new_system)

#     db.session.commit()

#     return system_schema.jsonify(new_system)

@app.route("/say_hello" , methods = ['GET'])
def sayHello():
    return "Hello world!"
    


@app.route("/video_process" , methods = ['GET'])
def carProcess():
    get_first = db.session.query(System).one_or_none()
    videoPath = get_first.video_path
    distance1= get_first.first_distance
    distance2= get_first.second_distance
    return Response(vp.car_process(videoPath, distance1, distance2), mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route("/stop_video_process" , methods = ['GET'])
def stopCarProcess():
    vp.stopVideo()
    

# get single system
@app.route("/system", methods = ['GET'])
def getFirstSystem():
    get_first = db.session.query(System).one_or_none()
    print(get_first)
    if get_first == None:
        video_path = ''
        first_distance = 0
        second_distance = 0
        isStop = "FALSE"

        new_system = System(video_path, first_distance, second_distance, isStop)

        db.session.add(new_system)

        db.session.commit()

        return system_schema.jsonify(new_system)
    else:
        system = db.session.query(System).one()
        
        return system_schema.jsonify(system)
    
# update system
@app.route('/system', methods=['PUT'])
def updateSystem():
    system = db.session.query(System).one()

    video_path = set_default(request.json['video_path'],system.video_path)
    first_distance = set_default(request.json['first_distance'],system.first_distance) 
    second_distance = set_default(request.json['second_distance'],system.second_distance) 

    system.video_path = video_path
    system.first_distance = first_distance
    system.second_distance = second_distance

    db.session.commit()

    return system_schema.jsonify(system)

# # set isStop system
@app.route('/system/is_stop', methods=['PUT'])
def updateSystemIsStop():
    system = db.session.query(System).one()
    print(request.json)

    isStop = set_default(request.json['isStop'],system.isStop) 

    system.isStop = isStop

    db.session.commit()

    return system_schema.jsonify(system)




def getIsStopValue():
    system = db.session.query(System).one()
    return system.isStop

# helper
def set_default(value, default):
    print( value)
    return value if value is not None else default
# run server
if __name__ == '__main__':
    app.run(debug=True)
