import os
import shutil
from datetime import *
from xml.etree.ElementTree import Element, ElementTree
from Conexao_Banco_Dados import ConexaoBancoDados


print("_"*80)
print("\t \t \t Sistema de cadastrar e consultar de alunos \n")
print("_"*80)

class Escola(ConexaoBancoDados):
    
    def menu(self):
        escolha = 0
            
        try:
            escolha = int(input("\t \t \t Escolha\n 1 - Cadastrar \n 2 - Consultar \n 3 - Alterar cadastro \n 4 - Excluir \n 5 - Ler Relatório \n 6 - Listar todos Alunos\n 7 - Sair \n Opção: "))
            if escolha <= 0 or escolha > 7:
                print("_"*80)
                print("Por favor digite uma opção válida ")

            if escolha == 1:
                print("_"*80)
                print("\t \t \t Cadastrar \n")
                self.cadastrar()
                    
            elif escolha == 2:
                print("_"*80)
                print("\t \t \t consultarr Registro \n")
                self.consultar()

            elif escolha == 3:
                print("_"*80)
                print("\t \t \t Alterar cadastrar \n")
                self.alterar()
                    
            elif escolha == 4:
                print("_"*80)
                print("\t \t \t Excluir \n")
                self.excluir()

            elif escolha == 5:
                print("_"*80)
                print("\t \t \t Ler Relatório \n")
                self.ler_relatorio()
                
            elif escolha == 6:
                print("_"*80)
                print("\t \t \t Listar Todos \n")
                self.listar_todos()
                    
            elif escolha == 7:
                print("_"*80)
                print("\t \t \t Sair \n")
                self.sair()
                    
        except ValueError:
            print("_"*80)
            print("Por favor digite uma opção válida")
            self.menu()

    def cadastrar(self):

        i = 1
        quant = 0
        nome = ""
        idade = 0
        nota1 = 0
        nota2 = 0
        media = 0

        try:
            print("_"*80)
            quant = int(input("Digite a quantidade de alunos que irão ser cadastrados: "))

            while quant <= 0:
                print("_"*80)
                print("Por favor digite uma quantidade válida.")
                quant = int(input("Digite a quantidade de alunos que irão ser cadastrados: "))
                        
            while i <= quant:
                print("_"*80)
                nome = input("Digite %d º Nome: " % (i))
                nome = nome.title()
                while nome == "" or nome.isdigit():
                    print("_"*80)
                    print("Por favor digite um nome válido.")
                    nome = input("Digite %d º Nome: " % (i))
                    nome = nome.title()

                idade = int(input("Digite a sua idade : "))
                while idade < 6:
                    print("_"*80)
                    print("Por favor digite uma idade maior ou igual a 6 anos.")
                    idade = int(input("Digite a sua idade : "))

                nota_aux = input("Digite a 1º Nota: ")
                nota_aux = nota_aux.replace(",", ".")
                nota1 = float(nota_aux)
                while nota1 < 0 or nota1 > 10 or nota1 == -0:
                    print("_"*80)
                    print("Por favor digite a 1º  nota válida.")
                    nota1 = float(input("Digite a 1º Nota: "))

                nota_aux = input("Digite a 2º Nota: ")
                nota_aux = nota_aux.replace(",", ".")
                nota2 = float(nota_aux)
                while nota2 < 0 or nota2 > 10 or nota2 == -0:
                    print("_"*80)
                    print("Por favor digite a 1º  nota válida.")
                    nota2 = float(input("Digite a 1º Nota: "))

                media = (nota1 + nota2) / 2
                i += 1
                    
                self.nome = nome
                self.idade = int(idade)
                self.nota1 = float(nota1)
                self.nota2 = float(nota2)
                self.media = media

                try:
                    self.conexao_aberta()
                    self.cursor = self.conexao.cursor()
                    sql = ("insert into alunos(nome,idade,nota1,nota2,media)values('%s',%d,%.2f,%.2f,%.2f);" % (self.nome,self.idade,self.nota1,self.nota2,self.media))
                    self.cursor.execute(sql)
                    self.conexao.commit()
                    print("_"*80)
                    print("Foi salvo um registro com sucesso no banco de dados.")

                except:
                     print("Erro ao tentar inserir o registro.")
                
                self.relatorio()
                self.gravar_txt()
                    
                            
        except ValueError:
                print("_"*80)
                print("Por favor digite apenas valores numéricos e valores válidos nos campos que são solicitados.")
        finally:
            self.conexao_fechada()
            
    def consultar(self):
        
        try:
            self.conexao_aberta()
            cod = ""
            cod = input("Digite o código do aluno: ")
            while cod.isdigit() is False:
                print("_"*80)
                print("Por favor digite corretamente o código do aluno.")
                cod = input("Digite o código do aluno: ")

            sql = ("select * from alunos where user_id_aluno = %s ;" % cod)
            self.cursor.execute(sql)
            consultar =  self.cursor.fetchone()

            codigo = consultar[0]
            nome   = consultar[1]
            idade  = consultar[2]
            nota1  = consultar[3]
            nota2  = consultar[4]
            media  = consultar[5]

            if consultar is not None:
                print("_"*80)
                print("Código do aluno: ",codigo)
                print("Nome do aluno: ",nome)
                print("Idade do aluno: ",idade)
                print("1 º Nota do aluno: %.2f" % nota1)
                print("2 º Nota do do aluno: %.2f " % nota2)
                print("Média do aluno: %.2f"% media)

            else:
                print("Não existe o código digitado.")

            self.conexao_fechada()
            
        except:
            print("Erro ao tentar consultarr o registro.")
            print("Não existe o código digitado.")

        finally:
            self.conexao_fechada()
        
    def alterar(self):
        try:
            self.conexao_aberta()
            cod = 0
            cod = int(input("Digite o código do aluno: "))

            while cod < 0 or cod == -0 :
               print("_"*80)
               print("Por favor digite um código válido.")
               cod = input("Digite o código para pesquisar: ")
            
            escolha = ""
            escolha = input("\t \t Escolha\n 1 - Alterar Nome\n 2 - Alterar Idade\n 3 - Alterar Nota 1\n 4 - Alterar Nota 2\n Opção: ")
            while escolha.isdigit() is False:
                print("_"*80)
                print("Por favor digite um escolha válida.")
                escolha = input("\t \t Escolha\n 1 - Alterar Nome\n 2 - Alterar Idade\n 3 - Alterar Nota 1\n 4 - Alterar Nota 2\n --> ")

            if escolha == "1":
                
                nome = input("Digite um novo nome: ")
                nome = nome.title()
                
                while nome == "" or nome.isdigit():
                    print("_"*80)
                    print("Por favor digite um nome válido.")
                    nome = input("Digite um novo nome: ")
                    nome = nome.title()

                sql = ("update alunos set nome = '%s' where user_id_aluno = %s ;" %( nome,cod))
                self.cursor.execute(sql)
                self.conexao.commit()
                print("O nome foi alterado com sucesso.")

            elif escolha == "2":
                idade = int(input("Digite um nova idade: "))

                while idade < 6 :
                    print("_"*80)
                    print("Por favor digite uma idade válido.")
                    idade = int(input("Digite uma nova idade: "))

                sql = ("update alunos set idade = %d where user_id_aluno = %s ;" % (idade,cod))
                self.cursor.execute(sql)
                self.conexao.commit()
                print("A idade foi alterada com sucesso.")

            elif escolha == "3":
                print("\t Nota da Primeira Prova \n")
                nota_aux = input("Digite a  1º nota: ")
                nota_aux = nota_aux.replace(",", ".")
                nota1 = float(nota_aux)

                while nota1 < 0 or nota1 == -0 or nota1 > 10 :
                    print("_"*80)
                    print("Por favor digite 1 º nota válida.")
                    nota_aux = input("Digite a  1º nota: ")
                    nota_aux = nota_aux.replace(",", ".")
                    nota1 = float(nota_aux)

                sql = ("update alunos set nota1 = %.2f where user_id_aluno = %s ;" % (nota1,cod))
                self.cursor.execute(sql)
                self.conexao.commit()
                print("A Primeira nota foi alterada com sucesso.")
                
            elif escolha == "4":
                print("\t Nota da Segunda Prova \n")
                nota_aux = input("Digite a 2º nota: ")
                nota_aux = nota_aux.replace(",", ".")
                nota2 = float(nota_aux)

                while nota2 <0 or nota2 == -0 or nota2 > 10:
                    print("_"*80)
                    print("Por favor digite a 2º nota válida.")
                    nota_aux = input("Digite a 2º nota: ")
                    nota_aux = nota_aux.replace(",", ".")
                    nota2 = float(nota_aux)

                sql = ("update alunos set nota2 = %.2f where user_id_aluno = %s ;" % (nota2,cod))
                self.cursor.execute(sql)
                self.conexao.commit()
                print("A Segunda nota  foi alterada com sucesso.")
                
            else:
                print("_"*80)
                print("Opção Inválida")          

        except ValueError:
            print("_"*80)
            print("Por favor digite somente números nos campos solicitados.")
        except:
            print("_"*80)
            print("Erro ao tentar alterar o registro.")

        finally:
            self.conexao_fechada()
            
    def excluir(self):

        try:
            self.conexao_aberta()
            cod = input("Digite o código que dejesa excluir: ")
            
            while cod.isdigit() is False:
                print("_"*80)
                print("Por favor digite um código válido")
                cod = input("Digite o código que dejesa excluir: ")

            id = int(cod)
            sql = ("delete from alunos where user_id_aluno = %d;" % id)
            self.cursor.execute(sql)
            self.conexao.commit()

            print("_"*80)
            print("O registro foi excluído com sucesso.")

        except:
            print("_"*80)
            print("Erro ao tentar excluir o registro.")

        finally:
            self.conexao_fechada()

    def sair(self):
        print("_"*80)
        print("Saindo do programa até a próxima.")
        exit()
                        
    def listar_todos(self):

        try:
            self.conexao_aberta()
            sql = ""
            sql = "select * from alunos;"
            self.cursor.execute(sql)
            consultar = self.cursor.fetchall()

            for registro in consultar:
                cod    = registro[0]
                nome   = registro[1]
                idade  = registro[2]
                nota1  = registro[3]
                nota2  = registro[4]
                media  = registro[5]

                print("_"*80)
                print(" Código do Aluno: %s \n Nome do Aluno: %s \n Idade: %d \n Nota 1: %.2f \n Nota 2: %.2f \n Média: %.2f . \n" %(cod,nome,idade,nota1,nota2,media))

        except:
            print("_"*80)
            print("Erro ao tentar listar os alunos.")

        finally:
            self.conexao_fechada()

    def relatorio(self):

        hoje = datetime.today()
        data = hoje.day
        mes = hoje.month
        ano = hoje.year

        horario = datetime.now()
        horas = horario.hour
        minutos = horario.minute
        segundos = horario.second

        self.data = data
        self.mes = mes
        self.ano = ano
        
        self.horas = horas
        self.minutos = minutos
        self.segundos = segundos

        print("_"*80)
        print("\t \t \t Relatório \n ")
        print("Nome: %s \nIdade: %d \n1 º Nota: %.2f \n2 º Nota: %.2f \nMédia: %.2f " % (self.nome,self.idade,self.nota1,self.nota2,self.media))
        if self.media >= 9 and self.media <= 10:
            print("%s você foi aprovado com louvor por causa da sua média: %.2f" % (self.nome,self.media))

        if self.media >= 7 and self.media < 9:
            print("%s você foi aprovado com sucesso por causa da sua média: %.2f" % (self.nome,self.media))

        elif self.media >= 5 and self.media < 7:
            print("%s você foi aprovado  por causa da sua média: %.2f" % (self.nome,self.media))

        elif self.media >= 4 and self.media < 5:
            print("%s você está de recuperação  por causa da sua média: %.2f" % (self.nome,self.media))

        elif self.media < 4:
            print("%s você foi reprovado  por causa da sua média: %.2f" % (self.nome,self.media))
            
        print("Data da operação realizada: %s\%s\%s " % (self.data,self.mes,self.ano))
        print("Horário da operação realizada: %s:%s:%s " % (self.horas,self.minutos,self.segundos))
        
    def gravar_txt(self):

        try:
            diretorio = ""
            print("_"*80)
            print("\t \t \t Gravando txt \n")
            diretorio = input("Digite um nome para o diretório e arquivo: ")

            while diretorio == "":
                print("_"*80)
                print("Por favor digite um nome para o diretório e arquivo.")
                diretorio = input("Digite um nome para o diretório e arquivo: ")

            #diretorio = self.nome.join(diretorio)
            os.mkdir(diretorio)
            print("O diretório foi criado com sucesso.")
            
            arquivo = open(diretorio+"\\"+self.nome+".txt","w")
            arquivo.write("Nome: %s \nIdade: %d \n1 º Nota: %.2f \n2 º Nota: %.2f \nMédia: %.2f\n" % (self.nome,self.idade,self.nota1,self.nota2,self.media))
            arquivo.write("Data da operação realizada: %s\%s\%s \n" % (self.data,self.mes,self.ano))
            arquivo.write("Horário da operação realizada: %s:%s:%s " % (self.horas,self.minutos,self.segundos))
            arquivo.close()
            print("_"*80)
            print("Foi salvo um arquivo com sucesso com o nome de %s ." % self.nome)
            self.diretorio = diretorio
            self.gravar_xml()

        except FileExistsError:
            if FileNotFoundError:
                print("_"*80)
                print("Erro ao tentar gerar o arquivo.")
                arquivo.close()

            elif FileExistsError:
                print("O diretório já existe.")

            else:
                print("_"*80)
                print("Erro em geral para gravar o arquivo ou o diretório já existente ")

    def gravar_xml(self):

        xml_cab         =   Element("relatorio")
        xml_nome        =   Element("Nome: %s" % self.nome)
        xml_idade       =   Element("Idade: %d" % self.idade)
        xml_nota1       =   Element("Nota1: %.2f" % self.nota1)
        xml_nota2       =   Element("Nota2: %.2f" % self.nota2)
        xml_media       =   Element("Media: %.2f" % self.media)
        xml_data        =   Element("Data \n")
        xml_dia         =   Element("Dia: %s" % self.data)
        xml_mes         =   Element("Mes: %s" % self.mes)
        xml_ano         =   Element("Ano: %s" % self.ano)
        xml_horas       =   Element("Horas: %s " % self.horas)
        xml_minutos     =   Element("Minutos: %s" % self.minutos)
        xml_segundos    =   Element("Segundos: %s" % self.segundos)

        xml_cab.append(xml_nome)
        xml_cab.append(xml_idade)
        xml_cab.append(xml_nota1)
        xml_cab.append(xml_nota2)
        xml_cab.append(xml_media)
        xml_cab.append(xml_data)
        xml_cab.append(xml_dia)
        xml_cab.append(xml_mes)
        xml_cab.append(xml_ano)
        xml_cab.append(xml_horas)
        xml_cab.append(xml_minutos)
        xml_cab.append(xml_segundos)

        ElementTree(xml_cab).write(self.nome+".xml")
        print("_"*80)
        print("Foi salvo um arquivo em xml com sucesso e o seu nome é: %s" % self.nome)
        shutil.move(self.nome+".xml",self.diretorio)
        print("_"*80)
        print("Este arquivo em xml foi movido para a pasta: %s" % self.diretorio)
        
    def ler_relatorio(self):
        
        try:
            nome_diretorio = ""
            nome_Arq = ""
            print("_"*80)
            nome_diretorio = input("Digite o nome do diretório que se encontra o arquivo: ")
            while nome_diretorio == "":
                print("_"*80)
                print("Por favor digite o nome do diretório corretamente.")
                nome_diretorio = input("Digite o nome do diretório que se encontra o arquivo: ")

            nome_Arq  = input("Por favor digite o nome do arquivo corretamente: ")
            nome_Arq = nome_Arq.title()
            while nome_Arq == "":
                print("_"*80)
                print("Por favor digite o nome do arquivo corretamente.")
                nome_Arq  = input("Por favor digite o nome do arquivo corretamente: ")
                nome_Arq = nome_Arq.title()

            print("_"*80)
            print("\t \t \t Leitura do Arquivo txt \n")
            arquivo = open(nome_diretorio+"\\"+nome_Arq+".txt","r")
            for leitura in arquivo.readlines():
                print(leitura)
            arquivo.close()
            print("_"*80)
            print("Leitura do arquivo txt realizado com sucesso.")

            print("_"*80)
            print("\t \t \t Leitura do arquivo em XMl \n")
            arquivoXml = open(nome_diretorio+"\\"+nome_Arq+".xml","r")
            for leituraXml in arquivoXml.readlines():
                print(leituraXml)
            arquivoXml.close()
            print("_"*80)
            print("Leitura do arquivo xml realizado com sucesso.")
                    
        except:

            if FileExistsError is False:
                print("_"*80)
                print("O arquivo não existe")
                
            elif FileNotFoundError is False:
                print("_"*80)
                print("Nome do diretório está errado")
                
            else:
                print("_"*80)
                print("Erro em geral: O nome do diretório está errado ou se não o nome do arquivo.")
                
                        
aluno = Escola()
aluno.menu()
                      
                      
                      

        
        
        
