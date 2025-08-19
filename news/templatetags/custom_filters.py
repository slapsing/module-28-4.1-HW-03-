from django import template
from news.templatetags.bad_words import bad_words

register = template.Library()


@register.filter()
def censor(value):
    if not isinstance(value, str):
        return value

    result = value

    for word in bad_words:
        stars = '*' * len(word)
        result = result.replace(word, stars)
        result = result.replace(word.capitalize(), stars)

    return result

@register.filter
def hide_forbidden(value):
    words = value.split()
    result = []
    for word in words:
        if word in censor.bad_words:
            result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)