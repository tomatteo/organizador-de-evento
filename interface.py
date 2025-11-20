import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from usuario import Usuario
from ingresso import Ingresso
from evento import Evento
from participante import Participante

# Listas globais
eventos_lista = []
participantes_lista = []

class InterfaceGrafica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Organizador de Eventos")
        self.geometry("550x520")
        self.configure(bg="#1e1e2e")  # Fundo escuro estiloso

        # Fonte padrão
        self.default_font = ("Segoe UI", 11)

        # Frame principal estilizado
        self.frame_principal = tk.Frame(self, bg="#1e1e2e")
        self.frame_principal.pack(pady=20)

        # Título principal
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

    # ==== COMPONENTE PARA CRIAR SEÇÕES COM BOTÕES ====

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

            # efeito hover
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#b4befe"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#89b4fa"))

    # ---------------------------------------------------
    #  DAQUI PRA BAIXO O CÓDIGO É O MESMO DO SEU (funções sem mudanças)
    # ---------------------------------------------------

    def cadastrar_evento(self):
        janela = tk.Toplevel(self)
        janela.title("Cadastrar Evento")
        janela.geometry("400x400")

        tk.Label(janela, text="Nome:").pack()
        nome_entry = tk.Entry(janela)
        nome_entry.pack()

        tk.Label(janela, text="Descrição:").pack()
        desc_entry = tk.Entry(janela)
        desc_entry.pack()

        tk.Label(janela, text="Data Início (YYYY-MM-DD HH:MM):").pack()
        data_inicio_entry = tk.Entry(janela)
        data_inicio_entry.pack()

        tk.Label(janela, text="Data Fim (YYYY-MM-DD HH:MM):").pack()
        data_fim_entry = tk.Entry(janela)
        data_fim_entry.pack()

        tk.Label(janela, text="Capacidade:").pack()
        cap_entry = tk.Entry(janela)
        cap_entry.pack()

        tk.Label(janela, text="ID do Local:").pack()
        local_id_entry = tk.Entry(janela)
        local_id_entry.pack()

        tk.Label(janela, text="Nome do Local:").pack()
        local_nome_entry = tk.Entry(janela)
        local_nome_entry.pack()

        tk.Label(janela, text="Endereço do Local:").pack()
        local_end_entry = tk.Entry(janela)
        local_end_entry.pack()

        tk.Label(janela, text="Capacidade do Local:").pack()
        local_cap_entry = tk.Entry(janela)
        local_cap_entry.pack()

        def salvar():
            try:
                nome = nome_entry.get()
                desc = desc_entry.get()
                data_inicio = datetime.strptime(data_inicio_entry.get(), "%Y-%m-%d %H:%M")
                data_fim = datetime.strptime(data_fim_entry.get(), "%Y-%m-%d %H:%M")
                cap = int(cap_entry.get())
                local_info = {
                    'id': int(local_id_entry.get()),
                    'nome': local_nome_entry.get(),
                    'endereco': local_end_entry.get(),
                    'capacidade': int(local_cap_entry.get())
                }
                if nome and desc and cap > 0:
                    evento_id = len(eventos_lista) + 1
                    evento = Evento(evento_id, nome, desc, data_inicio, data_fim, cap, local_info)
                    eventos_lista.append(evento)
                    messagebox.showinfo("Sucesso", "Evento cadastrado com sucesso!")
                    janela.destroy()
                else:
                    messagebox.showerror("Erro", "Preencha todos os campos corretamente!")
            except ValueError as e:
                messagebox.showerror("Erro", f"Dados inválidos: {str(e)}")

        tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

    def listar_eventos(self):
        janela = tk.Toplevel(self)
        janela.title("Listar Eventos")
        janela.geometry("400x300")

        text_area = tk.Text(janela)
        text_area.pack(expand=True, fill=tk.BOTH)

        for evento in eventos_lista:
            text_area.insert(tk.END, str(evento) + "\n\n")

    def excluir_evento(self):
        janela = tk.Toplevel(self)
        janela.title("Excluir Evento")
        janela.geometry("300x150")

        tk.Label(janela, text="Nome do Evento:").pack()
        nome_entry = tk.Entry(janela)
        nome_entry.pack()

        def excluir():
            nome = nome_entry.get()
            global eventos_lista
            eventos_filtrados = [e for e in eventos_lista if e.nome != nome]
            if len(eventos_filtrados) < len(eventos_lista):
                eventos_lista = eventos_filtrados
                messagebox.showinfo("Sucesso", "Evento excluído com sucesso!")
            else:
                messagebox.showerror("Erro", "Evento não encontrado!")
            janela.destroy()

        tk.Button(janela, text="Excluir", command=excluir).pack(pady=10)


    # --- Participantes (idêntico ao seu) ---

    def cadastrar_participante(self):
        janela = tk.Toplevel(self)
        janela.title("Cadastrar Participante")
        janela.geometry("300x250")

        tk.Label(janela, text="Nome:").pack()
        nome_entry = tk.Entry(janela)
        nome_entry.pack()

        tk.Label(janela, text="Email:").pack()
        email_entry = tk.Entry(janela)
        email_entry.pack()

        tk.Label(janela, text="Senha:").pack()
        senha_entry = tk.Entry(janela, show="*")
        senha_entry.pack()

        tk.Label(janela, text="CPF:").pack()
        cpf_entry = tk.Entry(janela)
        cpf_entry.pack()

        def salvar():
            try:
                nome = nome_entry.get()
                email = email_entry.get()
                senha = senha_entry.get()
                cpf = cpf_entry.get()
                if nome and email and senha and cpf:
                    part_id = len(participantes_lista) + 1
                    participante = Participante(part_id, nome, email, senha, cpf)
                    participantes_lista.append(participante)
                    messagebox.showinfo("Sucesso", "Participante cadastrado com sucesso!")
                    janela.destroy()
                else:
                    messagebox.showerror("Erro", "Preencha todos os campos!")
            except ValueError as e:
                messagebox.showerror("Erro", f"Dados inválidos: {str(e)}")

        tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

    def listar_participantes(self):
        janela = tk.Toplevel(self)
        janela.title("Listar Participantes")
        janela.geometry("400x300")

        text_area = tk.Text(janela)
        text_area.pack(expand=True, fill=tk.BOTH)

        for part in participantes_lista:
            ingressos_str = ", ".join([f"ID {ing.id}" for ing in part.ingressos])
            text_area.insert(tk.END, f"Nome: {part.nome}, Email: {part.email}, CPF: {part.cpf}, Ingressos: {ingressos_str}\n")

    def excluir_participante(self):
        janela = tk.Toplevel(self)
        janela.title("Excluir Participante")
        janela.geometry("300x150")

        tk.Label(janela, text="Nome do Participante:").pack()
        nome_entry = tk.Entry(janela)
        nome_entry.pack()

        def excluir():
            nome = nome_entry.get()
            global participantes_lista
            participantes_filtrados = [p for p in participantes_lista if p.nome != nome]
            if len(participantes_filtrados) < len(participantes_lista):
                participantes_lista = participantes_filtrados
                messagebox.showinfo("Sucesso", "Participante excluído com sucesso!")
            else:
                messagebox.showerror("Erro", "Participante não encontrado!")
            janela.destroy()

        tk.Button(janela, text="Excluir", command=excluir).pack(pady=10)

    def autenticar_participante(self):
        janela = tk.Toplevel(self)
        janela.title("Autenticar Participante")
        janela.geometry("300x150")

        tk.Label(janela, text="Nome:").pack()
        nome_entry = tk.Entry(janela)
        nome_entry.pack()

        tk.Label(janela, text="Senha:").pack()
        senha_entry = tk.Entry(janela, show="*")
        senha_entry.pack()

        def autenticar():
            nome = nome_entry.get()
            senha = senha_entry.get()
            participante = next((p for p in participantes_lista if p.nome == nome), None)
            if participante and participante.autenticar(senha):
                messagebox.showinfo("Sucesso", "Autenticação bem-sucedida!")
            else:
                messagebox.showerror("Erro", "Autenticação falhou!")
            janela.destroy()

        tk.Button(janela, text="Autenticar", command=autenticar).pack(pady=10)

    def inscrever_evento(self):
        janela = tk.Toplevel(self)
        janela.title("Inscrever em Evento")
        janela.geometry("300x250")

        tk.Label(janela, text="Nome do Participante:").pack()
        part_entry = tk.Entry(janela)
        part_entry.pack()

        tk.Label(janela, text="Nome do Evento:").pack()
        evento_entry = tk.Entry(janela)
        evento_entry.pack()

        tk.Label(janela, text="Tipo do Ingresso:").pack()
        tipo_entry = tk.Entry(janela)
        tipo_entry.pack()

        tk.Label(janela, text="Preço do Ingresso:").pack()
        preco_entry = tk.Entry(janela)
        preco_entry.pack()

        def inscrever():
            part_nome = part_entry.get()
            evento_nome = evento_entry.get()
            tipo = tipo_entry.get()
            preco = float(preco_entry.get())
            participante = next((p for p in participantes_lista if p.nome == part_nome), None)
            evento = next((e for e in eventos_lista if e.nome == evento_nome), None)
            if participante and evento:
                ingresso_id = len(evento.ingressos) + 1
                ingresso = participante.inscreverEvento(evento, ingresso_id, tipo, preco)
                if ingresso:
                    messagebox.showinfo("Sucesso", f"Inscrição bem-sucedida! Ingresso ID: {ingresso.id}")
                else:
                    messagebox.showerror("Erro", "Falha na inscrição (capacidade esgotada ou erro)!")
            else:
                messagebox.showerror("Erro", "Participante ou evento não encontrado!")
            janela.destroy()

        tk.Button(janela, text="Inscrever", command=inscrever).pack(pady=10)

    def cancelar_inscricao(self):
        janela = tk.Toplevel(self)
        janela.title("Cancelar Inscrição")
        janela.geometry("300x150")

        tk.Label(janela, text="Nome do Participante:").pack()
        part_entry = tk.Entry(janela)
        part_entry.pack()

        tk.Label(janela, text="ID do Ingresso:").pack()
        ingresso_id_entry = tk.Entry(janela)
        ingresso_id_entry.pack()

        def cancelar():
            part_nome = part_entry.get()
            ingresso_id = int(ingresso_id_entry.get())
            participante = next((p for p in participantes_lista if p.nome == part_nome), None)
            if participante:
                ingresso = next((ing for ing in participante.ingressos if ing.id == ingresso_id), None)
                if ingresso:
                    participante.cancelarInscricao(ingresso)
                    messagebox.showinfo("Sucesso", "Inscrição cancelada!")
                else:
                    messagebox.showerror("Erro", "Ingresso não encontrado!")
            else:
                messagebox.showerror("Erro", "Participante não encontrado!")
            janela.destroy()

        tk.Button(janela, text="Cancelar", command=cancelar).pack(pady=10)


if __name__ == "__main__":
    app = InterfaceGrafica()
    app.mainloop()
