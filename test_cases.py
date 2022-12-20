import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Firefox(executable_path="/Users/nikita_nik/Desktop/Firefoxtest/geckodriver")
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('a5tapenkonik@yandex.ru')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('12345')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
   my_pets = pytest.driver.find_element(By.CSS_SELECTOR, '[href="/my_pets"]')
   my_pets.click()
   yield

   pytest.driver.quit()


def test_show_my_pets1():

   # Сравниваем количество питомцев
   pets = pytest.driver.find_elements(By.CSS_SELECTOR, '.table > tbody > tr')
   count_pets = 0
   for i in range(len(pets)):
      pets[i].text != ''
      count_pets = count_pets + 1

   text = pytest.driver.find_element(By.CSS_SELECTOR, ('.left')).text

   text_delete_all = (text.split(':')[1])
   text_final = text_delete_all.replace('Друзей', '')

   assert count_pets == int(text_final)


def test_show_my_pets2():

   # Сравниваем количество фото питомцев
   pytest.driver.implicitly_wait(10)
   images = pytest.driver.find_elements(By.CSS_SELECTOR, '.table > tbody > tr > th > img')
   images_pets = 0
   for i in range(len(images)):
      if images[i].get_attribute('src') != '':
         images_pets = images_pets + 1

   text = pytest.driver.find_element(By.CSS_SELECTOR, ('.left')).text

   text_delete_all = (text.split(':')[1])
   text_final = text_delete_all.replace('Друзей', '')

   half = int(text_final)/2

   assert images_pets >= half

def test_show_my_pets3():

   # Проверка на заполнение полей "Имя", "Порода", "Возраст"
   element_names = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, ".table > tbody > tr > td:nth-child(2)")))
   element_breed = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, ".table > tbody > tr > td:nth-child(3)")))
   element_age = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, ".table > tbody > tr > td:nth-child(4)")))

   names = pytest.driver.find_elements(By.CSS_SELECTOR, '.table > tbody > tr > td:nth-child(2)')
   breed = pytest.driver.find_elements(By.CSS_SELECTOR, '.table > tbody > tr > td:nth-child(3)')
   age = pytest.driver.find_elements(By.CSS_SELECTOR, '.table > tbody > tr > td:nth-child(4)')
   for i in range(len(names)):
      assert names[i].text != ''
      assert breed[i].text != ''
      assert age[i].text != ''

def test_show_my_pets4():

   # Проверка на совпадение имен
   names = pytest.driver.find_elements(By.CSS_SELECTOR, '.table > tbody > tr > td:nth-child(2)')
   list_of_names = []
   for i in range(len(names)):
      list_of_names.append(names[i].text)

   list_of_duplicates_names = [x for i, x in enumerate(list_of_names) if i != list_of_names.index(x)]

   assert list_of_duplicates_names == []

def test_show_my_pets5():

   # Проверка на совпадением имени, породы или возраста
   names = pytest.driver.find_elements(By.CSS_SELECTOR, '.table > tbody > tr > td:nth-child(2)')
   breed = pytest.driver.find_elements(By.CSS_SELECTOR, '.table > tbody > tr > td:nth-child(3)')
   age = pytest.driver.find_elements(By.CSS_SELECTOR, '.table > tbody > tr > td:nth-child(4)')
   list_of_names = ''
   list_of_breed = ''
   list_of_age = ''

   for i in range(len(names)):
      if list_of_names != names[i].text:
         list_of_names = names[i].text
      else:
         for i in range(len(breed)):
            if list_of_breed != breed[i].text:
               list_of_breed = breed[i].text
            else:
               for i in range(len(age)):
                  if list_of_age != age[i].text:
                     list_of_age = age[i].text
                  else:
                     raise "Параметры предыдущего питомца схожи"



