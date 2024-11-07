from flask import Flask, render_template, request, url_for, redirect, jsonify
import requests
from flask_mysqldb import MySQL
import functions as f
import db_classes as c
import db_config as db_config

#global variables
page_index = 'home'
page_cadastro_cliente = 'cadastrar_cliente'
page_cliente = 'cliente'
page_busca = 'busca'
page_cadastro_veiculo = 'cadastro_veiculo'
page_ordem = 'ordem'
page_criar_ordem = 'ordem_criar'
page_exibir_ordem = 'ordem_exibir'
page_veiculo = 'veiculo'
page_exibir_estoque = 'exibir_estoque'
page_estoque = 'estoque'
page_erro = 'erro'
lista_erro = {
'450': 'Cadastro já existe',
'460': 'Informações incompletas',
'550' : 'Erro ao conectar-se ao db',
'551' : 'Erro ao salvar informações no db', 
'552' : 'Erro ao recuperar informações no db', 
'561' : 'Informação não localizada', 
'599' : 'Erro desconhecido de servidor'
}

app = Flask(__name__)
app.config['MYSQL_USER'] = db_config.user
app.config['MYSQL_PASSWORD'] = db_config.password
app.config['MYSQL_DB'] = db_config.db
app.config['MYSQL_HOST'] = db_config.host
mysql = MySQL(app)


@app.route('/', methods=['GET'])
def home():
    return render_template(f'{page_index}.html')


@app.route(f'/{page_cadastro_cliente}/', methods=['GET','POST'])
def register():
    status_code=599
    if request.method == 'GET':
        return render_template(f'{page_cadastro_cliente}.html')
    try:
        nome = request.form['nome']
        cpf = request.form['cpf']
        razao_social = request.form['razao_social']
        cnpj = request.form['cnpj']
        celular = request.form['telefone']
        email = request.form['email']
        cep = request.form['cep']
        logradouro = request.form['logradouro']
        numero = request.form['numero']
        complemento = request.form['complemento']
        bairro = request.form['bairro']
        estado = request.form['estado']
        cidade = request.form['cidade']
        telefone = celular
        endereco = f'{logradouro};;{numero};;{complemento};;{bairro};;{cidade};;{estado};;{cep}'
        if ((nome and cpf) or (razao_social and cnpj)) and telefone and email and cep:
            status_code=550
            cliente_encontrado = f.pesquisar_cliente(cpf,cnpj)
            if (len(cliente_encontrado)>0):
                status_code=450
                raise
            else:
                status_code=551
                novo_cliente = c.Cliente(cpf = cpf, cnpj = cnpj, nome = nome, razao_social = razao_social, endereco = endereco, telefone = telefone, email = email)
                novo_cliente.salvar()
                try:
                    cliente_confirmado = f.pesquisar_cliente(cpf,cnpj)[0]
                    return jsonify(cliente_confirmado), 200
                    
                except:
                    return jsonify(render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)])), 552
        else:
            status_code=460
            raise
    except:
        return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code


@app.route(f'/{page_busca}/', methods = ['GET', 'POST'])
def busca():
    if request.method == "GET":
        return render_template(f'{page_busca}.html', tipo="", resultado=[]), 200
    try:
        status_code = 460
        tipo = request.form['tipo']
        criterio = request.form['criterio']
        if tipo == 'cliente':
            status_code = 550
            resultado = f.pesquisar_cliente_geral(criterio)
            if len(resultado)>0:
                status_code = 200
            else:
                status_code = 561
                raise
        elif tipo == 'veiculo':
            status_code = 550
            resultado = f.pesquisar_veiculo_geral(criterio)
            if len(resultado)>0:
                status_code = 200
            else:
                status_code = 561
                raise
        elif tipo == 'ordem':
            status_code = 550
            resultado = f.pesquisar_ordem_geral(criterio)
            if len(resultado)>0:
                status_code = 200
            else:
                status_code = 561
                raise
        else:
            status_code = 599
            raise
        return render_template(f'{page_busca}.html', tipo = tipo, resultado=resultado), status_code
    except:
        if status_code != 561:
            return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code
        else:
            return render_template(f'{page_busca}.html', tipo = tipo, resultado = []), status_code


@app.route(f'/{page_cliente}/<id_cliente>/', methods = ['GET'])
def exibir_cliente(id_cliente):
    status_code = 550
    try:
        status_code = 561
        cliente_atual = c.Cliente(id_cliente=id_cliente)
        busca_veiculos = f.pesquisar_veiculo_cliente(cliente_atual.id_cliente)
        return render_template(f'{page_cliente}.html', cliente = cliente_atual.enviar(), veiculos = busca_veiculos), 200
    except:
        return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code


