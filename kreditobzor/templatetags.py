from django import template

register = template.Library()

@register.simple_tag(name='star_rating')
def get_rating(offer):
    rating = 0
    rating_list = []
    for comment in offer.comments.all():
        rating_list.append(comment.rating)
    if rating_list != []:
        rating = "%.2f" % (sum(rating_list) / len(rating_list))
    return rating


@register.simple_tag(name='comments_count')
def get_comments_quantity(offer):
    count = offer.count
    if str(count).endswith('0'):
        end = 'ов'
    elif str(count).endswith('11') or str(count).endswith('12') or str(count).endswith('13') or str(count).endswith('14'):
        end = 'ов'
    elif str(count).endswith('1'):
        end = ''
    elif str(count).endswith('2') or str(count).endswith('3') or str(count).endswith('4'):
        end = 'а'
    else:
        end = 'ов'
    return str(count) + ' отзыв' + end

