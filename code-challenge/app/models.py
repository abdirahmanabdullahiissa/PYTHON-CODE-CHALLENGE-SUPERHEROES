from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
db=SQLAlchemy()

class Hero(db.Model,SerializerMixin):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)

    hero_power = db.relationship('HeroPower', backref='heroes')

    def serialize(self):
        return {'id':self.id,'name':self.name,'super_name':self.super_name}

class Power(db.Model,SerializerMixin):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    hero_power = db.relationship('HeroPower', backref='powers')

    def serialize(self):
        return {'id': self.id, 'name': self.name, 'description': self.description}

    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return description

class HeroPower(db.Model,SerializerMixin):
    __tablename__ = 'hero_power'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)
    strength = db.Column(db.String(255), nullable=False)
    
    def serialize(self):
        return{'id': self.id, 'strength':self.strength}

    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            raise ValueError("Strength must be one of: 'Strong', 'Weak', 'Average'")
        return strength
