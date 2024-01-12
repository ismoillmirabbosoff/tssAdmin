from django.contrib import admin

# Register your models here.
from .models import Device, Company, SuperCompany

class DeviceAdmin(admin.ModelAdmin):
    # list_display = ('id','deviceID')
    list_display = ('deviceID','qrID','simCard','firmWareVersion','company') #'id',

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "leaseCompany":
    #         kwargs["queryset"] = Company.objects.filter(leasingFrom=request.leaseCompany)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)    

    # def has_delete_permission(self, request, obj=None):
    # # # Disable delete
    #     return False

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','active')

    # def has_delete_permission(self, request, obj=None):
    # # Disable delete
    #     return False

admin.site.register(Device,DeviceAdmin)
admin.site.register(Company,CompanyAdmin)
admin.site.register(SuperCompany,CompanyAdmin)