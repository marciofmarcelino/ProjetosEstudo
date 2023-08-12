import customtkinter as ctk
import sqlite3
from tkinter import ttk


class App:

    def __init__(self, master):

        self.janela_login = master
        self.tela_login()
        self.design_telalogin()

        self.conectar_cadastrobd()
        self.criar_bancosql()

        self.janela_atual = self.janela_login
        self.frms_criados = False

        self.user = None
        self.cpf = None
        self.nome = None
        self.senha = None
        self.cep = None

    def design_telalogin(self):
        self.janela_login.title("Recap")
        self.janela_login.geometry("310x310")
        self.janela_login.configure(fg_color='#00ced1')
        ##janelaroot.resizable(width="False",height="False")

    def tela_login(self):
        # sintaxe de widgets self.objeto = tk.tipowidget(widgetPai,op.config)

        ##frames ##

        self.frm_toplogin = ctk.CTkFrame(master=self.janela_login, width=310, height=50, fg_color='#00ced1')
        self.frm_lowlogin = ctk.CTkFrame(master=self.janela_login, width=310, height=250, fg_color='#00ced1')

        self.frm_toplogin.grid(row=0, column=0, padx=0, pady=1)
        self.frm_lowlogin.grid(row=1, column=0, padx=10, pady=1)

        self.lb = ctk.CTkLabel(master=self.frm_toplogin, text="Login", font=("", 20))
        self.lb.place(x=5, y=5)
        self.lb2 = ctk.CTkLabel(master=self.frm_lowlogin, text="CPF")
        self.lb2.place(x=15, y=15)
        self.lb3 = ctk.CTkLabel(master=self.frm_lowlogin, text="Senha")
        self.lb3.place(x=15, y=40)

        self.cpf_entrylog = ctk.CTkEntry(master=self.frm_lowlogin, width=100, border_color='teal')
        self.cpf_entrylog.place(x=110, y=15)

        self.senha_entrylog = ctk.CTkEntry(master=self.frm_lowlogin, show="*", width=100, border_color='teal')
        self.senha_entrylog.place(x=110, y=40)

        self.btnlogar = ctk.CTkButton(master=self.frm_lowlogin, text="Logar", command=self.logar, width=100, height=1)
        self.btnlogar.place(x=110, y=80)

        self.btncad = ctk.CTkButton(master=self.frm_lowlogin, text="Cadastrar", command=self.irtela_cadastro, width=100,
                                    height=1)
        self.btncad.place(x=50, y=170)

        self.btnesenha = ctk.CTkButton(master=self.frm_lowlogin, text="Esqueci a senha", command=self.irtela_recsenha,
                                       width=100, height=1)
        self.btnesenha.place(x=50, y=130)

    def conectar_cadastrobd(self):
        try:
            self.banco_cad = sqlite3.connect("cadastro_login.db")
            self.cursor = self.banco_cad.cursor()
            print("conexão iniciada!")
        except sqlite3.Error as e:
            print("Erro ao conectar com o banco de dados:", e)

    def desconectar_cadastrobd(self):
        self.banco_cad.close()
        print("Conexão encerrada")

    def criar_bancosql(self):
        # criando tabelas
        try:
            with self.banco_cad:
                query = "CREATE TABLE IF NOT EXISTS usuario (cpf int,nome string,data int,sexo string,rua string,numero int,bairro string,cep int,senha int)"
                if self.cursor.execute(query) == True:
                    print("tabela criada com sucesso")

                else:
                    print("Tabela ja existe")

            self.banco_cad.commit()


        except sqlite3.Error as e:
            print("Erro ao criar a tabela usuario:", e)

    def logar(self):
        self.cpf = self.cpf_entrylog.get()
        self.senha = self.senha_entrylog.get()
        self.user = self.validar_login()

        if self.user is None:
            print("Usuario ou senha incorreta")


        else:
            print("login efetuado")

            print(self.user[0:8])
            self.irmenu()

    def validar_login(self):

        with self.banco_cad:
            self.cursor = self.banco_cad.cursor()
            self.cursor.execute("SELECT * FROM usuario WHERE (cpf=? AND senha=?)",
                                (self.cpf, self.senha))
            user = self.cursor.fetchone()

        return user

    def retirar_janelaatual(self):
        if self.janela_atual == self.janela_login:
            self.janela_atual.withdraw()

        else:
            self.janela_atual.destroy()

    def criar_framesatual(self):

        if self.janela_atual == self.janela_login:
            print("Frames ja criados")

        elif self.janela_atual != self.janela_login and self.frms_criados == False:

            self.frm_topatual = ctk.CTkFrame(master=self.janela_atual, width=350, height=40, fg_color='#00ced1')
            self.frm_lowatual = ctk.CTkFrame(master=self.janela_atual, width=350, height=400, fg_color='#00ced1')
            self.frms_criados = True

            return self.frms_criados

        else:

            self.frm_topatual.destroy()
            self.frm_lowatual.destroy()

            self.frms_criados = False
            self.criar_framesatual()

    def retornar_login(self):
        self.retirar_janelaatual()
        self.janela_login.deiconify()
        self.janela_atual = self.janela_login
        self.user = None
        self.cpf = None
        self.nome = None
        self.senha = None
        self.cep = None

    def irtela_recsenha(self):
        self.retirar_janelaatual()
        self.criar_telarecsenha()
        self.criar_widgetsvalidardados()

    def criar_telarecsenha(self):
        self.janela_recsenha = ctk.CTkToplevel(self.janela_login)
        self.janela_atual = self.janela_recsenha
        self.janela_recsenha.title("Rec Senha")
        self.janela_recsenha.geometry("350x310")
        self.janela_recsenha.configure(fg_color='#00ced1')

    def criar_widgetsvalidardados(self):
        self.criar_framesatual()

        self.frm_topatual.place(x=0, y=0)
        self.frm_lowatual.place(x=0, y=60)

        self.lab_titulo = ctk.CTkLabel(master=self.frm_topatual, text="Recuperar a senha", font=("", 20))
        self.lab_titulo.place(x=5, y=10)

        self.lab_cpftext = ctk.CTkLabel(master=self.frm_lowatual, text='CPF')
        self.lab_cpftext.place(x=30, y=0)

        self.lab_nometext = ctk.CTkLabel(master=self.frm_lowatual, text="Nome")
        self.lab_nometext.place(x=30, y=30)

        self.lab_datantext = ctk.CTkLabel(master=self.frm_lowatual, text="Data de nascimento")
        self.lab_datantext.place(x=30, y=60)

        self.lab_ceptext = ctk.CTkLabel(master=self.frm_lowatual, text="CEP")
        self.lab_ceptext.place(x=30, y=90)

        self.cpf_entry = ctk.CTkEntry(master=self.frm_lowatual)
        self.cpf_entry.place(x=180, y=0)

        self.nome_entry = ctk.CTkEntry(master=self.frm_lowatual)
        self.nome_entry.place(x=180, y=30)

        self.datan_entry = ctk.CTkEntry(master=self.frm_lowatual)
        self.datan_entry.place(x=180, y=60)

        self.cep_entry = ctk.CTkEntry(master=self.frm_lowatual)
        self.cep_entry.place(x=180, y=90)

        self.btn_recuperarsenha = ctk.CTkButton(master=self.frm_lowatual, text="Recuperar", command=self.ir_trocarsenha)
        self.btn_recuperarsenha.place(x=180, y=150)

        self.retorno_btn = ctk.CTkButton(self.frm_lowatual, text='Retornar', command=self.retornar_login)
        self.retorno_btn.place(x=30, y=150)

    def ir_trocarsenha(self):
        self.cpf = self.cpf_entry.get()
        self.nome = self.nome_entry.get()
        self.datan = self.datan_entry.get()
        self.cep = self.cep_entry.get()
        dados = self.validar_cadastro()
        if dados is None:
            print("dados incorretos")

        else:
            print("ok")
            self.user = dados
            self.tela_alterarsenha()

    def validar_cadastro(self):

        self.cursor.execute("SELECT * FROM usuario WHERE (cpf=?)",
                            (self.cpf_entry.get(),))
        dados_cadastro = self.cursor.fetchone()

        return dados_cadastro

    def tela_alterarsenha(self):
        self.criar_framesatual()

        self.widgetstela_alterarsenha()

    def widgetstela_alterarsenha(self):

        self.frm_topatual.place(x=0, y=0)

        self.frm_lowatual.place(x=0, y=60)

        self.lab_titulo = ctk.CTkLabel(master=self.frm_topatual, text="Recuperar a senha", font=("", 20))
        self.lab_titulo.place(x=5, y=10)

        self.lab_ceptext = ctk.CTkLabel(master=self.frm_lowatual, text='CPF ' + str(self.user[0]), font=("", 20))
        self.lab_ceptext.place(x=80, y=0)

        self.lab_nometext = ctk.CTkLabel(master=self.frm_lowatual, text='Usuario ' + str(self.user[1]), font=("", 20))
        self.lab_nometext.place(x=80, y=30)

        self.lab_novasenhatext = ctk.CTkLabel(master=self.frm_lowatual, text="Insira a nova senha", font=("", 15))
        self.lab_novasenhatext.place(x=30, y=60)

        self.lab_repitasenhatext = ctk.CTkLabel(master=self.frm_lowatual, text="Por favor repita a nova senha",
                                                font=("", 15))
        self.lab_repitasenhatext.place(x=30, y=90)

        self.novasenha_entry = ctk.CTkEntry(master=self.frm_lowatual, show="*")
        self.novasenha_entry.place(x=180, y=60)

        self.repitasenha_entry = ctk.CTkEntry(master=self.frm_lowatual, show="*")
        self.repitasenha_entry.place(x=180, y=90)

        self.btn_alterarsenha = ctk.CTkButton(master=self.frm_lowatual, text="Salvar", command=self.alterar_senha)
        self.btn_alterarsenha.place(x=180, y=120)

        self.retorno_btn = ctk.CTkButton(master=self.frm_lowatual, text='Retornar', command=self.retornar_login)
        self.retorno_btn.place(x=30, y=150)

    def alterar_senha(self):
        self.conectar_cadastrobd()
        self.novasenha = self.novasenha_entry.get()
        self.novasenharep = self.repitasenha_entry.get()
        if self.novasenha == self.novasenharep:
            with self.banco_cad:
                self.cursor = self.banco_cad.cursor()
                query = "UPDATE usuario SET senha=? WHERE cpf=?"
                self.cursor.execute(query, (self.novasenha, self.user[0]))
                print(self.novasenha)
                self.banco_cad.commit()
                self.retornar_login()

        else:
            print("Por favor, verifique se as senhas digitadas conferem")

    def irtela_cadastro(self):
        self.retirar_janelaatual()
        self.criar_telacadastro()
        self.criar_widgetstelacadastro()

    def criar_telacadastro(self):
        self.janela_cadastro = ctk.CTkToplevel(self.janela_login)
        self.janela_atual = self.janela_cadastro
        self.janela_cadastro.title("Recap")
        self.janela_cadastro.geometry("350x400")
        self.janela_cadastro.configure(fg_color='#00ced1')

    def criar_widgetstelacadastro(self):

        self.criar_framesatual()

        self.frm_topatual.place(x=0, y=0)
        self.frm_lowatual.place(x=0, y=60)

        self.lab_cadtext = ctk.CTkLabel(master=self.frm_topatual, text='Cadastrar', font=("", 20))
        self.lab_cadtext.place(x=5, y=10)

        self.lab_nometext = ctk.CTkLabel(master=self.frm_lowatual, text='Nome')
        self.lab_nometext.place(x=30, y=0)

        self.lab_datantext = ctk.CTkLabel(master=self.frm_lowatual, text='Data de Nascimento')
        self.lab_datantext.place(x=30, y=30)

        self.lab_sexotext = ctk.CTkLabel(master=self.frm_lowatual, text='Sexo')
        self.lab_sexotext.place(x=30, y=60)

        self.lab_ruatext = ctk.CTkLabel(master=self.frm_lowatual, text="Rua")
        self.lab_ruatext.place(x=30, y=90)

        self.lab_numtext = ctk.CTkLabel(master=self.frm_lowatual, text="Numero")
        self.lab_numtext.place(x=30, y=120)

        self.lab_bairrotext = ctk.CTkLabel(master=self.frm_lowatual, text="Bairro")
        self.lab_bairrotext.place(x=30, y=150)

        self.lab_ceptext = ctk.CTkLabel(master=self.frm_lowatual, text="CEP")
        self.lab_ceptext.place(x=30, y=180)

        self.lab_cpftext = ctk.CTkLabel(master=self.frm_lowatual, text="CPF")
        self.lab_cpftext.place(x=30, y=210)

        self.lab_senhatext = ctk.CTkLabel(master=self.frm_lowatual, text="Senha")
        self.lab_senhatext.place(x=30, y=240)

        self.nome_entry = ctk.CTkEntry(master=self.frm_lowatual)
        self.nome_entry.place(x=180, y=0)

        self.datan_entry = ctk.CTkEntry(master=self.frm_lowatual)
        self.datan_entry.place(x=180, y=30)

        self.sexo_value = ctk.CTkComboBox(self.frm_lowatual, values=["Masculino", "Feminino"])
        self.sexo_value.place(x=180, y=60)

        self.rua_entry = ctk.CTkEntry(self.frm_lowatual)
        self.rua_entry.place(x=180, y=90)

        self.numero_entry = ctk.CTkEntry(self.frm_lowatual)
        self.numero_entry.place(x=180, y=120)

        self.bairro_entry = ctk.CTkEntry(self.frm_lowatual)
        self.bairro_entry.place(x=180, y=150)

        self.cep_entry = ctk.CTkEntry(self.frm_lowatual)
        self.cep_entry.place(x=180, y=180)

        self.cpf_entry = ctk.CTkEntry(self.frm_lowatual)
        self.cpf_entry.place(x=180, y=210)
        self.cpf_entry.insert(0, "000000000000")

        self.senha_entry = ctk.CTkEntry(self.frm_lowatual, show="*")
        self.senha_entry.place(x=180, y=240)

        self.cadastrar_btn = ctk.CTkButton(self.frm_lowatual, text='Cadastrar', command=self.registrar_usuario)
        self.cadastrar_btn.place(x=180, y=270)

        self.retorno_btn = ctk.CTkButton(self.frm_lowatual, text='Retornar', command=self.retornar_login)
        self.retorno_btn.place(x=30, y=270)

    def registrar_usuario(self):
        self.cpf = self.cpf_entry.get()
        self.nome = self.nome_entry.get()
        self.datan = self.datan_entry.get()
        self.sexo = self.sexo_value.get()
        self.rua = self.rua_entry.get()
        self.numero = self.numero_entry.get()
        self.bairro = self.bairro_entry.get()
        self.cep = self.bairro_entry.get()
        self.senha = self.senha_entry.get()

        self.user = [self.cpf, self.nome, self.datan, self.sexo,
                     self.rua,
                     self.numero, self.bairro, self.cep, self.senha]

        with self.banco_cad:
            try:
                if (self.cpf == "000000000000") or (self.nome == "") or (
                        self.datan == "") or (self.rua == "") or (self.cep == "") or (
                        self.senha == ""):
                    print("Erro de cadastro: Insira todos os dados")

                else:

                    entry = self.validar_cadastro()

                    if entry is None:

                        self.cursor.execute(
                            "INSERT INTO usuario (cpf,nome,data,sexo,rua,numero,bairro,cep,senha) VALUES (?,?,?,?,?,?,?,?,?)",
                            self.user)
                        print("cadastrado com sucesso")

                        self.banco_cad.commit()

                    else:

                        print("Usuario ja registrado")



            except (sqlite3.Error, TypeError) as e:
                print("erro ao:", e)

    def irmenu(self):
        self.retirar_janelaatual()
        self.criar_menu()
        self.criar_widgetsmenu()

    def criar_menu(self):
        self.janela_menu = ctk.CTkToplevel(self.janela_login)
        self.janela_atual = self.janela_menu
        self.janela_menu.title("Recap")
        self.janela_menu.geometry("270x300")
        self.janela_menu.configure(fg_color='#00ced1')

    def criar_widgetsmenu(self):
        self.criar_framesatual()

        self.frm_topatual.place(x=0, y=0)
        self.frm_lowatual.place(x=0, y=60)

        self.lab_titulo = ctk.CTkLabel(master=self.frm_topatual, text="Menu", font=("", 20))
        self.lab_titulo.place(x=80, y=15)

        self.btn_registrarrec = ctk.CTkButton(master=self.frm_lowatual, text="Fazer Reclamação",
                                              command=self.ir_registrarrec)
        self.btn_registrarrec.place(x=60, y=0)

        self.btn_acompanharrec = ctk.CTkButton(master=self.frm_lowatual, text="Acompanhar Reclamação",
                                               command=self.ir_verrec)
        self.btn_acompanharrec.place(x=60, y=40)

        self.btn_atualizarcad = ctk.CTkButton(master=self.frm_lowatual, text="Atualizar Cadastro",command=self.ir_attcadastro)
        self.btn_atualizarcad.place(x=60, y=80)

        self.btn_sair = ctk.CTkButton(master=self.frm_lowatual, text="Sair", command=self.retornar_login)
        self.btn_sair.place(x=60, y=120)

    def ir_registrarrec(self):
        self.retirar_janelaatual()
        self.criar_registrarrec()
        self.criar_widgetsregistrarrec()

        self.conectar_ocorrenciabd()
        self.criar_ocorrenciabd()

    def criar_registrarrec(self):
        self.janela_registarrec = ctk.CTkToplevel(self.janela_login)
        self.janela_atual = self.janela_registarrec
        self.janela_registarrec.title("Recap")
        self.janela_registarrec.geometry("350x270")
        self.janela_registarrec.configure(fg_color='#00ced1')

    def criar_widgetsregistrarrec(self):
        self.criar_framesatual()

        self.frm_topatual.place(x=0, y=0)
        self.frm_lowatual.place(x=0, y=60)

        self.lab_titulo = ctk.CTkLabel(self.frm_topatual, text="Registrar Ocorrencia", font=("", 20))
        self.lab_titulo.place(x=5, y=15)

        self.lab_enderecotext = ctk.CTkLabel(self.frm_lowatual, text="Endereço")
        self.lab_enderecotext.place(x=30, y=0)

        self.lab_numerotext = ctk.CTkLabel(self.frm_lowatual, text="numero")
        self.lab_numerotext.place(x=30, y=30)

        self.lab_bairrotext = ctk.CTkLabel(self.frm_lowatual, text="Bairro")
        self.lab_bairrotext.place(x=30, y=60)

        self.lab_ceptext = ctk.CTkLabel(self.frm_lowatual, text="CEP")
        self.lab_ceptext.place(x=30, y=90)

        self.entry_endereco = ctk.CTkEntry(self.frm_lowatual)
        self.entry_endereco.place(x=180, y=0)

        self.entry_numero = ctk.CTkEntry(self.frm_lowatual)
        self.entry_numero.place(x=180, y=30)

        self.entry_bairro = ctk.CTkEntry(self.frm_lowatual)
        self.entry_bairro.place(x=180, y=60)

        self.entry_cep = ctk.CTkEntry(self.frm_lowatual)
        self.entry_cep.place(x=180, y=90)

        self.btn_salvarrec = ctk.CTkButton(self.frm_lowatual, text="Salvar", command=self.inserir_rec)
        self.btn_salvarrec.place(x=180, y=120)

        self.btn_voltar = ctk.CTkButton(self.frm_lowatual, text="Voltar", command=self.voltar_menu)
        self.btn_voltar.place(x=30, y=120)

    def conectar_ocorrenciabd(self):
        try:
            self.banco_rec = sqlite3.connect("reclamacao.db")
            self.cursor_rec = self.banco_rec.cursor()
            print("conexão feita com sucesso!")

        except sqlite3.Error as e:
            print("erro ao conectar com o banco de dados:", e)

    def criar_ocorrenciabd(self):

        query = "CREATE TABLE IF NOT EXISTS protocolo (rua string,numero int,bairro string,cep int,imagem string,status_protocolo string, UNIQUE(rua))"

        try:
            with self.banco_rec:
                self.cursor_rec = self.banco_rec.cursor()
                self.cursor_rec.execute(
                    query)
                print("Tabela Reclamações criada com sucesso!")

        except sqlite3.Error as e:
            print("Erro ao criar a tabela protocolo:", e)

    def inserir_rec(self):
        self.cep = ""
        self.endereco = self.entry_endereco.get()
        self.numero = self.entry_numero.get()
        self.bairro = self.entry_bairro.get()
        self.cep = self.entry_cep.get()
        self.imagem = "......"
        self.status_protocolo = "Em Aberto"

        self.dados = None

        self.ocorrencia = [self.endereco, self.numero, self.bairro, self.cep, self.imagem, self.status_protocolo]
        try:
            with self.banco_rec:
                if self.endereco == "":
                    print("Inserir Dados Corretamente")


                else:

                    self.cursor_rec.execute(
                        "INSERT OR IGNORE INTO protocolo (rua,numero,bairro,cep,imagem,status_protocolo) VALUES(?,?,?,?,?,?)",
                        self.ocorrencia)

                    print(f'Reclamação: {self.ocorrencia} registrado')
                    self.voltar_menu()




        except (sqlite3.Error, TypeError) as e:
            print("erro ao:", e)

    '''def existedados(self,endereco):
        protocolo =[] #não funciona como deveria
        with self.banco_cad:
            self.cursor_rec.execute("SELECT * FROM protocolo WHERE (rua=?)", (endereco,))
            dados = self.cursor.fetchall()

            for informação in dados:
                protocolo.append(informação)
        return protocolo'''

    def voltar_menu(self):
        self.irmenu()

    def ir_verrec(self):
        self.retirar_janelaatual()
        self.criar_verrec()
        self.criar_widgetsverrec()
        self.conectar_ocorrenciabd()
        self.criar_ocorrenciabd()


    def criar_verrec(self):
        self.janela_verrec = ctk.CTkToplevel(self.janela_login)
        self.janela_atual = self.janela_verrec
        self.janela_verrec.title("Recap")
        self.janela_verrec.geometry("800x500")
        self.janela_verrec.configure(fg_color='#00ced1')

    def criar_widgetsverrec(self):

        self.frm_topatual = ctk.CTkFrame(self.janela_atual, width=600, height=40,fg_color="#00ced1")
        self.frm_topatual.place(x=0, y=0)

        self.frm_lowatual = ctk.CTkFrame(self.janela_atual,width=600,height=90,fg_color="#00ced1")
        self.frm_lowatual.place(x=0, y=50)

        self.titulo = ctk.CTkLabel(self.frm_topatual, text="Acompanhar Reclamações", font=("", 20), padx=200)
        self.titulo.place(x=0, y=0)

        self.lab_enderecotext = ctk.CTkLabel(self.frm_lowatual,text="Endereço", padx=50)
        self.lab_enderecotext.place(x=10,y=0)

        self.endereco_entry = ctk.CTkEntry(self.frm_lowatual,width=150)
        self.endereco_entry.place(x=30,y=30)

        self.btn_pesquisar = ctk.CTkButton(self.frm_lowatual,text="Pesquisar",width=50,command=self.pesquisar)
        self.btn_pesquisar.place(x=200,y=30)

        self.btn_limpar = ctk.CTkButton(self.frm_lowatual,text="Limpar",width=20,command=self.limpar)
        self.btn_limpar.place(x=200,y=60)

        self.btn_voltar = ctk.CTkButton(self.janela_atual, text="Voltar", command=self.voltar_menu)
        self.btn_voltar.place(x=30, y=300)

        self.colunas = ttk.Treeview(self.janela_atual, height=6,
                                    columns=("Endereço", "Numero", "Bairro", "CEP", "Status"))
        self.colunas.place(x=30, y=150)

        self.colunas.heading("#0", text="")
        self.colunas.heading("Endereço", text="Endereço")
        self.colunas.heading("Numero", text="Numero")
        self.colunas.heading("Bairro", text="Bairro")
        self.colunas.heading("CEP", text="CEP")
        self.colunas.heading("Status", text="Status")

        self.colunas.column("#0", width=1)
        self.colunas.column("Endereço", width=200)
        self.colunas.column("Numero", width=100)
        self.colunas.column("Bairro", width=150)
        self.colunas.column("CEP", width=150)
        self.colunas.column("Status", width=100)


    def pesquisar(self):
        endereco = self.endereco_entry.get()

        lista = self.existe_endereco(endereco)

        for i in lista:
                self.colunas.insert("", "end", values=i)

    def existe_endereco(self,endereco):
        lista = self.cursor_rec.execute(""" SELECT rua,numero,bairro,cep,status_protocolo FROM protocolo WHERE rua=?""",(endereco,))
        return lista
    def limpar(self):
        for i in self.colunas.get_children():
           self.colunas.delete(i)

    def ir_attcadastro(self):
        self.retirar_janelaatual()
        self.criar_attcadastro()
        self.criar_widgetsattcadastro()
        self.conectar_cadastrobd()


    def criar_attcadastro(self):
        self.janela_attcadastro = ctk.CTkToplevel(self.janela_login)
        self.janela_atual = self.janela_attcadastro
        self.janela_attcadastro.title("Recap")
        self.janela_attcadastro.geometry("500x400")
        self.janela_attcadastro.configure(fg_color='#00ced1')

    def criar_widgetsattcadastro(self):

        self.criar_framesatual()

        self.frm_topatual.configure(width=300)
        self.frm_lowatual.configure(width=700)

        self.frm_topatual.place(x=0, y=0)
        self.frm_lowatual.place(x=0, y=60)

        self.lab_cadtext = ctk.CTkLabel(master=self.frm_topatual, text='Cadastro', font=("", 20))
        self.lab_cadtext.place(x=5, y=10)

        self.lab_nometext = ctk.CTkLabel(master=self.frm_lowatual, text='Nome')
        self.lab_nometext.place(x=30, y=0)

        self.lab_datantext = ctk.CTkLabel(master=self.frm_lowatual, text='Data de Nascimento')
        self.lab_datantext.place(x=30,y=30)

        self.lab_sexotext = ctk.CTkLabel(master=self.frm_lowatual, text='Sexo')
        self.lab_sexotext.place(x=30, y=60)

        self.lab_ruatext = ctk.CTkLabel(master=self.frm_lowatual, text="Rua")
        self.lab_ruatext.place(x=30, y=90)

        self.lab_numtext = ctk.CTkLabel(master=self.frm_lowatual, text="Numero")
        self.lab_numtext.place(x=30, y=120)

        self.lab_bairrotext = ctk.CTkLabel(master=self.frm_lowatual, text="Bairro")
        self.lab_bairrotext.place(x=30, y=150)

        self.lab_ceptext = ctk.CTkLabel(master=self.frm_lowatual, text="CEP")
        self.lab_ceptext.place(x=30, y=180)

        self.lab_cpftext = ctk.CTkLabel(master=self.frm_lowatual, text="CPF")
        self.lab_cpftext.place(x=30, y=210)

        self.lab_nome = ctk.CTkLabel(master=self.frm_lowatual, text=''+str(self.user[1]))
        self.lab_nome.place(x=150, y=0)

        self.lab_datan = ctk.CTkLabel(master=self.frm_lowatual, text=''+str(self.user[2]))
        self.lab_datan.place(x=150,y=30)

        self.lab_sexo =  ctk.CTkLabel(master=self.frm_lowatual, text=''+str(self.user[3]))
        self.lab_sexo.place(x=150, y=60)

        self.lab_rua =  ctk.CTkLabel(master=self.frm_lowatual, text=''+str(self.user[4]))
        self.lab_rua.place(x=150, y=90)

        self.lab_num =  ctk.CTkLabel(master=self.frm_lowatual, text=''+str(self.user[5]))
        self.lab_num.place(x=150, y=120)

        self.lab_bairro =  ctk.CTkLabel(master=self.frm_lowatual, text=''+str(self.user[6]))
        self.lab_bairro.place(x=150, y=150)

        self.lab_cep =  ctk.CTkLabel(master=self.frm_lowatual, text=''+str(self.user[7]))
        self.lab_cep.place(x=150, y=180)

        self.lab_cpf = ctk.CTkLabel(master=self.frm_lowatual, text=''+str(self.user[0]))
        self.lab_cpf.place(x=150, y=210)

        self.entry_nome = ctk.CTkEntry(master=self.frm_lowatual)
        self.entry_nome.place(x=250, y=0)


        self.entry_rua =ctk.CTkEntry(master=self.frm_lowatual)
        self.entry_rua.place(x=250, y=90)

        self.entry_num = ctk.CTkEntry(master=self.frm_lowatual)
        self.entry_num.place(x=250, y=120)

        self.entry_bairro = ctk.CTkEntry(master=self.frm_lowatual)
        self.entry_bairro.place(x=250, y=150)

        self.entry_cep = ctk.CTkEntry(master=self.frm_lowatual)
        self.entry_cep.place(x=250, y=180)

        self.btn_salvar = ctk.CTkButton(master=self.frm_lowatual,text="Salvar Alteração",command=self.attcadastro)
        self.btn_salvar.place(x=200, y=240)

        self.btn_voltar = ctk.CTkButton(master=self.frm_lowatual,text="Voltar",command=self.voltar_menu)
        self.btn_voltar.place(x=30, y=240)

        self.btn_attsenha = ctk.CTkButton(master=self.frm_lowatual,text="Alterar Senha",command=self.attsenha)
        self.btn_attsenha.place(x=370, y=240)

    def attcadastro(self):
        self.att_infonome = self.entry_nome.get()

        self.att_inforua = self.entry_rua.get()
        self.att_infonum = self.entry_num.get()
        self.att_infobairro = self.entry_bairro.get()
        self.att_infocep = self.entry_cep.get()

        self.attnome()

        self.attrua()
        self.attnum()
        self.attbairro()
        self.attcep()
        self.retornar_login()


    def attnome(self):
        if self.att_infonome == "":
            return None

        else:
            with self.banco_cad:
                query = "UPDATE usuario SET nome=? WHERE cpf=?"
                self.cursor.execute(query,(self.att_infonome,self.user[0]))

    def attrua(self):
        if self.att_inforua == "":
            return None

        else:
            with self.banco_cad:
                query = "UPDATE usuario SET rua=? WHERE cpf=?"
                self.cursor.execute(query, (self.att_inforua, self.user[0]))

    def attnum(self):
        if self.att_infonum == "":
            return None

        else:
            with self.banco_cad:
                query = "UPDATE usuario SET numero=? WHERE cpf=?"
                self.cursor.execute(query, (self.att_infonum, self.user[0]))

    def attbairro(self):
        if self.att_infobairro == "":
            return None

        else:
            with self.banco_cad:
                query = "UPDATE usuario SET bairro=? WHERE cpf=?"
                self.cursor.execute(query, (self.att_infobairro, self.user[0]))

    def attcep(self):
        if self.att_infocep == "":
            return None

        else:
            with self.banco_cad:
                query = "UPDATE usuario SET cep=? WHERE cpf=?"
                self.cursor.execute(query, (self.att_infocep, self.user[0]))

    def attsenha(self):
        self.irtela_recsenha()



root = ctk.CTk()
App(root)
root.mainloop()
