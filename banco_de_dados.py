"""Módulo contendo funções para utilização de arquivo CSV como forma de salvar dados de clientes
    """
import pandas as pd
import os

def carregar_contas_de_csv(caminho_arquivo: str) -> dict:
    """Função para permitir melhor manipulação dos dados do CSV ao transformar sua informação em um dicionário

    Args:
        caminho_arquivo (str): Local do arquivo CSV

    Returns:
        dicionario_saida (dict): Um dicionário com as informações contidas no CSV
    Examples:
    >>> carregar_contas_de_csv("arquivo_nao_existente.csv")
    {}
    >>> dicio={'0001':{'cliente':'stuart','saldo': 15.3},'0030':{'cliente': 'roberto', 'saldo': 10000.0}}
    >>> salvar_contas_para_csv("temp_file.csv",dicio)
    >>> carregar_contas_de_csv("temp_file.csv")
    {'0001': {'cliente': 'stuart', 'saldo': 15.3}, '0030': {'cliente': 'roberto', 'saldo': 10000.0}}
    """
    dicionario_saida={}
    try: 
        with open(caminho_arquivo, "r") as archive:
            banco_de_dados=pd.read_csv(archive,dtype={"nome_conta":str})
            for i in banco_de_dados.loc[:,"nome_conta"]:
                linha_da_conta=banco_de_dados.index[banco_de_dados["nome_conta"]==i][0]
                dicionario_saida.update({f"{i}":{"cliente": banco_de_dados.loc[linha_da_conta,"cliente"],"saldo":float(banco_de_dados.loc[linha_da_conta,"saldo"])}})
            #Na linha acima colocamos no dicionario tomando o nome_conta como indice e o resto das informações são encontradas usando a linha referente aquela conta
            return dicionario_saida
    except: return dicionario_saida
print(carregar_contas_de_csv("contas.csv"))
def salvar_contas_para_csv(caminho_arquivo: str, contas: dict) -> None:
    """Função que recebe um dicionario e salva sua informação em um arquivo CSV

    Args:
        caminho_arquivo (str): local onde o arquivo deve ser salvo
        contas (dict): dicionário contendo informações que devem ser salvas em um CSV
    Examples:
    
    >>> dicio={}
    >>> salvar_contas_para_csv("temp_file.csv",dicio)

    >>> os.remove("temp_file.csv")

    >>> dicio={'0001':{'cliente':'stuart','saldo': 15.3},'0030':{'cliente': 'roberto', 'saldo': 10000.0}}
    >>> salvar_contas_para_csv("temp_file.csv",dicio)

    >>> os.remove("temp_file.csv")
    
    """
    dataframe=pd.DataFrame.from_dict(contas, orient="index")
    dataframe.columns
    dataframe.to_csv(caminho_arquivo,index_label="nome_conta")


if __name__=="__main__":
    import doctest
    doctest.testmod(verbose=True)