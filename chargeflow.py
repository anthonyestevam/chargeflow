import customtkinter as ctk
from tkinter import filedialog
import threading
import subprocess

# ===== TEMA =====
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

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
        label_csv.configure(text=caminho)

# ===== ESCOLHER TXT =====
def selecionar_bloqueados():
    global arquivo_bloqueados

    caminho = filedialog.askopenfilename(
        title="Selecionar bloqueados",
        filetypes=[("TXT Files", "*.txt")]
    )

    if caminho:
        arquivo_bloqueados = caminho
        label_bloqueados.configure(text=caminho)

# ===== ESCREVER LOG =====
def adicionar_log(texto):
    logs.insert("end", texto + "\n")
    logs.see("end")

# ===== CANCELAR =====
def cancelar_cobranca():

    global processo
    global executando

    if processo:
        processo.terminate()

    executando = False

    adicionar_log("🛑 Cobrança cancelada")

    btn_iniciar.configure(
        text="Iniciar Cobrança",
        fg_color="green",
        hover_color="#166534"
    )

# ===== EXECUTAR SCRIPT =====
def executar_script():

    global processo
    global executando

    adicionar_log("🚀 Iniciando cobrança...")

    processo = subprocess.Popen(
        [
            "python3",
            "-u",
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

    btn_iniciar.configure(
        text="Iniciar Cobrança",
        fg_color="green",
        hover_color="#166534"
    )

# ===== INICIAR =====
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

    btn_iniciar.configure(
        text="Cancelar",
        fg_color="red",
        hover_color="#991b1b"
    )

    thread = threading.Thread(target=executar_script)
    thread.start()

# ===== JANELA =====
janela = ctk.CTk()
janela.title("ChargeFlow")
janela.geometry("900x650")

# ===== TÍTULO =====
titulo = ctk.CTkLabel(
    janela,
    text="ChargeFlow",
    font=("Arial", 30, "bold")
)

titulo.pack(pady=(20,5))

subtitulo = ctk.CTkLabel(
    janela,
    text="Sistema de automação de cobranças via WhatsApp",
    font=("Arial", 14)
)

subtitulo.pack(pady=(0,20))

# ===== CARD =====
frame = ctk.CTkFrame(
    janela,
    corner_radius=15
)

frame.pack(fill="both", expand=True, padx=20, pady=10)

# ===== BOTÃO CSV =====
btn_csv = ctk.CTkButton(
    frame,
    text="Selecionar inadimplentes.csv",
    command=selecionar_csv,
    height=45,
    corner_radius=12,
    font=("Arial", 14, "bold")
)

btn_csv.pack(fill="x", padx=20, pady=(20,8))

label_csv = ctk.CTkLabel(
    frame,
    text="Nenhum arquivo selecionado"
)

label_csv.pack(anchor="w", padx=25)

# ===== BOTÃO BLOQUEADOS =====
btn_bloqueados = ctk.CTkButton(
    frame,
    text="Selecionar bloqueados.txt",
    command=selecionar_bloqueados,
    height=45,
    corner_radius=12,
    font=("Arial", 14, "bold")
)

btn_bloqueados.pack(fill="x", padx=20, pady=(20,8))

label_bloqueados = ctk.CTkLabel(
    frame,
    text="Nenhum arquivo selecionado"
)

label_bloqueados.pack(anchor="w", padx=25)

# ===== BOTÃO INICIAR =====
btn_iniciar = ctk.CTkButton(
    frame,
    text="Iniciar Cobrança",
    command=iniciar_cobranca,
    height=50,
    corner_radius=14,
    font=("Arial", 16, "bold"),
    fg_color="green",
    hover_color="#166534"
)

btn_iniciar.pack(fill="x", padx=20, pady=25)

# ===== LOGS =====
logs_label = ctk.CTkLabel(
    frame,
    text="Logs em tempo real",
    font=("Arial", 16, "bold")
)

logs_label.pack(anchor="w", padx=20)

logs = ctk.CTkTextbox(
    frame,
    height=300,
    corner_radius=12,
    font=("Consolas", 12)
)

logs.pack(fill="both", expand=True, padx=20, pady=(10,20))

# ===== LOOP =====
janela.mainloop()
