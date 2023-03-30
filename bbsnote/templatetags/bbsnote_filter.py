from django import template

register = template.Library()

@register.filter # @ : annotation(백엔드에서 주석 역할)
# 사용자 정의 함수
def sub(value, arg):
    return value - arg