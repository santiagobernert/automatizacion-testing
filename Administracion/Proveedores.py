from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time 

class Proveedores:
    campos = ["address","approved	","business_name","city	","contact	","deleted	","enrolled_in_gross_income	","fantasy_name	","iva_condition	","mail1	","mail2	","msc_code	","observations	","phone_number	","postal_code	","role	","tax_identification_number	","tax_identification_type	","country_id	","province_id	","include_in_tariff"]
    campos_obligatorios = ["approved", "business_name", "mail1", "tax_identification_type", "tax_identification_number"]

    @staticmethod
    def crear(driver, datos={}):
        #entrar a pestaña proveedores
        driver.find_element(By.XPATH, '//a[@href="/provider"]').click()
        #boton crear cliente
        driver.find_element(By.XPATH, '//button[text()="Crear nuevo"]').click()
        #mapear los datos para encontrar id y enviar valor
        if datos:
            for (campo, valor) in datos.items():
                id =  driver.find_element(By.XPATH, f'//label[text()="{campo}"]').get_attribute("for")
                driver.find_element(by=By.ID, value=id).send_keys(valor)
        else:
        #completar con datos de ejemplo
            driver.find_element(by=By.ID, value=':rn:').send_keys('ejemplo')
            driver.find_element(by=By.ID, value=':ro:').send_keys('alias')
            driver.find_element(by=By.ID, value=':rp:').send_keys('21-22231223-4')
            driver.find_element(by=By.ID, value=':rq:').send_keys('e@g.com')
            driver.find_element(by=By.ID, value=':rs:').send_keys('12345')
            pais = driver.find_element(By.XPATH, '//label[text()="País"]')
            ac = ActionChains(driver)
            ac.move_to_element(pais).move_by_offset(1, 1).click().perform()
            driver.find_element(By.XPATH, '//li[text()="Argentina"]').click()
            cdp = driver.find_element(By.XPATH, '//label[text()="Condición de pago"]')
            ac.move_to_element(cdp).move_by_offset(1, 1).click().perform()
            driver.find_element(By.XPATH, '//li[@data-value="CONDITION_30"]').click()

        #boton crear
        driver.find_element(By.XPATH, '//button[text()="Crear"]').click()

    @staticmethod
    def editar(driver, datos={}):
        #entrar a pestaña proveedores
        driver.find_element(By.XPATH, '//a[@href="/provider"]').click()
        #boton lapiz
        driver.find_element(By.XPATH, '//*[@aria-label="Editar"]').click()
        time.sleep(1)
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
                elif dato == "País":
                    ac = ActionChains(driver)
                    pais = driver.find_element(By.XPATH, '//label[text()="País"]')
                    ac.move_to_element(pais).move_by_offset(1, 1).click().perform()
                    driver.find_element(By.XPATH, f'//li[text()="{valor}"]').click()
                elif dato == "Condición de pago":
                    ac = ActionChains(driver)
                    driver.find_element(By.XPATH, '//div[contains(@class, "MuiSelect-select") and (contains(text(), "días") or contains(text(), "Otra"))]').click()
                    driver.find_element(By.XPATH, f'//li[text()="{valor}"]').click()
                else:
                    print(dato, valor)
                    id =  driver.find_element(By.XPATH, f'//label[text()="{dato}"]').get_attribute("for")
                    #borrar el texto existente
                    element = driver.find_element(by=By.ID, value=id)
                    value = element.get_attribute("value")
                    element.send_keys(Keys.BACK_SPACE for _ in range(len(value)))
                    #escribir el nuevo texto
                    element.send_keys(valor)
        #editar campo de ejemplo
        else:
            element = driver.find_element(by=By.ID, value=':ro:')
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
        #entrar a pestaña proveedores
        driver.find_element(By.XPATH, '//a[@href="/provider"]').click()
        #boton eliminar
        driver.find_element(By.XPATH, '//*[@aria-label="Eliminar"]').click()
        #confirmar
        driver.find_element(By.XPATH, '//button[text()="Eliminar"]').click()
        for request in driver.requests:
            if request.response:
                print(request.url)
                print(request.response.status_code)
                print(request.response.body)
