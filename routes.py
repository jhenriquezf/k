from flask import request, jsonify
from app import app, db
from models import Institucion, Proyecto, Usuario
from datetime import datetime, timedelta


#CRUD para Instituciones
@app.route('/instituciones/', methods=['GET', 'POST'])
def instituciones():
    if request.method == 'GET':
        instituciones = Institucion.query.all()
        return jsonify([institucion.serialize() for institucion in instituciones])

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        direccion = request.form['direccion']
        fecha_creacion = request.form['fecha_creacion']

        institucion = Institucion(nombre=nombre, descripcion=descripcion, direccion=direccion, fecha_creacion=fecha_creacion)
        db.session.add(institucion)
        db.session.commit()

        return jsonify(institucion.to_dict()), 201

@app.route('/instituciones/<int:institucion_id>', methods=['GET', 'PUT', 'DELETE'])
def institucion(institucion_id):
    institucion = Institucion.query.get(institucion_id)
    if institucion is None:
        return jsonify({'error': 'Institución no encontrada'}), 404

    if request.method == 'GET':
        return jsonify(institucion.serialize())

    if request.method == 'PUT':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        direccion = request.form['direccion']
        fecha_creacion = request.form['fecha_creacion']

        institucion.nombre = nombre
        institucion.descripcion = descripcion
        institucion.direccion = direccion
        institucion.fecha_creacion = fecha_creacion
        db.session.commit()

        return jsonify(institucion.serialize())

    if request.method == 'DELETE':
        db.session.delete(institucion)
        db.session.commit()
        return '', 204


#Servicios para listar instituciones,proyectos y usuarios.

@app.route('/listInstitutions', methods=['GET'])
def get_institutions():
    institutions = Institucion.query.all()
    return jsonify([i.serialize() for i in institutions])

@app.route('/listProjects', methods=['GET'])
def get_projects():
    projects = Proyecto.query.all()
    return jsonify([p.serialize() for p in projects])

@app.route('/listUsers', methods=['GET'])
def get_users():
    users = Usuario.query.all()
    return jsonify([u.serialize() for u in users])

#Servicio para listar una institución (Filtró por id) con sus respectivos proyectos y responsable del proyecto.
@app.route('/instituciones/<int:institucion_id>/detalles', methods=['GET'])
def institucion_detalles(institucion_id):
    institucion = Institucion.query.get(institucion_id)
    if institucion is None:
        return jsonify({'error': 'Institución no encontrada'}), 404

    proyectos = Proyecto.query.filter_by(institucion_id=institucion_id).all()
    proyectos_detalles = []
    for proyecto in proyectos:
        responsable = Usuario.query.get(proyecto.responsable_id)
        proyectos_detalles.append({
            'nombre_proyecto': proyecto.nombre,
            'descripcion_proyecto': proyecto.descripcion,
            'fecha_inicio': proyecto.fecha_inicio,
            'fecha_termino': proyecto.fecha_termino,
            'nombre_responsable': responsable.nombre,
            'apellidos_responsable': responsable.apellidos,
            'rut_responsable': responsable.rut
        })

    return jsonify({
        'nombre_institucion': institucion.nombre,
        'descripcion_institucion': institucion.descripcion,
        'direccion_institucion': institucion.direccion,
        'fecha_creacion_institucion': institucion.fecha_creacion,
        'proyectos': proyectos_detalles
    })


#Servicio para listar un usuario (filtro por Rut) con sus respectivos proyectos.
@app.route('/usuarios/<string:rut_usuario>/detalles', methods=['GET'])
def usuario_detalles(rut_usuario):
    usuario = Usuario.query.filter_by(rut=rut_usuario).first()
    if usuario is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    proyectos = Proyecto.query.filter_by(responsable_id=usuario.id).all()
    proyectos_detalles = []
    for proyecto in proyectos:
        institucion = Institucion.query.get(proyecto.institucion_id)
        proyectos_detalles.append({
            'nombre_proyecto': proyecto.nombre,
            'descripcion_proyecto': proyecto.descripcion,
            'fecha_inicio': proyecto.fecha_inicio,
            'fecha_termino': proyecto.fecha_termino,
            'nombre_institucion': institucion.nombre
        })

    return jsonify({
        'nombre_usuario': usuario.nombre,
        'apellidos_usuario': usuario.apellidos,
        'rut_usuario': usuario.rut,
        'fecha_nacimiento_usuario': usuario.fecha_nacimiento,
        'cargo_usuario': usuario.cargo,
        'edad_usuario': usuario.edad,
        'proyectos': proyectos_detalles
    })


#Servicio para listar instituciones donde a cada institución se agregue a la dirección la ubicación de google maps ejemplo: “https://www.google.com/maps/search/+ direccion ” y la abreviación del nombre (solo los primeros tres caracteres).
@app.route('/instituciones/g', methods=['GET'])
def instituciones():
    instituciones = Institucion.query.all()
    instituciones_detalles = []
    for institucion in instituciones:
        instituciones_detalles.append({
            'nombre_institucion': institucion.nombre,
            'descripcion_institucion': institucion.descripcion,
            'direccion_institucion': institucion.direccion,
            'fecha_creacion_institucion': institucion.fecha_creacion,
            'ubicacion_google_maps': "https://www.google.com/maps/search/" + institucion.direccion,
            'abrev_nombre_institucion': institucion.nombre[:3]
        })

    return jsonify({'instituciones': instituciones_detalles})


#Servicio para listar los proyectos que la respuesta sea el nombre del proyecto y los días que faltan para su término.
@app.route('/proyectos', methods=['GET'])
def proyectos():
    proyectos = Proyecto.query.all()
    proyectos_detalles = []
    for proyecto in proyectos:
        fecha_termino = proyecto.fecha_termino
        fecha_actual = datetime.now().date()
        dias_restantes = (fecha_termino - fecha_actual).days
        proyectos_detalles.append({
            'nombre_proyecto': proyecto.nombre,
            'dias_restantes': dias_restantes
        })

    return jsonify({'proyectos': proyectos_detalles})
