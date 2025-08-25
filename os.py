import gspread
import traceback
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def esperar_elemento_e_preencher(driver, by, seletor, texto):
    elemento = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, seletor)))
    elemento.click()
    elemento.clear()
    elemento.send_keys(texto)
    return elemento

def esperar_e_clicar(driver, by, seletor):
    elemento = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, seletor)))
    elemento.click()

def agendar(driver, url, usuario, senha, data, descricao, tecnico):
    try:
        url = url.strip().strip("'").strip('"')
        assert url.startswith("http"), f"URL inválida: {url}"
        print(f"\n[DEBUG] Tentando abrir URL: {url}")
        driver.get(url)

        # Espera a página carregar
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(3)

        try:
            username_field = driver.find_element(By.XPATH, '//*[@id="username"]')
            password_field = driver.find_element(By.XPATH, '//*[@id="password"]')

            username_field.clear()
            username_field.send_keys(usuario)
            password_field.clear()
            password_field.send_keys(senha)

            login_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div[1]/div/div[2]/div/form/div[3]/div/div/button')
            login_button.click()
            print("✅ Login enviado")

            time.sleep(5)

            esperar_elemento_e_preencher(driver, By.XPATH, '//*[@id="executionDate"]', data).send_keys(Keys.RETURN)

            esperar_e_clicar(driver, By.XPATH, '//*[@id="type"]')
            esperar_e_clicar(driver, By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[1]/div/div/div[4]/div/form/div[1]/div[3]/div[2]/div[2]/div[2]/div/div[1]/select/option[11]')

            esperar_e_clicar(driver, By.XPATH, '//*[@id="requesterId"]')
            esperar_e_clicar(driver, By.XPATH, '//*[@id="requesterId"]/option[15]')

            esperar_e_clicar(driver, By.XPATH, '//*[@id="defectId"]')
            esperar_e_clicar(driver, By.XPATH, '//*[@id="defectId"]/option[271]')

            tecnicos_map = {
                "ATP-SP-03-Eberson": "//*[@id='personExecutantId']/option[47]",
                "ROGER": "//*[@id='personExecutantId']/option[48]",
                "IGOR": "//*[@id='personExecutantId']/option[49]",
                "VINICIUS": "//*[@id='personExecutantId']/option[49]",
                "BLANC": "//*[@id='personExecutantId']/option[22]",
                "MULLER":"//*[@id='personExecutantId']/option[233]"
            }

            esperar_e_clicar(driver, By.XPATH, '//*[@id="personExecutantId"]')
            xpath_tecnico = tecnicos_map.get(tecnico)
            if xpath_tecnico:
                esperar_e_clicar(driver, By.XPATH, xpath_tecnico)
            else:
                print(f"❌ Técnico '{tecnico}' não mapeado.")
                return

            esperar_elemento_e_preencher(driver, By.XPATH, '//*[@id="description"]', descricao)

            esperar_e_clicar(driver, By.XPATH, '//*[@id="root"]/div/div[2]/div/div[1]/div/div/div[4]/div/form/div[2]/div[2]/div[2]/button[2]')
            print("✅ Agendamento salvo com sucesso.")

            time.sleep(2)

        except Exception as e:
            print(f"❌ Erro durante o preenchimento: {str(e)}")
            traceback.print_exc()

    except Exception as e:
        print(f"❌ Erro ao abrir URL ou durante o processo: {str(e)}")
        traceback.print_exc()
        try:
            driver.save_screenshot(f"erro_{url.replace('https://', '').replace('/', '_')}.png")
            print("✅ Screenshot salva para análise.")
        except:
            pass

def ler_dados_planilha_local(caminho_arquivo_excel):
    try:
        print(f"Lendo arquivo: {caminho_arquivo_excel}")
        df = pd.read_excel(caminho_arquivo_excel)  # remove o argumento 'sheet_name'
        print(f"Colunas encontradas na planilha: {df.columns.tolist()}")
        print(f"Número de linhas: {len(df)}")
        print(f"Primeira linha de dados: {df.iloc[0].to_dict()}")
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Erro ao ler planilha local: {e}")
        return []


def main():
    caminho_arquivo_excel = "C:/Users/HAGANA/Desktop/sistema/Manuntenção-Preventiva.xlsx"
    usuario = "seu_login"
    senha = "sua_senha"

    dados = ler_dados_planilha_local(caminho_arquivo_excel)
    if not dados:
        print("❌ Nenhum dado foi lido.")
        return

    colunas_necessarias = ["Resposta Monitorada", "URL", "Data", "Técnico"]
    if not all(col in dados[0] for col in colunas_necessarias):
        print("❌ Colunas necessárias ausentes.")
        return

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        for i, row in enumerate(dados):
            resposta = str(row.get("Resposta Monitorada", "")).strip().upper()
            url = str(row.get("URL", "")).strip().strip("'").strip('"')
            data_base = str(row.get("Data", "")).strip()
            tecnico = str(row.get("Técnico", "")).strip()
            descricao = "Manutenção Preventiva realizada automaticamente"

            if resposta == "SIM" and url and data_base and tecnico:
                try:
                    dt = pd.to_datetime(data_base)
                    hora = f"00:{str(i+1).zfill(2)}"
                    data = dt.strftime(f"%d/%m/%Y {hora}")
                except Exception as e:
                    print(f"❌ Erro ao formatar data: {data_base} -> {e}")
                    continue

                agendar(driver, url, usuario, senha, data, descricao, tecnico)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
