# 🎮 Steam Games Aggregator

**Um script Python para agregar jogos de múltiplas contas Steam, com contagem de cópias e logs detalhados.**

Este projeto permite que você consolide a lista de jogos de várias contas Steam em um único arquivo CSV, contando automaticamente o número de cópias e identificando os proprietários de cada jogo. Ideal para famílias ou grupos que compartilham bibliotecas na Steam.

---

## ✨ Funcionalidades

- **Agregação de múltiplas contas:** Adicione várias contas Steam para consolidar a lista de jogos.
- **Contagem automática de cópias:** O número de cópias é atualizado automaticamente quando um jogo é compartilhado por mais de uma conta.
- **Logs detalhados:** Acompanhe o progresso do script com logs claros e informativos.
- **Exportação para CSV:** Gera um arquivo CSV organizado para fácil visualização e análise.
- **Fácil de usar:** Basta configurar as credenciais das contas e executar o script.

---

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Biblioteca `requests` instalada
- API Key da Steam (obtenha [aqui](https://steamcommunity.com/dev/apikey))
- SteamID64 de cada conta (encontre o seu [aqui](https://steamid.io/))

---

## 🚀 Como usar

**Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/steam-games-aggregator.git
cd steam-games-aggregator
```

**Instale as depêndencias:**
```bash
pip install requests
```

**Configure as contas:**
- Abra o arquivo `steam_games_aggregator.py`
- Preencha a lista `USERS` com as credenciais de cada conta:

  ```python
  USERS = [
    {
        'api_key': 'SUA_API_KEY_1',
        'steam_id': 'SUA_ID_STEAM_1'
    },
    {
        'api_key': 'SUA_API_KEY_2', 
        'steam_id': 'SUA_ID_STEAM_2'
    },
    {
        'api_key': 'SUA_API_KEY_3', 
        'steam_id': 'SUA_ID_STEAM_3'
    },
    {
        'api_key': 'SUA_API_KEY_4', 
        'steam_id': 'SUA_ID_STEAM_4'
    },
     {
        'api_key': 'SUA_API_KEY_5', 
        'steam_id': 'SUA_ID_STEAM_5'
    },
     {
        'api_key': 'SUA_API_KEY_6', 
        'steam_id': 'SUA_ID_STEAM_6'
    }  
]
```

**Execute o script:**
```bash
python steam_games_aggregator.py
```

**Verifique o arquivo gerado:**
- O script criará um arquivo `steam_games_aggregated.csv` com todos os dados consolidados.

---

## 📂 Estrutura do CSV

**O arquivo CSV gerado contém as seguintes colunas:**

| ID  | Nome | Nº Cópias | Dono |
|:--- |:---- |:--------- |:---- |
|     |      |           |      |

---

## 📝 Logs de Execução

**O script gera logs detalhados para acompanhamento. Exemplo:**
```log
[14:30:45] Iniciando processamento...
[14:30:45] Nenhum arquivo existente encontrado. Criando novo arquivo.
[14:30:45] Processando conta 7656119XXXX...
[14:30:46] Conta 7656119XXXX possui 120 jogos.
[14:30:46] Conta 7656119XXXX adicionou 120 novos jogos e atualizou 0 existentes.
[14:30:46] Processando conta 7656119YYY...
[14:30:47] Conta 7656119YYY possui 80 jogos.
[14:30:47] Conta 7656119YYY adicionou 30 novos jogos e atualizou 50 existentes.
[14:30:47] Arquivo salvo com 150 jogos.
[14:30:47] Processamento concluído.
```

---