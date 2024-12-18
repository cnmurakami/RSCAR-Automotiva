from flask_mysqldb import MySQL
from flask import Flask
from abc import ABC
import db_operations as db
import functions as f

class Rscar(ABC):
    def enviar(self):
        return ''
    def salvar(self):
        return ''

class Cliente(Rscar):
    #id_cliente, cpf, cnpj, nome, razao_social, endereco, telefone, email
    def __init__ (self, id_cliente:str = '', cpf:str = '', cnpj:str = '', nome:str = '', razao_social:str = '', endereco:str = '', telefone:str = '', email:str = ''):
        if id_cliente != '':
            resultado = db.execute('select * from cliente where id_cliente = %s', (id_cliente,))
            if len(resultado) == 1:
                self.id_cliente = id_cliente
                self.cpf = resultado[0][1]
                self.cnpj = resultado[0][2]
                self.nome = resultado[0][3]
                self.razao_social = resultado[0][4]
                self.endereco = resultado[0][5]
                self.telefone = resultado[0][6]
                self.email = resultado[0][7]
            else:
                raise Exception
        else:
            self.id_cliente = id_cliente
            self.cpf = cpf
            self.cnpj = cnpj
            self.nome = nome
            self.razao_social = razao_social
            self.endereco = endereco
            self.telefone = telefone
            self.email = email

    @property
    def id_cliente(self):
        return self._id_cliente
    
    @id_cliente.setter
    def id_cliente (self, novo_id_cliente):
        self._id_cliente = novo_id_cliente

    @property
    def cpf(self):
        return self._cpf
    
    @cpf.setter
    def cpf (self, novo_cpf):
        self._cpf = novo_cpf
  
    @property
    def cnpj(self):
        return self._cnpj
    
    @cnpj.setter
    def cnpj (self, novo_cnpj):
        self._cnpj = novo_cnpj

    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome (self, novo_nome):
        self._nome = novo_nome

    @property
    def razao_social(self):
        return self._razao_social
    
    @razao_social.setter
    def razao_social (self, novo_razao_social):
        self._razao_social = novo_razao_social
        
    @property
    def endereco(self):
        return self._endereco
    
    @endereco.setter
    def endereco (self, novo_endereco):
        self._endereco = novo_endereco

    @property
    def telefone(self):
        return self._telefone
    
    @telefone.setter
    def telefone (self, novo_telefone):
        self._telefone = novo_telefone

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email (self, novo_email):
        self._email = novo_email
    
    def endereco_completo(self):
        #'MeuLogradouro;;000;;MeuComplmento;;MinhaCidade;;SP;;01001-000'
        try:
            logradouro, numero, complemento, bairro, cidade, estado, cep = self.endereco.split(';;')
            return {'logradouro':logradouro, 'numero':numero, 'complemento':complemento, 'bairro':bairro, 'cidade':cidade, 'estado':estado, 'cep':cep}
        except:
            return {'endereco':self.endereco}
    
    def salvar(self):
        try:
            db.procedure('inserir_cliente', (self.cpf, self.cnpj, self.nome, self.razao_social, self.endereco, self.telefone, self.email))
        except:
            print ('ERRO NO INSERT')
            raise Exception
    
    def enviar(self):
        info = {}
        info['id_cliente'] = self.id_cliente
        info['cpf'] = self.cpf
        info['cnpj'] = self.cnpj
        info['nome'] = self.nome
        info['razao_social'] = self.razao_social
        info.update(self.endereco_completo())
        info['telefone'] = self.telefone
        info['email'] = self.email
        return info

