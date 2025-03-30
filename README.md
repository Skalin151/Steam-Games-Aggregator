# Steam Game Manager

![Steam Manager](https://img.shields.io/badge/Steam-Manager-blue) ![Python](https://img.shields.io/badge/Python-3.x-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

Gerenciador de jogos Steam para múltiplas contas com interface gráfica moderna.

## 📋 Funcionalidades

✅ **Agregação de jogos**  
   - Combina jogos de múltiplas contas Steam  
   - Contabiliza cópias por jogo  
   - Identifica proprietários de cada jogo  

🔍 **Busca avançada**  
   - Filtra por nome do jogo ou AppID  
   - Filtro por usuário específico  
   - Ordenação por nome (A-Z/Z-A) ou número de cópias  

💾 **Exportação de dados**  
   - Gera CSV com todos os jogos agregados  
   - Formato organizado: AppID, Nome, Cópias, Proprietários  

🎨 **Interface moderna**  
   - Design escuro e limpo com ttkbootstrap  
   - Tabela responsiva com scroll  
   - Feedback visual para todas as operações  

## 🛠️ Requisitos

- Python 3.8+  
- Conta Steam com API Key ativa  
- Bibliotecas:  
  pip install ttkbootstrap requests

## 🚀 Como Usar
1. Configure o arquivo "users.txt"
```bash
SUA_API_KEY_1,STEAM_ID_1,Nome do Usuário 1
SUA_API_KEY_2,STEAM_ID_2,Nome do Usuário 2
```
2. Execute a aplicação:
```bash
python steam_manager.py
```
3. Principais operações:
-Clique em 🔄 Atualizar Dados para buscar jogos da API
-Use a barra de busca 🔍 para filtrar jogos
-Selecione filtros no dropdown ▼ para ordenar/limitar resultados
-Clique em 💾 Exportar CSV para salvar dados

## 📜 Créditos
-API Steam: https://developer.valvesoftware.com
-Interface gráfica: https://ttkbootstrap.readthedocs.io
-Ícones: https://fonts.google.com/icons