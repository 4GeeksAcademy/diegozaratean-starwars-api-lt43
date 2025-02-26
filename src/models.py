from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=False, nullable=False)
    ciudad = db.Column(db.String(80), unique=False, nullable=False)
    slogan = db.Column(db.String(120), unique=False, nullable=False)
    videojuegos = db.relationship('Videojuego', backref='empresa')

    def __repr__(self):
        return '<Empresa %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "name": self.nombre,
            "city": self.ciudad,
            "slogan": self.slogan,
            # do not serialize the password, its a security breach
        }


class Videojuego(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=False, nullable=False)
    genero = db.Column(db.String(80), unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'))

    def __repr__(self):
        return '<Videojuego %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "name": self.nombre,
            "genero": self.genero,
            "year": self.year,
            # do not serialize the password, its a security breach
        }