@app.route(f'/{page_veiculo}/<id_veiculo>', methods = ['GET'])
def exibir_veiculo(id_veiculo):
    status_code = 550
    try:
        status_code = 561
        veiculo_atual = c.Veiculo(id_veiculo=id_veiculo)
        cliente = c.Cliente(id_cliente=veiculo_atual.id_cliente)
        ordens = f.pesquisar_ordem_geral(veiculo_atual.placa)
        return render_template(f'{page_veiculo}.html', cliente = cliente.enviar(), veiculo = veiculo_atual.enviar(), ordens = ordens), 200
    except:
        return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code


@app.route(f'/{page_cliente}/<id_cliente>/{page_cadastro_veiculo}/', methods=['GET','POST'])
def vehicle_registration(id_cliente):
    status_code = 500
    try:
        status_code = 561
        cliente_atual = c.Cliente(id_cliente=id_cliente)
    except:
        cliente = {}
        return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code
    if request.method == 'GET':
        return render_template (f'{page_cadastro_veiculo}.html', cliente = cliente_atual.enviar()), 200
    status_code = 200
    try:
        status_code = 561
        status_code = 460
        placa = request.form['placa']
        chassi = request.form['chassi']
        marca = request.form['marca']
        modelo = request.form['modelo']
        ano_fabricacao = request.form['ano_fabricacao']
        ano_modelo = request.form['ano_modelo']
        cor = request.form['cor']
        status_code=550
        if placa and chassi:
            veiculo_encontrado = f.pesquisar_veiculo(placa,chassi)
            if (len(veiculo_encontrado)>0):
                status_code=450
                raise
            else:
                status_code=551
                novo_veiculo = c.Veiculo(id_cliente = cliente_atual.id_cliente, placa = placa, chassi = chassi, marca = marca, modelo = modelo, ano_fabricacao = ano_fabricacao, ano_modelo = ano_modelo, cor = cor)
                novo_veiculo.salvar()
                return jsonify(cliente_atual.enviar()), 200
        else:
            status_code = 460
            raise
    except:
        return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code


@app.route(f'/{page_cadastro_veiculo}/')
def vehicle_registration_default():
    return render_template(f'{page_cadastro_veiculo}_default.html')


@app.route(f'/{page_ordem}/', methods=['GET','POST'])
def ordem_default():
    return render_template(f'{page_ordem}_default.html')


@app.route(f'/<id_veiculo>/{page_criar_ordem}/', methods=['GET','POST'])
def criar_ordem(id_veiculo):
    try:
        status_code = 550
        lista_servicos = f.get_tipos_servicos()
        lista_de_pecas = f.get_pecas()
        status_code = 552
        veiculo = c.Veiculo(id_veiculo = id_veiculo)
        cliente = c.Cliente(id_cliente = veiculo.id_cliente)
        if (request.method == 'GET'):
            status_code = 599
            return render_template(f'{page_criar_ordem}.html', veiculo = veiculo.enviar(), cliente = cliente.enviar(), lista_servicos = lista_servicos, lista_de_pecas = lista_de_pecas), 200
        servicos_selecionados = []
        pecas_selecionadas = []
        for i in range(lista_servicos[len(lista_servicos)-1]['id_servico']):
            try:
                servicos_selecionados.append(request.form[f'servico{i}'].replace('servico', ''))
            except KeyError:
                pass
        for i in range(lista_de_pecas[len(lista_de_pecas)-1]['id_peca']):
            try:
                pecas_selecionadas.append([str(i), request.form[f'peca{i}'].replace('peca', '')])
            except KeyError:
                pass
        if len(pecas_selecionadas)==0 and len(servicos_selecionados)==0:
            status_code = 460
            raise
        nova_ordem = c.Ordem(id_cliente=cliente.id_cliente, id_veiculo=veiculo.id_veiculo)
        status_code = 551
        nova_ordem.salvar()
        status_code = 552
        nova_ordem.localizar_ultima_ordem()
        status_code = 551
        if len(servicos_selecionados) > 0:
            nova_ordem.salvar_servicos(servicos_selecionados)
        if len(pecas_selecionadas) > 0:
            nova_ordem.salvar_pecas(pecas_selecionadas)
        return jsonify(nova_ordem.enviar()), 200
    except:
        return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code


@app.route(f'/{page_ordem}/<id_ordem>/', methods = ['GET'])
def mostrar_ordem(id_ordem):
    try:
        status_code=561
        ordem = c.Ordem(id_ordem=id_ordem)
        cliente = c.Cliente(id_cliente=ordem.id_cliente)
        veiculo = c.Veiculo(id_veiculo=ordem.id_veiculo)
        status_code=552
        lista_servicos = []
        lista_servicos_cadastrados = ordem.recuperar_servicos()
        if len(lista_servicos_cadastrados) > 0:
            lista_servicos_completa = f.get_tipos_servicos()
            for dict_item in lista_servicos_completa:
                if dict_item['id_servico'] in lista_servicos_cadastrados:
                    lista_servicos.append(dict_item)
                if len(lista_servicos)==len(lista_servicos_cadastrados):
                    break
        lista_pecas = []
        lista_pecas_cadastradas = ordem.recuperar_pecas()
        if len(lista_pecas_cadastradas) > 0:
            lista_pecas_completa = f.get_pecas()
            for dict_item in lista_pecas_completa:
                if dict_item['id_peca'] in lista_pecas_cadastradas.keys():
                    lista_pecas.append(dict_item)
                if len(lista_pecas) == len(lista_servicos_cadastrados):
                    break
            for index in lista_pecas:
                index['qtd'] = lista_pecas_cadastradas[index['id_peca']]
        return render_template(f'{page_exibir_ordem}.html', ordem = ordem.enviar_completo(), veiculo=veiculo.enviar(), cliente = cliente.enviar(), lista_servicos=lista_servicos, lista_pecas=lista_pecas), 200
    except:
        return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code


