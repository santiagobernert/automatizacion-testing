from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, datetime

class CompraVenta:
    campos = ["ROE", "POL / POD", "Transporte", "COSTO", "AJUSTE_C", "IMPUESTO", "Proveedor", "Factura", "Destinatario", "PROFIT", "AJUSTE_V"]
    campos_obligatorios = ["ROE", "POL / POD", "Transporte", "COSTO", "AJUSTE_C", "IMPUESTO", "Proveedor", "Factura", "Destinatario", "PROFIT", "AJUSTE_V"]

    @staticmethod
    def crear(driver, datos_modificados):
        datos={
            "ROE": "2",
            "POL / POD": "PUERTO MADRYN",
            "Transporte": "CAMION ROUND TRIP EXPORTACION",
            "COSTO": "1500USD",
            "AJUSTE_C": "5PCT",
            "IMPUESTO": "15PCT",
            "Proveedor": "asd",
            "Factura": "B",
            "Destinatario": "Medlog",
            "PROFIT": "20PCT",
            "AJUSTE_V": "5PCT",
        }
        if datos_modificados:
            for (k,v) in datos_modificados.items():
                datos[k] = v
        #desplegar el menu cotizaciones
        driver.find_element(By.XPATH, '//span[text()="Cotizaciones"]').click() 
        #entrar a pestaña Compra Venta
        driver.find_element(By.XPATH, '//a[@href="/pricing"]').click()
        #boton crear cotizacion
        driver.find_element(By.XPATH, '//button[text()="Nueva cotización"]').click()
        #boton crear cotizacion
        driver.find_element(By.XPATH, '//button[text()="Crear"]').click()
        #entrar a datos del negocio
        driver.find_element(By.XPATH, '//p[text()="COMPRA / VENTA"]').click()
        #mapear los datos para encontrar id y enviar valor
        for (campo, valor) in datos.items():
            if valor == 'blanco':
                  valor = ''
            ac = ActionChains(driver)
            if any(x in campo for x in ["POL / POD", "Transporte", "Proveedor", "Factura", "Destinatario"]):
                element = driver.find_elements(By.XPATH, f'//label[text()="{campo}"]')[-1]
                print(element)
                ac.move_to_element(element).click().perform()
                driver.implicitly_wait(2)
                element =  driver.find_element(By.XPATH, f'//li[text()="{valor}"]')
                ac.move_to_element(element).click().perform()
                driver.implicitly_wait(2)
            elif any(x in campo for x in ["COSTO", "AJUSTE", "IMPUESTO", "PROFIT"]):
                div = driver.find_element(By.XPATH, f'//div[@class="MuiBox-root css-1xhj18k"]/p[text()={campo}]')
                div.find_element(By.XPATH, f'//div[@class="MuiToggleButtonGroup-root css-1tqh9qk"]/button[text()={valor[-3:] if valor[-3:] != "PCT" else "PERCENTAGE"}]').click()
            else:
                id =  driver.find_element(By.XPATH, f'//label[text()="{campo}"]').get_attribute("for")
                driver.find_element(by=By.ID, value=id).send_keys(valor)
        #botón crear
        driver.find_element(By.XPATH, '//button[text()="Guardar"]').click()
        time.sleep(1.5)
        for request in driver.requests:
            if request.method == 'POST' and 'buy-sell' in request.url:
                respuesta = (request.url, request.method, request.response.status_code, str(request.response.body.decode("utf-8")))
                return respuesta
        return '', '', '0', 'No se pudo crear, error en los campos'


    @staticmethod
    def editar(driver, datos={}):
        #desplegar el menu cotizaciones
        driver.find_element(By.XPATH, '//span[text()="Cotizaciones"]').click() 
        #entrar a pestaña Compra Venta
        driver.find_element(By.XPATH, '//a[@href="/pricing"]').click()
        #boton lapiz
        driver.find_element(By.XPATH, '//*[@aria-label="Editar"]').click()
        #entrar a datos del negocio
        driver.find_element(By.XPATH, '//p[text()="COMPRA / VENTA"]').click()
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
                id =  driver.find_element(By.XPATH, f'//label[text()="Vendedor"]').get_attribute("for")
                driver.find_element(by=By.ID, value=id).send_keys("Prueba")
        #botón crear
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
        #entrar a pestaña Compra Venta
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
            for c in CompraVenta.campos_obligatorios:
                campos[c] = ''
        else:
            for c in CompraVenta.campos:
                campos[c] = ''
        return json.dumps(campos, ensure_ascii=False).replace('{', '{\n').replace('}', '\n}').replace(',',',\n')
                
