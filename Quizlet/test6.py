
from quizlet import Quizlet

path = 'test.docx'

quizlet = Quizlet(path)

all_paragraphs = quizlet.xml_paragraphs()

highlighted = quizlet.filter_paragraphs(all_paragraphs)

words_defs = quizlet.convert_word_def(highlighted)

print(words_defs)
