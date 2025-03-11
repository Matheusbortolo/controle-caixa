import json
import tkinter as tk
from tkinter import messagebox, ttk

class ControleCaixa:
    def __init__(self, arquivo='caixa.json'):
        self.arquivo = arquivo
        self.transacoes = self.carregar_transacoes()
    
    def carregar_transacoes(self):
        try:
            with open(self.arquivo, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def salvar_transacoes(self):
        with open(self.arquivo, 'w') as f:
            json.dump(self.transacoes, f, indent=4)
    
    def adicionar_transacao(self, tipo, valor, descricao):
        if tipo not in ['entrada', 'saida'] or valor <= 0:
            messagebox.showerror("Erro", "Transação inválida!")
            return
        self.transacoes.append({'tipo': tipo, 'valor': valor, 'descricao': descricao})
        self.salvar_transacoes()
        atualizar_listagens()
    
    def remover_transacao(self, index):
        del self.transacoes[index]
        self.salvar_transacoes()
        atualizar_listagens()
        atualizar_saldo()
    
    def calcular_saldo(self):
        return sum(t['valor'] if t['tipo'] == 'entrada' else -t['valor'] for t in self.transacoes)

def adicionar_transacao(tipo):
    def salvar():
        try:
            valor = float(entry_valor.get())
            descricao = entry_descricao.get()
            caixa.adicionar_transacao(tipo, valor, descricao)
            janela_transacao.destroy()
            atualizar_saldo()
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor válido!")
    
    janela_transacao = tk.Toplevel(root)
    janela_transacao.title(f"Adicionar {tipo.capitalize()}")
    tk.Label(janela_transacao, text="Valor:").pack()
    entry_valor = tk.Entry(janela_transacao)
    entry_valor.pack()
    tk.Label(janela_transacao, text="Descrição:").pack()
    entry_descricao = tk.Entry(janela_transacao)
    entry_descricao.pack()
    tk.Button(janela_transacao, text="Salvar", command=salvar).pack()

def remover_transacao(index):
    caixa.remover_transacao(index)

def atualizar_saldo():
    saldo_label.config(text=f"Saldo: R$ {caixa.calcular_saldo():.2f}")

def atualizar_listagens():
    for i in tree_entradas.get_children():
        tree_entradas.delete(i)
    for i in tree_saidas.get_children():
        tree_saidas.delete(i)
    for index, t in enumerate(caixa.transacoes):
        if t['tipo'] == 'entrada':
            tree_entradas.insert("", "end", values=(t['valor'], t['descricao'], "Remover"), tags=(index,))
        else:
            tree_saidas.insert("", "end", values=(t['valor'], t['descricao'], "Remover"), tags=(index,))

def on_item_selected(event):
    item = event.widget.selection()[0]
    index = int(event.widget.item(item, "tags")[0])
    if messagebox.askyesno("Confirmação", "Deseja remover esta transação?"):
        remover_transacao(index)

def main():
    global root, caixa, saldo_label, tree_entradas, tree_saidas
    caixa = ControleCaixa()
    
    root = tk.Tk()
    root.title("Controle de Caixa")
    root.state('zoomed')
    
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)
    
    menu_transacoes = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Transações", menu=menu_transacoes)
    menu_transacoes.add_command(label="Adicionar Entrada", command=lambda: adicionar_transacao('entrada'))
    menu_transacoes.add_command(label="Adicionar Saída", command=lambda: adicionar_transacao('saida'))
    menu_transacoes.add_separator()
    menu_transacoes.add_command(label="Sair", command=root.quit)
    
    saldo_label = tk.Label(root, text=f"Saldo: R$ {caixa.calcular_saldo():.2f}", font=("Arial", 16))
    saldo_label.pack()
    
    frame_listagens = tk.Frame(root)
    frame_listagens.pack(fill=tk.BOTH, expand=True)
    
    frame_entradas = tk.Frame(frame_listagens)
    frame_entradas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    tk.Label(frame_entradas, text="Entradas", font=("Arial", 14)).pack()
    tree_entradas = ttk.Treeview(frame_entradas, columns=("Valor", "Descrição", "Ação"), show="headings")
    tree_entradas.heading("Valor", text="Valor")
    tree_entradas.heading("Descrição", text="Descrição")
    tree_entradas.heading("Ação", text="Ação")
    tree_entradas.pack(fill=tk.BOTH, expand=True)
    tree_entradas.bind("<Double-1>", on_item_selected)
    
    frame_saidas = tk.Frame(frame_listagens)
    frame_saidas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    tk.Label(frame_saidas, text="Saídas", font=("Arial", 14)).pack()
    tree_saidas = ttk.Treeview(frame_saidas, columns=("Valor", "Descrição", "Ação"), show="headings")
    tree_saidas.heading("Valor", text="Valor")
    tree_saidas.heading("Descrição", text="Descrição")
    tree_saidas.heading("Ação", text="Ação")
    tree_saidas.pack(fill=tk.BOTH, expand=True)
    tree_saidas.bind("<Double-1>", on_item_selected)
    
    atualizar_listagens()
    
    root.mainloop()

if __name__ == "__main__":
    main()