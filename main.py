from parser_pdd import parse_pdd
from sqlmodel import SQLModel, select
from db import session_scope, engine
from models import Category, Question, Answer

urls = ({'AB': {'category': 'AB', 'url': 'https://www.drom.ru/pdd', },
        'CD': {'category': 'CD', 'url': 'https://www.drom.ru/pdd/cd'}})

SQLModel.metadata.create_all(engine)
parse_pdd(urls)

# def select():
#     with session_scope() as session:
#         question = select(Question).filter(
#             Question.category_id == "AB",
#             Question.ticket == 1,
#             Question.number == 2
#             )
#         results = session.exec(question)
#         answers = [Answer(id=i.id,
#                 title=i.title,
#                 correct_answer=i.correct_answer)
#                 for i in results.answers]
#         print(answers)
