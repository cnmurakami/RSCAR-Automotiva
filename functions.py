import db_operations as db
import db_classes as c

def criar_lista_cliente(resultado):
    lista_clientes = []
    for i in resultado:
        lista_clientes.append(c.Cliente(id_cliente=str(i[0])))
    clientes = []
    for i in lista_clientes:
        clientes.append(i.enviar())
    return clientes

def pesquisar_cliente(cpf='', cnpj=''):
    resultado = db.execute('select * from cliente where cpf = %s and cnpj = %s', (cpf, cnpj))
    if len(resultado)>0:
        return criar_lista_cliente(resultado)
    else:
        return []

def criar_lista_veiculo(resultado):
    lista_veiculos = []
    for i in resultado:
        lista_veiculos.append(c.Veiculo(id_veiculo=str(i[0])))
    veiculos = []
    for i in lista_veiculos:
        veiculos.append(i.enviar())
    return veiculos

def criar_lista_ordem(resultado):
    lista_ordens = []
    for i in resultado:
        lista_ordens.append(c.Ordem(id_ordem=str(i[0])))
    ordens = []
    for i in lista_ordens:
        ordens.append(i.enviar_completo())
    return ordens


def pesquisar_veiculo(placa,chassi):
    resultado = db.execute('select * from veiculo where placa = %s or chassi = %s', (placa, chassi))
    if len(resultado)>0:
        return criar_lista_veiculo(resultado)
    else:
        return []

def pesquisar_cliente_geral(parametro):
    try:
        resultado = db.execute('SELECT * FROM cliente WHERE lower(nome) LIKE %s OR lower(email) LIKE %s OR telefone LIKE %s OR cpf LIKE %s OR cnpj LIKE %s', (f"%{parametro.lower()}%", f"%{parametro.lower()}%", f"%{parametro.lower()}%", f"%{parametro.lower()}%", f"%{parametro.lower()}%"))
        if len(resultado)>0:
            return criar_lista_cliente(resultado)
        else:
            return []
    except:
        return Exception
    
def pesquisar_veiculo_geral(parametro):
    try:
        resultado = db.execute('SELECT * FROM veiculo WHERE lower(id_veiculo) LIKE %s OR lower(placa) LIKE %s OR lower(chassi) LIKE %s OR id_cliente LIKE %s', (f"%{parametro.lower()}%", f"%{parametro.lower()}%", f"%{parametro.lower()}%", f"%{parametro.lower()}%"))
        if len(resultado)>0:
            return criar_lista_veiculo(resultado)
        else:
            return []
    except:
        return Exception
    
def pesquisar_ordem_geral(parametro):
    try:
        resultado = db.execute('select o.id_ordem, sum(ts.valor), v.placa, concat(c.nome,c.razao_social) from ordem as o left join tipo_servico_ordem as tso on tso.id_ordem = o.id_ordem left join tipo_servico as ts on ts.id_servico = tso.id_servico left join veiculo as v on o.id_veiculo=v.id_veiculo left join cliente as c on o.id_cliente=c.id_cliente where o.id_ordem = %s or lower(v.placa) = %s or lower(c.razao_social) = %s or lower(c.nome) = %s group by o.id_ordem', (parametro, parametro, parametro, parametro,))
        if len(resultado)>0:
            return criar_lista_ordem(resultado)
        else:
            return []
    except:
        return Exception

def pesquisar_veiculo_cliente(parametro):
    try:
        resultado = db.execute('SELECT * FROM veiculo WHERE id_cliente = %s', (parametro,))
        if len(resultado)>0:
            return criar_lista_veiculo(resultado)
        else:
            return []
    except:
        return Exception
    
def get_tipos_servicos():
    resultado = db.fullget('select * from tipo_servico')
    lista_servicos = []
    for item in resultado:
        lista_servicos.append({'id_servico':item[0], 'nome':item[1], 'valor':item[2]})
    return lista_servicos

def get_pecas():
    resultado = db.fullget('select * from peca')
    lista_pecas = []
    for peca in resultado:
        lista_pecas.append({'id_peca':peca[0], 'nome':peca[1], 'qtd':peca[2], 'valor':peca[3]})
    return lista_pecas