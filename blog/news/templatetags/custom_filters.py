from django import template
import re


register = template.Library()


black_list_word = ['fuck', 'lol', 'bot', 'FUCK']


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError('Нельзя цензурировать НЕ строку')

    for word in black_list_word:
        value = value.replace(word[1:], '*' * (len(word)-1))

    return value


# Цензурирование строки с учетом регистра, возвращает в исходном регистре строку
@register.filter(name='censorlower')
def censor(text_to_check):
    new_text = re.sub(r'[^\w\s]', '', text_to_check)
    word_list = new_text.strip().split()
    new_stop_list = [x.lower() for x in black_list_word]
    for word in word_list:
        word_len = len(word)
        if (word.lower() in new_stop_list) or (
                (word.lower()[-1] == 's') and (word.lower()[:word_len - 1] in new_stop_list)):
            substitute = word[0] + '*' * (len(word) - 2) + word[-1]
            text_to_check = text_to_check.replace(word, substitute)
    return text_to_check
