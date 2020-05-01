import mysql.connector


class ConexaoBancoDados:

    def conexao_aberta(self):
        try:
            conexao = mysql.connector.connect(user = "root", password = "", host = "localhost", database = "BD_ESCOLA")
            cursor =  conexao.cursor()
            self.conexao = conexao
            self.cursor = cursor
            print("_"*80)
            print("Conexão aberta.")

        except:
            print("_"*80)
            print("Erro ao conectar com o banco de dados")


    def conexao_fechada(self):
        try:
            if self.conexao.is_connected():
                self.conexao.close()
                print("_"*80)
                print("Conexão fechada.")

        except:
            print("_"*80)
            print("Erro ao tentar fechar a conexão.")
    

"""conectar = ConexaoBancoDados()
conectar.conexao_aberta()
conectar.conexao_fechada()"""
