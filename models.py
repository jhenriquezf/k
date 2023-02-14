from app import db
from datetime import datetime

# Definir modelo de base de datos para la tabla 'Usuario'
class Institucion(db.Model):
    __tablename__ = 'institucion'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(200))
    direccion = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.Date, default=datetime.utcnow)

    proyectos = db.relationship('Proyecto', backref='institucion', lazy=True)
    
    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'direccion': self.direccion,
            'fecha_creacion': self.fecha_creacion
        }

class Proyecto(db.Model):
    __tablename__ = 'proyecto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(200))
    fecha_inicio = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    fecha_termino = db.Column(db.Date)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    institucion_id = db.Column(db.Integer, db.ForeignKey('institucion.id'), nullable=False)


    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.ddescripcion,
            'fecha_inicio': self.fecha_inicio,
            'fecha_termino': self.fecha_termino
        }

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    rut = db.Column(db.String(20), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    cargo = db.Column(db.String(50))
    edad = db.Column(db.Integer)

    proyectos = db.relationship('Proyecto', backref='user', lazy=True)
    
    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'rut': self.rut,
            'fecha_nacimiento': self.fecha_nacimiento,
            'cargo': self.cargo,
            'edad': self.edad
        }