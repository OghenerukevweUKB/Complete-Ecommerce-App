
from django.contrib import admin, messages
from . import models
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
# Register your models here.


class inventoryFilter(admin.SimpleListFilter):
    title='inventory'
    parameter_name='inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value()== '<10':
            return queryset.filter(inventory__lt=10)


class ProductImageInline(admin.TabularInline):
    model= models.ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')
        return ''    



@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields=['collection']
    prepopulated_fields={
        'slug':['title']
    }
    actions=['clear_inventory']
    inlines=[ProductImageInline]
    list_display=['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable=['unit_price']
    list_per_page=10
    list_select_related=['collection']
    list_filter=['collection', 'last_update' ,inventoryFilter]
    search_fields=['orderItemInLine']

    def collection_title(self , product):
        return product.collection.title


    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'low'
        return 'ok'  


    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count=queryset.update(inventory=0)  
        self.message_user(
            request,
            f'{updated_count} product was successfully updated',
            messages.ERROR
        ) 

    class Media:
        css={
            'all':['store/ styles.css']
        }     




@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display=['title', 'products_count']
    search_fields=['title']
  

    @admin.display(ordering='products_count')
    def products_count(self , collection):
        url=reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id':str(collection.id)})
        return format_html('<a href="{}">{}</a>', url,collection.products_count)
        

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('products')) 


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name', 'last_name', 'membership']
    list_editable=['membership']
    list_select_related = ['user']
    ordering=['user__first_name', 'user__last_name']
    search_fields=['first_name__istartswith', 'last_name__istartswith']
    list_per_page=10



class OrderItemInLine(admin.TabularInline):
    model=models.OrderItem
    autocomplete_fields=['product']
    min_num=1
    max_num=10
    extra=0



@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields=['customer']
    list_display=['id','placed_at','customer'] 
    inlines=[OrderItemInLine]
    ordering=['customer']   
