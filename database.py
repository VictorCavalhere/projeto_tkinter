import sqlite3

class DB:
    def __init__(self):
        self.conn = sqlite3.connect("pi.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS cliente (id INTEGER PRIMARY KEY,nome TEXT,data DATETIME DEFAULT CURRENT_TIMESTAMP)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS operador (id INTEGER PRIMARY KEY,nome TEXT,hist_manutencao  DATETIME DEFAULT CURRENT_TIMESTAMP)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS maquina (id INTEGER PRIMARY KEY, num_serie INTEGER, hist_op DATETIME DEFAULT CURRENT_TIMESTAMP, id_operador_fk INTEGER, id_cliente_fk INTEGER, FOREIGN KEY(id_operador_fk) REFERENCES operador(id),FOREIGN KEY(id_cliente_fk) REFERENCES cliente(id))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS regiao (id INTEGER PRIMARY KEY,hist_atuacao DATETIME DEFAULT CURRENT_TIMESTAMP)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS capsula (quantidade INTEGER,hist_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP, id_maquina_fk INTEGER,FOREIGN KEY(id_maquina_fk) REFERENCES maquina(id))")


        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def view(self,nome):
        self.cur.execute("SELECT nome FROM operador WHERE nome=?)",(nome))
        rows = self.cur.fetchall()
        return rows

    def view_capsula(self,num):
        self.cur.execute("SELECT quantidade FROM capsula WHERE id_maquina_fk=?",(num,))
        rows = self.cur.fetchone()
        return rows

    def view_cliente(self):
        self.cur.execute("SELECT nome FROM cliente")
        rows = self.cur.fetchall()
        return rows

    def insert_cliente(self,nome,data):
        self.cur.execute("INSERT INTO cliente VALUES (NULL,?,?)", (nome,data))
        self.conn.commit()

    def insert_operador(self, nome,data):
        self.cur.execute("INSERT INTO operador VALUES (NULL,?,?)", (nome,data))
        self.conn.commit()


    def insert_maquina(self,num,data,id_op,id_cl):
        self.cur.execute("INSERT INTO maquina VALUES (NULL,?,?,?,?)", (num,data,id_op,id_cl))
        self.conn.commit()


    def insert_capsula(self,qtd,data,id_maq):
        self.cur.execute("INSERT INTO capsula VALUES (?,?,?)", (qtd,data,id_maq))
        self.conn.commit()

    
    def update_capsula(self, qtd, data,id_maq):
        self.cur.execute("UPDATE capsula SET quantidade=? WHERE hist_atualizacao=? and id_maquina_fk=?", (qtd,data,id_maq))


    def delete(self, id):
        self.cur.execute("DELETE FROM paciente WHERE id=?", (id,))
        self.conn.commit()


    def search(self, nome="", telefone="", cpf=""):
        self.cur.execute("SELECT * FROM paciente WHERE nome=? OR telefone=? OR cpf=?", (nome,telefone,cpf))
        rows = self.cur.fetchall()
        return rows
    
    def select_id_cliente(self,nome):
        self.cur.execute("SELECT id FROM cliente WHERE nome=?", (nome,))
        rows = self.cur.fetchone()
        return rows

    def select_id_operador(self,nome):
        self.cur.execute("SELECT id,nome FROM operador WHERE nome=?", (nome,))
        rows = self.cur.fetchone()
        return rows

    def select_id_maquina(self,numero):
        self.cur.execute("SELECT id FROM maquina WHERE num_serie=?", (numero,))
        rows = self.cur.fetchone()
        return rows