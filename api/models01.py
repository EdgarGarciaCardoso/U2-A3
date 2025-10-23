from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Juego(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50))
    plataforma = db.Column(db.String(50))

    def __repr__(self):
        return f"<Juego {self.nombre}>"
