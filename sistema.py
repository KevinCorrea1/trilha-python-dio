from abc import ABC, abstractmethod 
from datetime import datetime
from typing import Any

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, telefone, email, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.email = email

class PessoaJuridica(Cliente):
    def __init__(self, nome, cnpj, razao_social, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cnpj = cnpj
        self.razao_social = razao_social

class Conta:
    def __init__(self, agencia, conta, saldo):
        self.agencia = agencia
        self.conta = conta
        self.saldo = saldo
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, agencia, cliente):
        return cls(agencia, len(cliente.contas) + 1, 0)

    def sacar(self, valor):
        if valor > self.saldo:
            print("Operação falhou! O valor de saque excede o saldo.")
            return False
        elif valor > 0:
            self.saldo -= valor
            print("Saque realizado com sucesso.")
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print("Depósito realizado com sucesso.")
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False

class ContaCorrente(Conta):
    def __init__(self, agencia, conta, saldo, limite=500, limite_saque=3):
        super().__init__(agencia, conta, saldo)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])
        excedeu_limite = valor > self.limite
        excedeu_saldo = valor > self.saldo
        excedeu_saques = numero_saques >= self.limite_saque
        if excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")
        elif excedeu_saldo:
            print("Operação falhou! O valor do saque excede o saldo.")
        elif excedeu_saques:
            print("Operação falhou! Número de saques excedido.")
        elif valor > 0:
            self.saldo -= valor
            print("Saque realizado com sucesso.")
            return True
        else:
            return super().sacar(valor)

    def __str__(self):
        return f"""\
        Agência: {self.agencia}
        Conta: {self.conta}
        Saldo: {self.saldo}"""

class ContaPoupanca(Conta):
    def __init__(self, agencia, conta, saldo, rendimento):
        super().__init__(agencia, conta, saldo)
        self.rendimento = rendimento

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            'data': datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor
        })

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self._valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self._valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

import textwrap

def depositar(clientes):
    cpf = input("CPF: ")
    cliente = filtrar_clientes(cpf, clientes)
    if not cliente:
        print("Não foi encontrado um cliente com este CPF.")
        return
    valor = float(input("Quanto deseja depositar? "))
    transacao = Deposito(valor)
    conta = recuperar_conta(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def filtrar_clientes(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta(cliente):
    if not cliente.contas:
        print("Ainda não existem contas. Cadastre uma conta para prosseguir.")
        return
    return cliente.contas[0]

def sacar(clientes):
    cpf = input("CPF: ")
    cliente = filtrar_clientes(cpf, clientes)
    if not cliente:
        print("Não foi encontrado um cliente com este CPF.")
        return
    valor = float(input("Quanto deseja sacar? "))
    transacao = Saque(valor)
    conta = recuperar_conta(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("CPF: ")
    cliente = filtrar_clientes(cpf, clientes)
    if not cliente:
        print("Não foi encontrado um cliente com este CPF.")
        return
    conta = recuperar_conta(cliente)
    if not conta:
        return
    print("========== EXTRATO ==========")
    print(f"Na sua conta: {conta}")
    print(f"Saldo: {conta.saldo}")
    print(f"Transações: {conta.historico.transacoes}")
    print("========== FIM EXTRATO ==========")

def criar_contas(numero_contas, cliente, contas):
    for _ in range(numero_contas):
        conta = ContaCorrente.nova_conta(123, cliente)
        cliente.adicionar_conta(conta)
        contas.append(conta)
        print("Conta criada com sucesso. Seu código de acesso:", conta.conta)

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def nova_conta(clientes, contas):
    cpf = input("CPF (somente números): ")
    cliente = filtrar_clientes(cpf, clientes)
    if not cliente:
        print("Não foi encontrado um cliente com este CPF.")
        return
    print(f"Criando uma nova conta corrente para o cliente {cliente.nome}")
    criar_contas(1, cliente, contas)

def novo_usuario(clientes):
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ") 
    endereco = input("Informe o endereço: ")
    cpf = input("Informe o CPF: ")
    telefone = input("Informe o telefone: ")    
    email = input("Informe o email: ")
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, endereco=endereco, cpf=cpf, telefone=telefone, email=email)
    clientes.append(cliente)
    print("\n========== CADASTRO REALIZADO COM SUCESSO ==========")

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()
        if  opcao == 'd':
            depositar(clientes)
        elif opcao == 's':
            sacar(clientes)
        elif opcao == 'e':
            exibir_extrato(clientes)
        elif opcao == 'nc':
            nova_conta(clientes, contas)
        elif opcao == 'lc':
            listar_contas(contas)
        elif opcao == 'nu':
            novo_usuario(clientes)
        elif opcao == 'q':
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
