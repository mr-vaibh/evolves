from django import template

register = template.Library()

@register.simple_tag
def product_price(product, num=False):
    price = product.price
    discount = product.discount if product.discount else 0
    value = float(100 - discount)/100 * float(price)
    value = round(value, 2)

    if num == True: # in case you need num value
        return value
    
    return f'{value:,}'