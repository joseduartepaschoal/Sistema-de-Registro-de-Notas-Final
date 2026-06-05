import sqlite3


class SistemaNotasDB:
    def __init__(self, db_name='escola.db'):
        self.db_name = db_name

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def criar_tabela(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricula TEXT NOT NULL DEFAULT '',
                nome TEXT NOT NULL,
                curso TEXT NOT NULL DEFAULT '',
                nota REAL NOT NULL
            )
        """)
        cursor.execute("PRAGMA table_info(alunos)")
        colunas = [coluna[1] for coluna in cursor.fetchall()]
        if "matricula" not in colunas:
            cursor.execute("ALTER TABLE alunos ADD COLUMN matricula TEXT NOT NULL DEFAULT ''")
        if "curso" not in colunas:
            cursor.execute("ALTER TABLE alunos ADD COLUMN curso TEXT NOT NULL DEFAULT ''")
        conn.commit()
        conn.close()

    def inserir_aluno(self, matricula, nome, curso, nota):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO alunos (matricula, nome, curso, nota) VALUES (?, ?, ?, ?)",
            (matricula, nome, curso, nota)
        )
        conn.commit()
        conn.close()

    def listar_alunos(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, matricula, nome, curso, nota FROM alunos")
        dados = cursor.fetchall()
        conn.close()
        return dados

    def buscar_aluno(self, nome="", matricula="", curso=""):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, matricula, nome, curso, nota
            FROM alunos
            WHERE nome LIKE ?
              AND matricula LIKE ?
              AND curso LIKE ?
            """,
            ('%' + nome + '%', '%' + matricula + '%', '%' + curso + '%')
        )
        dados = cursor.fetchall()
        conn.close()
        return dados

    def atualizar_aluno(self, id, matricula, nome, curso, nota):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE alunos SET matricula=?, nome=?, curso=?, nota=? WHERE id=?",
            (matricula, nome, curso, nota, id)
        )
        conn.commit()
        conn.close()

    def deletar_aluno(self, id):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alunos WHERE id=?", (id,))
        conn.commit()
        conn.close()
