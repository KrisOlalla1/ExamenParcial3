import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_crud_paciente(driver):
    driver.get("http://127.0.0.1:5500/avalon/index.html")
    wait = WebDriverWait(driver, 30)

    # Esperar que Avalon esté definido y vmodel 'app' exista
    wait.until(lambda d: d.execute_script(
        "return typeof avalon !== 'undefined' && avalon.vmodels.app !== undefined"
    ))

    # Esperar que el input de nombre del paciente esté listo y ligado a vmodel
    wait.until(lambda d: d.execute_script(
        "var inp = document.querySelector('input[ms-duplex=\"nuevoPaciente.nombre\"]');"
        "return inp && inp.msData && inp.msData.duplex === 'nuevoPaciente.nombre';"
    ))

    # Ahora sí podemos interactuar con los inputs
    nombre_input = driver.find_element(By.CSS_SELECTOR, 'input[ms-duplex="nuevoPaciente.nombre"]')
    apellido_input = driver.find_element(By.CSS_SELECTOR, 'input[ms-duplex="nuevoPaciente.apellido"]')
    fecha_input = driver.find_element(By.CSS_SELECTOR, 'input[ms-duplex="nuevoPaciente.fecha_nacimiento"]')
    email_input = driver.find_element(By.CSS_SELECTOR, 'input[ms-duplex="nuevoPaciente.email"]')

    nombre_input.send_keys("Kris")
    apellido_input.send_keys("Olalla")
    fecha_input.send_keys("1995-08-13")
    email_input.send_keys("kris@example.com")

    driver.find_element(By.CSS_SELECTOR, 'form[ms-submit="agregarPaciente"] button[type="submit"]').click()

    # Esperar que el paciente aparezca en la lista
    wait.until(lambda d: d.execute_script(
        "return Array.from(document.querySelectorAll('ul li')).some(li => li.textContent.includes('Kris Olalla'));"
    ))

    paciente_li = driver.find_element(By.XPATH, "//ul/li[contains(text(),'Kris Olalla')]")
    assert "Kris" in paciente_li.text
    assert "Olalla" in paciente_li.text
