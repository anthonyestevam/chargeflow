import pandas as pd
import time
import random
import urllib.parse
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===== ABRIR WHATSAPP =====
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# ===== SALVAR SESSÃO DO WHATSAPP ====
options.add_argument("--user-data-dir=/home/thxny/chrome-whatsapp")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://web.whatsapp.com")

print("Escaneie o QR Code...")
time.sleep(25)

# ===== LER PLANILHA =====
enviados = 0
arquivo = sys.argv[1]

try:

    df = pd.read_csv(
        arquivo,
        sep=";",
        encoding="utf-8"
)

    df.columns = df.columns.str.strip()

except pd.errors.EmptyDataError:
    print("❌ O arquivo CSV está vazio.", flush=True)
    exit()

except Exception as e:
    print(f"❌ Erro ao ler CSV: {e}", flush=True)
    exit()
    
clientes_chamados = set()

mensagens = [

"""Oi {nome}, tudo bem?

Sou Anthony do financeiro da Bestlaser.

Percebi um atraso em seu contrato.

Para facilitar, segue o link:
{link}

Caso já tenha realizado o pagamento, desconsidere esta mensagem.
""",

"""Oi {nome}, tudo bem com você?

Gostaria de conversar sobre o seu contrato, que atualmente está com um atraso.

Segue o link para regularização:
{link}
""",

"""Olá {nome}, tudo certo?

Aqui é o Anthony do financeiro da Bestlaser 😊

Identificamos um valor pendente em seu contrato.

Posso te enviar o link para regularização caso queira.
""",

"""Oi {nome}, espero que esteja bem!

Sou Anthony do financeiro da Bestlaser.

Notei um atraso em aberto.

Você pode regularizar pelo link:
{link}
""",

"""Olá {nome}, tudo bem?

Passando para informar que seu contrato possui um valor em aberto.

Posso te enviar o link para regularização caso queira.

Se já realizou o pagamento, pode desconsiderar esta mensagem.
"""
]
# ===== CLIENTES BLOQUEADOS =====
with open(sys.argv[2], "r") as arquivo_bloqueados:
    bloqueados = set()

    for linha in arquivo_bloqueados:
        numero = linha.strip()
        bloqueados.add(numero)
# ===== LOOP CLIENTES =====
for index, cliente in df.iterrows():

    nome = str(cliente['Nome Cliente'])
    telefone = str(cliente['Telefone Cliente'])
    
    # limpar telefone
    telefone = ''.join(filter(str.isdigit, telefone))
    
    # verificar bloqueados
    if telefone in bloqueados:
        print(f"🚫 {nome} está na lista de bloqueados. Pulando...", flush=True)
        continue
    
    # evitar envio duplicado
    if telefone in clientes_chamados:
        print(f"⚠️ {nome} já foi cobrado. Pulando...", flush=True)
        continue
        
    link = str(cliente['Link para Pagamento'])

    # limpar telefone
    telefone = ''.join(filter(str.isdigit, telefone))

    # ===== ESCOLHER MENSAGEM =====
    mensagem_template = random.choice(mensagens)

    mensagem = mensagem_template.format(
        nome=nome,
        link=link
)

    mensagem = urllib.parse.quote(mensagem)

    url = f"https://web.whatsapp.com/send?phone=55{telefone}&text={mensagem}"

    driver.get(url)

    time.sleep(random.uniform(12,18))

    try:
        caixa = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//div[@contenteditable="true"][@role="textbox"]'
                )
            )
        )

        time.sleep(random.uniform(1,3))

        caixa.send_keys(Keys.ENTER)
        clientes_chamados.add(telefone)

        print(f"✅ Enviado para {nome}", flush=True)
        enviados += 1
        print(f"📊 Total enviados:{enviados}", flush=True)

        time.sleep(random.uniform(25,45))

    except Exception as e:
        print(f"❌ Erro com {nome} -> {e}", flush=True)

print("Cobrança finalizada!", flush=True)
