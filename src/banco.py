import regex
from src.cliente import PessoaFisica
from src.conta import Conta, ContaCorrente
from src.transacao import Deposito, Saque
from datetime import datetime

usuarios = []
contas = []


def validar_data(data):
    try:
        datetime.strptime(data, '%d/%m/%Y')
        return True
    except ValueError:
        return False


def validar_cpf(cpf):
    if not cpf.isdigit() or len(cpf) != 11:
        return False
    
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    if digito1 != int(cpf[9]):
        return False
    
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    if digito2 != int(cpf[10]):
        return False
    
    return True


def cadastrar_usuario(nome, data_nascimento, cpf, endereco):
    if not regex.match(r'^[\p{L} \s\'-]+$', nome):
        print('Nome de usuário inválido. Digite apenas letras e espaços.')
        return

    cpf_numeros = regex.sub(r'\D', '', cpf)

    if any(user.cpf == cpf_numeros for user in usuarios):
        print('CPF já cadastrado para outro usuário.')
        return

    usuario = PessoaFisica(nome, data_nascimento, cpf_numeros, endereco)
    usuarios.append(usuario)
    print(f'Usuário {nome} cadastrado com sucesso.')


def cadastrar_conta(cpf, numero_conta):
    usuario_encontrado = None
    for user in usuarios:
        if user.cpf == cpf:
            usuario_encontrado = user
            break

    if usuario_encontrado:
        conta = ContaCorrente(usuario_encontrado, numero_conta)
        contas.append(conta)
        print(f'Conta bancária {numero_conta} cadastrada para o usuário {usuario_encontrado.nome}.')
    else:
        print(f'Usuário com CPF {cpf} não encontrado.')


def depositar(numero_conta, valor):
    if valor <= 0:
        print('Valor de depósito inválido. O valor deve ser maior que zero.')
        return

    conta_encontrada = next((conta for conta in contas if conta.numero == numero_conta), None)
    
    if not conta_encontrada:
        print(f'Conta bancária {numero_conta} não encontrada.')
        return

    conta_encontrada.depositar(valor)
    print(f'Depósito de R$ {valor:.2f} realizado na conta {numero_conta}.')


def sacar(numero_conta, valor):
    conta_encontrada = next((conta for conta in contas if conta.numero == numero_conta), None)
    
    if not conta_encontrada:
        print(f'Conta bancária {numero_conta} não encontrada.')
        return

    if conta_encontrada.sacar(valor):
        print(f'Saque de R$ {valor:.2f} realizado na conta {numero_conta}.')
    else:
        print(f'Não foi possível realizar o saque de R$ {valor:.2f} na conta {numero_conta}.')


def extrato(numero_conta):
    conta_encontrada = next((conta for conta in contas if conta.numero == numero_conta), None)

    if not conta_encontrada:
        print(f'Conta bancária {numero_conta} não encontrada.')
        return

    print(f'Extrato da conta {numero_conta}:')
    print('-' * 40)

    movimentacoes = conta_encontrada.historico.transacoes

    if not movimentacoes:
        print('Nenhuma movimentação realizada.')
    else:
        print('Movimentações:')
        print('-' * 40)
        for movimentacao in movimentacoes:
            if isinstance(movimentacao, Deposito):
                print(f'Depósito de R$ {movimentacao.valor:.2f}')
            elif isinstance(movimentacao, Saque):
                print(f'Saque de R$ {movimentacao.valor:.2f}')

    print('-' * 40)
    print(f'Saldo atual: R$ {conta_encontrada.saldo:.2f}')
    print('-' * 40)


def menu_principal():
    while True:
        print('\nMenu:\n')
        print('1. Cadastrar Cliente')
        print('2. Cadastrar Conta Bancária')
        print('3. Depositar')
        print('4. Sacar')
        print('5. Extrato')
        print('6. Sair')

        escolha = input('\nEscolha uma opção: ')

        if escolha == '1':
            nome = input('\nDigite o nome do cliente: ')
            if not nome.replace(' ', '').isalpha():
                print('Nome inválido. O nome deve conter apenas letras, espaços e acentos.')
                continue

            data_nascimento = input('Digite a data de nascimento (DD/MM/AAAA): ')
            if not validar_data(data_nascimento):
                print('Data de nascimento inválida ou fora do formato DD/MM/AAAA.')
                continue

            cpf = input('Digite o CPF (somente números): ')
            if not validar_cpf(cpf):
                print('CPF inválido ou com formato inválido. O CPF deve conter exatamente 11 números.')
                continue

            endereco = input('Digite o endereço no formato (Logradouro, nº - Bairro - Cidade/UF): ')
            cadastrar_usuario(nome, data_nascimento, cpf, endereco)

        elif escolha == '2':
            cpf = input('\nDigite o CPF (somente números) do usuário para vincular a conta: ')
            if not validar_cpf(cpf):
                print('CPF inválido ou com formato inválido. O CPF deve conter exatamente 11 números.')
                continue

            numero_conta = input('Digite o número da conta bancária: ')
            cadastrar_conta(cpf, numero_conta)

        elif escolha == '3':
            numero_conta = input('\nDigite o número da conta para depósito: ')
            try:
                valor = float(input('Digite o valor do depósito: '))
                depositar(numero_conta, valor)
            except ValueError:
                print('Valor inválido. Certifique-se de digitar um número válido para o depósito.')

        elif escolha == '4':
            numero_conta = input('\nDigite o número da conta para saque: ')
            try:
                valor = float(input('Digite o valor do saque: '))
                sacar(numero_conta, valor)
            except ValueError:
                print('Valor inválido. Certifique-se de digitar um número válido para o saque.')

        elif escolha == '5':
            numero_conta = input('\nDigite o número da conta para extrato: ')
            if numero_conta.isdigit():
                extrato(numero_conta)
            else:
                print('Número de conta inválido. Certifique-se de digitar apenas números.')

        elif escolha == '6':
            print('Saindo do programa...')
            break

        else:
            print('\nOpção inválida. Por favor, escolha uma opção válida.')