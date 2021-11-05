from django import template

register = template.Library()

@register.simple_tag
def product_price(product):
    price = product.price
    discount = product.discount if product.discount else 0
    value = float(100 - discount)/100 * float(price)
    value = round(value, 2)
    return f'{value:,}'