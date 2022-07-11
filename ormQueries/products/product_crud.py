from .models import Product 
from django.db.models import Q, Avg, Max, Count
from django.db.models.functions import Length


class ProductCrud:
    @classmethod
    def get_all_products(cls):
        return Product.objects.all()

    @classmethod
    def find_by_model(cls, model_name):
        return(Product.objects.get(model=model_name))

    @classmethod
    def last_record(cls):
        return Product.objects.all()[len(Product.objects.all())-1]

    @classmethod
    def by_rating(cls, rate):
        print(Product.objects.filter(rating = rate))
        return Product.objects.filter(rating = rate)

    @classmethod
    def by_rating_range(cls, range_one, range_two):
        return Product.objects.filter(rating__gte = range_one) & Product.objects.filter(rating__lte = range_two)

    @classmethod
    def by_rating_and_color(cls, rate, color):
        return Product.objects.filter(rating__exact = rate) & Product.objects.filter(color__exact = color)
        
    @classmethod
    def by_rating_or_color(cls, rate, color):
        return Product.objects.filter(rating__exact = rate) | Product.objects.filter(color__exact = color)
        

    @classmethod
    def no_color_count(cls):
        return Product.objects.filter(color = None).count()
        
    @classmethod
    def below_price_or_above_rating(cls, below_price, above_rating):
        return Product.objects.filter(price_cents__lt = below_price) | Product.objects.filter(rating__gt = above_rating)

        
    @classmethod
    def ordered_by_category_alphabetical_order_and_then_price_decending(cls):
        return Product.objects.order_by('category', '-price_cents')

    @classmethod
    def products_by_manufacturer_with_name_like(cls, name):
        return Product.objects.filter(manufacturer__contains = name)

    @classmethod
    def manufacturer_names_for_query(cls, name):
        return list(Product.objects.filter(manufacturer__contains = name).values_list('manufacturer', flat=True))
        

    @classmethod
    def not_in_a_category(cls, name):
        return Product.objects.exclude(category = name)
    
    @classmethod
    def limited_not_in_a_category(cls, name, limit):
        return Product.objects.exclude(category = name)[:limit]

    @classmethod
    def category_manufacturers(cls, str_category):
        return list(Product.objects.filter(category__icontains = str_category).values_list('manufacturer', flat=True))


    @classmethod
    def average_category_rating(cls, str_category):
        return Product.objects.aggregate(rating__avg = Avg('rating', filter=Q(category=str_category)))
    
    @classmethod
    def greatest_price(cls):
        return Product.objects.all().aggregate(Max('price_cents'))

    @classmethod
    def longest_model_name(cls):
        return Product.objects.annotate(model_length = (Length('model'))).order_by('-model_length')[:1][0].pk

    @classmethod
    def ordered_by_model_length(cls):
        return Product.objects.annotate(product_length = (Length('model'))).order_by('product_length')