class Veiculo(Rscar):
    #id_veiculo, id_cliente, placa, chassi, marca, modelo, ano_fabricacao, ano_modelo, cor
    def __init__ (self, id_veiculo:str = '', id_cliente:str = '', placa:str = '', chassi:str = '', marca:str = '', modelo:str = '', ano_fabricacao:str = '', ano_modelo:str = '', cor:str = ''):
        #lista completa: id_veiculo, id_cliente, cpf, cnpj, nome, razao_social, endereco, telefone, email
        if id_veiculo != '':
            resultado = db.execute('select * from veiculo where id_veiculo = %s', (id_veiculo,))
            if len(resultado) == 1:
                self.id_veiculo = id_veiculo
                self.id_cliente = resultado[0][1]
                self.placa = resultado[0][2]
                self.chassi = resultado[0][3]
                self.marca = resultado[0][4]
                self.modelo = resultado[0][5]
                self.ano_fabricacao = resultado[0][6]
                self.ano_modelo = resultado[0][7]
                self.cor = resultado[0][8]
            else:
                raise
        else:
            self.id_veiculo = ''
            self.id_cliente = id_cliente
            self.placa = placa
            self.chassi = chassi
            self.marca = marca
            self.modelo = modelo
            self.ano_fabricacao = ano_fabricacao
            self.ano_modelo = ano_modelo
            self.cor = cor

    @property
    def id_veiculo(self):
        return self._id_veiculo

    @id_veiculo.setter
    def id_veiculo(self, novo_id_veiculo):
        self._id_veiculo = novo_id_veiculo
    

    @property
    def id_cliente(self):
        return self._id_cliente

    @id_cliente.setter
    def id_cliente(self, novo_id_cliente):
        self._id_cliente = novo_id_cliente
    

    @property
    def placa(self):
        return self._placa

    @placa.setter
    def placa(self, novo_placa):
        self._placa = novo_placa
    

    @property
    def chassi(self):
        return self._chassi

    @chassi.setter
    def chassi(self, novo_chassi):
        self._chassi = novo_chassi
    

    @property
    def marca(self):
        return self._marca

    @marca.setter
    def marca(self, novo_marca):
        self._marca = novo_marca
    

    @property
    def modelo(self):
        return self._modelo

    @modelo.setter
    def modelo(self, novo_modelo):
        self._modelo = novo_modelo
    

    @property
    def ano_fabricacao(self):
        return self._ano_fabricacao

    @ano_fabricacao.setter
    def ano_fabricacao(self, novo_ano_fabricacao):
        self._ano_fabricacao = novo_ano_fabricacao
    

    @property
    def ano_modelo(self):
        return self._ano_modelo

    @ano_modelo.setter
    def ano_modelo(self, novo_ano_modelo):
        self._ano_modelo = novo_ano_modelo
    

    @property
    def cor(self):
        return self._cor

    @cor.setter
    def cor(self, novo_cor):
        self._cor = novo_cor

    
    def salvar(self):
        try:
            db.procedure('inserir_veiculo', (self.id_cliente, self.placa, self.chassi, self.marca, self.modelo, self.ano_fabricacao, self.ano_modelo, self.cor))
        except:
            print ('ERRO NO INSERT')
            raise Exception
    
    def enviar(self):
        info = {}
        info['id_veiculo'] = self.id_veiculo
        info['id_cliente'] = self.id_cliente
        info['placa'] = self.placa
        info['chassi'] = self.chassi
        info['marca'] = self.marca
        info['modelo'] = self.modelo
        info['ano_fabricacao'] = self.ano_fabricacao
        info['ano_modelo'] = self.ano_modelo
        info['cor'] = self.cor
        return info

