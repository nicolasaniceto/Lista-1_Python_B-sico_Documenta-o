# Lista 1 - Linguagens de programação

**Objetivo Geral:** Desenvolver um pequeno projeto com uma interface em terminal (CLI) que simula um sistema de gerenciamento bancário. O programa deverá permitir que o usuário interaja por terminal para realizar as operações descritas abaixo. Os dados das contas deverão ser armazenados em um arquivo CSV, que será alterado pelo programa sempre que novas alterações aos dados bancários sejam feitas ou caso seja necessário buscar informações sobre as contas.

**Prazo:** 31/08

**Forma de entrega:** Repositório no GitHub Classroom.

## Estrutura do Projeto

O projeto deve ser organizado nos seguintes arquivos:

- `banco_de_dados.py`: Contém funções para carregar os dados bancários do CSV para um dicionário em memória, e para salvar o dicionário de volta no CSV.

- `operacoes_bancarias.py`: Contém todas as funções de lógica de negócio (tanto de cliente quanto de gerente).

- `main.py`: Arquivo que implementa a interface em terminal e que realiza corretamente as chamadas de funções de acordo com a opção escolhida pelo usuário.

- `contas.csv`: O arquivo que funciona como a base de dados do sistema.

> ⚠️ **Aviso:** Siga exatamente os nomes dos arquivos e funções apresentados neste README, incluindo letras maiúsculas e minúsculas. O não cumprimento dessa regra poderá resultar em penalidade na nota.

## Descrição Detalhada dos Módulos e Funções

### Arquivo: `contas.csv`

O arquivo `contas.csv` deve conter os dados das contas bancárias organizados em formato tabular, com um cabeçalho indicando os campos. Por exemplo:

```
numero_conta,cliente,saldo
0001,Joao,1000.50
0002,Maria,250.75
0003,Carlos,5000.00
```

Cada linha representa uma conta, onde `numero_conta` é o identificador único da conta, `cliente` é o nome do titular, e `saldo` é o valor atual disponível na conta.

### Módulo: `banco_de_dados.py`

```py
carregar_contas_de_csv(caminho_arquivo: str) -> dict:
```
**Descrição:** Lê o arquivo CSV e o carrega em um dicionário. Se o arquivo não existir, deve retornar um dicionário vazio.

**Retorno:** Um dicionário no formato `{"numero_conta": {"cliente": "Nome", "saldo": 123.45}, ...}`. O saldo deve ser um float.

```py
salvar_contas_para_csv(caminho_arquivo: str, contas: dict) -> None:
```
**Descrição:** Recebe o dicionário de contas e o salva completamente no arquivo CSV, substituindo o conteúdo anterior. Deve incluir o cabeçalho.

**Retorno:** Nenhum.
### Módulo: `operacoes_banco.py`

Este módulo deve conter as funções principais relacionadas às operações bancárias. É importante destacar que você pode criar funções auxiliares para facilitar a implementação e manter o código organizado. Lembre-se de seguir o princípio de responsabilidade única, garantindo que cada função tenha um propósito claro e específico, tornando-a mais reutilizável.

O carregamento e salvamento do arquivo CSV devem gerenciados internamente pelas funções, sem a necessidade de passar o dicionário de contas como argumento. Para isso, vocês devem usar as funções do módulo `banco_de_dados.py` para ler e salvar o CSV ao realizar as operações.
 
```py
criar_conta(numero_conta: str, nome_cliente: str) -> tuple[int, dict]:
```
**Descrição:** Deve criar uma conta nova, incluindo no csv. Note que essa conta deve começar com um saldo de 0 reais.

**Retorno:** Uma tupla com o numero da nova conta criada e o dicionário completo dela (ex: `(0001, {"cliente": "Joao", "saldo": 0.00})`).

```py
depositar(numero_conta: str, valor: float) -> tuple[bool, str]:
```
**Descrição:** Se a conta existir e o valor for positivo, adiciona o valor ao saldo.

**Retorno:** Uma tupla indicando sucesso/falha com uma mensagem apropriada (ex: `(False, "Erro: conta inexistente.")`).

```py
sacar(numero_conta: str, valor: float) -> tuple[bool, str]:
```
**Descrição:** Verifica se a conta existe, se o valor é positivo e se há saldo suficiente. Se tudo estiver OK, subtrai o valor do saldo.

**Retorno:** Uma tupla indicando sucesso/falha com uma mensagem apropriada (ex: `(False, "Erro: saldo insuficiente.")`).

```py
consultar_saldo(numero_conta: str) -> float | None:
```
**Descrição:** Procura pela conta no dicionário e retorna o saldo dela.

**Retorno:** O saldo (um float) se a conta existir, ou `None` se não existir.

