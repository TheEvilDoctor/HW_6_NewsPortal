from django import template

register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
    replace_words: list = ('chinese', 'aggression', 'list')

    if isinstance(value, str):
        for word in value.split():
            if word.lower().replace(':', '').replace('(', '').replace(')', '') in replace_words:
                value = value.replace(word, f'''{word[0]}{'*' * (len(word) - 1)}''')
    else:
        raise TypeError()
    return value
