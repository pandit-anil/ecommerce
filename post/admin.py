from django.contrib import admin
from . models import Bpost,Systemsetting,Category,CustomerFeedback,Clients,Order

# Register your models here.

admin.site.register(Bpost)
@admin.register(Systemsetting)
class SystemAdmin(admin.ModelAdmin):
    list_display =('id','sysname')

@admin.register(CustomerFeedback)
class Feedback(admin.ModelAdmin):
    list_display = ('feedback',)
    

admin.site.register(Category)
admin.site.register(Clients)
admin.site.register(Order)

