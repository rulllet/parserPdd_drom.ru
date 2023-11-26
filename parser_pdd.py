from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import requests
import time
import re

from db import session_scope
from models import Category, Question, Answer


def parse_pdd(urls):
    service = Service(executable_path="./chromedriver.exe")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    with session_scope() as db:
        for category_pdd in urls:
            category = Category(name=urls[category_pdd]["category"], description = 'None')
            category.questions = []
            for i in range(40):
                url = f'{urls[category_pdd]["url"]}/bilet_{i + 1}/'
                driver.get(url)
                time.sleep(1)
                question_data = driver.find_elements(By.XPATH, "//div[@class='pdd-ticket b-media-cont']")
                image_question = driver.find_elements(By.XPATH,
                                                    "//div[@class='pdd-placeholder']|//div[@class='b-media-cont']/img")

                for index, (q, im) in enumerate(zip(question_data, image_question)):
                    help = q.find_element(By.XPATH, f"//div[@id='c{index + 1}']")
                    driver.execute_script("arguments[0].style.display = 'block';", help)
                    data = validation(q.text)
                    image_question = im.get_attribute("src")
                    if image_question:
                        name_img = f"{urls[category_pdd]['category']}-{i}-{index}.jpg"
                        p = requests.get(image_question)
                        out = open(f"static\{name_img}", "wb")
                        out.write(p.content)
                        out.close()
                    else:
                        name_img = 'image.jpg'

                    question_result = Question(ticket=i + 1,
                                               number=index + 1,
                                               title=data['title'],
                                               help=data['help'],
                                               image=name_img)
                    category.questions.append(question_result)
                    question_result.answers = []

                    for index, answer_data in enumerate(data['answer']):
                        question_result.answers.append(
                            Answer(title=answer_data,
                                   correct_answer=int(data['correct_answer']) == index + 1))
            db.add(category)
            db.commit()
    print("Ready")


def validation(data_question):
    result = data_question.split('\n')
    result = result[1:-2]
    title = result[0]
    help = result[-1]
    answer = []
    for q in result:
        if 'Правильный ответ:' in q:
            correct_answer = result.index(q)

    for w in range(2, correct_answer, 2):
        answer.append(result[w])
    correct_answer = re.sub("[^0-9]", '', result[correct_answer])
    return {'title': title, 'help': help, 'correct_answer': correct_answer, 'answer': answer}


def edit_img():
    # парсер сохранил название картинки в дб без формата (.jpg),
    # а вопросы без картинки с форматом
    # скрипт добавляет формат к названию картинки
    with session_scope() as db:
        for i in range(1, 1601):
            w = db.query(Question).filter(Question.id == i).one()
            if 'image' in w.image:
                continue
            else:
                w.image = w.image + '.jpg'
            print(w.image)
            db.commit(w, db)
