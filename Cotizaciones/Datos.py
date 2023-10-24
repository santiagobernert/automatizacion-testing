from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, datetime

class Datos:
    campos = ["Cliente","Freight Forwarder","Vendedor","Fecha Pedido","Validez Desde","Validez Hasta","Cliente facturable","Mercadería","Dirección","POL / POD","MTY PICK UP",]
    campos_obligatorios = ["Cliente","Freight Forwarder","Vendedor","Fecha Pedido","Validez Desde","Validez Hasta","Cliente facturable","Mercadería","Dirección","POL / POD","MTY PICK UP",]

    @staticmethod
    def crear(driver, datos_modificados):
        datos={
        "Cliente": "General",
        "Freight Forwarder": "General",
        "Vendedor": "Vendedor",
        "Fecha Pedido": f"{datetime.datetime.now().day}",
        "Validez Desde": f"{datetime.datetime.now().day}",
        "Validez Hasta": f"{datetime.datetime.now().day}",
        "Cliente facturable": "Aser SAA",
        "Mercadería": "Mercadería",
        "Dirección": "IMPORTACION",
        "POL / POD": "PUERTO MADRYN",
        "MTY PICK UP": "IMPORTACION",

        }
        if datos_modificados:
            for (k,v) in datos.items():
                datos[k] = v
        #desplegar el menu cotizaciones
        driver.find_element(By.XPATH, '//span[text()="Cotizaciones"]').click() 
        #entrar a pestaña Datos
        driver.find_element(By.XPATH, '//a[@href="/pricing"]').click()
        #boton crear cotizacion
        driver.find_element(By.XPATH, '//button[text()="Nueva cotización"]').click()
        #boton crear cotizacion
        driver.find_element(By.XPATH, '//button[text()="Crear"]').click()
        #entrar a datos del negocio
        driver.find_element(By.XPATH, '//p[text()="DATOS DEL NEGOCIO"]').click()
        #mapear los datos para encontrar id y enviar valor
        for (campo, valor) in datos.items():
            if valor == 'blanco':
                  valor = ''
            ac = ActionChains(driver)
            if campo == "Fecha Pedido":
                element = driver.find_elements(By.XPATH, '//button[@aria-label="Choose date"]')[0]
                ac.move_to_element_with_offset(element, 5, 5).click().perform()
                element = driver.find_element(By.XPATH, f'//button[text()="{valor}"]')
                ac.move_to_element(element).click().perform()
            elif campo == "Validez Desde":
                element = driver.find_elements(By.XPATH, '//button[@aria-label="Choose date"]')[1]
                ac.move_to_element(element).click().perform()
                time.sleep(0.5)
                element = driver.find_element(By.XPATH, f'//button[text()="{valor}"]')
                ac.move_to_element(element).click().perform()
            elif campo == "Validez Hasta":
                driver.implicitly_wait(3)
                element = driver.find_elements(By.XPATH, '//button[@aria-label="Choose date"]')[1]
                ac.move_to_element(element).click().perform()
                element = driver.find_element(By.XPATH, f'//button[text()="{valor}"]')
                print(element.get_attribute("data-timestamp"))
                driver.execute_script("arguments[0].setAttribute('aria-selected',arguments[1])",element, "true")
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='24']"))).click()
                # ac.move_to_element_with_offset(element, 2, 2).click().perform()
            
            
            elif campo == "Dirección":
                element = driver.find_element(By.XPATH, '//label[text()="Dirección"]')
                ac.move_to_element(element).click().perform()
                driver.find_element(By.XPATH, f'//li[text()="{valor}"]').click()
            elif campo == "POL / POD":
                element = driver.find_element(By.XPATH, '//label[text()="POL / POD"]')
                ac.move_to_element(element).click().perform()
                driver.implicitly_wait(2)
                element =  driver.find_element(By.XPATH, f'//li[text()="{valor}"]')
                ac.move_to_element(element).click().perform()
                driver.implicitly_wait(2)
            elif campo == "MTY PICK UP":
                element = driver.find_element(By.XPATH, '//label[text()="MTY PICK UP"]')
                ac.move_to_element(element).click().perform()
                ac.move_to_element(driver.find_element(By.XPATH, '//label[text()="MTY PICK UP"]')).click().perform()
                driver.implicitly_wait(2)
                driver.find_element(By.XPATH, f'//li[text()="{valor}"]').click()
            elif campo == "Cliente":
                id = driver.find_element(By.XPATH, f'//label[text()="{campo}"]').get_attribute("for")
                element = driver.find_element(by=By.ID, value=id)
                element.send_keys(valor)
                ac.move_to_element(element).click().perform()
                element.send_keys(Keys.DOWN)
                element.send_keys(Keys.RETURN)
                driver.implicitly_wait(2)
            elif campo == "Freight Forwarder":
                id = driver.find_element(By.XPATH, f'//label[text()="{campo}"]').get_attribute("for")
                element = driver.find_element(by=By.ID, value=id)
                element.send_keys(valor)
                ac.move_to_element(element).click().perform()
                element.send_keys(Keys.DOWN)
                element.send_keys(Keys.RETURN)
                driver.implicitly_wait(2)
            elif campo == "Cliente facturable":
                id = driver.find_element(By.XPATH, f'//label[text()="{campo}"]').get_attribute("for")
                element = driver.find_element(by=By.ID, value=id)
                element.send_keys(valor)
                ac.move_to_element(element).click().perform()
                element.send_keys(Keys.DOWN)
                element.send_keys(Keys.RETURN)
                driver.implicitly_wait(2)
            else:
                id =  driver.find_element(By.XPATH, f'//label[text()="{campo}"]').get_attribute("for")
                driver.find_element(by=By.ID, value=id).send_keys(valor)
        #botón crear
        driver.find_element(By.XPATH, '//button[text()="Guardar"]').click()
        time.sleep(1.5)
        for request in driver.requests:
            if request.method == 'POST' and 'quotations' in request.url:
                respuesta = (request.url, request.method, request.response.status_code, str(request.response.body.decode("utf-8")))
                return respuesta
        return '', '', '0', 'No se pudo crear, error en los campos'


    @staticmethod
    def editar(driver, datos={}):
        #desplegar el menu cotizaciones
        driver.find_element(By.XPATH, '//span[text()="Cotizaciones"]').click() 
        #entrar a pestaña Datos
        driver.find_element(By.XPATH, '//a[@href="/pricing"]').click()
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
        #desplegar el menu cotizaciones
        driver.find_element(By.XPATH, '//span[text()="Cotizaciones"]').click() 
        #entrar a pestaña Datos
        driver.find_element(By.XPATH, '//a[@href="/pricing"]').click()
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
            for c in Datos.campos_obligatorios:
                campos[c] = ''
        else:
            for c in Datos.campos:
                campos[c] = ''
        return json.dumps(campos, ensure_ascii=False).replace('{', '{\n').replace('}', '\n}').replace(',',',\n')
                
