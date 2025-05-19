import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= 0:
            print("\n@@@ Operacao falhou! Valor invalido. @@@")
            return False

        if valor > self._saldo:
            print("\n@@@ Operacao falhou! Saldo insuficiente. @@@")
            return False

        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Operacao falhou! Valor invalido. @@@")
            return False

        self._saldo += valor
        print("\n=== Deposito realizado com sucesso! ===")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([
            t for t in self.historico.transacoes if t["tipo"] == Saque.__name__
        ])

        if numero_saques >= self._limite_saques:
            print("\n@@@ Operacao falhou! Limite de saques excedido. @@@")
            return False

        if valor > self._limite:
            print("\n@@@ Operacao falhou! Valor excede o limite permitido. @@@")
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"""
Agencia:	{self.agencia}
Conta:		{self.numero}
Titular:	{self.cliente.nome}
"""


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
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
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


# Utilitarios

def menu():
    opcoes = """
=============== MENU ===============
[d] Depositar
[s] Sacar
[e] Extrato
[nc] Nova conta
[lc] Listar contas
[nu] Novo usuario
[q] Sair
=> """
    return input(textwrap.dedent(opcoes))


def filtrar_cliente(cpf, clientes):
    return next((c for c in clientes if c.cpf == cpf), None)


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente nao possui conta! @@@")
        return

    print("\nContas disponiveis:")
    for i, conta in enumerate(cliente.contas, 1):
        print(f"[{i}] Agencia: {conta.agencia} - Conta: {conta.numero}")

    try:
        indice = int(input("Escolha a conta: ")) - 1
        return cliente.contas[indice]
    except (ValueError, IndexError):
        print("\n@@@ Opcao invalida. @@@")
        return


def depositar(clientes):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente nao encontrado! @@@")
        return

    try:
        valor = float(input("Valor do deposito: "))
    except ValueError:
        print("\n@@@ Valor invalido. @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, Deposito(valor))


def sacar(clientes):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente nao encontrado! @@@")
        return

    try:
        valor = float(input("Valor do saque: "))
    except ValueError:
        print("\n@@@ Valor invalido. @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, Saque(valor))


def exibir_extrato(clientes):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente nao encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n=========== EXTRATO ===========")
    if not conta.historico.transacoes:
        print("Nao foram realizadas movimentacoes.")
    else:
        for t in conta.historico.transacoes:
            print(f"{t['tipo']} em {t['data']} - R$ {t['valor']:.2f}")

    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("================================")


def criar_cliente(clientes):
    cpf = input("CPF (somente numeros): ")
    if filtrar_cliente(cpf, clientes):
        print("\n@@@ Ja existe cliente com esse CPF! @@@")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereco (logradouro, nro - bairro - cidade/UF): ")

    clientes.append(PessoaFisica(nome, data_nascimento, cpf, endereco))
    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente nao encontrado. Criacao de conta encerrada. @@@")
        return

    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            break
        else:
            print("\n@@@ Opcao invalida. Tente novamente. @@@")


if __name__ == "__main__":
    main()
