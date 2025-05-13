import psycopg2
import time
from flask import Flask
from flask_restx import Api, Resource, fields


app = Flask(__name__)
api = Api(app, version='1.0', title='Aulno API',
            description='API para conectar e consultar dados no PostgreSQL',
            doc='/swagger')

ns = api.namespace('alunos', description='Operações de conexão com PostgreSQL')

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

@ns.route('/')
class AlunosList(Resource):
    def get(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alunos")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return {'alunos': rows}, 200
    def get(self):
        time.sleep(5)  # Simula um atraso de 5 segundos
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(50)
            );
        """)

        conn.commit()
        cur.execute("INSERT INTO alunos (nome) VALUES ('João'), ('Maria'), ('José');")
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
