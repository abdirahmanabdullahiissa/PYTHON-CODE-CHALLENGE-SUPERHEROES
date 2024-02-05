#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import  Hero, Power, HeroPower, db
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hero_powers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

migrate = Migrate(app, db)
api=Api(app)
db.init_app(app)

@app.route('/')
def home():
    return 'SUPERHEROES'

class Heroes(Resource):
 def get(self):
    heroes = Hero.query.all()
    hero_dict=[hero.serialize() for hero in heroes]
    response= make_response(jsonify(hero_dict),200)
    return response
api.add_resource(Heroes,'/heroes')

class HeroesById(Resource):
 def get(self,id):
    heroes = Hero.query.get(id)
    if not heroes:
        return make_response(jsonify({'error': 'Hero not found'}), 404)
    else :
        hero_dict=heroes.serialize()
        response= make_response(jsonify(hero_dict),200)
        return response
api.add_resource(HeroesById, '/heroes/<int:id>')

class Powers(Resource):
  def get(self):
    powers = Power.query.all()
    power_dict=[power.serialize() for power in powers]
    response=make_response(jsonify(power_dict),200)
    return response
api.add_resource(Powers, '/power')

  

class PowerById(Resource):
  def get(self,id):
        power = Power.query.get(id)
        if not power:
            return make_response(jsonify({'error': 'Power not found'}), 404)
        else:
            power_dict=power.serialize()
            response=make_response(jsonify(power_dict),200)
            return response
  def patch(self,id):
     data= request.get_json()
     name=data.get('name')
     description=data.get('description')
     power_id = Power.query.get(id)
     if not power_id:
        return {'error':'id not found'}
     else:
        power_id.name=name
        power_id.description= description

        db.session.commit()
        response=make_response(jsonify(power_id.serialize()),201)
        return response

     
api.add_resource(PowerById,'/power/<int:id>')
class HeroPowers(Resource): 
   def post(self):
      data=request.get_json()
      strength=data.get('strength')
      hero_id=data.get('hero_id')
      power_id=data.get('power_id')

      new_data=HeroPower(strength=strength,hero_id=hero_id,power_id=power_id)
      db.session.add(new_data)
      db.session.commit
      
      response=make_response(jsonify(new_data.serialize()),200)
      return response
api.add_resource(HeroPowers,'/heropower')
   


if __name__ == '__main__':
    app.run(port=5555)

    