from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, json

class Clientes:
    campos = ["Dirección","Razón social","Ciudad","Contacto","Alias","E-mail","E-mail opcional","Código MSC-Link","Comentario","Teléfono","Código postal","CUIT","Tipo de clave tributaria","País","Provincia"]
    campos_obligatorios = ["Razón social", "E-mail", "CUIT", "Teléfono"]

    @staticmethod
    def crear(driver, datos_modificados):
        datos={
        'Razón social': 'ejemplo',
        'Alias': 'alias',
        'Clave tributaria (CUIT)': '21-22231223-4',
        'E-mail': 'e@g.com',
        'Teléfono': '12345',
        }
        if datos_modificados:
            for (k,v) in datos_modificados.items():
                datos[k] = v
        #desplegar el menu administracion
        driver.find_element(By.XPATH, '//span[text()="Administración"]').click() 
        #entrar a pestaña clientes
        driver.find_element(By.XPATH, '//a[@href="/customer"]').click()
        #boton crear cliente
        driver.find_element(By.XPATH, '//button[text()="Crear nuevo"]').click()
        #mapear los datos para encontrar id y enviar valor
        for (campo, valor) in datos.items():
            if valor == 'blanco':
                  valor = ''
            id =  driver.find_element(By.XPATH, f'//label[text()="{campo}"]').get_attribute("for")
            driver.find_element(by=By.ID, value=id).send_keys(valor)
        #botón crear
        driver.find_element(By.XPATH, '//button[text()="Crear"]').click()
        time.sleep(1.5)
        for request in driver.requests:
            if request.method == 'POST' and 'clients' in request.url:
                respuesta = (request.url, request.method, request.response.status_code, str(request.response.body.decode("utf-8")))
                return respuesta
        return '', '', '0', 'No se pudo crear, error en los campos'


    @staticmethod
    def editar(driver, datos={}):
        #desplegar el menu administracion
        driver.find_element(By.XPATH, '//span[text()="Administración"]').click() 
        #entrar a pestaña clientes
        driver.find_element(By.XPATH, '//a[@href="/customer"]').click()
        #boton lapiz
        driver.find_element(By.XPATH, '//*[@aria-label="Editar"]').click()
        #editar campos con los datos recibidos
        if datos:
            for (dato, valor) in datos.items():
                #setear valor en blanco
                if valor == 'blanco':
                  valor = ''
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
        #entrar a pestaña clientes
        driver.find_element(By.XPATH, '//a[@href="/customer"]').click()
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
            for c in Clientes.campos_obligatorios:
                campos[c] = ''
        else:
            for c in Clientes.campos:
                campos[c] = ''
        return json.dumps(campos, ensure_ascii=False).replace('{', '{\n').replace('}', '\n}').replace(',',',\n')
                
