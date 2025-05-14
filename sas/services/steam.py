from utils.faker import generate_user_data
from services.mail import TempMail
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome, ChromeOptions
import asyncio
import random

async def create_steam_account(region: str, use_proxy: bool = False) -> dict:
    # Генерация пользовательских данных
    user_data = generate_user_data(region)
    
    # Создание временной почты
    mail = TempMail()
    email_data = await mail.create_email()
    
    # Настройка Selenium
    options = ChromeOptions()
    options.add_argument("--headless")  # Фоновый режим
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    if use_proxy:
        # Заглушка для прокси (замените на BrightData)
        proxy = "http://username:password@brd.superproxy.io:22225"
        options.add_argument(f"--proxy-server={proxy}")
    
    driver = Chrome(options=options)
    try:
        # Открытие страницы регистрации Steam
        driver.get("https://store.steampowered.com/join")
        await asyncio.sleep(random.uniform(1, 3))  # Случайная задержка
        
        # Заполнение формы
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
        driver.find_element(By.ID, "email").send_keys(email_data["email"])
        driver.find_element(By.ID, "reenter_email").send_keys(email_data["email"])
        
        # Подтверждение возраста
        driver.find_element(By.ID, "i_agree_check").click()
        
        # Обход капчи (заглушка для 2Captcha)
        # site_key = driver.find_element(By.CLASS_NAME, "g-recaptcha").get_attribute("data-sitekey")
        # captcha_solution = await solve_captcha(site_key, driver.current_url)
        # driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML = '{captcha_solution}'")
        
        # Отправка формы
        driver.find_element(By.ID, "createAccountButton").click()
        
        # Ожидание верификационной ссылки
        verification_link = await mail.get_verification_link(email_data["account_id"])
        driver.get(verification_link)
        
        # Завершение регистрации (заглушка для имени и пароля)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "accountname")))
        driver.find_element(By.ID, "accountname").send_keys(user_data["username"])
        driver.find_element(By.ID, "password").send_keys(user_data["password"])
        driver.find_element(By.ID, "reenter_password").send_keys(user_data["password"])
        driver.find_element(By.ID, "createAccountButton").click()
        
        await asyncio.sleep(random.uniform(1, 3))
        
        return {
            "login": user_data["username"],
            "password": user_data["password"],
            "email": email_data["email"],
            "region": region
        }
    except Exception as e:
        raise Exception(f"Registration failed: {str(e)}")
    finally:
        driver.quit()