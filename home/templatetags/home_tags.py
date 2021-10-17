from django import template

register = template.Library()

@register.simple_tag
def discount_price(price, off):
    value = float(100 - off)/100 * float(price)
    return f'{value:,}'