import pandas as pd
import time
import random
from tkinter import Tk, Button, Label, filedialog, messagebox, StringVar, Radiobutton, Frame
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread
from google.oauth2.service_account import Credentials
import matplotlib.pyplot as plt

monitoramento = True
# === Mensagens automáticas ===
mensagem_1 = "Manutenção Preventiva Agendada!"
mensagem_2 = "Manutenção Preventiva Cancelada! Por favor, indique o melhor dia para a manutenção entrando em contato com o ChatBot:https://wa.me/5511940056645/"
mensagem_padrao = "Por favor, responda apenas com 'SIM' ou 'NÃO'."

# === Abrir conversa com número ===
def abrir_conversa_com_numero(driver, numero):
    numero = ''.join(filter(str.isdigit, numero))
    url = f"https://web.whatsapp.com/send?phone={numero}&text&app_absent=0"
    driver.get(url)

# === Obter nome do contato ===
def obter_nome_do_contato(driver):
    try:
        nome_elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='main']/header/div[2]/div[1]/div/div/div/span"))
        )
        return nome_elemento.text
    except Exception as e:
        return f"Erro ao obter nome: {e}"

# === Obter última mensagem recebida do contato ===
def obter_ultima_mensagem_recebida(driver):
    try:
        mensagens = driver.find_elements(By.XPATH, "//div[contains(@class,'message-in')]//span[@dir='ltr']")
        if mensagens:
            return mensagens[-1].text.strip()
        return ""
    except Exception as e:
        return f"Erro ao capturar mensagem: {e}"

# === Responder mensagens recebidas ===
def responder_conversa(driver, ultima_mensagens):
    try:
        mensagens = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]')
        if not mensagens:
            return ultima_mensagens

        ultima_msg = mensagens[-1].text.strip().lower()
        contato_nome = obter_nome_do_contato(driver)

        # Evita responder repetidamente a mesma mensagem
        if contato_nome in ultima_mensagens and ultima_mensagens[contato_nome] == ultima_msg:
            return ultima_mensagens

        ultima_mensagens[contato_nome] = ultima_msg

        partes_msg = ultima_msg.splitlines()
        mensagem_relevante = partes_msg[0]

        caixa_texto = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true" and @data-tab="10"]'))
        )

        if mensagem_relevante == "sim":
            resposta = mensagem_1
        elif mensagem_relevante == "não":
            resposta = mensagem_2
        else:
            resposta = mensagem_padrao

        caixa_texto.click()
        caixa_texto.send_keys(resposta)
        time.sleep(1)
        caixa_texto.send_keys(Keys.ENTER)
        print(f"Resposta enviada para {contato_nome}.")

        return ultima_mensagens

    except Exception as e:
        print(f"Erro ao responder: {e}")
        return ultima_mensagens

# === Monitorar mensagens após envio e atualizar dados ===
def verificar_status_mensagem(driver):
    try:
        # Localiza a div que contém o status da mensagem
        status_elemento = driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[9]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/span')
        return status_elemento.text.strip()  # Retorna o texto contido na div
    except Exception as e:
        print(f"Erro ao verificar o status da mensagem: {e}")
        return None

def monitorar_conversas(driver, dados_envio):
    print("Monitoramento iniciado. Pressione Ctrl+C para encerrar e salvar o log.")
    ultima_mensagens = {}
    try:
        global monitorando
        monitorando = True  
        while monitorando:

            # Detecta contatos com mensagens não lidas
            notificados = driver.find_elements(
                By.XPATH,
                '//div[@class="_ahlk"]/span[contains(@aria-label, "mensagem não lida") or contains(@aria-label, "mensagens não lidas")]'
            )
            if not notificados:
                time.sleep(5)
                continue

            for _ in notificados:
                try:
                    # Clica no contato com mensagem não lida
                    contato_elemento = _.find_element(By.XPATH, "./ancestor::div[contains(@class, '_ak8l')]")
                    contato_elemento.click()
                    time.sleep(3)

                    nome_contato = obter_nome_do_contato(driver)
                    resposta = obter_ultima_mensagem_recebida(driver)
                    
                    # Atualiza o dados_envio com resposta para esse contato
                    for registro in dados_envio:
                        if registro["Nome"] == nome_contato:
                            registro["Resposta Monitorada"] = resposta
                            
                            # Verifica o status da mensagem
                            status_mensagem = verificar_status_mensagem(driver)
                            if status_mensagem:
                                registro["Status Detalhado"] = status_mensagem  # Atualiza o status detalhado com o texto encontrado
                            else:
                                registro["Status Detalhado"] = "Status Indefinido"  # Caso não consiga obter o status
                            
                            break

                    
                    ultima_mensagens = responder_conversa(driver, ultima_mensagens)

                    time.sleep(2)
                except Exception as erro:
                    print(f"Erro ao processar contato no monitoramento: {erro}")
                    continue

            time.sleep(2)

    except KeyboardInterrupt:
        print("Monitoramento encerrado pelo usuário.")

