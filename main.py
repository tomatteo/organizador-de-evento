import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from usuario import Usuario
from ingresso import Ingresso
from evento import Evento
from participante import Participante
from bancoDeDados import Database 


class InterfaceGrafica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Organizador de Eventos")
        self.geometry("550x520")
        self.configure(bg="#1e1e2e")

        # BANCO DE DADOS
        self.db = Database()

        self.default_font = ("Segoe UI", 11)

        self.frame_principal = tk.Frame(self, bg="#1e1e2e")
        self.frame_principal.pack(pady=20)

        tk.Label(
            self.frame_principal,
            text="📅 Organizador de Eventos",
            font=("Segoe UI Black", 20),
            bg="#1e1e2e",
            fg="#89dceb"
        ).pack(pady=15)

        # Seção de eventos
        self.criar_card("Gerenciar Eventos", [
            ("Cadastrar Evento", self.cadastrar_evento),
            ("Listar Eventos", self.listar_eventos),
            ("Excluir Evento", self.excluir_evento)
        ])

        # Seção de participantes
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
        card.pack(pady=10, fill="both")

        tk.Label(card, text=titulo, font=("Segoe UI", 14, "bold"), bg="#313244", fg="white").pack(pady=5)

        for texto, comando in botoes:
            btn = tk.Button(
                card,
                text=texto,
                font=self.default_font,
                bg="#89b4fa",
                fg="black",
                relief="flat",
                activebackground="#b4befe",
                padx=10,
                pady=5,
                command=comando
            )
            btn.pack(pady=4, fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#b4befe"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#89b4fa"))

    # --------------------------
    # eventos
    # --------------------------
    def cadastrar_evento(self):
        janela = tk.Toplevel(self)
        janela.title("Cadastrar Evento")
        janela.geometry("400x500")

        # campos
        tk.Label(janela, text="Nome:").pack()
        nome_entry = tk.Entry(janela); nome_entry.pack()
        tk.Label(janela, text="Descrição:").pack()
        desc_entry = tk.Entry(janela); desc_entry.pack()
        tk.Label(janela, text="Data Início (YYYY-MM-DD HH:MM):").pack()
        data_inicio_entry = tk.Entry(janela); data_inicio_entry.pack()
        tk.Label(janela, text="Data Fim (YYYY-MM-DD HH:MM):").pack()
        data_fim_entry = tk.Entry(janela); data_fim_entry.pack()
        tk.Label(janela, text="Capacidade:").pack()
        cap_entry = tk.Entry(janela); cap_entry.pack()
        tk.Label(janela, text="ID do Local:").pack()
        local_id_entry = tk.Entry(janela); local_id_entry.pack()
        tk.Label(janela, text="Nome do Local:").pack()
        local_nome_entry = tk.Entry(janela); local_nome_entry.pack()
        tk.Label(janela, text="Endereço do Local:").pack()
        local_end_entry = tk.Entry(janela); local_end_entry.pack()
        tk.Label(janela, text="Capacidade do Local:").pack()
        local_cap_entry = tk.Entry(janela); local_cap_entry.pack()

        def salvar():
            try:
                nome = nome_entry.get().strip()
                desc = desc_entry.get().strip()
                data_inicio = datetime.strptime(data_inicio_entry.get().strip(), "%Y-%m-%d %H:%M")
                data_fim = datetime.strptime(data_fim_entry.get().strip(), "%Y-%m-%d %H:%M")
                cap = int(cap_entry.get().strip())

                local_info = {
                    "id": int(local_id_entry.get().strip()),
                    "nome": local_nome_entry.get().strip(),
                    "endereco": local_end_entry.get().strip(),
                    "capacidade": int(local_cap_entry.get().strip())
                }

                evento = Evento(
                    id=None,
                    nome=nome,
                    descricao=desc,
                    dataInicio=data_inicio,
                    dataFim=data_fim,
                    capacidade=cap,
                    local_info=local_info
                )

                self.db.salvar_evento(evento)
                messagebox.showinfo("Sucesso", "Evento cadastrado com sucesso!")
                janela.destroy()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar evento: {e}")

        tk.Button(janela, text="Salvar Evento", command=salvar).pack(pady=10)

    def listar_eventos(self):
        janela = tk.Toplevel(self)
        janela.title("Listar Eventos")
        janela.geometry("420x350")
        text_area = tk.Text(janela); text_area.pack(expand=True, fill="both")
        eventos = self.db.listar_eventos()
        if not eventos:
            text_area.insert(tk.END, "Nenhum evento cadastrado.\n")
            return
        for e in eventos:
            linha = f"ID:{e[0]} | Nome: {e[1]} | Data Início: {e[3]} | Capacidade: {e[5]} | Local: {e[7]}\n"
            text_area.insert(tk.END, linha)

    def excluir_evento(self):
        janela = tk.Toplevel(self)
        janela.title("Excluir Evento")
        janela.geometry("300x150")
        tk.Label(janela, text="Nome do Evento:").pack()
        nome_entry = tk.Entry(janela); nome_entry.pack()

        def excluir():
            nome = nome_entry.get().strip()
            if self.db.excluir_evento(nome):
                messagebox.showinfo("Sucesso", "Evento excluído com sucesso!")
            else:
                messagebox.showerror("Erro", "Evento não encontrado!")
            janela.destroy()

        tk.Button(janela, text="Excluir", command=excluir).pack(pady=10)

    # --------------------------
    # participantes
    # --------------------------
    def cadastrar_participante(self):
        janela = tk.Toplevel(self)
        janela.title("Cadastrar Participante")
        janela.geometry("320x260")

        tk.Label(janela, text="Nome:").pack(); nome_entry = tk.Entry(janela); nome_entry.pack()
        tk.Label(janela, text="Email:").pack(); email_entry = tk.Entry(janela); email_entry.pack()
        tk.Label(janela, text="Senha:").pack(); senha_entry = tk.Entry(janela, show="*"); senha_entry.pack()
        tk.Label(janela, text="CPF:").pack(); cpf_entry = tk.Entry(janela); cpf_entry.pack()

        def salvar():
            nome = nome_entry.get().strip()
            email = email_entry.get().strip()
            senha = senha_entry.get().strip()
            cpf = cpf_entry.get().strip()
            if not (nome and email and senha and cpf):
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return
            participante = Participante(0, nome, email, senha, cpf)
            ok = self.db.salvar_participante(participante)
            if ok:
                messagebox.showinfo("Sucesso", "Participante cadastrado!")
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Não foi possível cadastrar (email pode já existir).")

        tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

    def listar_participantes(self):
        janela = tk.Toplevel(self)
        janela.title("Listar Participantes")
        janela.geometry("400x300")
        text_area = tk.Text(janela); text_area.pack(expand=True, fill="both")

        participantes = self.db.listar_participantes()
        if not participantes:
            text_area.insert(tk.END, "Nenhum participante cadastrado.\n")
            return

        # participantes (id, nome, email, senha, cpf)
        for p in participantes:
            linha = f"ID:{p[0]} | Nome: {p[1]} | Email: {p[2]} | CPF: {p[4]}\n"
            text_area.insert(tk.END, linha)

    def excluir_participante(self):
        janela = tk.Toplevel(self)
        janela.title("Excluir Participante")
        janela.geometry("300x150")
        tk.Label(janela, text="Nome do Participante:").pack()
        nome_entry = tk.Entry(janela); nome_entry.pack()

        def excluir():
            nome = nome_entry.get().strip()
            if self.db.excluir_participante(nome):
                messagebox.showinfo("Sucesso", "Participante excluído!")
            else:
                messagebox.showerror("Erro", "Participante não encontrado!")
            janela.destroy()

        tk.Button(janela, text="Excluir", command=excluir).pack(pady=10)

    # --------------------------
    # autenticação
    # --------------------------
    def autenticar_participante(self):
        janela = tk.Toplevel(self)
        janela.title("Autenticar Participante"); janela.geometry("360x200")
        tk.Label(janela, text="Email:").pack(anchor="w", padx=10, pady=(10,0))
        email_entry = tk.Entry(janela); email_entry.pack(fill="x", padx=10, pady=5)
        tk.Label(janela, text="Senha:").pack(anchor="w", padx=10)
        senha_entry = tk.Entry(janela, show="*"); senha_entry.pack(fill="x", padx=10, pady=5)

        def autenticar():
            email = email_entry.get().strip(); senha = senha_entry.get().strip()
            if not email or not senha:
                messagebox.showerror("Erro", "Preencha email e senha."); return
            res = self.db.autenticar_participante(email, senha)
            if res:
                participante_id, nome = res[0], res[1]
                messagebox.showinfo("Sucesso", f"Autenticação bem-sucedida!\nBem-vindo, {nome} (ID {participante_id}).")
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Credenciais inválidas.")

        tk.Button(janela, text="Autenticar", command=autenticar).pack(pady=12, padx=10, fill="x")

    # --------------------------
    # inscrever no evento
    # --------------------------
    def inscrever_evento(self):
        janela = tk.Toplevel(self)
        janela.title("Inscrever em Evento"); janela.geometry("420x260")

        participantes = self.db.listar_participantes()
        eventos = self.db.listar_eventos()

        if not participantes:
            messagebox.showerror("Erro", "Não há participantes cadastrados."); janela.destroy(); return
        if not eventos:
            messagebox.showerror("Erro", "Não há eventos cadastrados."); janela.destroy(); return

        # cria listas ordenadas (garante ordem previsível)
        part_items = [ (p[0], f"{p[1]} ({p[2]})") for p in participantes ]
        evt_items  = [ (e[0], f"{e[1]} (cap {e[5]})") for e in eventos ]

        part_map = { f"{pid} - {label}": pid for pid, label in part_items }
        evt_map  = { f"{eid} - {label}": eid  for eid, label in evt_items }

        part_keys = list(part_map.keys())
        evt_keys = list(evt_map.keys())

        tk.Label(janela, text="Selecione o Participante:").pack(anchor="w", padx=10, pady=(10,0))
        part_var = tk.StringVar(janela); part_var.set(part_keys[0])
        tk.OptionMenu(janela, part_var, *part_keys).pack(fill="x", padx=10, pady=5)

        tk.Label(janela, text="Selecione o Evento:").pack(anchor="w", padx=10)
        evt_var = tk.StringVar(janela); evt_var.set(evt_keys[0])
        tk.OptionMenu(janela, evt_var, *evt_keys).pack(fill="x", padx=10, pady=5)

        def confirmar_inscricao():
            participante_id = part_map[part_var.get()]
            evento_id = evt_map[evt_var.get()]

            cur = self.db.conn.cursor()
            cur.execute("SELECT COUNT(*) FROM inscricoes WHERE evento_id = ?", (evento_id,))
            inscritos_count = cur.fetchone()[0]

            cur.execute("SELECT capacidade FROM eventos WHERE id = ?", (evento_id,))
            row = cur.fetchone(); capacidade = row[0] if row else None

            if capacidade is not None and inscritos_count >= capacidade:
                messagebox.showerror("Erro", "Não é possível inscrever: evento lotado."); return

            if self.db.verificar_inscricao(participante_id, evento_id):
                messagebox.showerror("Erro", "Participante já inscrito neste evento."); return

            ok = self.db.inscrever_participante(participante_id, evento_id)
            if ok:
                messagebox.showinfo("Sucesso", "Inscrição realizada com sucesso!"); janela.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao inscrever (duplicidade ou erro).")

        tk.Button(janela, text="Confirmar Inscrição", command=confirmar_inscricao).pack(pady=12, padx=10, fill="x")

    # --------------------------
    # cancelar inscreção
    # --------------------------
    def cancelar_inscricao(self):
        janela = tk.Toplevel(self)
        janela.title("Cancelar Inscrição"); janela.geometry("420x260")

        participantes = self.db.listar_participantes()
        eventos = self.db.listar_eventos()

        if not participantes:
            messagebox.showerror("Erro", "Não há participantes cadastrados."); janela.destroy(); return
        if not eventos:
            messagebox.showerror("Erro", "Não há eventos cadastrados."); janela.destroy(); return

        part_items = [ (p[0], f"{p[1]} ({p[2]})") for p in participantes ]
        evt_items  = [ (e[0], f"{e[1]}") for e in eventos ]

        part_map = { f"{pid} - {label}": pid for pid, label in part_items }
        evt_map  = { f"{eid} - {label}": eid  for eid, label in evt_items }

        part_keys = list(part_map.keys())
        evt_keys = list(evt_map.keys())

        tk.Label(janela, text="Selecione o Participante:").pack(anchor="w", padx=10, pady=(10,0))
        part_var = tk.StringVar(janela); part_var.set(part_keys[0])
        tk.OptionMenu(janela, part_var, *part_keys).pack(fill="x", padx=10, pady=5)

        tk.Label(janela, text="Selecione o Evento:").pack(anchor="w", padx=10)
        evt_var = tk.StringVar(janela); evt_var.set(evt_keys[0])
        tk.OptionMenu(janela, evt_var, *evt_keys).pack(fill="x", padx=10, pady=5)

        def confirmar_cancelamento():
            participante_id = part_map[part_var.get()]
            evento_id = evt_map[evt_var.get()]

            if not self.db.verificar_inscricao(participante_id, evento_id):
                messagebox.showerror("Erro", "Esse participante não está inscrito neste evento."); return

            ok = self.db.cancelar_inscricao(participante_id, evento_id)
            if ok:
                messagebox.showinfo("Sucesso", "Inscrição cancelada com sucesso."); janela.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao cancelar inscrição.")

        tk.Button(janela, text="Cancelar Inscrição", command=confirmar_cancelamento).pack(pady=12, padx=10, fill="x")


if __name__ == "__main__":
    app = InterfaceGrafica()
    app.mainloop()