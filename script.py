from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

driver_path = '/home/santiago/Descargas/Midas/chromedriver'
binary_path = '/usr/bin/brave-browser'

options = webdriver.ChromeOptions()
options.binary_location = binary_path

driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)
driver.get("http://external.midasconsultores.com.ar:30080/customer")

#completar formulario login
driver.find_element(by=By.ID, value=':r0:').send_keys('intermodalAdmin')
driver.find_element(by=By.ID, value=':r1:').send_keys('1nt3rm0d4lO%')
driver.find_element(by=By.CLASS_NAME, value='css-15gq054').click()

driver.implicitly_wait(2)

#abrir menu
driver.find_element(by=By.CLASS_NAME, value='css-13gjbs7').click()

#desplegar a administracion
driver.find_element(by=By.CLASS_NAME, value='css-xjrkim').click()

driver.implicitly_wait(2)

#entrar a pestaña clientes
driver.find_element(By.XPATH, '//a[@href="/customer"]').click()

driver.quit()

