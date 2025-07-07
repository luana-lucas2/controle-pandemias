import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

# Garante a pasta do banco
if not os.path.exists("dados"):
    os.makedirs("dados")

# Conexão com banco de dados
con = sqlite3.connect("dados/pandemias.db")
cur = con.cursor()

# Tabelas
cur.execute("""
CREATE TABLE IF NOT EXISTS casos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estado TEXT,
    cidade TEXT,
    hospital TEXT,
    doenca TEXT,
    casos INTEGER,
    mortes INTEGER,
    internados INTEGER
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS doencas (
    nome TEXT PRIMARY KEY
);
""")
con.commit()

# Estados e cidades
estados_cidades = {
    "Acre": ["Rio Branco", "Cruzeiro do Sul", "Sena Madureira"],
    "Alagoas": ["Maceió", "Arapiraca", "Palmeira dos Índios"],
    "Amapá": ["Macapá", "Santana", "Laranjal do Jari"],
    "Amazonas": ["Manaus", "Parintins", "Itacoatiara"],
    "Bahia": ["Salvador", "Feira de Santana", "Vitória da Conquista"],
    "Ceará": ["Fortaleza", "Caucaia", "Juazeiro do Norte"],
    "Distrito Federal": ["Brasília"],
    "Espírito Santo": ["Vitória", "Vila Velha", "Serra"],
    "Goiás": ["Goiânia", "Aparecida de Goiânia", "Anápolis"],
    "Maranhão": ["São Luís", "Imperatriz", "Caxias"],
    "Mato Grosso": ["Cuiabá", "Várzea Grande", "Rondonópolis"],
    "Mato Grosso do Sul": ["Campo Grande", "Dourados", "Três Lagoas"],
    "Minas Gerais": ["Belo Horizonte", "Uberlândia", "Contagem"],
    "Pará": ["Belém", "Ananindeua", "Santarém"],
    "Paraíba": ["João Pessoa", "Campina Grande", "Patos"],
    "Paraná": ["Curitiba", "Londrina", "Maringá"],
    "Pernambuco": ["Recife", "Jaboatão", "Olinda"],
    "Piauí": ["Teresina", "Parnaíba", "Picos"],
    "Rio de Janeiro": ["Rio de Janeiro", "Niterói", "Duque de Caxias"],
    "Rio Grande do Norte": ["Natal", "Mossoró", "Parnamirim"],
    "Rio Grande do Sul": ["Porto Alegre", "Canoas", "São Leopoldo"],
    "Rondônia": ["Porto Velho", "Ji-Paraná", "Ariquemes"],
    "Roraima": ["Boa Vista", "Rorainópolis", "Caracaraí"],
    "Santa Catarina": ["Florianópolis", "Joinville", "Blumenau"],
    "São Paulo": ["São Paulo", "Campinas", "Santos"],
    "Sergipe": ["Aracaju", "Nossa Senhora do Socorro", "Lagarto"],
    "Tocantins": ["Palmas", "Araguaína", "Gurupi"]
}

# Interface principal
janela = tk.Tk()
janela.title("Cadastro de Casos")
janela.geometry("900x650")
janela.configure(bg="#e6faff")

# Estilo visual
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Segoe UI", 12), background="#e6faff")
style.configure("TButton", font=("Segoe UI", 12), padding=6)
style.configure("TCombobox", font=("Segoe UI", 12))


# Título estilizado
titulo = tk.Label(janela, text="Cadastro de Casos", font=("Segoe UI", 20, "bold"), bg="#e6faff", fg="#007f99")
titulo.pack(pady=10)

# Função para atualizar cidades

def atualizar_cidades(event):
    estado = estado_cb.get()
    cidades_cb["values"] = estados_cidades.get(estado, [])

# Frame principal
form = tk.Frame(janela, bg="#f9f9f9")
form.pack(pady=20)

# Estado
ttk.Label(form, text="Estado:").grid(row=0, column=0, sticky="w")
estado_cb = ttk.Combobox(form, values=list(estados_cidades.keys()), width=30)
estado_cb.grid(row=0, column=1)
estado_cb.bind("<<ComboboxSelected>>", atualizar_cidades)

# Cidade
ttk.Label(form, text="Cidade:").grid(row=1, column=0, sticky="w")
cidades_cb = ttk.Combobox(form, width=30)
cidades_cb.grid(row=1, column=1)

# Hospital
ttk.Label(form, text="Hospital:").grid(row=2, column=0, sticky="w")
hospital_entry = ttk.Entry(form, width=33)
hospital_entry.grid(row=2, column=1)

# Doença
ttk.Label(form, text="Doença:").grid(row=3, column=0, sticky="w")
doenca_cb = ttk.Combobox(form, width=30)
doenca_cb.grid(row=3, column=1)

# Atualiza doenças do banco

