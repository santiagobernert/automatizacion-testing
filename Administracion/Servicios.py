from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time, json

class Servicios:
    campos = ["Código", "Concepto", "Definición", "Subcategoría", "Aplicable a", "Unidad de medida", "MSC charge code", "MEDLOG charge code", "MSC ARG charge code", "Comentario"]
    campos_obligatorios = ["Código", "Concepto", "Definición", "Subcategoría", "Aplicable a", "Unidad de medida", "MSC charge code", "MSC ARG charge code", "MEDLOG charge code"]

    @staticmethod
    def crear(driver, datos_modificados):
        datos={
        "Código": "aa11",
        "Concepto": "prueba",
        "Definición": "prueba de servicio",
        "Subcategoría": "Intermodal",
        "Aplicable a": "Mercadería",
        "Unidad de medida": "Camión",
        "MSC charge code": "abc",
        "MSC ARG charge code": "a12",
        "MEDLOG charge code": "abcd12",
        }
        if datos_modificados:
            for (k,v) in datos_modificados.items():
                datos[k] = v
        #desplegar el menu administracion
        driver.find_element(By.XPATH, '//span[text()="Administración"]').click() 
        #entrar a pestaña Servicios
        driver.find_element(By.XPATH, '//a[@href="/additional-services"]').click()
        #boton crear cliente
        driver.find_element(By.XPATH, '//button[text()="Crear nuevo"]').click()
        #mapear los datos para encontrar id y enviar valor
        for (campo, valor) in datos.items():
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
                ac.move_to_element(driver.find_element(By.XPATH, '//label[text()="Código"]')).move_by_offset(1, 1).click().perform()

            elif campo == "Unidad de medida":
                elemento = driver.find_element(By.XPATH, '//label[text()="Unidad de medida"]')
                ac.move_to_element(elemento).move_by_offset(1, 1).click().perform()
                driver.find_element(By.XPATH, f'//span[text()="{valor}"]').click()
                ac.move_to_element(driver.find_element(By.XPATH, '//label[text()="Código"]')).move_by_offset(1, 1).click().perform()
            
            else:
                id =  driver.find_element(By.XPATH, f'//label[text()="{campo}"]').get_attribute("for")
                driver.find_element(by=By.ID, value=id).send_keys(valor)
        #botón crear
        driver.find_element(By.XPATH, '//button[text()="Crear"]').click()
        time.sleep(1.5)
        for request in driver.requests:
            if request.method == 'POST' and 'additional-services' in request.url:
                respuesta = (request.url, request.method, request.response.status_code, str(request.response.body.decode("utf-8")))
                return respuesta
        return '', '', '0', 'No se pudo crear, error en los campos'


    @staticmethod
    def editar(driver, datos={}):
        #desplegar el menu administracion
        driver.find_element(By.XPATH, '//span[text()="Administración"]').click() 
        #entrar a pestaña Servicios
        driver.find_element(By.XPATH, '//a[@href="/additional-services"]').click()
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
    def eliminar(driver, datos={}):
        #desplegar el menu administracion
        driver.find_element(By.XPATH, '//span[text()="Administración"]').click() 
        #entrar a pestaña Servicios
        driver.find_element(By.XPATH, '//a[@href="/additional-services"]').click()
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
            for c in Servicios.campos_obligatorios:
                campos[c] = ''
        else:
            for c in Servicios.campos:
                campos[c] = ''
        return json.dumps(campos, ensure_ascii=False).replace('{', '{\n').replace('}', '\n}').replace(',',',\n')
                
