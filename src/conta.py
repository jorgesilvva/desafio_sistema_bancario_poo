from src.historico import Historico
from src.transacao import Saque, Deposito
from datetime import datetime, timedelta

class Conta:
    def __init__(self, cliente, numero, agencia='0001'):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()
        self.limite_diario = 500.0
        self.max_saques_diarios = 3
        self.ultimo_reset = datetime.now()
        cliente.adicionar_conta(self)

    def saldo(self):
        return self.saldo

    def adicionar_conta(self, cliente, numero):
        return Conta(cliente, numero)

    def sacar(self, valor):
        if valor <= 0 or valor > self.limite_diario or self.max_saques_diarios <= 0 or valor > self.saldo:
            return False
        
        now = datetime.now()
        if now.day != self.ultimo_reset.day:
            self.ultimo_reset = now
            self.max_saques_diarios = 3
            self.limite_diario = 500.0
        
        self.saldo -= valor
        self.historico.adicionar_transacao(Saque(valor))
        self.max_saques_diarios -= 1
        return True

    def depositar(self, valor):
        if valor <= 0:
            return False
        self.saldo += valor
        self.historico.adicionar_transacao(Deposito(valor))
        return True

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500.0, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques























# from src.historico import Historico
# from src.transacao import Saque, Deposito

# class Conta:
#     def __init__(self, cliente, numero, agencia='0001'):
#         self.saldo = 0.0
#         self.numero = numero
#         self.agencia = agencia
#         self.cliente = cliente
#         self.historico = Historico()
#         cliente.adicionar_conta(self)

#     def saldo(self):
#         return self.saldo

#     def adicionar_conta(cliente, numero):
#         return Conta(cliente, numero)

#     def sacar(self, valor):
#         if valor <= 0 or valor > self.saldo:
#             return False
#         self.saldo -= valor
#         self.historico.adicionar_transacao(Saque(valor))
#         return True

#     def depositar(self, valor):
#         if valor <= 0:
#             return False
#         self.saldo += valor
#         self.historico.adicionar_transacao(Deposito(valor))
#         return True

# class ContaCorrente(Conta):
#     def __init__(self, cliente, numero, limite=500.0, limite_saques=3):
#         super().__init__(cliente, numero)
#         self.limite = limite
#         self.limite_saques = limite_saques
