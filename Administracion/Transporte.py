from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time, json

class Transporte:
    campos = ["Código", "Concepto", "Definición", "Subcategoría", "Aplicable a", "Unidad de medida", "MSC charge code", "MEDLOG charge code", "MSC ARG charge code", "Comentario"]
    campos_obligatorios = ["Código", "Concepto", "Definición", "Subcategoría", "Aplicable a", "Unidad de medida", "MSC charge code", "MSC ARG charge code", "MEDLOG charge code"]

    @staticmethod
    def crear(driver, datos_modificados={}):
        #entrar a pestaña clientes
        driver.find_element(By.XPATH, '//a[@href="/transport"]').click()
        #boton crear cliente
        driver.find_element(By.XPATH, '//button[text()="Agregar nuevo"]').click()
        #mapear los datos para encontrar id y enviar valor
        datos={
        "Código": "a111",
        "Concepto": "prueba",
        "Definición": "prueba de servicio",
        "Subcategoría": "Intermodal",
        "Aplicable a": "MERCADERIA",
        "Unidad de medida": "camion",
        "MSC charge code": "abc",
        "MSC Arg charge code": "a12",
        "Medlog charge code": "abcd12",
        }
        if datos_modificados:
            for (k,v) in datos.items():
                datos[k] = v
        for (campo, valor) in datos.items():
            if valor == 'blanco':
                    valor = ''
            if campo == "Subcategoría":
                ac = ActionChains(driver)
                pais = driver.find_element(By.XPATH, '//label[text()="Subcategoría"]')
                ac.move_to_element(pais).move_by_offset(1, 1).click().perform()
                driver.find_element(By.XPATH, f'//li[text()="{valor}"]').click()
            elif campo == "Aplicable a":
                ac = ActionChains(driver)
                pais = driver.find_element(By.XPATH, '//label[text()="Aplicable a"]')
                ac.move_to_element(pais).move_by_offset(1, 1).click().perform()
                driver.find_element(By.XPATH, f'//li[text()="{valor}"]').click()
            elif campo == "Unidad de medida":
                ac = ActionChains(driver)
                pais = driver.find_element(By.XPATH, '//label[text()="Unidad de medida"]')
                ac.move_to_element(pais).move_by_offset(1, 1).click().perform()
                driver.find_element(By.XPATH, f'//li[text()="{valor}"]').click()
            else:   
                id =  driver.find_element(By.XPATH, f'//label[text()="{campo}"]').get_attribute("for")
                driver.find_element(by=By.ID, value=id).send_keys(valor)
        #boton crear
        driver.find_element(By.XPATH, '//button[text()="Crear"]').click()
        time.sleep(1.5)
        for request in driver.requests:
            if request.method == 'POST' and 'quoted-transports' in request.url:
                respuesta = (request.url, request.method, request.response.status_code, str(request.response.body.decode("utf-8")))
                return respuesta
        return '', '', '0', 'No se pudo crear, error en los campos'

    @staticmethod
    def editar(driver, datos={}):
        #entrar a pestaña clientes
        driver.find_element(By.XPATH, '//a[@href="/transport"]').click()
        #boton lapiz
        driver.find_element(By.XPATH, '//*[@aria-label="Editar"]').click()
        #editar campos con los datos recibidos
        if datos:
            for (campo, valor) in datos.items():
                #setear valor en blanco
                if valor == 'blanco':
                  valor = ''
                ac = ActionChains(driver)
                if campo == "Aplicable a":
                    elemento = driver.find_element(By.XPATH, '//label[text()="Aplicable a"]')
                    ac.move_to_element(elemento).move_by_offset(1, 1).click().perform()
                    driver.find_element(By.XPATH, f'//li[text()="{valor}"]').click()
                
                elif campo == "Subcategoría":
                    elemento = driver.find_element(By.XPATH, '//label[text()="Subcategoría"]')
                    ac.move_to_element(elemento).move_by_offset(1, 1).click().perform()
                    driver.find_element(By.XPATH, f'//span[text()="{valor}"]').click()
                
                elif campo == "Unidad de medida":
                    elemento = driver.find_element(By.XPATH, '//label[text()="Unidad de medida"]')
                    ac.move_to_element(elemento).move_by_offset(1, 1).click().perform()
                    driver.find_element(By.XPATH, f'//span[text()="{valor}"]').click()
                
                else:
                    id =  driver.find_element(By.XPATH, f'//label[text()="{campo}"]').get_attribute("for")
                #borrar el texto existente
                element = driver.find_element(by=By.ID, value=id)
                value = element.get_attribute("value")
                element.send_keys(Keys.BACK_SPACE for _ in range(len(value)))
                driver.implicitly_wait(2)
                #escribir el nuevo texto
                element.send_keys(valor)
        #editar campo de ejemplo
        else:
            id =  driver.find_element(By.XPATH, f'//label[text()="Concepto"]').get_attribute("for")
            element = driver.find_element(By.ID, id)
            #borrar el texto existente
            value = element.get_attribute("value")
            element.send_keys(Keys.BACK_SPACE for _ in range(len(value)))
            driver.implicitly_wait(2)
            #escribir el nuevo texto
            element.send_keys("prueba")
        driver.find_element(By.XPATH, '//button[text()="Guardar"]').click()
        time.sleep(1.5)
        for request in driver.requests:
            if request.method == 'PUT':
                respuesta = (request.url, request.method, request.response.status_code, str(request.response.body.decode("utf-8")))
                return respuesta
        return '', '', '0', 'No se pudo editar, error en los campos'
    
    @staticmethod
    def eliminar(driver, datos):
        #entrar a pestaña clientes
        driver.find_element(By.XPATH, '//a[@href="/transport"]').click()
        #boton eliminar
        driver.find_element(By.XPATH, '//*[@aria-label="Eliminar"]').click()
        #confirmar
        driver.find_element(By.XPATH, '//button[text()="Eliminar"]').click()
        time.sleep(1.5)
        for request in driver.requests:
            if request.method == 'DELETE':
                respuesta = (request.url, request.method, request.response.status_code, str(request.response.body.decode("utf-8")))
                return respuesta
        return '', '', '0', 'No se pudo eliminar'
                
    @staticmethod
    def get_campos(all=False):
        campos = {}
        if not all:
            for c in Transporte.campos_obligatorios:
                campos[c] = ''
        else:
            for c in Transporte.campos:
                campos[c] = ''
        return json.dumps(campos, ensure_ascii=False).replace('{', '{\n').replace('}', '\n}').replace(',',',\n')
                

