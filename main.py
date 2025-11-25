import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import traceback 

# Imports do projeto
try:
    from usuario import Usuario
    from ingresso import Ingresso
    from evento import Evento
    from participante import Participante
    from bancoDeDados import Database
except ImportError as e:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Erro de Arquivo", f"Faltam arquivos.\nErro: {e}")
    exit()

class InterfaceGrafica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Organizador de Eventos")
        self.geometry("600x800") # Aumentado para 800px para caber todos os botões sem cortar
        self.configure(bg="#1e1e2e")

        # --- BANCO DE DADOS ---
        try:
            self.db = Database()
        except Exception as e:
            messagebox.showerror("Erro no Banco", f"Erro ao conectar:\n{e}")
            return

        # --- ESTILOS ---
        style = ttk.Style()
        style.theme_use("clam")
        
        # Estilo da Tabela
        style.configure("Treeview", background="#313244", foreground="white", fieldbackground="#313244", rowheight=25)
        style.configure("Treeview.Heading", background="#89b4fa", foreground="#1e1e2e", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[('selected', '#b4befe')])
        
        # Estilo dos Inputs
        style.configure("TSpinbox", fieldbackground="#45475a", background="#89b4fa", foreground="white")
        style.configure("TCombobox", fieldbackground="#45475a", background="#89b4fa", foreground="white")

        self.default_font = ("Segoe UI", 11)

        # Frame Principal
        self.frame_principal = tk.Frame(self, bg="#1e1e2e")
        self.frame_principal.pack(pady=20, fill="both", expand=True)

        tk.Label(self.frame_principal, text="📅 Organizador de Eventos", font=("Segoe UI Black", 22), bg="#1e1e2e", fg="#89dceb").pack(pady=15)

        # --- MENUS ---
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
            btn = tk.Button(card, text=texto, font=self.default_font, bg="#89b4fa", fg="#1e1e2e", relief="flat", activebackground="#b4befe", padx=10, pady=5, cursor="hand2", command=comando)
            btn.pack(pady=4, fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#b4befe"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#89b4fa"))

    # ==================================================================
    #  EVENTOS
    # ==================================================================

    def cadastrar_evento(self):
        janela = tk.Toplevel(self)
        janela.title("Cadastrar Evento")
        janela.geometry("550x700")
        janela.configure(bg="#1e1e2e")

        tk.Label(janela, text="Novo Evento", font=("Segoe UI", 16, "bold"), bg="#1e1e2e", fg="#89dceb").pack(pady=15)

        def criar_campo(texto):
            tk.Label(janela, text=texto, bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 10)).pack(anchor="w", padx=30, pady=(5, 0))
            entry = tk.Entry(janela, font=("Segoe UI", 10), bg="#45475a", fg="white", relief="flat", insertbackground="white")
            entry.pack(fill="x", padx=30, pady=5, ipady=3)
            return entry

        def criar_seletor_data_hora(texto):
            tk.Label(janela, text=texto, bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 10)).pack(anchor="w", padx=30, pady=(10, 0))
            frame = tk.Frame(janela, bg="#1e1e2e")
            frame.pack(fill="x", padx=30, pady=2)
            
            sb_dia = ttk.Spinbox(frame, from_=1, to=31, width=3); sb_dia.set(datetime.now().day); sb_dia.pack(side="left", padx=2)
            tk.Label(frame, text="/", bg="#1e1e2e", fg="white").pack(side="left")
            sb_mes = ttk.Spinbox(frame, from_=1, to=12, width=3); sb_mes.set(datetime.now().month); sb_mes.pack(side="left", padx=2)
            tk.Label(frame, text="/", bg="#1e1e2e", fg="white").pack(side="left")
            sb_ano = ttk.Spinbox(frame, from_=2024, to=2030, width=5); sb_ano.set(datetime.now().year); sb_ano.pack(side="left", padx=2)
            
            tk.Label(frame, text=" às ", bg="#1e1e2e", fg="white").pack(side="left", padx=10)
            sb_hora = ttk.Spinbox(frame, from_=0, to=23, width=3, format="%02.0f"); sb_hora.set("19"); sb_hora.pack(side="left", padx=2)
            tk.Label(frame, text=":", bg="#1e1e2e", fg="white").pack(side="left")
            sb_min = ttk.Spinbox(frame, from_=0, to=59, width=3, format="%02.0f"); sb_min.set("00"); sb_min.pack(side="left", padx=2)
            return sb_dia, sb_mes, sb_ano, sb_hora, sb_min

        nome_entry = criar_campo("Nome do Evento:")
        desc_entry = criar_campo("Descrição:")
        
        d1, m1, a1, h1, min1 = criar_seletor_data_hora("Início:")
        d2, m2, a2, h2, min2 = criar_seletor_data_hora("Fim:")
        
        cap_entry = criar_campo("Capacidade Máxima:")
        
        tk.Label(janela, text="--- Dados do Local ---", bg="#1e1e2e", fg="#fab387", font=("Segoe UI", 10, "bold")).pack(pady=15)
        local_nome_entry = criar_campo("Nome do Local:")
        local_end_entry = criar_campo("Endereço:")

        def salvar():
            try:
                nome = nome_entry.get().strip()
                desc = desc_entry.get().strip()
                
                try:
                    data_inicio = datetime(int(a1.get()), int(m1.get()), int(d1.get()), int(h1.get()), int(min1.get()))
                    data_fim = datetime(int(a2.get()), int(m2.get()), int(d2.get()), int(h2.get()), int(min2.get()))
                except ValueError:
                    messagebox.showerror("Erro", "Data inválida.")
                    return

                if data_fim <= data_inicio:
                    messagebox.showerror("Erro", "A data final deve ser posterior à inicial.")
                    return

                cap = int(cap_entry.get().strip())

                local_info = {
                    "id": 0, 
                    "nome": local_nome_entry.get().strip(),
                    "endereco": local_end_entry.get().strip(),
                    "capacidade": cap
                }

                if not (nome and local_info["nome"]):
                    messagebox.showerror("Erro", "Nome do evento e do local são obrigatórios.")
                    return

                evento = Evento(None, nome, desc, data_inicio, data_fim, cap, local_info)

                self.db.salvar_evento(evento)
                messagebox.showinfo("Sucesso", "Evento cadastrado com sucesso!")
                janela.destroy()

            except ValueError:
                messagebox.showerror("Erro", "Capacidade deve ser um número.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {e}")

        tk.Button(janela, text="SALVAR EVENTO", bg="#a6e3a1", fg="#1e1e2e", font=("Segoe UI", 10, "bold"), command=salvar).pack(pady=20, fill="x", padx=30)

    def listar_eventos(self):
        janela = tk.Toplevel(self)
        janela.title("Listar Eventos")
        janela.geometry("900x400")
        janela.configure(bg="#1e1e2e")

        frame_tabela = tk.Frame(janela, bg="#1e1e2e")
        frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

        colunas = ("id", "nome", "data", "local", "vagas")
        tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", selectmode="browse")

        tree.heading("id", text="ID")
        tree.heading("nome", text="Evento")
        tree.heading("data", text="Início")
        tree.heading("local", text="Local")
        tree.heading("vagas", text="Capacidade")

        tree.column("id", width=40, anchor="center")
        tree.column("nome", width=200)
        tree.column("data", width=120, anchor="center")
        tree.column("local", width=150)
        tree.column("vagas", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        eventos = self.db.listar_eventos()
        for e in eventos:
            tree.insert("", tk.END, values=(e[0], e[1], e[3], e[7], e[5]))

    def excluir_evento(self):
        janela = tk.Toplevel(self)
        janela.title("Excluir Evento")
        janela.geometry("400x250") # Aumentado
        janela.configure(bg="#1e1e2e")

        tk.Label(janela, text="Nome do Evento:", bg="#1e1e2e", fg="#cdd6f4").pack(pady=(30, 5))
        nome_entry = tk.Entry(janela, font=("Segoe UI", 10))
        nome_entry.pack(fill="x", padx=40)

        def excluir():
            nome = nome_entry.get().strip()
            if self.db.excluir_evento(nome):
                messagebox.showinfo("Sucesso", "Evento excluído!")
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Evento não encontrado.")

        tk.Button(janela, text="EXCLUIR", bg="#f38ba8", fg="#1e1e2e", font=("Segoe UI", 10, "bold"), command=excluir).pack(pady=30, padx=40, fill="x")

    # ==================================================================
    #  PARTICIPANTES
    # ==================================================================

    def cadastrar_participante(self):
        janela = tk.Toplevel(self)
        janela.title("Cadastrar Participante")
        janela.geometry("400x450")
        janela.configure(bg="#1e1e2e")

        tk.Label(janela, text="Novo Participante", font=("Segoe UI", 16, "bold"), bg="#1e1e2e", fg="#89dceb").pack(pady=15)

        def criar_campo(texto, is_senha=False):
            tk.Label(janela, text=texto, bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", padx=30, pady=(5,0))
            entry = tk.Entry(janela, show="*" if is_senha else "", font=("Segoe UI", 10))
            entry.pack(fill="x", padx=30, pady=5, ipady=3)
            return entry

        nome_entry = criar_campo("Nome:")
        email_entry = criar_campo("Email:")
        senha_entry = criar_campo("Senha:", True)
        cpf_entry = criar_campo("CPF:")

        def salvar():
            nome = nome_entry.get().strip()
            email = email_entry.get().strip()
            senha = senha_entry.get().strip()
            cpf = cpf_entry.get().strip()

            if not (nome and email and senha):
                messagebox.showerror("Erro", "Preencha os campos obrigatórios.")
                return

            part = Participante(0, nome, email, senha, cpf)
            if self.db.salvar_participante(part):
                messagebox.showinfo("Sucesso", "Participante cadastrado!")
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao salvar.")

        tk.Button(janela, text="CADASTRAR", bg="#a6e3a1", fg="#1e1e2e", font=("Segoe UI", 10, "bold"), command=salvar).pack(pady=20, fill="x", padx=30)

    def listar_participantes(self):
        janela = tk.Toplevel(self)
        janela.title("Listar Participantes")
        janela.geometry("800x400")
        janela.configure(bg="#1e1e2e")

        frame_tabela = tk.Frame(janela, bg="#1e1e2e")
        frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

        colunas = ("id", "nome", "email", "cpf")
        tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

        tree.heading("id", text="ID")
        tree.heading("nome", text="Nome")
        tree.heading("email", text="Email")
        tree.heading("cpf", text="CPF")

        tree.column("id", width=40, anchor="center")
        tree.column("nome", width=200)
        tree.column("email", width=200)
        tree.column("cpf", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        parts = self.db.listar_participantes()
        for p in parts:
            tree.insert("", tk.END, values=(p[0], p[1], p[2], p[4]))

    def excluir_participante(self):
        janela = tk.Toplevel(self)
        janela.title("Excluir Participante")
        janela.geometry("400x250") # Aumentado
        janela.configure(bg="#1e1e2e")
        
        tk.Label(janela, text="Nome do Participante:", bg="#1e1e2e", fg="#cdd6f4").pack(pady=(30,5))
        nome_entry = tk.Entry(janela, font=("Segoe UI", 10))
        nome_entry.pack(fill="x", padx=40)
        
        def acao():
            nome = nome_entry.get().strip()
            if self.db.excluir_participante(nome):
                messagebox.showinfo("Sucesso", "Participante excluído!")
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Participante não encontrado.")
                
        tk.Button(janela, text="EXCLUIR", bg="#f38ba8", fg="#1e1e2e", font=("Segoe UI", 10, "bold"), command=acao).pack(pady=30, padx=40, fill="x")

    def autenticar_participante(self):
        janela = tk.Toplevel(self)
        janela.title("Login")
        janela.geometry("350x250")
        janela.configure(bg="#1e1e2e")
        
        tk.Label(janela, text="Email:", bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", padx=30, pady=(20,0))
        email_entry = tk.Entry(janela); email_entry.pack(fill="x", padx=30, pady=5)
        
        tk.Label(janela, text="Senha:", bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", padx=30)
        senha_entry = tk.Entry(janela, show="*"); senha_entry.pack(fill="x", padx=30, pady=5)
        
        def login():
            res = self.db.autenticar_participante(email_entry.get().strip(), senha_entry.get().strip())
            if res:
                messagebox.showinfo("Sucesso", f"Bem-vindo, {res[1]}!")
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Dados inválidos.")
        
        tk.Button(janela, text="ENTRAR", bg="#89b4fa", fg="#1e1e2e", font=("Segoe UI", 10, "bold"), command=login).pack(fill="x", padx=30, pady=20)

    # ==================================================================
    #  INSCRIÇÕES E CANCELAMENTOS (VISUAL NOVO)
    # ==================================================================

    def inscrever_evento(self):
        janela = tk.Toplevel(self)
        janela.title("Inscrição")
        janela.geometry("450x400") # Aumentado para caber tudo sem cortar
        janela.configure(bg="#1e1e2e")
        
        tk.Label(janela, text="Nova Inscrição", font=("Segoe UI", 16, "bold"), bg="#1e1e2e", fg="#a6e3a1").pack(pady=20)

        parts = self.db.listar_participantes()
        evts = self.db.listar_eventos()
        
        if not parts or not evts:
            messagebox.showerror("Erro", "Cadastre participantes e eventos primeiro.")
            janela.destroy()
            return

        part_options = [f"{p[0]} - {p[1]}" for p in parts]
        evt_options = [f"{e[0]} - {e[1]}" for e in evts]

        tk.Label(janela, text="Selecione o Participante:", bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", padx=30, pady=(10,0))
        part_combo = ttk.Combobox(janela, values=part_options)
        part_combo.pack(fill="x", padx=30, pady=5)
        
        tk.Label(janela, text="Selecione o Evento:", bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", padx=30, pady=(10,0))
        evt_combo = ttk.Combobox(janela, values=evt_options)
        evt_combo.pack(fill="x", padx=30, pady=5)
        
        def confirmar():
            try:
                p_sel = part_combo.get()
                e_sel = evt_combo.get()
                if not p_sel or not e_sel: return

                p_id = int(p_sel.split(" - ")[0])
                e_id = int(e_sel.split(" - ")[0])
                
                if self.db.verificar_inscricao(p_id, e_id):
                    messagebox.showinfo("Aviso", "Participante já está inscrito.")
                    return
                
                if self.db.inscrever_participante(p_id, e_id):
                    messagebox.showinfo("Sucesso", "Inscrito com sucesso!")
                    janela.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao inscrever.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")
                
        tk.Button(janela, text="CONFIRMAR INSCRIÇÃO", bg="#a6e3a1", fg="#1e1e2e", font=("Segoe UI", 10, "bold"), command=confirmar).pack(fill="x", padx=30, pady=40)

    def cancelar_inscricao(self):
        janela = tk.Toplevel(self)
        janela.title("Cancelar Inscrição")
        janela.geometry("450x400") # Aumentado para resolver o problema do botão "la em baixo"
        janela.configure(bg="#1e1e2e")
        
        tk.Label(janela, text="Cancelar Inscrição", font=("Segoe UI", 16, "bold"), bg="#1e1e2e", fg="#f38ba8").pack(pady=20)
        
        parts = self.db.listar_participantes()
        evts = self.db.listar_eventos()
        
        if not parts or not evts:
            messagebox.showerror("Erro", "Sem dados para cancelar.")
            janela.destroy()
            return
        
        part_options = [f"{p[0]} - {p[1]}" for p in parts]
        evt_options = [f"{e[0]} - {e[1]}" for e in evts]

        tk.Label(janela, text="Participante:", bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", padx=30, pady=(10,0))
        part_combo = ttk.Combobox(janela, values=part_options)
        part_combo.pack(fill="x", padx=30, pady=5)
        
        tk.Label(janela, text="Evento:", bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", padx=30, pady=(10,0))
        evt_combo = ttk.Combobox(janela, values=evt_options)
        evt_combo.pack(fill="x", padx=30, pady=5)
        
        def cancelar():
            try:
                p_sel = part_combo.get()
                e_sel = evt_combo.get()
                
                if not p_sel or not e_sel:
                    messagebox.showwarning("Atenção", "Selecione participante e evento.")
                    return

                p_id = int(p_sel.split(" - ")[0])
                e_id = int(e_sel.split(" - ")[0])
                
                if self.db.cancelar_inscricao(p_id, e_id):
                    messagebox.showinfo("Sucesso", "Inscrição cancelada.")
                    janela.destroy()
                else:
                    messagebox.showerror("Erro", "Inscrição não encontrada ou erro no banco.")
            except Exception as e: 
                messagebox.showerror("Erro", str(e))

      
        tk.Button(janela, text="CANCELAR INSCRIÇÃO", bg="#f38ba8", fg="#1e1e2e", font=("Segoe UI", 10, "bold"), command=cancelar).pack(fill="x", padx=30, pady=40)

if __name__ == "__main__":
    try:
        app = InterfaceGrafica()
        app.mainloop()
    except Exception as e:
        import traceback
        traceback.print_exc()
        try:
            err_window = tk.Tk()
            err_window.withdraw()
            messagebox.showerror("Erro Fatal ao Iniciar", f"Ocorreu um erro:\n{e}\n\nVerifique o console para mais detalhes.")
        except:
            print(f"Erro fatal irrecuperável: {e}")