def atualizar_doencas():
    cur.execute("SELECT nome FROM doencas")
    doencas = [r[0] for r in cur.fetchall()]
    doenca_cb["values"] = doencas

atualizar_doencas()

# Adicionar nova doença

def adicionar_doenca():
    nova = nova_doenca_entry.get()
    if nova:
        try:
            cur.execute("INSERT INTO doencas (nome) VALUES (?)", (nova,))
            con.commit()
            atualizar_doencas()
            nova_doenca_entry.delete(0, tk.END)
            messagebox.showinfo("Sucesso", f"{nova} adicionada com sucesso.")
        except:
            messagebox.showwarning("Erro", "Essa doença já existe!")

nova_doenca_entry = ttk.Entry(form, width=33)
nova_doenca_entry.grid(row=4, column=1)
ttk.Button(form, text="Nova Doença", command=adicionar_doenca, style="TButton").grid(row=4, column=0, pady=10)

# Casos
ttk.Label(form, text="Casos:").grid(row=5, column=0, sticky="w")
casos_entry = ttk.Entry(form, width=33)
casos_entry.grid(row=5, column=1)

# Mortes
ttk.Label(form, text="Mortes:").grid(row=6, column=0, sticky="w")
mortes_entry = ttk.Entry(form, width=33)
mortes_entry.grid(row=6, column=1)

# Internados
ttk.Label(form, text="Internados:").grid(row=7, column=0, sticky="w")
internados_entry = ttk.Entry(form, width=33)
internados_entry.grid(row=7, column=1)

# Cadastrar caso

def cadastrar():
    dados = (
        estado_cb.get(), cidades_cb.get(), hospital_entry.get(), doenca_cb.get(),
        int(casos_entry.get()), int(mortes_entry.get()), int(internados_entry.get())
    )
    cur.execute("""
    INSERT INTO casos (estado, cidade, hospital, doenca, casos, mortes, internados)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, dados)
    con.commit()
    estado_cb.set("")
    cidades_cb.set("")
    hospital_entry.delete(0, tk.END)
    doenca_cb.set("")
    casos_entry.delete(0, tk.END)
    mortes_entry.delete(0, tk.END)
    internados_entry.delete(0, tk.END)
    messagebox.showinfo("Sucesso", "Caso registrado com sucesso!")

ttk.Button(form, text="Cadastrar Caso", command=cadastrar).grid(row=8, column=0, columnspan=2, pady=15)

# Consulta em nova janela

def abrir_consulta():
    def consultar():
        for widget in resultado_frame.winfo_children():
            widget.destroy()

        estado = consulta_estado_cb.get()
        doenca = consulta_doenca_cb.get()
        cur.execute("""
        SELECT cidade, hospital, casos, mortes, internados FROM casos
        WHERE estado=? AND doenca=?
        """, (estado, doenca))
        resultados = cur.fetchall()

        total_casos = sum([r[2] for r in resultados])
        total_mortes = sum([r[3] for r in resultados])
        total_internados = sum([r[4] for r in resultados])

        cor = "green" if total_casos <= 5000 else "orange" if total_casos <= 50000 else "red"

        for r in resultados:
            tk.Label(resultado_frame, text=f"Cidade: {r[0]}, Hospital: {r[1]}, Casos: {r[2]}, Mortes: {r[3]}, Internados: {r[4]}", font=("Segoe UI", 11), bg="#fff").pack(anchor="w")

        tk.Label(resultado_frame, text=f"\nTOTAL {doenca} EM {estado}:", font=("Segoe UI", 13, "bold"), fg=cor, bg="#fff").pack(anchor="w")
        tk.Label(resultado_frame, text=f"Casos: {total_casos} | Mortes: {total_mortes} | Internados: {total_internados}", font=("Segoe UI", 12), bg="#fff").pack(anchor="w")

    nova = tk.Toplevel(janela)
    nova.title("Consulta de Casos")
    nova.geometry("800x500")
    nova.configure(bg="#fff")

    consulta_estado_cb = ttk.Combobox(nova, values=list(estados_cidades.keys()), width=30)
    consulta_estado_cb.pack(pady=10)

    consulta_doenca_cb = ttk.Combobox(nova, width=30)
    consulta_doenca_cb.pack(pady=10)

    cur.execute("SELECT nome FROM doencas")
    consulta_doenca_cb["values"] = [r[0] for r in cur.fetchall()]

    ttk.Button(nova, text="Consultar", command=consultar).pack()

    canvas = tk.Canvas(nova, bg="#fff")
    scrollbar = ttk.Scrollbar(nova, orient="vertical", command=canvas.yview)
    resultado_frame = tk.Frame(canvas, bg="#fff")

    resultado_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=resultado_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

# Botão consulta
btn_consulta = ttk.Button(janela, text="Consultar Casos", command=abrir_consulta)
btn_consulta.pack(pady=10)

# Inicia janela
janela.mainloop()