```py
somar_saldos_gerais( ) -> float:
```
**Descrição:** Soma o saldo de todas as contas existentes no banco.

**Retorno:** O valor total (float) da soma de todos os saldos.

```py
identificar_cliente_mais_rico( ) -> dict | None:
```
**Descrição:** Percorre todas as contas e identifica qual cliente possui o maior saldo.

**Retorno:** O dicionário completo da conta com o maior saldo (ex: `{"cliente": "Carlos", "saldo": 5000.00}`). Se não houver contas, retorna `None`.

```py
somar_saldos_em_lote(**kwargs) -> int:
```
**Descrição:** Soma valores aos saldos de múltiplas contas de uma vez. As chaves dos kwargs serão os números das contas e os valores serão os montantes a serem adicionados.

**Retorno:** A quantidade de contas que foram atualizadas com sucesso. Contas inexistentes ou valores negativos devem ser ignorados.

```py
subtrair_saldos_em_lote(**kwargs) -> int:
```
**Descrição:** Subtrai valores dos saldos de múltiplas contas de uma vez. Falha para uma conta específica se o saldo for insuficiente, mas continua para as outras.

**Retorno:** A quantidade de contas que tiveram o saldo removido com sucesso. Contas inexistentes, valores negativos ou tentativas de saque maiores que o saldo devem ser ignoradas.

```py
realizar_transferencia(conta_origem: str, conta_destino: str, valor: float) -> tuple[bool, str]:
```
**Descrição:** Realiza uma transferência entre duas contas. Se não for possível realizar a operação, seja por falta de saldo ou pela outra conta não existir, o retorno deve indicar a falha.

**Retorno:** Tupla (sucesso, mensagem). Ex: `(True, "Transferência realizada com sucesso.")` ou `(False, "Saldo insuficiente")`.

### Driver code: `main.py`

A aplicação deve operar em um loop contínuo, apresentando menus no terminal ao usuário. Tomem como exemplo a seguinte interação:

```
Bem-vindo ao Banco Digital!
Escolha o modo de operação:
1 - Operações de Gerente
2 - Operações de Cliente
3 - Sair
```

#### Operações de Gerente

Ao escolher 1, o programa entra no modo Gerente e apresenta o seguinte menu:

```
Escolha uma operação:
1 - Verificar saldo total do banco
2 - Identificar cliente mais rico
3 - Adicionar fundos em lote
4 - Debitar fundos em lote
5 - Abrir uma nova conta no banco
6 - Voltar ao menu principal
```

#### Operações de Cliente

Ao escolher 2, o programa entra no modo Cliente e pede ao usuário o número da conta para "fazer login":

```
Digite o número da conta:
```

Se a conta não existir, exibe a seguinte mensagem de erro e volta ao menu principal:

```
Erro: Conta inexistente.
```

Se a conta existir, o programa apresenta o seguinte menu específico para o cliente:

```
Escolha uma operação:
1 - Consultar meu saldo
2 - Realizar um depósito
3 - Realizar um saque
4 - Realizar uma transferência
5 - Voltar ao menu principal
```

Lembrando que para as funções que dependem de um argumento, esse argumento precisa ser digitado pelo usuário. Por exemplo, ao escolher a opção 3, o usuário precisará passar o saldo a ser sacado. Então o menu do terminal precisa pedir algo como:

```
Digite o valor a ser sacado:
```

Certifique-se de validar as entradas do usuário antes de prosseguir com as operações, garantindo que valores negativos ou inválidos sejam rejeitados com mensagens de erro apropriadas.

Ao escolher 3, o programa encerra.



## Documentação

O projeto deverá documentado adequadamente, seguindo as práticas ensinadas em aula. Tanto os módulos quanto as funções devem ser documentados com docstrings ([aula sobre documentação e docstrings](https://github.com/matwerner/fgv-lp/blob/0bb5a6549623de7ece087a1d8f0e0ffab1809596/2025_2/aulas/Semana%203%20-%20Documentacao%20%26%20Type%20Hint/10_documentacao.md)) que expliquem seus funcionamentos e comportamentos. 

O projeto deverá ser acompanhado de uma página de documentação, feita em `sphinx` ([aula sobre sphinx](https://github.com/matwerner/fgv-lp/blob/0bb5a6549623de7ece087a1d8f0e0ffab1809596/2024_2/aulas/Semana%205%20-%20Sphinx%20%26%20Programa%C3%A7%C3%A3o%20Funcional/18_documentacao_projeto.md)), e os arquivos relacionados à essa página devem estar própriamente organizados dentro de uma pasta `docs`. Essa página deverá estar disponível por meio do **GitHub Pages**.
