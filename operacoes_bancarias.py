"""Modulo de funções para operações bancárias

    Raises:
        AccountError: Erro levantado quando o usuário se refere a uma conta que não existe
    """
from banco_de_dados import carregar_contas_de_csv,salvar_contas_para_csv
class AccountError(Exception):
    """Erros relacionados a(s conta(s) utilizada(s)"""


import logging

logging.basicConfig(level=logging.INFO,filename="errors.log",filemode="a",format="%(asctime)s;%(levelname)s;%(name)s;%(message)s",force=True)
logaccount=logging.getLogger("documentacao_conta")
logmoney=logging.getLogger("documentacao_dinheiro")


def criar_conta(numero_conta: str, nome_cliente: str) -> tuple[int, dict]:
    """Cria uma nova conta. Se a conta já existe retorna um erro

    Args:
        numero_conta (str): valor numérico representativo da conta. Deve ser único para cada cliente
        nome_cliente (str): nome do cliente dono da conta

    Raises:
        AccountError: Erro consequente da tentativa de criar uma conta já existente

    Returns:
        tuple[int, dict]: Explicita a informação que foi adicionada ao CSV
    """
    numb=("0","1","2","3","4","5","6","7","8","9")
    dicionario=carregar_contas_de_csv(r"contas.csv")
    if numero_conta.rjust(4,"0") in dicionario.keys():
        logaccount.info("Tentativa de criar uma conta ja existente")
        raise AccountError("Uma conta não pode ser criada com um número que já existe")
    
    elif numero_conta.isnumeric() and len(numero_conta)<=4 and not nome_cliente.startswith(numb):
        numero_conta=numero_conta.rjust(4,"0")
        dicionario.update({numero_conta:{"cliente":f"{nome_cliente}","saldo":0}})
        salvar_contas_para_csv(r"contas.csv",dicionario)
        return (numero_conta,{"cliente":f"{nome_cliente}","saldo":0.0})
    else: return "Conta inválida, uma conta deve ter no máximo 4 dígitos"

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
        logmoney.info("Tentativa de input de valor negativo")
        return (False,"Erro: Tentativa de adicionar um saldo negativo")
    dicionario_contas = carregar_contas_de_csv('contas.csv')
 
    if numero_conta in dicionario_contas:
            dicionario_contas[numero_conta]["saldo"] += valor
            salvar_contas_para_csv('contas.csv',dicionario_contas)
            return (True,"Deposito realizado com sucesso!")
    else:
            logaccount.info("Referencia a conta inexistente")
            return (False,"Erro: conta inexistente!")

def sacar(numero_conta: str, valor: float) -> tuple[bool, str]:
    """Remove valor do saldo da conta especificada desde que a conta existe e o valor seja positivo

    Args:
        numero_conta (str): valor numérico representativo da conta. Deve ser único para cada cliente
        valor (float): valor desejado para a operação. Deve ser sempre positivo

    Returns:
        tuple[bool, str]: Uma tupla descrevendo o sucesso ou falha da operação
    """
    dicionario=carregar_contas_de_csv(r"contas.csv")
    if dicionario[f"{numero_conta}"]["saldo"]-valor<0:
        logmoney("Tentativa de sacar mais do que o possivel")
        return (False, "Erro: saldo insuficiente para o saque") 
    elif valor <0:
        logmoney("Tentativa de input de valor negativo")
        return (False, "Erro: tentou sacar valor negativo")
    
    elif numero_conta in dicionario.keys():
        dicionario[f"{numero_conta}"]["saldo"]-=valor
        salvar_contas_para_csv(r"contas.csv",dicionario)
        return (True, "operação realizada")
    else:
        logaccount("Referencia a conta inexistente")
        return (False, "Erro: Conta especificada não existe")
    
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
            logaccount("Referencia a conta inexistente")
            return None
    
def somar_saldos_gerais( ) -> float:
    """Retorna a soma de todos os saldos das contas no banco

    Returns:
        float: Valor da soma de todos os saldos
    
    Examples:
    >>> somar_saldos_gerais()
    100.0

    """
    dicionario=carregar_contas_de_csv(r"contas.csv")
    somatorio=0
    for key in dicionario.keys():
        somatorio+=dicionario[key]["saldo"]
    return somatorio

def identificar_cliente_mais_rico( ) -> dict | None:
    """Procura o cliente com maior saldo e retorna o nome e saldo desse cliente

    Returns:
        dict | None: Caso o cliente exista retorna o dicionário com as informações do mesmo. Caso contrário retorna nada
    
    """
    dicionario=carregar_contas_de_csv(r"contas.csv")
    maximo=0
    for key in dicionario.keys():
        if dicionario[key]["saldo"]>maximo:
            maximo=dicionario[key]["saldo"]
            rico=key
    ricos=[]
    for key in dicionario.keys():
        if maximo!=0 and dicionario[key]["saldo"]==maximo:
            ricos.append(dicionario[key])
    if len(ricos)>1:
        return ricos
    else:
        try: return dicionario[rico]
        except: return None

def somar_saldos_em_lote(**kwargs) -> int:
    """deposita valores em diversas contas. Se uma conta não existir ou um valor ser inválido ignora e continua

    Returns:
        int: quantidade de operações que foram realizadas com sucesso
    """
    dicionario=carregar_contas_de_csv(r"contas.csv")
    tries=0
    for key in kwargs.keys():
        if kwargs[key] is not float:
            pass
        if kwargs[key]>=0:
            try: 
                dicionario[key]["saldo"]+=kwargs[key]
                tries+=1
                salvar_contas_para_csv(r"contas.csv",dicionario)
            except: logaccount("Referência a conta inexistente")
        else:
            logmoney("Tentativa de input de valor negativo")
    return tries

def subtrair_saldos_em_lote(**kwargs) -> int:
    """Realiza vários saques de contas simultâneamente, caso o valor seja inválido, o saldo seja insuficiente
    ou a conta não exista log o erro e continua

    Returns:
        int: número de operações que obtiveram sucesso
    """
    dicionario=carregar_contas_de_csv(r"contas.csv")
    tries=0
    for key in kwargs.keys():
        if kwargs[key] is not float:
            pass
        try:
                if kwargs[key]<0:
                    logmoney("Tentativa de input de valor negativo")
                elif dicionario[key]["saldo"]-kwargs[key]<0:
                    logmoney("Tentativa de saque maior do que disponível na conta")
                else:
                    dicionario[key]["saldo"]-=kwargs[key]
                    tries+=1
                    salvar_contas_para_csv(r"contas.csv",dicionario)
        except: logaccount("Referência a conta inexistente")
    return tries

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
    if conta_origem not in dicionario_contas.keys():
        logaccount("Referência a conta inexistente")
        return (False, "Erro: Conta origem inexistente!")
    elif conta_destino not in dicionario_contas.keys():
        logaccount("Referência a conta inexistente")
        return (False, "Erro: Conta destino inexistente!")
    elif valor < 0:
        logmoney("Tentativa de input negativo")
        return (False, "Erro: Tentativa de transferir saldo negativo")
    elif dicionario_contas[conta_origem]["saldo"] < valor:
        logmoney("Tentativa de transferência de um valor maior do que o disponível na conta")
        return (False, "Erro: Saldo insuficiente")
    else:
        dicionario_contas[conta_origem]["saldo"] -= valor
        dicionario_contas[conta_destino]["saldo"] += valor
        salvar_contas_para_csv('contas.csv',dicionario_contas)
        return (True, "Transferência realizada com sucesso!")

if __name__=="__main__":
    import doctest
    doctest.testmod(verbose=True)