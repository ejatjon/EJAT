from django import template

register=template.Library()


@register.filter(name="category_page_range")
def category_page_range(value):
    try:
        num=value.number
        end_num=value.paginator.num_pages
        resulit=[]
        if num < end_num-2:
            for i in range(num-2,num+3):
                resulit.append(i)
            return resulit
        else:
            for i in range(end_num-5,end_num+1):
                resulit.append(i)
            return resulit
    except Exception:
        return []

@register.filter(name="category_str_to_int")
def category_str_to_int(value):
    try:
        return int(value)
    except Exception:
        return value