import sqlite3

class DB:
    def __init__(self):
        self.conn = sqlite3.connect("pi.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS cliente (id INTEGER PRIMARY KEY, data DATETIME DEFAULT CURRENT_TIMESTAMP)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS maquina (id INTEGER PRIMARY KEY, num_serie INTEGER, hist_op DATETIME DEFAULT CURRENT_TIMESTAMP, id_operador_fk INTEGER, id_cliente_fk INTEGER, FOREIGN KEY(id_operador_fk) REFERENCES operador(id),FOREIGN KEY(id_cliente_fk) REFERENCES cliente(id))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS operador (id INTEGER PRIMARY KEY,nome TEXT,hist_manutencao  DATETIME DEFAULT CURRENT_TIMESTAMP)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS regiao (id INTEGER PRIMARY KEY,hist_atuacao DATETIME DEFAULT CURRENT_TIMESTAMP)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS capsula (quantidade INTEGER,hist_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP)")


        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def view(self):
        self.cur.execute("SELECT * FROM paciente")
        rows = self.cur.fetchall()
        return rows

    def insert(self, nome, telefone,cpf ,endereco,data_nasc,data_entrada ):
        self.cur.execute("INSERT INTO paciente VALUES (NULL,?,?,?,?,?,?)", (nome,telefone,cpf,endereco,data_nasc,data_entrada))
        self.conn.commit()
        self.view()

    def insert_temp(self,temp,intervalo,condicao,id_paciente):
        self.cur.execute("INSERT INTO temperatura VALUES (NULL,?,?,?,?)", (temp,intervalo,condicao,id_paciente))
        self.conn.commit()
        self.view()
    
    def insert_pressao(self,pressao,intervalo,condicao,id_paciente):
        self.cur.execute("INSERT INTO pressao VALUES (NULL,?,?,?,?)", (pressao,intervalo,condicao,id_paciente))
        self.conn.commit()
        self.view()

    def insert_batimento(self,batimento,intervalo,condicao,id_paciente):
        self.cur.execute("INSERT INTO batimento VALUES (NULL,?,?,?,?)", (batimento,intervalo,condicao,id_paciente))
        self.conn.commit()
        self.view()

    def update(self, id, nome, telefone, cpf):
        self.cur.execute("UPDATE paciente SET nome=?, telefone=?, cpf=? WHERE id=?", (nome,telefone,cpf,id))
        self.view()

    def delete(self, id):
        self.cur.execute("DELETE FROM paciente WHERE id=?", (id,))
        self.conn.commit()
        self.view()

    def search(self, nome="", telefone="", cpf=""):
        self.cur.execute("SELECT * FROM paciente WHERE nome=? OR telefone=? OR cpf=?", (nome,telefone,cpf))
        rows = self.cur.fetchall()
        return rows
    
    def select_id(self, nome="", telefone="", cpf=""):
        self.cur.execute("SELECT id FROM paciente WHERE nome=? OR telefone=? OR cpf=?", (nome,telefone,cpf))
        rows = self.cur.fetchone()
        return rows

    def view_temp(self,id_):
        self.cur.execute("SELECT temperatura FROM temperatura WHERE id_paciente = ?",(id_))
        rows = self.cur.fetchall()
        return rows

    def view_pressao(self,id_):
        self.cur.execute("SELECT pressao FROM pressao WHERE id_paciente = ?",(id_))
        rows = self.cur.fetchall()
        return rows

    def view_batimento(self,id_):
        self.cur.execute("SELECT batimento FROM batimento WHERE id_paciente = ?",(id_))
        rows = self.cur.fetchall()
        return rows