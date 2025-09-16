import time
import random
from datetime import datetime
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Credenciais de login (substitua pelos valores reais)
USERNAME = "ricardo.france@funcamp.unicamp.br"
PASSWORD = "Rija#1948"

# URL da página de marcação de ponto
CLOCKING_URL = "https://platform.senior.com.br/senior-x/#/Gest%C3%A3o%20de%20Pessoas%20%7C%20HCM/1/res:%2F%2Fsenior.com.br%2Fhcm%2Fpontomobile%2FclockingEvent?category=frame&link=https:%2F%2Fplatform.senior.com.br%2Fhcm-pontomobile%2Fhcm%2Fpontomobile%2F%23%2Fclocking-event&withCredentials=true&r=4"

def login_and_clock_in():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Tentando logar e marcar o ponto com Selenium...")
    
    # Configuração do WebDriver (exemplo com Chrome)
    # Certifique-se de que o chromedriver está no seu PATH ou especifique o caminho
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Executar em modo headless (sem interface gráfica)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path="C:\Program Files\chrome-win64\chrome.exe", options=options)

    try:
        # Navegar para a página de login
        driver.get("https://platform.senior.com.br/login/")
        
        # Esperar o campo de usuário e senha aparecerem
        wait = WebDriverWait(driver, 10)
        user_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        pass_field = driver.find_element(By.ID, "password")

        # Preencher credenciais e submeter
        user_field.send_keys(USERNAME)
        pass_field.send_keys(PASSWORD)
        driver.find_element(By.TAG_NAME, "form").submit()

        # Esperar o carregamento da página de marcação e o botão aparecer
        wait.until(EC.url_to_be(CLOCKING_URL))
        clock_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Registrar Ponto")]')))

        # Usar ActionChains para clicar e segurar o botão
        actions = ActionChains(driver)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Pressionando o botão 'Registrar Ponto'...")
        actions.click_and_hold(clock_in_button).perform()
        time.sleep(5)
        actions.release(clock_in_button).perform()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Botão 'Registrar Ponto' liberado.")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ponto registrado com sucesso!")

    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ocorreu um erro durante a marcação de ponto: {e}")
    finally:
        driver.quit()

def mark_point_scheduled(fixed_hour, min_minute, max_minute):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Aviso: A verificação de feriados não está implementada neste script. O agendamento CRON exclui apenas sábados e domingos.")

    # Gerar um minuto e segundo aleatórios dentro do intervalo
    random_minute = random.randint(min_minute, max_minute)
    random_second = random.randint(0, 59)

    now = datetime.now()
    target_time = now.replace(hour=fixed_hour, minute=random_minute, second=random_second, microsecond=0)

    # Se o tempo alvo já passou para hoje, agendar para amanhã (isso não deve acontecer com cron jobs bem configurados)
    if target_time < now:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Aviso: O horário alvo ({target_time.strftime('%H:%M:%S')}) já passou para hoje. Não será realizada a marcação.")
        return

    delay_seconds = (target_time - now).total_seconds()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Agendando marcação para {target_time.strftime('%H:%M:%S')}. Esperando {delay_seconds:.2f} segundos.")
    time.sleep(delay_seconds)
    login_and_clock_in()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Script de marcação de ponto concluído.")


