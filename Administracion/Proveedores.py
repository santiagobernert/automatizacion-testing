from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time, json

class Proveedores:
    campos = ["Domicilio","Razón social","Ciudad","Contacto","Alias","E-mail","E-mail opcional","Condición de pago","Comentario","Teléfono","Código postal","CUIT","Tipo de clave tributaria","País","Provincia", "Condición frente a IVA"]
    campos_obligatorios = ["Razón social", "E-mail", "CUIT", "Teléfono", "País"]

    @staticmethod
    def crear(driver, datos_modificados):
        datos={
        'Razón social': 'ejemplo',
        'Alias': 'alias',
        'CUIT': '21-22231223-4',
        'E-mail': 'e@g.com',
        'Teléfono': '12345',
        'País': 'Argentina'
        }
        if datos_modificados:
            for (k,v) in datos.items():
                datos[k] = v
        #entrar a pestaña Proveedores
        driver.find_element(By.XPATH, '//a[@href="/provider"]').click()
        #boton crear cliente
        driver.find_element(By.XPATH, '//button[text()="Crear nuevo"]').click()
        #mapear los datos para encontrar id y enviar valor
        for (campo, valor) in datos.items():
            if valor == 'blanco':
                  valor = ''
            if campo == "País":
                ac = ActionChains(driver)
                pais = driver.find_element(By.XPATH, '//label[text()="País"]')
                ac.move_to_element(pais).move_by_offset(1, 1).click().perform()
                driver.find_element(By.XPATH, f'//li[text()="{valor}"]').click()
            elif campo == "Condición de pago":
                    ac = ActionChains(driver)
                    driver.find_element(By.XPATH, '//div[contains(@class, "MuiSelect-select") and (contains(text(), "días") or contains(text(), "Otra"))]').click()
                    driver.find_element(By.XPATH, f'//li[text()="{valor}"]').click()
            else:
                id =  driver.find_element(By.XPATH, f'//label[text()="{campo}"]').get_attribute("for")
                driver.find_element(by=By.ID, value=id).send_keys(valor)
        #botón crear
        driver.find_element(By.XPATH, '//button[text()="Crear"]').click()
        time.sleep(1.5)
        for request in driver.requests:
            if request.method == 'POST' and 'providers' in request.url:
                respuesta = (request.url, request.method, request.response.status_code, str(request.response.body.decode("utf-8")))
                print(respuesta)
                return respuesta
        return '', '', '0', 'No se pudo crear, error en los campos'


    @staticmethod
    def editar(driver, datos={}):
        #entrar a pestaña Proveedores
        driver.find_element(By.XPATH, '//a[@href="/provider"]').click()
        #boton lapiz
        driver.find_element(By.XPATH, '//*[@aria-label="Editar"]').click()
        #editar campos con los datos recibidos
        if datos:
            for (campo, valor) in datos.items():
                #setear valor en blanco
                if valor == 'blanco':
                  valor = ''
                #antes de completar el CUIT, intentar con tipo de clave tributaria = Otra
                if campo == "CUIT":
                    try:
                        id =  driver.find_element(By.XPATH, f'//label[text()="OTHER"]').get_attribute("for")
                    except:
                        id =  driver.find_element(By.XPATH, f'//label[text()="CUIT"]').get_attribute("for")
                elif campo == "País":
                    ac = ActionChains(driver)
                    pais = driver.find_element(By.XPATH, '//label[text()="País"]')
                    ac.move_to_element(pais).move_by_offset(1, 1).click().perform()
                    driver.find_element(By.XPATH, f'//li[text()="{valor}"]').click()
                elif campo == "Condición de pago":
                    ac = ActionChains(driver)
                    driver.find_element(By.XPATH, '//div[contains(@class, "MuiSelect-select") and (contains(text(), "días") or contains(text(), "Otra"))]').click()
                    driver.find_element(By.XPATH, f'//li[text()="{valor}"]').click()
                #obtener id del input según su label
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
            id =  driver.find_element(By.XPATH, f'//label[text()="Alias"]').get_attribute("for")
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
        #entrar a pestaña Proveedores
        driver.find_element(By.XPATH, '//a[@href="/provider"]').click()
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
            for c in Proveedores.campos_obligatorios:
                campos[c] = ''
        else:
            for c in Proveedores.campos:
                campos[c] = ''
        return json.dumps(campos, ensure_ascii=False).replace('{', '{\n').replace('}', '\n}').replace(',',',\n')
                
