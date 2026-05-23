# 🚀 COBRADOR: Sistema de Cobrança Automática via WhatsApp

Automação desenvolvida em Python para facilitar cobranças via WhatsApp Web utilizando planilhas CSV de inadimplentes.

O sistema permite:

* ✅ Envio automático de mensagens
* ✅ Interface gráfica simples
* ✅ Seleção dinâmica de arquivos
* ✅ Controle de clientes bloqueados
* ✅ Evitar cobranças duplicadas
* ✅ Logs em tempo real
* ✅ Alternância automática de mensagens
* ✅ Delays humanos anti-bloqueio
* ✅ Sessão permanente do WhatsApp

---

# 🖥️ Preview

## Interface do sistema

* Seleção da planilha CSV
* Seleção do TXT de bloqueados
* Botão iniciar/cancelar
* Logs em tempo real

---

# 📂 Estrutura do Projeto

```bash
/cobrador/
│
├── cobrador.py
├── backend.py
├── bloqueados.txt
├── inadimplentes.csv
└── README.md
```

---

# ⚙️ Tecnologias Utilizadas

* Python 3
* Selenium
* Pandas
* Tkinter
* WhatsApp Web
* WebDriver Manager

---

# 📦 Instalação

## 1️⃣ Clone o repositório

```bash
git clone https://github.com/anthonyestevam/cobrador.git
```

---

## 2️⃣ Entre na pasta

```bash
cd cobrador
```

---

## 3️⃣ Instale as dependências

```bash
pip install selenium pandas webdriver-manager
```

---

## 4️⃣ Instale o Tkinter (Linux)

Ubuntu / Debian:

```bash
sudo apt install python3-tk
```

Arch Linux:

```bash
sudo pacman -S tk
```

Fedora:

```bash
sudo dnf install python3-tkinter
```

---

# ▶️ Como executar

```bash
python3 cobrador.py
```

---

# 📄 Formato da planilha CSV

O sistema espera um CSV contendo colunas como:

```text
Nome Cliente
Telefone Cliente
Valor em Atraso
Dias de Atraso
Link para Pagamento
```

---

# 🚫 Lista de bloqueados

Crie um arquivo:

```text
bloqueados.txt
```

Com um número por linha:

```text
11999999999
11988888888
```

Clientes presentes nessa lista não serão cobrados.

---

# 🧠 Recursos do Sistema

## ✅ Controle de duplicados

Evita enviar múltiplas mensagens para o mesmo cliente.

---

## ✅ Mensagens alternadas

O sistema alterna automaticamente diferentes modelos de mensagens para reduzir padrões repetitivos.

---

## ✅ Delays humanos

Intervalos aleatórios entre envios para simular comportamento humano.

---

## ✅ Sessão permanente do WhatsApp

Mantém o WhatsApp Web logado sem necessidade de escanear QR Code diariamente.

---

# 📊 Logs em tempo real

Exemplo:

```text
🚀 Iniciando cobrança...
✅ Enviado para João
📊 Total enviados: 1
⚠️ Maria já foi cobrada. Pulando...
🚫 Carlos está na lista de bloqueados. Pulando...
🏁 Processo finalizado
```

---

# 🔐 Observações

Este projeto foi desenvolvido para automação de cobranças e contatos via WhatsApp Web.

Recomenda-se:

* utilizar delays humanos
* evitar grandes volumes de mensagens
* utilizar contas já aquecidas
* sempre respeitar boas práticas de comunicação

---

# 📌 Funcionalidades Futuras

* [ ] Barra de progresso
* [ ] Tema dark
* [ ] Exportação de logs
* [ ] Executável Linux/Windows
* [ ] Dashboard de métricas

---

