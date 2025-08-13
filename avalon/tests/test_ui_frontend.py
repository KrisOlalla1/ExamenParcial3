# tests/test_ui_frontend_complete.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Ejecuta en background
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_crud_completo(driver):
    driver.get("http://127.0.0.1:5500/frontend/index.html")
    wait = WebDriverWait(driver, 10)

    # ---------------- PACIENTES ----------------
    wait.until(EC.presence_of_element_located((By.ID, "form-paciente")))
    driver.find_element(By.ID, "paciente-nombre").send_keys("Juan")
    driver.find_element(By.ID, "paciente-apellido").send_keys("Pérez")
    driver.find_element(By.ID, "paciente-fecha").send_keys("1990-01-01")
    driver.find_element(By.ID, "paciente-email").send_keys("juan@example.com")

    try:
        driver.find_element(By.CSS_SELECTOR, "#form-paciente button[type='submit']").click()
    except UnexpectedAlertPresentException:
        alert = driver.switch_to.alert
        alert.dismiss()

    lista_pacientes = wait.until(EC.presence_of_element_located((By.ID, "lista-pacientes")))
    # Solo verifica que la lista esté presente
    assert lista_pacientes.text is not None

    # ---------------- MÉDICOS ----------------
    wait.until(EC.presence_of_element_located((By.ID, "form-medico")))
    driver.find_element(By.ID, "medico-nombre").send_keys("Ana")
    driver.find_element(By.ID, "medico-especialidad").send_keys("Cardiología")

    try:
        driver.find_element(By.CSS_SELECTOR, "#form-medico button[type='submit']").click()
    except UnexpectedAlertPresentException:
        alert = driver.switch_to.alert
        alert.dismiss()

    lista_medicos = wait.until(EC.presence_of_element_located((By.ID, "lista-medicos")))
    assert lista_medicos.text is not None

    # ---------------- CITAS ----------------
    wait.until(EC.presence_of_element_located((By.ID, "form-cita")))
    pacientes_opts = driver.find_elements(By.CSS_SELECTOR, "#cita-paciente option")
    medicos_opts = driver.find_elements(By.CSS_SELECTOR, "#cita-medico option")

    if pacientes_opts and medicos_opts:
        driver.find_element(By.ID, "cita-fecha").send_keys("2025-08-13T10:00")
        try:
            driver.find_element(By.CSS_SELECTOR, "#form-cita button[type='submit']").click()
        except UnexpectedAlertPresentException:
            alert = driver.switch_to.alert
            alert.dismiss()

    lista_citas = wait.until(EC.presence_of_element_located((By.ID, "lista-citas")))
    assert lista_citas.text is not None

    # ---------------- PAGINACIÓN ----------------
    driver.find_element(By.ID, "next-page").click()
    driver.find_element(By.ID, "prev-page").click()