def parar_monitoramento():
    global monitorando
    monitorando = False
    messagebox.showinfo("Parado", "Monitoramento interrompido pelo usuário.")


# === Salvar log somente após monitoramento ===
def salvar_log_excel(dados, nome_arquivo="log_envio.xlsx"):
    df_log = pd.DataFrame(dados)
    df_log.to_excel(nome_arquivo, index=False)
    print(f"Log salvo em {nome_arquivo}")

def interpretar_status_icone(driver):
    try:
        # Localiza a última de mensagem enviada
        elementos_mensagem = driver.find_elements(By.XPATH, '//div[contains(@class,"message-out")]')
        if not elementos_mensagem:
            return "Nenhum ícone encontrado"
        
        ultima_mensagem = elementos_mensagem[-1]
        
        # Procura o ícone de status dentro da mensagem
        icone = ultima_mensagem.find_element(By.XPATH, './/span[contains(@data-icon, "msg-")]')
        data_icon = icone.get_attribute("data-icon")

        if data_icon == "msg-check":
            return "Enviado"
        elif data_icon == "msg-dblcheck":
            return "Entregue"
        elif data_icon == "msg-dblcheck-ack":
            return "Lido"
        else:
            return f"Desconhecido ({data_icon})"
    except Exception as e:
        return f"Erro ao interpretar ícone: {e}"

# === Enviar mensagens da planilha ===
def enviar_mensagens(caminho_arquivo):
    try:
        excel = pd.ExcelFile(caminho_arquivo)
        planilhas = excel.sheet_names

        dados_envio = []

        for nome_planilha in planilhas:
            df = excel.parse(nome_planilha)
            df.columns = df.columns.str.strip()
            df = df.fillna("")

            print(f"Processando planilha: {nome_planilha}")

            driver = webdriver.Chrome()
            driver.get("https://web.whatsapp.com")
            messagebox.showinfo("Login", "Escaneie o QR Code do WhatsApp Web e clique em OK para continuar.")

            total = len(df)
            enviados = 0

            plt.ion()
            fig, ax = plt.subplots()
            barra = ax.bar(['Enviadas', 'Restantes'], [enviados, total - enviados], color=['green', 'red'])
            ax.set_ylim(0, total)
            ax.set_title("Progresso do Envio de Mensagens")
            ax.set_ylabel("Quantidade")
            plt.show()
            fig.canvas.manager.window.wm_attributes("-topmost", 1)

            for _, row in df.iterrows():
                conta = row['Cliente']
                contrato = row['Conta']
                dia = row['Data']
                tipo_manutencao = row.get('Tipo Manutenção', '').lower().strip()
                if isinstance(dia, pd.Timestamp):
                    dia = dia.strftime("%d/%m/%Y")

                numero = str(row['Numero']).strip()
                if not numero.startswith("+"):
                    numero = "+5511" + numero

                # Escolher modelo de mensagem com base na coluna "Tipo Manutenção"
                if "portão" in tipo_manutencao:
                    mensagem_modelo = (
                        "Prezados, informamos que está agendada a manutenção preventiva dos portões "
                        "referente à conta {contrato} - {conta}, no dia {dia}. Para confirmar digite SIM e para remarcar ou cancelar digite NÃO ou entre em contato: "
                        "https://wa.me/5511940056645/"
                    )
                else:
                    mensagem_modelo = (
                        "Prezados, informamos que está agendada a manutenção preventiva dos sistemas "
                        "referente à conta {contrato} - {conta}, no dia {dia}. Para confirmar digite SIM e para remarcar ou cancelar digite NÃO ou entre em contato: "
                        "https://wa.me/5511940056645/"
                    )

                mensagem = mensagem_modelo.format(conta=conta, contrato=contrato, dia=dia)
                print(f"Enviando para {numero}...")

                try:
                    abrir_conversa_com_numero(driver, numero)
                    time.sleep(2)
                    nome_contato = obter_nome_do_contato(driver)

                    caixa_msg = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
                    caixa_msg.click()
                    caixa_msg.send_keys(mensagem)
                    time.sleep(7)
                    caixa_msg.send_keys(Keys.ENTER)
                    print("Mensagem enviada.")

                    time.sleep(5)
                    status_mensagem = interpretar_status_icone(driver)

                    dados_envio.append({
                        "Nome": nome_contato,
                        "Número": numero,
                        "Mensagem": mensagem,
                        "Status": "Enviada",
                        "Resposta Monitorada": "",
                        "Status Detalhado": status_mensagem or "Status Indefinido"
                    })

                    enviados += 1
                    barra[0].set_height(enviados)
                    barra[1].set_height(total - enviados)
                    fig.canvas.draw()
                    fig.canvas.flush_events()

                    time.sleep(random.randint(10, 20))

                except Exception as e:
                    print(f"Erro com {numero}: {e}")
                    continue

            plt.ioff()
            plt.close()
            fig.canvas.manager.window.wm_attributes("-topmost", 0)

            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)

            monitorar_conversas(driver, dados_envio)
            salvar_log_excel_local(dados_envio, caminho_arquivo)
            import os
            os.system("python C:/Users/HAGANA/Desktop/sistema/os.py")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# === Selecionar planilha ===  
