from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from Administracion.Clientes import Clientes
from Administracion.Proveedores import Proveedores

driver_path = '/home/santiago/Descargas/Midas/chromedriver'
binary_path = '/usr/bin/brave-browser'

options = webdriver.ChromeOptions()
options.binary_location = binary_path
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)
driver.get("http://external.midasconsultores.com.ar:30080/login")

#completar formulario login
driver.find_element(by=By.ID, value=':r0:').send_keys('intermodalAdmin')
driver.find_element(by=By.ID, value=':r1:').send_keys('1nt3rm0d4lO%')
driver.find_element(by=By.CLASS_NAME, value='css-15gq054').click()

driver.implicitly_wait(2)

#abrir menu
driver.find_element(by=By.CLASS_NAME, value='css-13gjbs7').click()

#desplegar el menu administracion
driver.find_element(by=By.CLASS_NAME, value='css-xjrkim').click()

datos = {
    "Alias": "huhuaksd"
}
Proveedores.crear(driver)