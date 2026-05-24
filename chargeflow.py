import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading
import subprocess

# ===== VARIÁVEIS =====
arquivo_csv = ""
arquivo_bloqueados = ""
processo = None
executando = False

# ===== ESCOLHER CSV =====
def selecionar_csv():
    global arquivo_csv

    caminho = filedialog.askopenfilename(
        title="Selecionar planilha CSV",
        filetypes=[("CSV Files", "*.csv")]
    )

    if caminho:
        arquivo_csv = caminho
        label_csv.config(text=caminho)

# ===== ESCOLHER TXT =====
def selecionar_bloqueados():
    global arquivo_bloqueados

    caminho = filedialog.askopenfilename(
        title="Selecionar bloqueados",
        filetypes=[("TXT Files", "*.txt")]
    )

    if caminho:
        arquivo_bloqueados = caminho
        label_bloqueados.config(text=caminho)

# ===== ESCREVER NO LOG =====
def adicionar_log(texto):
    logs.insert(tk.END, texto + "\n")
    logs.see(tk.END)

# ===== EXECUTAR BOT =====
def iniciar_cobranca():

    global executando

    if executando:
        cancelar_cobranca()
        return

    if not arquivo_csv:
        adicionar_log("❌ Selecione o arquivo CSV")
        return

    if not arquivo_bloqueados:
        adicionar_log("❌ Selecione o arquivo de bloqueados")
        return

    executando = True

    btn_iniciar.config(
        text="Cancelar",
        bg="red"
    )

    thread = threading.Thread(target=executar_script)
    thread.start()
    
def cancelar_cobranca():

    global processo
    global executando

    if processo:
        processo.terminate()

    adicionar_log("🛑 Cobrança cancelada")

    executando = False

    btn_iniciar.config(
        text="Iniciar Cobrança",
        bg="green"
    )

# ===== RODAR SCRIPT =====
def executar_script():

    adicionar_log("🚀 Iniciando cobrança...")
    global processo
    global executando

    processo = subprocess.Popen(
        [
            "python3",
            "backend.py",
            arquivo_csv,
            arquivo_bloqueados
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for linha in processo.stdout:
        adicionar_log(linha.strip())

    adicionar_log("🏁 Processo finalizado")
    executando = False

    btn_iniciar.config(
        text="Iniciar Cobrança",
        bg="green"
)

# ===== JANELA =====
janela = tk.Tk()
janela.title("Cobrador WhatsApp")
janela.geometry("800x600")

# ===== TÍTULO =====
titulo = tk.Label(
    janela,
    text="Sistema de Cobrança via WhatsApp",
    font=("Arial", 16, "bold")
)

titulo.pack(pady=10)

# ===== BOTÃO CSV =====
btn_csv = tk.Button(
    janela,
    text="Selecionar inadimplentes.csv",
    command=selecionar_csv,
    width=30,
    height=2
)

btn_csv.pack(pady=5)

label_csv = tk.Label(janela, text="Nenhum arquivo selecionado")
label_csv.pack()

# ===== BOTÃO BLOQUEADOS =====
btn_bloqueados = tk.Button(
    janela,
    text="Selecionar bloqueados.txt",
    command=selecionar_bloqueados,
    width=30,
    height=2
)

btn_bloqueados.pack(pady=10)

label_bloqueados = tk.Label(janela, text="Nenhum arquivo selecionado")
label_bloqueados.pack()

# ===== BOTÃO INICIAR =====
btn_iniciar = tk.Button(
    janela,
    text="Iniciar Cobrança",
    command=iniciar_cobranca,
    bg="green",
    fg="white",
    width=25,
    height=2
)

btn_iniciar.pack(pady=20)

# ===== ÁREA DE LOG =====
logs = scrolledtext.ScrolledText(
    janela,
    width=95,
    height=20,
    font=("Consolas", 10)
)

logs.pack(padx=10, pady=10)

# ===== LOOP =====
janela.mainloop()
