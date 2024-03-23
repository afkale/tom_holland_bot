'''
Python bot for tim hortons.
'''
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bot.bot import Bot


class HortonsBot(Bot):
    codes = []

    def __init__(self):
        super().__init__()
        self.steps = [
            (self.go_next, ()),
            (self.press_option, ('Para comer en el local',),),
            (self.press_option, ('En el mostrador con un empleado',),),
            (self.press_option, ('Tanto comida como bebida',),),
            (self.press_option, ('Muy satisfecho',),),
            (self.fill_textarea, ('Venimos todos los dias los compis del' +
             ' curro y siempre nos tratan genial!!',),),
            (self.check_box, ()),
            (self.go_next, ()),
            (self.check_box, ()),
            (self.press_option, ('No',),),
            (self.press_option, ('Productos de desayuno',),),
            (self.press_option, ('Bebida caliente (por ejemplo, Latte,' +
                                 ' Cappuccino, etc.)',),),
            (self.press_option, ('English Muffin',),),
            (self.press_option, ('Latte',),),
            (self.press_option, ('Muy satisfecho',),),
            (self.check_box, ()),
            (self.check_box, ()),
            (self.press_option, ('Altamente probable',),),
            (self.fill_textarea, ('Pues porque lleva leche y cafe, todo lo' +
             ' que me gusta de un latte!!',),),
            (self.press_option, ('5 veces o más',),),
            (self.go_next, ()),
            (self.press_option, ('Prefiero no responder',),),
            (self.press_option, ('Prefiero no responder',),),
            (self.press_option, ('No',),),
        ]

    def get_code(self):
        element = self.wait.until(
            EC.visibility_of_element_located((By.ID, 'EndOfSurvey')))
        regex = r"\w{2}\d{5}"
        match = re.findall(regex, element.text)
        if match:
            return match[0]

    def go_next(self):
        self.click((By.ID, "NextButton"), force=True)

    def next(function):
        def wrapper(self, *args, **kwargs):
            result = function(self, *args, **kwargs)
            self.go_next()
            return result
        return wrapper

    @next
    def press_option(self, option_text):
        self.click((By.XPATH, f"//label[span[text()='{option_text}']]"))

    @next
    def check_box(self):
        self.click((By.XPATH, "//td[@class='c4   ']"),
                   ec=EC.presence_of_all_elements_located)

    @next
    def fill_textarea(self, text):
        self.send_keys((By.XPATH, "//div[@class='ChoiceStructure']//textarea"),
                       text, EC.element_to_be_clickable)

    @Bot.action
    def fill_out_survey(self, url):
        self.driver.get(url)
        for func, args in self.steps:
            func(*args)
        code = self.get_code()
        self.codes.append(code)
