from banco_de_dados import *
from operacoes_banco import *


def criar_conta(numero_conta: str, nome_cliente: str) -> tuple[int, dict]:
    """
    Cria conta

    Args:
        numero_conta (str): Numero da conta a ser criada
        nome_cliente (str): Nome do usuário da conta a ser criada

    Returns:
        tuple[int, dict]: Tupla cujos elementos são: número da conta criada, e um dicionário com o nome do cliente e o saldo da nova conta criada

    Examples:
        #Preparando o arquivo 'contas.csv' para realização dos testes
        >>> salvar_contas_para_csv("contas.csv", {})

        >>> criar_conta("0001", "Joao")
        ('0001', {'cliente': 'Joao', 'saldo': 0.0})

        >>> criar_conta("0002", "Maria") 
        ('0002', {'cliente': 'Maria', 'saldo': 0.0})

        >>> criar_conta("0002","Maria")
        'Erro: Conta ja existente'
    """
    diconario_contas = carregar_contas_de_csv('contas.csv')
    if numero_conta in diconario_contas.keys():
        return "Erro: Conta ja existente"     
    usuario_novo = {"cliente":nome_cliente , "saldo": 0.00}
    diconario_contas[numero_conta] = usuario_novo
    salvar_contas_para_csv('contas.csv', diconario_contas)
    return (numero_conta,{"cliente":nome_cliente , "saldo": 0.00})


def depositar(numero_conta: str, valor: float) -> tuple[bool, str]:
    """
        Função destinada ao cliente realizar um depósito em sua conta
    Args:
        numero_conta (str): Número da conta a ser depositado o saldo
        valor (float): Valor a ser depositado na conta

    Returns:
        tuple[bool, str]: Retorna uma tupla, composta por dois elementos: um valor 
        booleano e uma string indicando sucesso ou falha no depósito
    Examples:
    #Preparando o arquivo 'contas.csv' para realização dos testes
        >>> salvar_contas_para_csv("contas.csv", {})
        >>> # Criar conta para os testes
        >>> criar_conta("0001", "Joao")
        ('0001', {'cliente': 'Joao', 'saldo': 0.0})
        >>> depositar("0001", 50)  # conta existente
        (True, 'Deposito realizado com sucesso!')
        >>> consultar_saldo("0001")
        50.0

        >>> depositar("9999", 100)  # conta inexistente
        (False, 'Erro: conta inexistente!')

        >>> depositar("0001", -10)  # valor negativo
        (False, 'Erro: Tentativa de adicionar um saldo negativo')
    """
    if valor < 0:
        return (False,"Erro: Tentativa de adicionar um saldo negativo")
    dicionario_contas = carregar_contas_de_csv('contas.csv')
 
    if numero_conta in dicionario_contas:
            dicionario_contas[numero_conta]["saldo"] += valor
            salvar_contas_para_csv('contas.csv',dicionario_contas)
            return (True,"Deposito realizado com sucesso!")
    else:
            return (False,"Erro: conta inexistente!")

def consultar_saldo(numero_conta: str) -> float | None:
    """
    Função destinada a consultar saldo de uma conta

    Args:
        numero_conta (str): Número da conta com saldo a ser consultado

    Returns:
        float | None: Retorna o saldo(float) caso a conta exista, e retorna None caso
        a conta seja inexisnte
    Examples:
        # Preparando o arquivo 'contas.csv' para realização dos testes
        >>> salvar_contas_para_csv("contas.csv", {})
        >>> # Criar conta e adicionar saldo
        >>> criar_conta("0001", "Joao")
        ('0001', {'cliente': 'Joao', 'saldo': 0.0})
        >>> depositar("0001", 200.0)
        (True, 'Deposito realizado com sucesso!')
        >>> consultar_saldo("0001")
        200.0

        >>> consultar_saldo("9999") 
        
        
    """
    dicionario_contas = carregar_contas_de_csv('contas.csv')
    if numero_conta in dicionario_contas.keys():
            return dicionario_contas[numero_conta]["saldo"]
    else:
            return None


def realizar_transferencia(conta_origem: str, conta_destino: str, valor: float) -> tuple[bool, str]:
    """
    Função que realiza uma transferência entre duas contas.

    Args:
        conta_origem (str): Número da conta cujo saldo será retirado
        conta_destino (str): Número da conta cujo saldo será depositado
        valor (float): Valor a ser transferido entre as duas contas

    Returns:
        tuple[bool, str]: Tupla composta por dois elementos:
        bool - um valor booleano indicando sucesso(True) ou falha(False) no transferencia
        str - Um texto(str) indicando sucesso ou falha na transferencia
Examples:
#Preparando o arquivo 'contas.csv' para realização dos testes
    >>> salvar_contas_para_csv("contas.csv", {})
>>> _ = criar_conta("0001", "Joao")
>>> _ = criar_conta("0002", "Maria")
>>> depositar("0001", 100.0)
(True, 'Deposito realizado com sucesso!')
>>> realizar_transferencia("0001", "0002", 50.0)
(True, 'Transferência realizada com sucesso!')
>>> consultar_saldo("0001")
50.0
>>> consultar_saldo("0002")
50.0

>>> realizar_transferencia("0001", "9999", 10.0)
(False, 'Erro: Conta destino inexistente!')

>>> realizar_transferencia("9999", "0002", 10.0)
(False, 'Erro: Conta origem inexistente!')

>>> realizar_transferencia("0001", "0002", -5.0)
(False, 'Erro: Tentativa de transferir saldo negativo')

>>> realizar_transferencia("0001", "0002", 200.0)
(False, 'Erro: Saldo insuficiente')

    """
    
    dicionario_contas = carregar_contas_de_csv('contas.csv')
    if conta_origem not in dicionario_contas:
        return (False, "Erro: Conta origem inexistente!")
    elif conta_destino not in dicionario_contas:
        return (False, "Erro: Conta destino inexistente!")
    elif valor < 0:
        return (False, "Erro: Tentativa de transferir saldo negativo")
    elif dicionario_contas[conta_origem]["saldo"] < valor:
        return (False, "Erro: Saldo insuficiente")
    else:
        dicionario_contas[conta_origem]["saldo"] -= valor
        dicionario_contas[conta_destino]["saldo"] += valor
        salvar_contas_para_csv('contas.csv',dicionario_contas)
        return (True, "Transferência realizada com sucesso!")


