import tkinter as tk
from tkinter import ttk, messagebox
import requests
import csv
from datetime import datetime
import ttkbootstrap as tb
from ttkbootstrap.constants import *

# Configurações iniciais
USERS_FILE = 'users.txt'
OUTPUT_FILE = 'steam_games_aggregated.csv'

# Carregar usuários do arquivo TXT
def load_users():
    users = []
    user_names = {}
    try:
        with open(USERS_FILE, 'r') as f:
            for line in f:
                api_key, steam_id, name = line.strip().split(',')
                users.append({'api_key': api_key, 'steam_id': steam_id})
                user_names[steam_id] = name
    except FileNotFoundError:
        messagebox.showerror("Erro", f"Arquivo {USERS_FILE} não encontrado")
    return users, user_names

USERS, USER_NAMES = load_users()


class SteamManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steam Game Manager")
        self.style = tb.Style("darkly")
        
        # Variáveis de controle
        self.games_data = {}
        self.filtered_data = {}
        self.search_var = tb.StringVar()
        self.filter_var = tb.StringVar(value="All")
        
        # Interface
        self.create_header()
        self.create_search_and_filters()
        self.create_table()
        self.create_action_buttons()
        
        # Carregar dados automaticamente
        self.refresh_data()

    def create_header(self):
        header = tb.Frame(self.root)
        header.pack(padx=20, pady=20, fill=tk.X)
        tb.Label(header, text="Steam Game Manager", font=("Helvetica", 18, "bold")).pack()

    def create_search_and_filters(self):
        filter_frame = tb.Frame(self.root)
        filter_frame.pack(padx=20, pady=10, fill=tk.X)
        
        # Barra de busca
        self.search_entry = tb.Entry(
            filter_frame,
            textvariable=self.search_var,
            bootstyle="primary",
            width=40
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        # Dropdown de filtros
        user_filters = [f"User: {name}" for name in USER_NAMES.values()]
        sort_options = [
            "Sort: Name (A-Z)",
            "Sort: Name (Z-A)",
            "Sort: Copies (Asc)",
            "Sort: Copies (Desc)"
        ]
        all_filters = ["All"] + user_filters + sort_options
        
        self.filter_combobox = tb.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=all_filters,
            state="readonly",
            bootstyle="secondary"
        )
        self.filter_combobox.pack(side=tk.LEFT, padx=5)
        self.filter_combobox.bind("<<ComboboxSelected>>", self.filter_games)
        
        # Vincular eventos
        self.search_var.trace("w", self.filter_games)

    def create_table(self):
        table_frame = tb.Frame(self.root)
        table_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=("appid", "name", "copies", "owners"),
            show="headings",
            height=20
        )
        
        self.tree.heading("appid", text="AppID")
        self.tree.heading("name", text="Nome do Jogo")
        self.tree.heading("copies", text="Cópias")
        self.tree.heading("owners", text="Proprietários")
        
        self.tree.column("appid", width=80)
        self.tree.column("name", width=300)
        self.tree.column("copies", width=80, anchor="center")
        self.tree.column("owners", width=200)
        
        scrollbar = tb.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_action_buttons(self):
        button_frame = tb.Frame(self.root)
        button_frame.pack(padx=20, pady=10, fill=tk.X)
        
        self.export_btn = tb.Button(
            button_frame,
            text="Exportar CSV",
            command=self.export_csv,
            bootstyle="success"
        )
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        self.refresh_btn = tb.Button(
            button_frame,
            text="Atualizar Dados",
            command=self.refresh_data,
            bootstyle="info"
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=5)

    def get_user_games(self, api_key, steam_id):
        url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
        params = {
            'key': api_key,
            'steamid': steam_id,
            'include_appinfo': True,
            'format': 'json'
        }
        
        try:
            response = requests.get(url, params=params)
            games = response.json().get('response', {}).get('games', [])
            return games
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao obter jogos para {steam_id}: {str(e)}")
            return []

    def aggregate_games(self):
        aggregated = {}
        for user in USERS:
            games = self.get_user_games(user['api_key'], user['steam_id'])
            for game in games:
                appid = str(game['appid'])
                name = game.get('name', 'Desconhecido')
                
                if appid in aggregated:
                    if user['steam_id'] not in aggregated[appid]['owners']:
                        aggregated[appid]['copies'] += 1
                        aggregated[appid]['owners'].append(user['steam_id'])
                else:
                    aggregated[appid] = {
                        'appid': appid,
                        'name': name,
                        'copies': 1,
                        'owners': [user['steam_id']]
                    }
        return aggregated

    def refresh_data(self):
        try:
            self.games_data = self.aggregate_games()
            self.filtered_data = self.games_data.copy()
            self.update_table()
            
            # Nova lógica de exportação com confirmação visual
            if self.export_csv():
                messagebox.showinfo("Sucesso", f"Dados atualizados e arquivo {OUTPUT_FILE} salvo com sucesso!")
            else:
                messagebox.showwarning("Aviso", "Dados atualizados mas falha ao salvar CSV")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar dados: {str(e)}")

    def filter_games(self, *args):
        query = self.search_var.get().lower()
        selected_filter = self.filter_var.get()
        
        # Filtrar por busca
        filtered = {
            appid: data for appid, data in self.games_data.items()
            if query in data['name'].lower() or query in appid
        }
        
        # Aplicar filtros adicionais
        if selected_filter.startswith("User: "):
            user = selected_filter.split(": ")[1]
            steam_id = next((k for k, v in USER_NAMES.items() if v == user), None)
            if steam_id:
                filtered = {
                    appid: data for appid, data in filtered.items()
                    if steam_id in data['owners']
                }
                
        elif selected_filter.startswith("Sort: "):
            sort_by = selected_filter.split(": ")[1]
            
            if sort_by == "Name (A-Z)":
                filtered = dict(sorted(filtered.items(), key=lambda x: x[1]['name']))
            elif sort_by == "Name (Z-A)":
                filtered = dict(sorted(filtered.items(), key=lambda x: x[1]['name'], reverse=True))
            elif sort_by == "Copies (Asc)":
                filtered = dict(sorted(filtered.items(), key=lambda x: x[1]['copies']))
            elif sort_by == "Copies (Desc)":
                filtered = dict(sorted(filtered.items(), key=lambda x: x[1]['copies'], reverse=True))
        
        self.filtered_data = filtered
        self.update_table()

    def update_table(self):
        self.tree.delete(*self.tree.get_children())
        for appid, data in self.filtered_data.items():
            owners = ', '.join([USER_NAMES.get(u, u) for u in data['owners']])
            self.tree.insert('', tk.END, values=(
                appid,
                data['name'],
                data['copies'],
                owners
            ))

    def export_csv(self):
        try:
            with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['AppID', 'Game Name', 'Copies', 'Owners'])
                
                # Formatação corrigida para garantir escrita
                for appid, data in self.games_data.items():
                    owners = ', '.join([USER_NAMES.get(u, u) for u in data['owners']])
                    writer.writerow([
                        data['appid'],
                        data['name'],
                        data['copies'],
                        owners
                    ])
            return True  # Confirmação de sucesso
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar CSV: {str(e)}")
            return False  # Indica falha

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = SteamManagerApp(root)
    root.geometry("1000x700")
    root.mainloop()