def selecionar_planilha():
    caminho = filedialog.askopenfilename(
        title="Selecione a planilha de clientes",
        filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
    )
    if caminho:
        enviar_mensagens(caminho)  


def salvar_log_excel_local(dados, caminho_arquivo):
    try:
        df_original = pd.read_excel(caminho_arquivo)
        df_original = df_original.fillna("")

        for i, row in df_original.iterrows():
            nome_planilha = row.get("Cliente", "").strip()
            for dado in dados:
                if dado["Nome"] == nome_planilha:
                    df_original.at[i, "Resposta Monitorada"] = dado.get("Resposta Monitorada", "")
                    df_original.at[i, "Status Detalhado"] = dado.get("Status Detalhado", "")
                    break

        df_original.to_excel(caminho_arquivo, index=False)
        print(f"Log salvo na planilha original: {caminho_arquivo}")

    except Exception as e:
        print(f"Erro ao salvar log local: {e}")


# === Interface Tkinter ===
janela = Tk()
janela.title("Envio de Mensagens - Haganá Tecnologia")
janela.geometry("500x350")
janela.configure(bg="#FFFFFF")


font_titulo = ("Arial", 16, "bold")
font_normal = ("Arial", 12)
cor_fundo = "#FFFFFF"
cor_destaque = "#ECD06F"
cor_texto = "#000000"

Label(janela, text="Envio de Mensagens", bg=cor_fundo, fg=cor_texto, font=font_titulo).pack(pady=(20, 10))
Label(janela, text="Selecione o tipo de manutenção:", bg=cor_fundo, fg=cor_texto, font=font_normal).pack()

frame_radio = Frame(janela, bg=cor_fundo)
frame_radio.pack(pady=10)


# Botão Selecionar Planilha
Button(
    janela, text="Selecionar Planilha", font=font_normal,
    bg=cor_destaque, fg="#000000", activebackground="#f5e8ac",
    command=selecionar_planilha, relief="flat", padx=20, pady=10,
    width=25
).pack(pady=30)

# Botão Parar Monitoramento
Button(
    janela, text="Parar Monitoramento", font=font_normal,
    bg="#FF6B6B", fg="#FFFFFF", activebackground="#ffb3b3",
    command=parar_monitoramento, relief="flat", padx=20, pady=10,
    width=25
).pack(pady=10)

janela.mainloop()