class Ordem(ABC):
    def __init__ (self, id_ordem:str = '', id_cliente:str = '', id_veiculo:str = ''):
        if id_ordem != '':
            resultado = db.execute('select * from ordem where id_ordem = %s', (id_ordem,))
            if len(resultado) >= 1:
                self.id_ordem = id_ordem
                self.id_cliente = resultado[0][1]
                self.id_veiculo = resultado[0][2]
                self.id_status = resultado[0][3]
                self.ativo = bool(resultado[0][4])
            else:
                raise Exception
        else:
            self.id_ordem = id_ordem
            self.id_cliente = id_cliente
            self.id_veiculo = id_veiculo
            self.id_status = 0
            self.ativo = True
    
    @property
    def id_ordem(self):
        return self._id_ordem
    
    @id_ordem.setter
    def id_ordem (self, novo_id_ordem):
        self._id_ordem = novo_id_ordem
    
    @property
    def id_cliente(self):
        return self._id_cliente
    
    @id_cliente.setter
    def id_cliente (self, novo_id_cliente):
        self._id_cliente = novo_id_cliente
    
    @property
    def id_veiculo(self):
        return self._id_veiculo
    
    @id_veiculo.setter
    def id_veiculo (self, novo_id_veiculo):
        self._id_veiculo = novo_id_veiculo
    
    @property
    def id_status(self):
        return self._id_status
    
    @id_status.setter
    def id_status (self, novo_id_status):
        self._id_status = novo_id_status

    def enviar(self):
        info = {}
        info['id_ordem'] = self.id_ordem
        info['id_cliente'] = self.id_cliente
        info['id_veiculo'] = self.id_veiculo
        info['id_status'] = self.id_status
        info['ativo'] = self.ativo
        return info

    def salvar(self):
        try:
            db.insert('insert into ordem (id_cliente, id_veiculo) values (%s, %s)', (self.id_cliente, self.id_veiculo,))
        except:
            print('ERRO no INSERT')
            raise Exception
    
    def localizar_ultima_ordem(self):
        resultado = db.execute('select * from ordem where id_veiculo = %s or id_cliente = %s order by id_ordem desc', (self.id_veiculo, self.id_cliente))
        if len(resultado) >= 1:
            self.id_ordem = resultado[0][0]
        else:
            raise Exception
        
    def salvar_servicos(self, servicos):
        query = 'insert into tipo_servico_ordem (id_ordem, id_servico) values '
        args = []
        for i in servicos:
            query += '(%s, %s), '
            args.append(str(self.id_ordem))
            args.append(i)
        args = tuple(args,)
        query = query[:-2]
        db.insert(query, args)
        
    def editar_servicos(self, servicos):
        db.execute('delete from tipo_servico_ordem where id_ordem = %s', (self.id_ordem,))
        self.salvar_servicos(servicos)
        
    def recuperar_servicos(self):
        resultado = db.execute('select * from tipo_servico_ordem where id_ordem = %s',(self.id_ordem,))
        lista_servicos = []
        for i in resultado:
            lista_servicos.append(i[2])
        return lista_servicos
    
    def salvar_pecas(self, pecas):
        query = 'insert into peca_ordem (id_ordem, id_peca, qtd) values '
        args = []
        for i in pecas:
            query += '(%s, %s ,%s), '
            args.append(str(self.id_ordem))
            args.append(i[0])
            args.append(i[1])
            peca = Peca(i[0])
            peca.remover_peca(i[1])
        args = tuple(args,)
        query = query[:-2]
        db.insert(query, args)

    
    def editar_pecas(self, pecas):
        db.execute('delete from peca_ordem where id_ordem = %s', (self.id_ordem,))
        self.salvar_pecas(pecas)

    def recuperar_pecas(self):
        resultado = db.execute('select * from peca_ordem where id_ordem = %s',(self.id_ordem,))
        lista_pecas = {}
        for i in resultado:
            lista_pecas[i[2]]=i[3]
        return lista_pecas
    
    def recuperar_status(self):
        resultado = db.execute('select status from status_servico where id_status = %s',(self.id_status,))
        return resultado[0][0]
    
    def avancar_status(self):
        novo_status = str(int(self.id_status)+1)
        if novo_status == '2':
            self.ativo = False
        db.insert('update ordem set id_status = %s, ativo = %s where id_ordem = %s', (novo_status, int(self.ativo), self.id_ordem,))
        self.id_status = db.execute('select id_status from ordem where id_ordem = %s', (self.id_ordem,))[0][0]
        return

    def cancelar(self):
        self.id_status = '-1'
        self.ativo = False
        pecas = self.recuperar_pecas()
        for i in pecas.keys():
            peca = Peca(id_peca = i)
            peca.adicionar_peca(pecas[i])
        db.insert('update ordem set id_status = %s, ativo = %s where id_ordem = %s', (self.id_status, int(self.ativo), self.id_ordem,))
        return

    def enviar_completo(self):
        consulta = db.execute(
            """select v.placa, concat(c.nome,c.razao_social), sum(ts.valor)
            FROM ordem AS o
                LEFT JOIN tipo_servico_ordem AS tso ON tso.id_ordem = o.id_ordem
                LEFT JOIN tipo_servico AS ts ON ts.id_servico = tso.id_servico
                LEFT JOIN veiculo AS v ON o.id_veiculo=v.id_veiculo
                LEFT JOIN cliente AS c ON o.id_cliente=c.id_cliente
            where o.id_ordem = %s""",
            (self.id_ordem,))
        dicionario = self.enviar()
        dicionario['nome'] = consulta[0][1]
        dicionario['placa'] = consulta[0][0]
        dicionario['total'] = consulta[0][2]
        lista_pecas = self.recuperar_pecas()
        pecas_total = 0
        if len(lista_pecas) > 0:
            for i in lista_pecas.keys():
                pecas_total += Peca(id_peca=i).valor * lista_pecas[i]
        if dicionario['total'] == None or dicionario['total'] == 'None':
            dicionario['total'] = '0.00'
        dicionario['total'] = float(dicionario['total'])+float(pecas_total)
        dicionario['total'] = str(f'{dicionario['total']:.2f}').replace('.', ',')
        dicionario['status'] = self.recuperar_status()
        return dicionario

class Peca(ABC):
    def __init__ (self, id_peca:str = '', nome: str = '', qtd:str = '', valor:str = ''):
        if id_peca != '':
            resultado = db.execute('select * from peca where id_peca = %s', (id_peca,))
            if len(resultado) >= 1:
                self.id_peca = resultado[0][0]
                self.nome = resultado[0][1]
                self.qtd = resultado[0][2]
                self.valor = resultado[0][3]
        else:
            self.id_peca = id_peca
            self.nome = nome
            self.qtd = qtd
            self.valor = valor

    @property
    def id_peca(self):
        return self._id_peca
    
    @id_peca.setter
    def id_peca(self, novo_id_peca):
        self._id_peca = novo_id_peca
    
    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, novo_nome):
        self._nome = novo_nome
    
    @property
    def qtd(self):
        return self._qtd
    
    @qtd.setter
    def qtd(self, novo_qtd):
        self._qtd = novo_qtd
    
    @property
    def valor(self):
        return self._valor
    
    @valor.setter
    def valor(self, novo_valor):
        self._valor = novo_valor
    
    def adicionar_peca(self, qtd_to_change):
        db.insert('UPDATE peca SET qtd = qtd + %s where id_peca = %s', (str(qtd_to_change), self.id_peca,))
        self.qtd = db.execute('SELECT qtd FROM peca WHERE id_peca = %s', (self.id_peca,))[0][0]
    
    def remover_peca(self, qtd_to_change):
        db.insert('UPDATE peca SET qtd = qtd - %s where id_peca = %s', (str(qtd_to_change), self.id_peca,))
        self.qtd = db.execute('SELECT qtd FROM peca WHERE id_peca = %s', (self.id_peca,))[0][0]