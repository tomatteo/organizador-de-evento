import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("eventos.db")
        self.criar_tabelas()

    def criar_tabelas(self):
        cursor = self.conn.cursor()

        # Tabela EVENTOS
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                data_inicio TEXT,
                data_fim TEXT,
                capacidade INTEGER,
                local_id INTEGER,
                local_nome TEXT,
                local_endereco TEXT,
                local_capacidade INTEGER
            )
        """)

        # Tabela PARTICIPANTES
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS participantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                senha TEXT NOT NULL,
                cpf TEXT NOT NULL
            )
        """)

        # Tabela INSCRIÇÕES
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inscricoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                participante_id INTEGER,
                evento_id INTEGER,
                UNIQUE (participante_id, evento_id)
            )
        """)

        self.conn.commit()

    # ----------------------------
    # EVENTOS
    # ----------------------------

    def salvar_evento(self, evento):
        cursor = self.conn.cursor()

       
        cursor.execute("""
            INSERT INTO eventos (
                nome, descricao, data_inicio, data_fim, capacidade,
                local_id, local_nome, local_endereco, local_capacidade
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            evento.nome,
            evento.descricao,
            evento.data_inicio.strftime("%Y-%m-%d %H:%M"),
            evento.data_fim.strftime("%Y-%m-%d %H:%M"),
            evento.capacidade,
            evento.local.id,          # Corrigido
            evento.local.nome,        # Corrigido
            evento.local.endereco,    # Corrigido
            evento.local.capacidade   # Corrigido
        ))

        self.conn.commit()

    def listar_eventos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM eventos")
        return cursor.fetchall()

    def excluir_evento(self, nome_evento):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM eventos WHERE nome = ?", (nome_evento,))
        self.conn.commit()
        return cursor.rowcount > 0

    # ----------------------------
    # PARTICIPANTES
    # ----------------------------

    def salvar_participante(self, participante):
        cursor = self.conn.cursor()
        # O try/except ajuda a evitar erro se o email já existir (caso adicione UNIQUE no banco depois)
        try:
            cursor.execute("""
                INSERT INTO participantes (nome, email, senha, cpf)
                VALUES (?, ?, ?, ?)
            """, (
                participante.nome,
                participante.email,
                participante.senha,
                participante.cpf
            ))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao salvar participante: {e}")
            return False

    def listar_participantes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM participantes")
        return cursor.fetchall()

    def excluir_participante(self, nome):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM participantes WHERE nome = ?", (nome,))
        self.conn.commit()
        return cursor.rowcount > 0

    def autenticar_participante(self, email, senha):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nome FROM participantes WHERE email = ? AND senha = ?", (email, senha))
        return cursor.fetchone()

    # ----------------------------
    # INSCRIÇÕES
    # ----------------------------

    def verificar_inscricao(self, participante_id, evento_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 1 FROM inscricoes
            WHERE participante_id = ? AND evento_id = ?
        """, (participante_id, evento_id))
        return cursor.fetchone() is not None

    def inscrever_participante(self, participante_id, evento_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO inscricoes (participante_id, evento_id)
                VALUES (?, ?)
            """, (participante_id, evento_id))
            self.conn.commit()
            return True
        except:
            return False

    def cancelar_inscricao(self, participante_id, evento_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM inscricoes 
            WHERE participante_id = ? AND evento_id = ?
        """, (participante_id, evento_id))
        self.conn.commit()
        return cursor.rowcount > 0