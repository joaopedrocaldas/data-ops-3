import psycopg2
import time
from flask import Flask, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Aluno API',
          description='API para conectar ao PostgreSQL e operações matemáticas',
          doc='/swagger')

ns_alunos = api.namespace('alunos', description='Operações com banco de dados PostgreSQL')
ns_calc = api.namespace('calc', description='Operações matemáticas')

# Modelo de entrada para soma/multiplicação
math_model = api.model('Operacao', {
    'a': fields.Float(required=True, description='Primeiro número'),
    'b': fields.Float(required=True, description='Segundo número')
})

def get_connection():
    conn = psycopg2.connect(
        host="db",
        dbname="postgres",
        user="postgres",
        password="senha123"
    )
    return conn

@ns_alunos.route('/')
class AlunosList(Resource):
    def get(self):
        time.sleep(2)  # Simula um atraso de 2 segundos
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(50)
            );
        """)
        conn.commit()

        cur.execute("INSERT INTO alunos (nome) VALUES ('João'), ('Maria'), ('José') ON CONFLICT DO NOTHING;")
        conn.commit()

        cur.execute("SELECT * FROM alunos;")
        alunos = cur.fetchall()
        cur.close()
        conn.close()
        return {"alunos": [{"id": aluno[0], "nome": aluno[1]} for aluno in alunos]}

@ns_calc.route('/soma')
class Soma(Resource):
    @api.expect(math_model)
    def post(self):
        data = request.get_json()
        a = data['a']
        b = data['b']
        return {'resultado': a + b}, 200

@ns_calc.route('/multiplicacao')
class Multiplicacao(Resource):
    @api.expect(math_model)
    def post(self):
        data = request.get_json()
        a = data['a']
        b = data['b']
        return {'resultado': a * b}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
