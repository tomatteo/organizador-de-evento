import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from usuario import Usuario
from ingresso import Ingresso
from evento import Evento
from participante import Participante

# Listas globais (simulando banco de dados)
eventos_lista = []
participantes_lista = []

class InterfaceGrafica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Organizador de Eventos")
        self.geometry("600x650") # Aumentei um pouco para caber os novos campos
        self.configure(bg="#1e1e2e")  

        # --- ESTILOS ---
        style = ttk.Style()
        style.theme_use("clam")
        
        # Estilo da Tabela
        style.configure("Treeview", 
                        background="#313244", 
                        foreground="white", 
                        fieldbackground="#313244", 
                        rowheight=25,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading", 
                        background="#89b4fa", 
                        foreground="#1e1e2e", 
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[('selected', '#b4befe')])

       
        style.configure("TCombobox", fieldbackground="#45475a", background="#89b4fa", foreground="white")
        style.configure("TSpinbox", fieldbackground="#45475a", background="#89b4fa", foreground="white")
        
        # Fonte padrão
        self.default_font = ("Segoe UI", 11)

       
        self.frame_principal = tk.Frame(self, bg="#1e1e2e")
        self.frame_principal.pack(pady=20, fill="both", expand=True)

        # Título
        tk.Label(
            self.frame_principal,
            text="📅 Organizador de Eventos",
            font=("Segoe UI Black", 22),
            bg="#1e1e2e",
            fg="#89dceb"
        ).pack(pady=15)

        # ------- MENUS --------
        self.criar_card("Gerenciar Eventos", [
            ("Cadastrar Evento", self.cadastrar_evento),
            ("Listar Eventos", self.listar_eventos),
            ("Excluir Evento", self.excluir_evento)
        ])

        self.criar_card("Gerenciar Participantes", [
            ("Cadastrar Participante", self.cadastrar_participante),
            ("Listar Participantes", self.listar_participantes),
            ("Excluir Participante", self.excluir_participante),
            ("Autenticar Participante", self.autenticar_participante),
            ("Inscrever em Evento", self.inscrever_evento),
            ("Cancelar Inscrição", self.cancelar_inscricao),
        ])

    def criar_card(self, titulo, botoes):
        card = tk.Frame(self.frame_principal, bg="#313244", padx=15, pady=10)
        card.pack(pady=10, padx=20, fill="x")

        tk.Label(card, text=titulo, font=("Segoe UI", 14, "bold"), bg="#313244", fg="white").pack(pady=5)

        for texto, comando in botoes:
            btn = tk.Button(
                card,
                text=texto,
                font=self.default_font,
                bg="#89b4fa",
                fg="#1e1e2e",
                relief="flat",
                activebackground="#b4befe",
                padx=10,
                pady=5,
                cursor="hand2",
                command=comando
            )
            btn.pack(pady=4, fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#b4befe"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#89b4fa"))

    # ------------------------------------------------------------------
    # FUNÇÕES DE EVENTOS
    # ------------------------------------------------------------------

    def cadastrar_evento(self):
        janela = tk.Toplevel(self)
        janela.title("Cadastrar Evento")
        janela.geometry("500x650") # Mais largo para caber as datas
        janela.configure(bg="#1e1e2e")

        tk.Label(janela, text="Novo Evento", font=("Segoe UI", 16, "bold"), bg="#1e1e2e", fg="#89dceb").pack(pady=15)

        # Função para criar campos de texto normais
        def criar_campo(texto):
            tk.Label(janela, text=texto, bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 10)).pack(anchor="w", padx=30, pady=(5, 0))
            entry = tk.Entry(janela, font=("Segoe UI", 10), bg="#45475a", fg="white", relief="flat", insertbackground="white")
            entry.pack(fill="x", padx=30, pady=5, ipady=3)
            return entry

        # seletores de data de caixinhas
        def criar_seletor_data_hora(texto):
            tk.Label(janela, text=texto, bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 10)).pack(anchor="w", padx=30, pady=(10, 0))
            frame = tk.Frame(janela, bg="#1e1e2e")
            frame.pack(fill="x", padx=30, pady=2)
            
            # Dia
            sb_dia = ttk.Spinbox(frame, from_=1, to=31, width=3, font=("Segoe UI", 10))
            sb_dia.set(datetime.now().day)
            sb_dia.pack(side="left", padx=2)
            tk.Label(frame, text="/", bg="#1e1e2e", fg="white").pack(side="left")
            
            # Mês
            sb_mes = ttk.Spinbox(frame, from_=1, to=12, width=3, font=("Segoe UI", 10))
            sb_mes.set(datetime.now().month)
            sb_mes.pack(side="left", padx=2)
            tk.Label(frame, text="/", bg="#1e1e2e", fg="white").pack(side="left")
            
            # Ano
            ano_atual = datetime.now().year
            sb_ano = ttk.Spinbox(frame, from_=ano_atual, to=ano_atual+5, width=5, font=("Segoe UI", 10))
            sb_ano.set(ano_atual)
            sb_ano.pack(side="left", padx=2)
            
            tk.Label(frame, text=" às ", bg="#1e1e2e", fg="white").pack(side="left", padx=10)
            
            # Hora
            sb_hora = ttk.Spinbox(frame, from_=0, to=23, width=3, font=("Segoe UI", 10), format="%02.0f")
            sb_hora.set("19") # sugestao de hora padrão
            sb_hora.pack(side="left", padx=2)
            tk.Label(frame, text=":", bg="#1e1e2e", fg="white").pack(side="left")
            
            # Minuto
            sb_min = ttk.Spinbox(frame, from_=0, to=59, width=3, font=("Segoe UI", 10), format="%02.0f")
            sb_min.set("00")
            sb_min.pack(side="left", padx=2)
            
            return sb_dia, sb_mes, sb_ano, sb_hora, sb_min

        nome_entry = criar_campo("Nome do Evento:")
        desc_entry = criar_campo("Descrição:")
        
        # usando os seletores criados aqui em cima
        dia_ini, mes_ini, ano_ini, hora_ini, min_ini = criar_seletor_data_hora("Data e Hora de Início:")
        dia_fim, mes_fim, ano_fim, hora_fim, min_fim = criar_seletor_data_hora("Data e Hora de Fim:")
        
        cap_entry = criar_campo("Capacidade Máxima:")
        
        tk.Label(janela, text="--- Dados do Local ---", bg="#1e1e2e", fg="#fab387", font=("Segoe UI", 10, "bold")).pack(pady=15)
        
        local_nome_entry = criar_campo("Nome do Local:")
        local_end_entry = criar_campo("Endereço:")

        def salvar():
            try:
                nome = nome_entry.get()
                desc = desc_entry.get()
                
                # montando as datas a partir dos seletores
                try:
                    data_inicio = datetime(
                        int(ano_ini.get()), int(mes_ini.get()), int(dia_ini.get()),
                        int(hora_ini.get()), int(min_ini.get())
                    )
                    data_fim = datetime(
                        int(ano_fim.get()), int(mes_fim.get()), int(dia_fim.get()),
                        int(hora_fim.get()), int(min_fim.get())
                    )
                except ValueError:
                    messagebox.showerror("Erro", "Data ou Hora inválida (ex: dia 31 em mês de 30 dias).")
                    return

                cap = int(cap_entry.get())
                
                local_info = {
                    'id': len(eventos_lista) + 100,
                    'nome': local_nome_entry.get(),
                    'endereco': local_end_entry.get(),
                    'capacidade': cap
                }
                
                if nome and cap > 0:
                    if data_fim <= data_inicio:
                        messagebox.showerror("Erro", "A data final deve ser depois da inicial!")
                        return

                    evento_id = len(eventos_lista) + 1
                    evento = Evento(evento_id, nome, desc, data_inicio, data_fim, cap, local_info)
                    eventos_lista.append(evento)
                    messagebox.showinfo("Sucesso", "Evento cadastrado!")
                    janela.destroy()
                else:
                    messagebox.showerror("Erro", "Preencha os campos obrigatórios!")
            except ValueError as e:
                messagebox.showerror("Erro", f"Dados inválidos (números): {str(e)}")

        tk.Button(janela, text="SALVAR EVENTO", bg="#a6e3a1", fg="#1e1e2e", font=("Segoe UI", 10, "bold"), relief="flat", command=salvar).pack(pady=30, fill="x", padx=30)

    def listar_eventos(self):
        janela = tk.Toplevel(self)
        janela.title("Lista de Eventos")
        janela.geometry("900x400")
        janela.configure(bg="#1e1e2e")

        frame_tabela = tk.Frame(janela, bg="#1e1e2e")
        frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

        colunas = ("id", "nome", "data", "local", "vagas", "status")
        tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", selectmode="browse")

        headers = ["ID", "Nome do Evento", "Data Início", "Local", "Lotação", "Status"]
        for col, text in zip(colunas, headers):
            tree.heading(col, text=text)

        tree.column("id", width=40, anchor="center")
        tree.column("nome", width=200, anchor="w")
        tree.column("data", width=120, anchor="center")
        tree.column("local", width=150, anchor="w")
        tree.column("vagas", width=80, anchor="center")
        tree.column("status", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for evento in eventos_lista:
            try:
                ocupadas = len([ing for ing in evento.ingressos if ing.status == "Vendido"])
            except: ocupadas = 0
            
            vagas_str = f"{ocupadas} / {evento.capacidade}"
            try:
                data_str = evento._dataInicio.strftime("%d/%m/%Y %H:%M")
            except:
                data_str = str(evento._dataInicio)

            tree.insert("", tk.END, values=(evento._id, evento.nome, data_str, evento.local.nome, vagas_str, evento._status))

    def excluir_evento(self):
        janela = tk.Toplevel(self)
        janela.title("Excluir Evento")
        janela.geometry("400x200")
        janela.configure(bg="#1e1e2e")

        tk.Label(janela, text="Excluir Evento", font=("Segoe UI", 14, "bold"), bg="#1e1e2e", fg="#f38ba8").pack(pady=15)
        tk.Label(janela, text="Nome do Evento:", bg="#1e1e2e", fg="#cdd6f4").pack(pady=5)
        
        nome_entry = tk.Entry(janela, font=("Segoe UI", 10), bg="#45475a", fg="white", relief="flat", insertbackground="white")
        nome_entry.pack(fill="x", padx=40, pady=5)

        def excluir():
            nome = nome_entry.get()
            global eventos_lista
            for e in eventos_lista:
                if e.nome == nome:
                    eventos_lista.remove(e)
                    messagebox.showinfo("Sucesso", f"Evento '{nome}' removido!")
                    janela.destroy()
                    return
            messagebox.showerror("Erro", "Evento não encontrado!")

        tk.Button(janela, text="CONFIRMAR EXCLUSÃO", bg="#f38ba8", fg="#1e1e2e", font=("Segoe UI", 10, "bold"), relief="flat", command=excluir).pack(pady=20, padx=40, fill="x")

    # -----------------------------------------------------------------
    # FUNÇÕES DE PARTICIPANTES
    # -----------------------------------------------------------------

    def cadastrar_participante(self):
        janela = tk.Toplevel(self)
        janela.title("Cadastrar Participante")
        janela.geometry("400x450")
        janela.configure(bg="#1e1e2e")

        tk.Label(janela, text="Novo Participante", font=("Segoe UI", 16, "bold"), bg="#1e1e2e", fg="#89dceb").pack(pady=15)

        def criar_campo(texto, is_senha=False):
            tk.Label(janela, text=texto, bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", padx=30, pady=(5,0))
            entry = tk.Entry(janela, show="*" if is_senha else "", font=("Segoe UI", 10), bg="#45475a", fg="white", relief="flat", insertbackground="white")
            entry.pack(fill="x", padx=30, pady=5, ipady=3)
            return entry

        nome_entry = criar_campo("Nome:")
        email_entry = criar_campo("Email:")
        senha_entry = criar_campo("Senha:", True)
        cpf_entry = criar_campo("CPF:")

        def salvar():
            try:
                nome = nome_entry.get()
                email = email_entry.get()
                senha = senha_entry.get()
                cpf = cpf_entry.get()
                
                if nome and email:
                    part_id = len(participantes_lista) + 1
                    participante = Participante(part_id, nome, email, senha, cpf)
                    participantes_lista.append(participante)
                    messagebox.showinfo("Sucesso", "Participante cadastrado!")
                    janela.destroy()
                else:
                    messagebox.showerror("Erro", "Preencha os campos obrigatórios!")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(janela, text="CADASTRAR", bg="#a6e3a1", fg="#1e1e2e", font=("Segoe UI", 10, "bold"), relief="flat", command=salvar).pack(pady=20, fill="x", padx=30)

    def listar_participantes(self):
        janela = tk.Toplevel(self)
        janela.title("Lista de Participantes")
        janela.geometry("800x400")
        janela.configure(bg="#1e1e2e")

        frame_tabela = tk.Frame(janela, bg="#1e1e2e")
        frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

        colunas = ("id", "nome", "email", "cpf", "ingressos")
        tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

        headers = ["ID", "Nome", "Email", "CPF", "Qtd Ingressos"]
        for col, text in zip(colunas, headers):
            tree.heading(col, text=text)

        tree.column("id", width=40, anchor="center")
        tree.column("nome", width=150)
        tree.column("email", width=150)
        tree.column("cpf", width=100, anchor="center")
        tree.column("ingressos", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for p in participantes_lista:
            qtd = len(p.ingressos)
            tree.insert("", tk.END, values=(p.id, p.nome, p.email, p.cpf, qtd))

    def excluir_participante(self):
        janela = tk.Toplevel(self)
        janela.title("Excluir Participante")
        janela.geometry("400x200")
        janela.configure(bg="#1e1e2e")
        
        tk.Label(janela, text="Excluir Participante", font=("Segoe UI", 14, "bold"), bg="#1e1e2e", fg="#f38ba8").pack(pady=15)
        tk.Label(janela, text="Nome do Participante:", bg="#1e1e2e", fg="#cdd6f4").pack(pady=5)
        
        nome_entry = tk.Entry(janela, font=("Segoe UI", 10), bg="#45475a", fg="white", relief="flat", insertbackground="white")
        nome_entry.pack(fill="x", padx=40, pady=5)
        
        def acao():
            nome = nome_entry.get()
            global participantes_lista
            for p in participantes_lista:
                if p.nome == nome:
                    participantes_lista.remove(p)
                    messagebox.showinfo("Sucesso", f"'{nome}' excluído!")
                    janela.destroy()
                    return
            messagebox.showerror("Erro", "Participante não encontrado")
                
        tk.Button(janela, text="CONFIRMAR EXCLUSÃO", bg="#f38ba8", fg="#1e1e2e", font=("Segoe UI", 10, "bold"), relief="flat", command=acao).pack(pady=20, padx=40, fill="x")

    def autenticar_participante(self):
        janela = tk.Toplevel(self)
        janela.title("Login do Participante")
        janela.geometry("350x280")
        janela.configure(bg="#1e1e2e")
        
        tk.Label(janela, text="Login", font=("Segoe UI", 16, "bold"), bg="#1e1e2e", fg="#89b4fa").pack(pady=15)
        
        tk.Label(janela, text="Nome:", bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", padx=30)
        nome_entry = tk.Entry(janela, font=("Segoe UI", 10), bg="#45475a", fg="white", relief="flat", insertbackground="white")
        nome_entry.pack(fill="x", padx=30, pady=(0, 10), ipady=3)
        
        tk.Label(janela, text="Senha:", bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", padx=30)
        senha_entry = tk.Entry(janela, show="*", font=("Segoe UI", 10), bg="#45475a", fg="white", relief="flat", insertbackground="white")
        senha_entry.pack(fill="x", padx=30, pady=(0, 20), ipady=3)
        
        def login():
            nome = nome_entry.get()
            senha = senha_entry.get()
            user = next((p for p in participantes_lista if p.nome == nome), None)
            if user and user.autenticar(senha):
                messagebox.showinfo("Sucesso", f"Bem-vindo, {user.nome}!")
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Credenciais inválidas")
        
        tk.Button(janela, text="ENTRAR", bg="#89b4fa", fg="#1e1e2e", font=("Segoe UI", 10, "bold"), relief="flat", command=login).pack(fill="x", padx=30)

    def inscrever_evento(self):
        janela = tk.Toplevel(self)
        janela.title("Inscrição em Evento")
        janela.geometry("400x400")
        janela.configure(bg="#1e1e2e")
        
        tk.Label(janela, text="Nova Inscrição", font=("Segoe UI", 16, "bold"), bg="#1e1e2e", fg="#a6e3a1").pack(pady=15)
        
        # caixa de seleção de participante
        tk.Label(janela, text="Selecione o Participante:", bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", padx=30)
        part_names = [p.nome for p in participantes_lista]
        part_combo = ttk.Combobox(janela, values=part_names)
        part_combo.pack(fill="x", padx=30, pady=(0, 10), ipady=3)
        
        # caixa de seleção de evento
        tk.Label(janela, text="Selecione o Evento:", bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", padx=30)
        evt_names = [e.nome for e in eventos_lista]
        evt_combo = ttk.Combobox(janela, values=evt_names)
        evt_combo.pack(fill="x", padx=30, pady=(0, 10), ipady=3)
        
        # caixa de seleção do tipo
        tk.Label(janela, text="Tipo de Ingresso:", bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", padx=30)
        tipo_combo = ttk.Combobox(janela, values=["Geral", "Estudante", "VIP"])
        tipo_combo.current(0) # Seleciona o primeiro por padrão
        tipo_combo.pack(fill="x", padx=30, pady=(0, 20), ipady=3)
        
        def confirmar():
            p_nome = part_combo.get()
            e_nome = evt_combo.get()
            
            part = next((p for p in participantes_lista if p.nome == p_nome), None)
            evt = next((e for e in eventos_lista if e.nome == e_nome), None)
            
            if part and evt:
                novo_id = 1000 + len(evt.ingressos)
                # Simulação de preço
                preco = 50.0 if tipo_combo.get() == "Geral" else 25.0
                
                res = part.inscreverEvento(evt, novo_id, tipo_combo.get(), preco)
                if res:
                    messagebox.showinfo("Sucesso", "Inscrição realizada com sucesso!")
                    janela.destroy()
                else:
                    messagebox.showerror("Erro", "Falha: Evento lotado ou erro no sistema.")
            else:
                messagebox.showerror("Erro", "Selecione um Participante e um Evento válidos.")
                
        tk.Button(janela, text="CONFIRMAR INSCRIÇÃO", bg="#a6e3a1", fg="#1e1e2e", font=("Segoe UI", 10, "bold"), relief="flat", command=confirmar).pack(fill="x", padx=30)

    def cancelar_inscricao(self):
        janela = tk.Toplevel(self)
        janela.title("Cancelar Inscrição")
        janela.geometry("400x300")
        janela.configure(bg="#1e1e2e")
        
        tk.Label(janela, text="Cancelar Inscrição", font=("Segoe UI", 14, "bold"), bg="#1e1e2e", fg="#f38ba8").pack(pady=15)
        
        tk.Label(janela, text="Nome do Participante:", bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", padx=30)
        part_names = [p.nome for p in participantes_lista]
        part_combo = ttk.Combobox(janela, values=part_names)
        part_combo.pack(fill="x", padx=30, pady=5)
        
        tk.Label(janela, text="ID do Ingresso:", bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", padx=30)
        ing_entry = tk.Entry(janela, font=("Segoe UI", 10), bg="#45475a", fg="white", relief="flat", insertbackground="white")
        ing_entry.pack(fill="x", padx=30, pady=5)
        
        def cancelar():
            try:
                p_nome = part_combo.get()
                ing_id = int(ing_entry.get())
                
                part = next((p for p in participantes_lista if p.nome == p_nome), None)
                if part:
                    ingresso = next((ing for ing in part.ingressos if ing.id == ing_id), None)
                    if ingresso:
                        part.cancelarInscricao(ingresso)
                        messagebox.showinfo("Sucesso", "Inscrição cancelada!")
                        janela.destroy()
                    else:
                        messagebox.showerror("Erro", "Ingresso não encontrado!")
                else:
                    messagebox.showerror("Erro", "Participante não encontrado!")
            except ValueError:
                messagebox.showerror("Erro", "ID do ingresso deve ser um número.")

        tk.Button(janela, text="CANCELAR", bg="#f38ba8", fg="#1e1e2e", font=("Segoe UI", 10, "bold"), relief="flat", command=cancelar).pack(pady=20, fill="x", padx=30)

if __name__ == "__main__":
    app = InterfaceGrafica()
    app.mainloop()