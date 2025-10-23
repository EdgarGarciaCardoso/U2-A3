from flask import Blueprint, request
from flask_restful import Api, Resource, fields, marshal_with, abort
from .models import db, Juego

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)


juego_fields = {
    'id': fields.Integer,
    'nombre': fields.String,
    'genero': fields.String,
    'plataforma': fields.String
}

class JuegoList(Resource):
    @marshal_with(juego_fields)
    def get(self):
        """Obtener todos los juegos"""
        return Juego.query.all(), 200

    @marshal_with(juego_fields)
    def post(self):
        """Crear un nuevo juego"""
        data = request.get_json()
        if not data or 'nombre' not in data:
            abort(400, message="El campo 'nombre' es obligatorio")

        nuevo_juego = Juego(
            nombre=data['nombre'],
            genero=data.get('genero', ''),
            plataforma=data.get('plataforma', '')
        )
        db.session.add(nuevo_juego)
        db.session.commit()
        return nuevo_juego, 201


class JuegoResource(Resource):
    @marshal_with(juego_fields)
    def get(self, id):
        """Obtener un juego por ID"""
        juego = Juego.query.get(id)
        if not juego:
            abort(404, message="Juego no encontrado")
        return juego, 200

    @marshal_with(juego_fields)
    def put(self, id):
        """Modificar un juego"""
        juego = Juego.query.get(id)
        if not juego:
            abort(404, message="Juego no encontrado")

        data = request.get_json()
        juego.nombre = data.get('nombre', juego.nombre)
        juego.genero = data.get('genero', juego.genero)
        juego.plataforma = data.get('plataforma', juego.plataforma)
        db.session.commit()
        return juego, 200

    def delete(self, id):
        """Eliminar un juego"""
        juego = Juego.query.get(id)
        if not juego:
            abort(404, message="Juego no encontrado")
        db.session.delete(juego)
        db.session.commit()
        return '', 204


# Registrar los recursos
api.add_resource(JuegoList, '/juegos')
api.add_resource(JuegoResource, '/juegos/<int:id>')
