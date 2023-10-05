from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 


driver_path = '/home/santiago/Descargas/Midas/chromedriver'
binary_path = '/usr/bin/brave-browser'

options = webdriver.ChromeOptions()
options.binary_location = binary_path
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)
driver.get("http://external.midasconsultores.com.ar:30080/customer")

#completar formulario login
driver.find_element(by=By.ID, value=':r0:').send_keys('intermodalAdmin')
driver.find_element(by=By.ID, value=':r1:').send_keys('1nt3rm0d4lO%')
driver.find_element(by=By.CLASS_NAME, value='css-15gq054').click()

driver.implicitly_wait(2)

#abrir menu
driver.find_element(by=By.CLASS_NAME, value='css-13gjbs7').click()

#desplegar el menu administracion
driver.find_element(by=By.CLASS_NAME, value='css-xjrkim').click()

driver.implicitly_wait(2)

#entrar a pestaña clientes
driver.find_element(By.XPATH, '//a[@href="/customer"]').click()


def agregar_cliente(datos={}):
    #boton crear cliente
    driver.find_element(By.XPATH, '//button[text()="Crear nuevo"]').click()
    driver.implicitly_wait(2)
    #llenar formulario con los datos recibidos
    if datos:
        for (campo, valor) in datos.items():
            id =  driver.find_element(By.XPATH, f'//label[text()="{campo}"]').get_attribute("for")
            driver.find_element(by=By.ID, value=id).send_keys(valor)
    else:
    #llenar formulario
        driver.find_element(by=By.ID, value=':r13:').send_keys('ejemplo')
        driver.find_element(by=By.ID, value=':r14:').send_keys('alias')
        driver.find_element(by=By.ID, value=':r15:').send_keys('21-22231223-4')
        driver.find_element(by=By.ID, value=':r16:').send_keys('e@g.com')
        driver.find_element(by=By.ID, value=':r18:').send_keys('12345')
    #boton crear
    driver.find_element(By.XPATH, '//button[text()="Crear"]').click()

def editar_cliente(campo="", valor="editar", datos={}):
    #boton lapiz
    driver.find_element(By.XPATH, '//*[@aria-label="Editar"]').click()
    #editar campos
    if datos:
        for (dato, valor) in datos.items():
            print(dato)
            if dato == "CUIT":
                id =  driver.find_element(By.XPATH, f'//label[text()="OTHER"]').get_attribute("for")
            else:
                id =  driver.find_element(By.XPATH, f'//label[text()="{dato}"]').get_attribute("for")
            element = driver.find_element(by=By.ID, value=id)
            value = element.get_attribute("value")
            element.send_keys(Keys.BACK_SPACE for k in range(len(value)))
            element.send_keys(valor)
    else:
        if campo:
            id =  driver.find_element(By.XPATH, f'//label[text()="{campo}"]').get_attribute("for")
            element = driver.find_element(by=By.ID, value=id)
        else:
            element = driver.find_element(by=By.ID, value=':r14:')

        value = element.get_attribute("value")
        element.send_keys(Keys.BACK_SPACE for k in range(len(value)))
        time.sleep(1)
        element.send_keys(valor)
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[text()="Guardar"]').click()


def eliminar_cliente():
    #boton eliminar
    driver.find_element(By.XPATH, '//*[@aria-label="Eliminar"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[text()="Eliminar"]').click()


datos = {
    "Razón social": "rs1",
    "Alias": "alias1",
    "CUIT": "asdjs",
    "E-mail": "g@g.g",
    "Teléfono": "+54 911 1234 5671",
}
eliminar_cliente()

driver.quit()

