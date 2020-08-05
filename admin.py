from django.contrib import admin
from NurtureHealthApp.models import Department, Contact_Us, register_table,add_treatment,Appointments,Reviews,cart,Order,Feedback

# Register your models here.
admin.site.site_header="NURTURE HEALTH"

class Contact_UsAdmin(admin.ModelAdmin):
    fields = ["contact_number","name","subject","message","address"]

    list_display = ["id","name","contact_number","address","subject","message","added_on"]
    search_fields = ["name"]
    list_filter = ["added_on","name"]
    list_editable = ["name"]

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["id","Dep_name","description","added_on"]


admin.site.register(Contact_Us,Contact_UsAdmin)
admin.site.register(Department,DepartmentAdmin)
admin.site.register(register_table)
admin.site.register(add_treatment)
admin.site.register(Appointments)
admin.site.register(Reviews)
admin.site.register(cart)
admin.site.register(Order)
admin.site.register(Feedback)

