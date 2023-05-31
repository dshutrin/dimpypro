from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Sale)
admin.site.register(Order)
admin.site.register(OrderStatus)
admin.site.register(DefaultProfileImage)
admin.site.register(CustomUser)
admin.site.register(Message)
admin.site.register(Utilit)
admin.site.register(PaidUtils)


class PaymentHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)


admin.site.register(PaymentHistory, PaymentHistoryAdmin)
