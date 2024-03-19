
from django.contrib import admin
from django.urls import path
from django.conf import settings
from MyApp import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_home/',views.admin_home),
    path('add_category/',views.add_category),
    path('add_category_post/',views.add_category_post),
    path('view_category/',views.view_category),
    path('edit_category/<id>',views.edit_category),
    path('edit_category_post/',views.edit_category_post),
    path('delete_category/<id>',views.delete_category),
    path('add_product/',views.add_product),
    path('add_product_post/',views.add_product_post),
    path('view_product/',views.view_product),    
    path('edit_product/<id>',views.edit_product),
    path('edit_product_post/',views.edit_product_post),        
    path('delete_product/<id>',views.delete_product),
    path('add_staff/',views.add_staff),
    path('add_staff_post/',views.add_staff_post),
    path('view_staff/',views.view_staff),
    path('edit_staff/<id>',views.edit_staff),
    path('edit_staff_post/',views.edit_staff_post),
    path('delete_staff/<id>',views.delete_staff),
    path('add_scheduler/<id>',views.add_scheduler),
    path('view_scheduler/',views.view_scheduler),
    path('edit_scheduler/<id>',views.edit_scheduler),
    path('edit_scheduler_post/',views.edit_scheduler_post),
    path('delete_scheduler/<id>',views.delete_scheduler),
    path('add_vehicle/',views.add_vehicle),
    path('add_vehicle_post/',views.add_vehicle_post),
    path('view_vehicle/',views.view_vehicle),
    path('edit_vehicle/<id>',views.edit_vehicle),
    path('edit_vehicle_post/',views.edit_vehicle_post),
    path('delete_vehicle/<id>',views.delete_vehicle),
    path('view_complaint/',views.view_complaint),
    path('view_review/',views.view_review),
    
    # Scheduler
    
    path('scheduler_home/',views.scheduler_home),
    path('view_category2/',views.view_category2),
    path('view_product2/<id>',views.view_product2),  
    path('edit_quantity/<id>',views.edit_quantity),  
    path('edit_quantity_post/<int:id>',views.edit_quantity_post),  
    path('view_order/',views.view_order),  
    
    #public
    path('signup/',views.signup),
    path('signup_post/',views.signup_post),
    path('signin/',views.signin),
    path('signin_post/',views.signin_post),
    path('public_home/',views.public_home),
    
    
    #customer
    path('customer_home/',views.customer_home),
    path('home/',views.home),
    path('view_categories/',views.view_categories),
    path('view_products/<id>',views.view_products),
    path('view_products2/<id>',views.view_products2), 
    path('add_order/<id>',views.add_order), 
    path('submit_order/<id>',views.submit_order), 
    path('make_payment_post/',views.make_payment_post), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)