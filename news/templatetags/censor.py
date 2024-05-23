from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    bad_words = ['слово1', 'слово2', 'слово3']

    for word in bad_words:
        value = value.replace(word, '*' * len(word))

    return value
