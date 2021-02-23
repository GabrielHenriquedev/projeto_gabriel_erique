from sqlite3.dbapi2 import Cursor
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

jan= Tk()
'Parte lógica do projeto '
class funcs():
    #Aqui estão as funcionalidades do projeto, como a criação do banco de dados é funções como salvar, apagar é etc.
    def liparlabels(self):
        
        self.identre.delete(0, END)
        self.nomeentr.delete(0, END)
        self.emailentr.delete(0, END)
        self.numeroentre.delete(0, END)

    def conetaraobanco(self):
        self.conn= sqlite3.connect("socios.db")
        self.cursor= self.conn.cursor()

    def desconectar(self):
        self.conn.close()

    def montartabelas(self):
        self.conetaraobanco(); print("conectado ao banco de dados")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS socios (
                id INTEGER PRIMARY KEY,
                nome CHAR(40) NOT NUll,
                email CHAR(20) NOT NUll,
                telefone INTEGER(20) NOT NUll
            );
        """) 
        self.conn.commit(); print("banco de dados criado")
        self.desconectar()

    def variaveis(self):
        self.id= self.identre.get()
        self.nome= self.nomeentr.get() 
        self.email= self.emailentr.get() 
        self.numero= self.numeroentre.get() 

    def add_socios(self):
        self.variaveis()
        self.conetaraobanco()
        # Abaixo estão validações para que a funcionalidade do código não seja comprometida. 
        # Elas se repetem durante o código algumas vezes.
        if self.nome == "" and self.email== "" and  self.numero == "" :
            messagebox.showerror(title="Atenção", message="Os campos não podem estar vazios")
        else:
            self.cursor.execute(""" INSERT INTO socios ( nome, email, telefone) 
                VALUES(?,?,?)""",(self.nome, self.email,self.numero))
            self.conn.commit()
            self.mensagem= messagebox.showinfo(title="Parabens", message="O sócio foi salvo")
            self.desconectar()
            self.select()
            self.liparlabels()

    def Ondoubleclick(self,event):
        self.liparlabels()
        self.lista.selection()
        
        for n in self.lista.selection():
            col1, col2, col3, col4= self.lista.item(n, "values")
            self.identre.insert(END, col1)
            self.nomeentr.insert(END, col2)
            self.emailentr.insert(END, col3)
            self.numeroentre.insert(END, col4)

    def select(self):
        self.lista.delete(*self.lista.get_children())
        self.conetaraobanco()
        tabe= self.cursor.execute(""" SELECT id, nome, email, telefone FROM socios ORDER BY nome ASC;""")
        for i in tabe:
            self.lista.insert("", END, values=i)
        self.desconectar()

    def delet_socio(self):
        self.variaveis()
        self.conetaraobanco()
        if self.nome == "" and self.email== "" and  self.numero == "":
            messagebox.showerror(title="Atenção", message="Os campos não podem estar vazios")
        else:
            self.cursor.execute("""DELETE FROM socios WHERE id= ?""", (self.id,))
            self.conn.commit()

            self.desconectar()
            self.liparlabels()
            self.select()
            self.mensagem2= messagebox.showinfo(title="Info", message="O sócio foi deletado")

    def alterardados(self):
        self.variaveis()
        self.conetaraobanco()
        if self.nome == "" and self.email== "" and  self.numero == "":
            messagebox.showerror(title="Atenção", message="Os campos não podem estar vazios")
        else:
            self.cursor.execute("""UPDATE socios SET nome= ?, email= ?, telefone= ?
                WHERE id= ? """,(self.nome, self.email,self.numero,self.id))
            self.conn.commit()
            messagebox.showinfo(title="Atenção", message="O sócio foi alterado")
            self.desconectar()
            self.select()
            self.liparlabels()

    def buscar(self):
        self.conetaraobanco()
        self.lista.delete(*self.lista.get_children())
        self.nomeentr.insert(END, "%")
        nome= self.nomeentr.get()
        if self.nome == "":
            messagebox.showerror(title="Atenção", message="O nome não pode estar vazio")
        else:
            self.cursor.execute(
                """ SELECT id, nome, email, telefone FROM socios
                WHERE nome LIKE '%s' ORDER BY nome ASC """ % nome)
            busca= self.cursor.fetchall()
            for i in busca:
                self.lista.insert("", END, values=i)
                self.mensagem3= messagebox.showinfo(title="INFO", message="Sócios encontrados")
            self.liparlabels()
            self.desconectar()

class aplicaçoes(funcs):
    'Parte gráfica  do projeto'
    def __init__(self):
        #Aqui e onde as funções são chamadas para que o código possa funcionar.
        self.jan=jan
        self.tela()
        self.frames()
        self.botoes()
        self.tabela()
        self.montartabelas()
        self.select()

        jan.mainloop()

    def tela(self):
        #Aqui começa a parte visual do projeto onde você pode interagir de fato com o código,
        #acontecem coisas como a criação da janela a criação de Label, botões e etc. 
        self.jan.title("Cadastro de Sócio")
        self.jan.geometry("700x500")
        self.jan.configure(background="white")
        self.jan.resizable(width=True, height=True)
        self.jan.maxsize(width=900, height=700)
        self.jan.minsize(width=500, height=400)
        self.jan.iconbitmap("data/icone.ico")

    def frames(self):
      self.frame1= Frame(jan, bd=4, bg='#74d4d0',highlightbackground="#a0f2ef", highlightthickness=6 )
      self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
      self.frame2= Frame(jan, bd=4, bg='#74d4d0',highlightbackground="#a0f2ef", highlightthickness=6 )
      self.frame2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def botoes(self):
        #botão de salvar
        self.but_salvar= Button(self.frame1, text="Salvar", bd=4, bg="white", fg="black", font=("arial", 10,"bold"), command=self.add_socios)
        self.but_salvar.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)
        #botão de buscar
        self.but_busca= Button(self.frame1, text="Buscar", bd=4, bg="white", fg="black", font=("arial", 10,"bold"), command=self.buscar)
        self.but_busca.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)
        #botão de apagar
        self.but_apagar= Button(self.frame1, text="Apagar", bd=4, bg="white", fg="black", font=("arial", 10,"bold"), command=self.delet_socio)
        self.but_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)
        #botão de alterar
        self.but_alterar= Button(self.frame1, text="Alterar", bd=4, bg="white", fg="black", font=("arial", 10,"bold"), command=self.alterardados)
        self.but_alterar.place(relx=0.9, rely=0.1, relwidth=0.1, relheight=0.15)

        #label title
        self.title= Label(self.frame1, text="Cadastro de Sócios", bg='#74d4d0', font=("arial", 15,"bold"))
        self.title.place(relx=0.25, rely=0.05)
         #label id 
        self.id= Label(self.frame1, text="ID do Sócio", bg='#74d4d0', font=("arial", 10,"bold"))
        self.id.place(relx=0.05, rely=0.10)
        
        self.identre= Entry(self.frame1)
        self.identre.place(relx=0.05, rely=0.20, relwidth=0.12)
        #label nome
        self.nome= Label(self.frame1, text="Nome do Sócio", bg='#74d4d0', font=("arial", 10,"bold"))
        self.nome.place(relx=0.05, rely=0.35)
        
        self.nomeentr= Entry(self.frame1)
        self.nomeentr.place(relx=0.05, rely=0.45, relwidth=0.85)
        #label email
        self.email= Label(self.frame1, text="Email", bg='#74d4d0', font=("arial", 10,"bold"))
        self.email.place(relx=0.05, rely=0.6)
        
        self.emailentr= Entry(self.frame1)
        self.emailentr.place(relx=0.05, rely=0.7, relwidth=0.4)
        #label numero
        self.numero= Label(self.frame1, text="Número para contato", bg='#74d4d0', font=("arial", 10,"bold"))
        self.numero.place(relx=0.5, rely=0.6)
        
        self.numeroentre= Entry(self.frame1)
        self.numeroentre.place(relx=0.5, rely=0.7, relwidth=0.4)
 
    def tabela(self):
        #Abaixo é onde acontece a criação da tabela, responsável por mostrar quais sócios estão salvos 
        self.lista= ttk.Treeview(self.frame2, height=3, columns=("col1","col2","col3","col4"))
        self.lista.heading("#0", text="")
        self.lista.heading("#1", text="ID")
        self.lista.heading("#2", text="Nome")
        self.lista.heading("#3", text="Email")
        self.lista.heading("#4", text="Contato")

        self.lista.column("#0", width=1)
        self.lista.column("#1", width=50)
        self.lista.column("#2", width=200)
        self.lista.column("#3", width=125)
        self.lista.column("#4", width=125)

        self.lista.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroollist= Scrollbar(self.frame2,orient="vertical")
        self.lista.configure(yscroll=self.scroollist.set)
        self.scroollist.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.lista.bind("<Double-1>", self.Ondoubleclick)


aplicaçoes()