from django.contrib import admin

from dispatch.models import Client, Mailing, Dispatch


admin.site.register(Client)
admin.site.register(Mailing)
admin.site.register(Dispatch)


