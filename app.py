from flask import Flask, jsonify, request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import abort
from flask_cors import cross_origin
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Dados(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    TipoSangue = db.Column(db.Integer)
    email = db.Column(db.String(100))
    DataNasc = db.Column(db.String(20))
    cpf = db.Column(db.String(20))
    senha = db.Column(db.String(100))
    peso_atual = db.Column(db.Float)

class Agendamento(db.Model):
    id_agendamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_atendimento = db.Column(db.Date)
    horario_atendimento = db.Column(db.String(20))
    id_doador = db.Column(db.Integer, db.ForeignKey('dados.id'))
    nome_doador = db.Column(db.String(100))
    hemocentro = db.Column(db.String(100) )
    status = db.Column(db.String(20))
    
    # Relacionamento com a tabela de usuários
    doador = db.relationship('Dados', backref=db.backref('agendamentos', lazy=True))    
      

db.create_all()

usuarios =[ 
   
]

@app.route('/usuarios',methods=['GET'])
@cross_origin()
def obter_usuarios():
    todos_os_dados = Dados.query.all()
    usuarios_serializados = []
    for dado in todos_os_dados:
        usuario_serializado = {
            'id': dado.id,
            'nome': dado.nome,
            'TipoSangue': dado.TipoSangue,
            'email': dado.email,
            'DataNasc': dado.DataNasc,
            'cpf': dado.cpf,
            'senha': dado.senha
        }
        usuarios_serializados.append(usuario_serializado)
    return jsonify(usuarios_serializados)

@app.route('/usuarios/<int:id>', methods=['GET'])
def obter_usuario_id(id):
    usuario = Dados.query.get(id)
    if usuario:
        usuario_serializado = {
            'id': usuario.id,
            'nome': usuario.nome,
            'TipoSangue': usuario.TipoSangue,
            'email': usuario.email,
            'DataNasc': usuario.DataNasc,
            'cpf': usuario.cpf,
            'senha': usuario.senha
        }
        return jsonify(usuario_serializado)
    else:
        return jsonify({'message': 'Usuário não encontrado'}), 404

@app.route('/usuarios/alterar/<int:id>', methods = ['PUT'])        
def editar_usuario_id(id):
    usuario_editado = request.get_json()
    usuario = Dados.query.get(id)
    if usuario:
        usuario.nome = usuario_editado.get('Nome',usuario.nome)
        usuario.TipoSangue = usuario_editado.get('TipoSang', usuario.TipoSangue)
        usuario.email = usuario_editado.get('Email', usuario.email)
        usuario.DataNasc = usuario_editado.get('DataNasc', usuario.DataNasc)
        usuario.cpf = usuario_editado.get('CPF', usuario.cpf)
        usuario.senha = usuario_editado.get('Senha', usuario.senha)
        db.session.commit()
        return jsonify({'message': 'Usuário atualizado com sucesso'}), 200
    else:
        return jsonify({'message': 'Usuário não encontrado'}), 404 

@app.route('/usuarios/cadastrar', methods= ['POST'])
def cadastrar_usuario():
    novo_usuario = request.get_json()
    #usuarios.append(novo_usuario)
    novo_dado = Dados(nome=novo_usuario['Nome'], cpf=novo_usuario['CPF'], DataNasc=novo_usuario['DataNasc'], email=novo_usuario['Email'], senha=novo_usuario['Senha'], TipoSangue=novo_usuario['TipoSang'], peso_atual = novo_usuario['Peso_atual'])
    db.session.add(novo_dado)
    db.session.commit()
    return jsonify(novo_usuario) 

@app.route('/usuarios/excluir/<int:id>', methods = ['DEL'])
def excluir_usuario(id):
    usuario = Dados.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuário excluído com sucesso'}), 200
    else:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    #for indice, usuario in enumerate(usuarios):
        #if usuario.get('id') == id:
            #del usuarios[indice]        
    #return jsonify(usuarios)

@app.route('/usuarios/login', methods = ['POST'])
def login():
    dados_login = request.get_json()
    usuario = Dados.query.filter_by(email=dados_login.get('email')).first()
    if usuario and usuario.senha == dados_login.get('senha'):
        usuario_serializado = {
            'id': usuario.id,
            'nome': usuario.nome,
            'TipoSangue': usuario.TipoSangue,
            'email': usuario.email,
            'DataNasc': usuario.DataNasc,
            'cpf': usuario.cpf,
            'senha': usuario.senha
        }
        return jsonify(usuario_serializado), 200
    else:
        return jsonify({'message': 'Credenciais inválidas'}), 401
    
@app.route('/agendamento/agendar', methods = ['POST'])
def agendar():
    dados_agendamento = request.get_json()
    novo_agendamento = Agendamento( data_atendimento = datetime.strptime(dados_agendamento["data_agendamento"], '%Y-%m-%d').date(), horario_atendimento = dados_agendamento["horario_agendamento"], id_doador = dados_agendamento["id_doador"], nome_doador = dados_agendamento["nome_doador"], hemocentro = dados_agendamento["hemocentro"], status = dados_agendamento["status"])    
    db.session.add(novo_agendamento)
    db.session.commit()
    return jsonify(dados_agendamento)

@app.route('/agendamento',methods=['GET'])
@cross_origin()
def obter_agendamento():
    todos_os_dados = Agendamento.query.all()
    agendamento_serializados = []
    for agendamento in todos_os_dados:
        agendamento_serializado = {
            'id_agendamento': agendamento.id_agendamento,
            'data_agendamento': agendamento.data_atendimento,
            'horario_agendamento': agendamento.horario_atendimento,
            'id_doador': agendamento.id_doador,
            'nome_doador': agendamento.nome_doador,
            'hemocentro': agendamento.hemocentro,
            'status' : agendamento.status
        }
        agendamento_serializados.append(agendamento_serializado)
    return jsonify(agendamento_serializados)

@app.route('/agendamento/<int:id_agendamento>', methods=['GET'])
def obter_agendamento_id(id_agendamento):
    # Buscar todos os agendamentos com o ID do doador correspondente
    agendamentos = Agendamento.query.filter_by(id_doador=id_agendamento).all()
    
    # Se houver agendamentos encontrados, serializar e retornar como JSON
    if agendamentos:
        agendamentos_serializados = []
        for agendamento in agendamentos:
            agendamento_serializado = {
                'id_agendamento': agendamento.id_agendamento,
                'data_agendamento': agendamento.data_atendimento.strftime('%Y%m%d'),
                'horario_agendamento': agendamento.horario_atendimento,
                'id_doador': agendamento.id_doador,
                'nome_doador': agendamento.nome_doador,
                'hemocentro': agendamento.hemocentro,
                'status': agendamento.status
            }
            agendamentos_serializados.append(agendamento_serializado)
        
        return jsonify(agendamentos_serializados)
    else:
        return jsonify({'message': 'Nenhum agendamento encontrado para este doador'}), 404

@app.route('/agendamento/atualizar/<int:id_agendamento>', methods=['PUT','OPTIONS'])
def atualizar_status(id_agendamento):
    agendamento = Agendamento.query.get(id_agendamento)
    if agendamento:
        agendamento.status = "Concluído"
        db.session.commit()
        return jsonify({'message': 'Status atualizado com sucesso'}), 200
    else:
        return jsonify({'message': 'Usuário não encontrado'}), 404 
    
@app.route('/agendamento/cancelar/<int:id_agendamento>', methods=['PUT','OPTIONS'])
def atualizar_cancelar(id_agendamento):
    agendamento = Agendamento.query.get(id_agendamento)
    if agendamento:
        agendamento.status = "Cancelado"
        db.session.commit()
        return jsonify({'message': 'Status atualizado com sucesso'}), 200
    else:
        return jsonify({'message': 'Usuário não encontrado'}), 404     

@app.route('/agendamento/verificar/<string:data_agendamento>', methods=['GET'])
def data_agendamento_data(data_agendamento):
    data_agendamentos = Agendamento.query.filter_by(data_atendimento = data_agendamento).all()
    print(data_agendamentos)
    if data_agendamentos:
        data_serializada = []
        for data in data_agendamentos:
            datas_serializada = {
                'horario_agendamento' :data.horario_atendimento
            }
            data_serializada.append(datas_serializada)
        return jsonify(data_serializada)
    else:
        return jsonify({'message': "Não encontrado"})  
    
@app.route('/agendamento/peso/<int:id_agendamento>', methods=['PUT','OPTIONS'])
def atualizar_peso(id_agendamento):
    agendamento = Dados.query.get(id_agendamento)

    if agendamento:
        dados_agendamento = request.get_json()
        agendamento.peso_atual = dados_agendamento['Peso_atual']
        db.session.commit()  
        return jsonify({'message': 'Status atualizado com sucesso'}), 200
    else:
        return jsonify({'message': 'Usuário não encontrado'}), 404 
    
app.run(port=5000, host='192.168.1.202', debug=True)

