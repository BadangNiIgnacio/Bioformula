from django import template

register = template.Library()

@register.filter
def times(number):
    return range(number)

@register.filter
def stars(rating):
    filled = "&#9733;" * int(rating)
    empty = "&#9734;" * (5 - int(rating))
    return filled + empty

@register.filter
def stars(value):
    # Create a star rating representation based on the numeric value
    full_stars = int(value)
    half_star = 1 if value - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    return '★' * full_stars + ('☆' * empty_stars) + ('☆' if half_star else '')
