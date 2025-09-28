from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from dataclasses import dataclass

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veiculos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

MARCAS_VALIDAS = {
    'ford', 'chevrolet', 'volkswagen', 'fiat', 'honda', 'toyota',
    'hyundai', 'renault', 'nissan', 'bmw', 'mercedes-benz', 'audi'
}


class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    veiculo = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.Text)
    vendido = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'veiculo': self.veiculo,
            'marca': self.marca,
            'ano': self.ano,
            'descricao': self.descricao,
            'vendido': self.vendido,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


#Criacao das tabelas
with app.app_context():
    db.create_all()

def validar_marca(marca):
    """Valida se a marca está na lista de marcas válidas"""
    return marca.lower() in MARCAS_VALIDAS


def get_decada(ano):
    """Retorna a década do ano"""
    return (ano // 10) * 10


#Endpoint da API
@app.route('/veiculos', methods=['GET'])
def listar_veiculos():
    """Retorna todos os veículos com filtros opcionais"""
    try:
        query = Veiculo.query

        #Filtros das marcas dos veiculos
        marca = request.args.get('marca')
        ano = request.args.get('ano')
        vendido = request.args.get('vendido')

        if marca:
            query = query.filter(Veiculo.marca.ilike(f'%{marca}%'))
        if ano:
            query = query.filter(Veiculo.ano == int(ano))
        if vendido:
            query = query.filter(Veiculo.vendido == (vendido.lower() == 'true'))

        veiculos = query.all()
        return jsonify([veiculo.to_dict() for veiculo in veiculos])

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/veiculos/<int:id>', methods=['GET'])
def obter_veiculo(id):
    """Retorna os detalhes de um veículo específico"""
    veiculo = Veiculo.query.get_or_404(id)
    return jsonify(veiculo.to_dict())


@app.route('/veiculos', methods=['POST'])
def criar_veiculo():
    """Adiciona um novo veículo"""
    try:
        data = request.get_json()

        # Validações
        if not validar_marca(data.get('marca', '')):
            return jsonify({'error': 'Marca inválida. Marcas válidas: ' + ', '.join(MARCAS_VALIDAS)}), 400

        if not data.get('veiculo') or not data.get('marca') or not data.get('ano'):
            return jsonify({'error': 'Campos obrigatórios: veiculo, marca, ano'}), 400

        veiculo = Veiculo(
            veiculo=data['veiculo'],
            marca=data['marca'].lower(),
            ano=data['ano'],
            descricao=data.get('descricao', ''),
            vendido=data.get('vendido', False)
        )

        db.session.add(veiculo)
        db.session.commit()

        return jsonify(veiculo.to_dict()), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/veiculos/<int:id>', methods=['PUT'])
def atualizar_veiculo(id):
    """Atualiza todos os dados de um veículo"""
    try:
        veiculo = Veiculo.query.get_or_404(id)
        data = request.get_json()

        if 'marca' in data and not validar_marca(data['marca']):
            return jsonify({'error': 'Marca inválida'}), 400

        veiculo.veiculo = data.get('veiculo', veiculo.veiculo)
        veiculo.marca = data.get('marca', veiculo.marca).lower()
        veiculo.ano = data.get('ano', veiculo.ano)
        veiculo.descricao = data.get('descricao', veiculo.descricao)
        veiculo.vendido = data.get('vendido', veiculo.vendido)

        db.session.commit()
        return jsonify(veiculo.to_dict())

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/veiculos/<int:id>', methods=['PATCH'])
def atualizar_parcial_veiculo(id):
    """Atualiza apenas alguns dados do veículo"""
    try:
        veiculo = Veiculo.query.get_or_404(id)
        data = request.get_json()

        if 'marca' in data and not validar_marca(data['marca']):
            return jsonify({'error': 'Marca inválida'}), 400

        if 'veiculo' in data:
            veiculo.veiculo = data['veiculo']
        if 'marca' in data:
            veiculo.marca = data['marca'].lower()
        if 'ano' in data:
            veiculo.ano = data['ano']
        if 'descricao' in data:
            veiculo.descricao = data['descricao']
        if 'vendido' in data:
            veiculo.vendido = data['vendido']

        db.session.commit()
        return jsonify(veiculo.to_dict())

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/veiculos/<int:id>', methods=['DELETE'])
def excluir_veiculo(id):
    """Exclui um veículo"""
    veiculo = Veiculo.query.get_or_404(id)
    db.session.delete(veiculo)
    db.session.commit()
    return jsonify({'message': 'Veículo excluído com sucesso'})


# Endpoints de relatórios
@app.route('/dashboard/nao-vendidos', methods=['GET'])
def contar_nao_vendidos():
    """Retorna a quantidade de veículos não vendidos"""
    count = Veiculo.query.filter_by(vendido=False).count()
    return jsonify({'nao_vendidos': count})


@app.route('/dashboard/decada-fabricacao', methods=['GET'])
def distribuicao_decada():
    """Retorna a distribuição de veículos por década de fabricação"""
    veiculos = Veiculo.query.all()
    distribuicao = {}

    for veiculo in veiculos:
        decada = get_decada(veiculo.ano)
        distribuicao[decada] = distribuicao.get(decada, 0) + 1

    return jsonify(distribuicao)


@app.route('/dashboard/distribuicao-marca', methods=['GET'])
def distribuicao_marca():
    """Retorna a distribuição de veículos por fabricante"""
    veiculos = Veiculo.query.all()
    distribuicao = {}

    for veiculo in veiculos:
        distribuicao[veiculo.marca] = distribuicao.get(veiculo.marca, 0) + 1

    return jsonify(distribuicao)


@app.route('/dashboard/ultima-semana', methods=['GET'])
def registros_ultima_semana():
    """Retorna os veículos registrados na última semana"""
    uma_semana_atras = datetime.utcnow() - timedelta(days=7)
    veiculos = Veiculo.query.filter(Veiculo.created_at >= uma_semana_atras).all()

    return jsonify([veiculo.to_dict() for veiculo in veiculos])


@app.route('/marcas-validas', methods=['GET'])
def listar_marcas_validas():
    """Retorna a lista de marcas válidas"""
    return jsonify(sorted(list(MARCAS_VALIDAS)))


if __name__ == '__main__':
    app.run(debug=True)