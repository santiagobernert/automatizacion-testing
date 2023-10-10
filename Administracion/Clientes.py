from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time 

class Clientes:
    campos = ["address","approved	","business_name","city	","contact	","deleted	","enrolled_in_gross_income	","fantasy_name	","iva_condition	","mail1	","mail2	","msc_code	","observations	","phone_number	","postal_code	","role	","tax_identification_number	","tax_identification_type	","country_id	","province_id	","include_in_tariff"]
    campos_obligatorios = ["approved", "business_name", "mail1", "tax_identification_type", "tax_identification_number"]

    @staticmethod
    def crear(driver, datos={}):
        #entrar a pestaña clientes
        driver.find_element(By.XPATH, '//a[@href="/customer"]').click()
        #boton crear cliente
        driver.find_element(By.XPATH, '//button[text()="Crear nuevo"]').click()
        #mapear los datos para encontrar id y enviar valor
        if datos:
            for (campo, valor) in datos.items():
                id =  driver.find_element(By.XPATH, f'//label[text()="{campo}"]').get_attribute("for")
                driver.find_element(by=By.ID, value=id).send_keys(valor)
        else:
        #completar con datos de ejemplo
            driver.find_element(by=By.ID, value=':r15:').send_keys('ejemplo')
            driver.find_element(by=By.ID, value=':r16:').send_keys('alias')
            driver.find_element(by=By.ID, value=':r17:').send_keys('21-22231223-4')
            driver.find_element(by=By.ID, value=':r18:').send_keys('e@g.com')
            driver.find_element(by=By.ID, value=':r1a:').send_keys('12345')
        #boton crear
        driver.find_element(By.XPATH, '//button[text()="Crear"]').click()

    @staticmethod
    def editar(driver, datos={}):
        #entrar a pestaña clientes
        driver.find_element(By.XPATH, '//a[@href="/customer"]').click()
        #boton lapiz
        driver.find_element(By.XPATH, '//*[@aria-label="Editar"]').click()
        #editar campos con los datos recibidos
        if datos:
            for (dato, valor) in datos.items():
                #antes de completar el CUIT, intentar con tipo de clave tributaria = Otra
                if dato == "CUIT":
                    try:
                        id =  driver.find_element(By.XPATH, f'//label[text()="OTHER"]').get_attribute("for")
                    except:
                        id =  driver.find_element(By.XPATH, f'//label[text()="CUIT"]').get_attribute("for")
                #obtener id del input según su label
                else:
                    id =  driver.find_element(By.XPATH, f'//label[text()="{dato}"]').get_attribute("for")
                #borrar el texto existente
                element = driver.find_element(by=By.ID, value=id)
                value = element.get_attribute("value")
                element.send_keys(Keys.BACK_SPACE for _ in range(len(value)))
                #escribir el nuevo texto
                element.send_keys(valor)
        #editar campo de ejemplo
        else:
            element = driver.find_element(by=By.ID, value=':r14:')
            #borrar el texto existente
            value = element.get_attribute("value")
            element.send_keys(Keys.BACK_SPACE for _ in range(len(value)))
            time.sleep(1)
            #escribir el nuevo texto
            element.send_keys("prueba")
        time.sleep(1)
        driver.find_element(By.XPATH, '//button[text()="Guardar"]').click()

    @staticmethod
    def eliminar(driver):
        #entrar a pestaña clientes
        driver.find_element(By.XPATH, '//a[@href="/customer"]').click()
        #boton eliminar
        driver.find_element(By.XPATH, '//*[@aria-label="Eliminar"]').click()
        #time.sleep(1)
        #confirmar
        driver.find_element(By.XPATH, '//button[text()="Eliminar"]').click()
        for request in driver.requests:
            if request.response and request.response.status_code > 200:
                print(request.url)
                print(request.method)
                print(request.response.status_code)
                print(request.response.body.splitlines())
                
