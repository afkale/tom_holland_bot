import threading

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

thread_local = threading.local()


class Bot:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")

    @property
    def driver(self):
        return thread_local.driver

    @property
    def wait(self):
        return thread_local.wait

    def click(self, mask: tuple, force=False, ec=EC.element_to_be_clickable):
        result = self.wait.until(ec(mask))
        if isinstance(result, list):
            [self._click_element(force, element) for element in result]
        else:
            self._click_element(force, result)

    def _click_element(self, force, element):
        try:
            while element:
                element.click()
                if not force:
                    break
        except Exception:
            pass

    def send_keys(self, mask: tuple, text, ec=EC.visibility_of):
        element = self.wait.until(ec(mask))
        element.send_keys(text)

    def action(function):
        def wrapper(self, *args, **kwargs):
            def starts(*args, **kwargs):
                thread_local.driver = webdriver.Chrome(options=self.options)
                thread_local.wait = WebDriverWait(thread_local.driver, 3000)
                function(self, *args, **kwargs)
                thread_local.driver.quit()

            thread = threading.Thread(target=starts, args=args, kwargs=kwargs)
            thread.start()

        return wrapper