@app.route(f'/{page_ordem}/<id_ordem>/avancar', methods = ['POST'])
def avancar_ordem(id_ordem):
    try:
        status_code=561
        ordem = c.Ordem(id_ordem=id_ordem)
        if not ordem.ativo:
            status_code = 562
            raise
        status_code=551
        ordem.avancar_status()
        return jsonify(success = True, status_code = 200, id_ordem = id_ordem)
    except:
        return jsonify(success = False, status_code = status_code, id_ordem = id_ordem)


@app.route(f'/{page_ordem}/<id_ordem>/cancelar', methods = ['POST'])
def cancelar_ordem(id_ordem):
    try:
        status_code=561
        ordem = c.Ordem(id_ordem=id_ordem)
        if not ordem.ativo:
            status_code = 562
            raise
        status_code=551
        ordem.cancelar()
        return jsonify(success = True, status_code = 200, id_ordem = id_ordem)
    except:
        return jsonify(success = False, status_code = status_code, id_ordem = id_ordem)


@app.route(f'/{page_ordem}/<id_ordem>/editar', methods=['GET','POST'])
def editar_ordem(id_ordem):
    try:
        status_code = 550
        lista_servicos = f.get_tipos_servicos()
        lista_de_pecas = f.get_pecas()
        status_code = 552
        ordem = c.Ordem(id_ordem)
        veiculo = c.Veiculo(ordem.id_veiculo)
        cliente = c.Cliente(ordem.id_cliente)
        if (request.method == 'GET'):
            servicos_selecionados = ordem.recuperar_servicos()
            pecas_selecionadas = ordem.recuperar_pecas()
            status_code = 599
            return render_template(f'{page_ordem}_editar.html', ordem = ordem.enviar_completo(), veiculo = veiculo.enviar(), cliente = cliente.enviar(), lista_servicos = lista_servicos, servicos_selecionados = servicos_selecionados, lista_de_pecas = lista_de_pecas, pecas_selecionadas = pecas_selecionadas), 200
        servicos_selecionados = []
        pecas_selecionadas = []
        for i in range(lista_servicos[len(lista_servicos)-1]['id_servico']):
            try:
                servicos_selecionados.append(request.form[f'servico{i}'].replace('servico', ''))
            except KeyError:
                pass
        for i in range(lista_de_pecas[len(lista_de_pecas)-1]['id_peca']):
            try:
                pecas_selecionadas.append([str(i), request.form[f'peca{i}'].replace('peca', '')])
            except KeyError:
                pass
        if len(pecas_selecionadas)==0 and len(servicos_selecionados)==0:
            status_code = 460
            raise
        ordem.editar_servicos(servicos_selecionados)
        ordem.editar_pecas(pecas_selecionadas)
        return jsonify(ordem.enviar()), 200
    except:
        return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code


@app.route(f'/{page_estoque}', methods = ['GET'])
def exibir_estoque():
    status_code = 550
    try:
        lista_de_pecas = f.get_pecas()
        status_code = 599
        return render_template(f'{page_exibir_estoque}.html', lista_de_pecas = lista_de_pecas), 200
    except:
        return render_template(f'{page_erro}.html', code=status_code, erro=lista_erro[str(status_code)]), status_code


@app.route(f'/{page_estoque}/atualizar', methods = ['POST'])
def atualizar_estoque():
    try:
        status_code = 561
        id_peca = request.form["id_peca"]
        status_code = 460
        qtd, operacao = int(request.form["qtd"]), request.form["operacao"]
        status_code = 552
        peca = c.Peca(id_peca = id_peca)
        status_code = 551
        if operacao == 'adicionar':
            peca.adicionar_peca(qtd)
        elif operacao == 'subtrair':
            if qtd > peca.qtd:
                status_code = 551
                raise
            peca.remover_peca(qtd)
        else:
            status_code = 460
            raise
        return jsonify(success = True, status_code = 200, nova_qtd = peca.qtd)
    except:
        return jsonify(success = False, status_code = status_code)

@app.route('/teste/', methods = ['GET'])
def teste():
    return render_template('teste.html', teste = [1,2,3])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)