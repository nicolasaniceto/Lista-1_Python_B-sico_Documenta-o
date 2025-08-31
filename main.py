"""Módulo de escolha e execução de funções para clientes e gerentes
    """

from operacoes_bancarias import *
from banco_de_dados import *


def gerente():
    """Define o menu de funções acessáveis por um gerente, sendo as funções:\n
    somar_saldos_gerais\n
    identificar_cliente_mais_rico\n
    somar_saldos_em_lote\n
    subtrair_saldos_em_lote\n
    criar_conta
    """
    while True:
        gerente = {
            1: "Verificar saldo total do banco",
            2: "Identificar cliente mais rico",
            3: "Adicionar fundos em lote",
            4: "Debitar fundos em lote",
            5: "Abrir uma nova conta no banco",
            6: "Voltar ao menu principal"
        }
        print("Escolha uma operação:")
        for key in gerente:
                print(f"{key} - {gerente[key]}")
        try: op = int(input())
        except:
            print("Entrada invalida")
            continue
        match op:
            case 1:
                print(f"O saldo total do banco corresponde a {somar_saldos_gerais()}")
            case 2:
                print(f"O cliente mais rico corresponde a {identificar_cliente_mais_rico()}")
            case 3:
                answer=input("digite todas as contas nas quais quer adicionar fundos, separe cada conta por um espaço\n")
                contas=answer.split(" ")
                answer=input("digite todos os valores que quer para cada conta em ordem, separe cada valor por um espaço\n")
                valores=answer.split(" ")
                if len(valores)>len(contas):
                    print("Existem mais valores do que contas, tente novamente")
                elif len(valores)<len(contas):
                    print("Existem mais contas do que valores, tente novamente")
                else:
                    dict_para_input={}
                    for i in range(len(contas)):
                        try:dict_para_input.update({contas[i]:float(valores[i])})
                        except: pass
                    try: 
                        resultado=somar_saldos_em_lote(**dict_para_input)
                        print(f"De todas as tentativas, {resultado} foram bem sucedidas")
                    except: pass
                            
            case 4:
                answer=input("digite todas as contas nas quais quer debitar fundos, separe cada conta por um espaço\n")
                contas=answer.split(" ")
                answer=input("digite todos os valores que quer para cada conta em ordem, separe cada valor por um espaço\n")
                valores=answer.split(" ")
                if len(valores)>len(contas):
                    print("Existem mais valores do que contas, tente novamente")
                elif len(valores)<len(contas):
                    print("Existem mais contas do que valores, tente novamente")
                else:
                    dict_para_input={}
                    for i in range(len(contas)):
                        try:dict_para_input.update({contas[i-1]:float(valores[i-1])})
                        except: pass
                    try: 
                        resultado=subtrair_saldos_em_lote(**dict_para_input)
                        print(f"De todas as tentativas, {resultado} foram bem sucedidas")
                    except: pass
            case 5:
                numero = input("Digite o número da conta: ")
                nome = input("Digite o nome do usuário: ")
                try:criar_conta(numero,nome)
                except:print("Erro: a conta já existe. Tente outro numero para a conta")
            case 6:
                return()
              

def cliente():
    """Define o menu de funções acessáveis por um cliente, sendo as funções:\n
    consultar_saldo\n
    depositar\n
    sacar\n
    realizar_transferencia
    """
    operacoes = {
        1: "Consultar meu saldo",
        2: "Realizar um depósito",
        3: "Realizar um saque",
        4: "Realizar uma transferência",
        5: "Voltar ao menu principal"
    }
    conta = input("Digite o número da conta: ")
    contas = carregar_contas_de_csv('contas.csv')
    if conta not in contas.keys():
         print("Erro: Conta inexistente.")
         return
    else: print(f"Olá {contas[conta]["cliente"]}! Seja muito bem-vindo(a)!")    
    while True:
        for key in operacoes:
                print(f"{key} - {operacoes[key]}")
        op = int(input())     
        match op:
            case 1:
                print(f"O saldo de sua conta corresponde a {consultar_saldo(conta)}")
            case 2:
                try: 
                    valor = float(input("Digite o valor a ser depositado: "))
                    depositar(conta, valor)
                except:
                    print("Entrada invalida")
                    continue
                
            case 3:
                try: 
                    valor = float(input("Digite o valor a ser sacado: "))
                    sacar(conta, valor)
                except:
                     print("Entrada invalida")
            case 4:
                try:
                    destino = input("Digite o número da conta que irá trasnferir: ")
                    valor = float(input("Digite o valor a ser transferido: "))
                    realizar_transferencia(conta,destino,valor)
                except:
                    print("Entrada invalida")
            case 5:
                return()            
              

def main():
    """Define o menu inicial e como devem ser acessados os outros menus, sendo esses:\n
    gerente\n
    cliente
    """
    menu_principal = {
     1 : "Operações de Gerente",
     2 : "Operações de Cliente",
     3 : "Sair"
    } 
    while True:
        print("Bem-vindo ao Banco Digital!")
        print("Escolha o modo de operação:")
        for key in menu_principal:
            print(f"{key} - {menu_principal[key]}")
        try: op = int(input())
        except: 
             print("Entrada invalida")
             continue
        match op:
            case 1:
                gerente()
            case 2:
                cliente()
            case 3:
                 return()
  

main()