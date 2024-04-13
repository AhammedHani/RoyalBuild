
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
    path('view_category_post/',views.view_category_post),
    path('edit_category/<id>',views.edit_category),
    path('edit_category_post/',views.edit_category_post),
    path('delete_category/<id>',views.delete_category),
    path('add_product/',views.add_product),
    path('add_product_post/',views.add_product_post),
    path('view_product/',views.view_product),
    path('view_product_post/',views.view_product_post),  
    path('edit_product/<id>',views.edit_product),
    path('edit_product_post/',views.edit_product_post),        
    path('delete_product/<id>',views.delete_product),
    path('add_staff/',views.add_staff),
    path('add_staff_post/',views.add_staff_post),
    path('view_staff/',views.view_staff),
    path('view_staff_post/',views.view_staff_post), 
    path('edit_staff/<id>',views.edit_staff),
    path('edit_staff_post/',views.edit_staff_post),
    path('delete_staff/<id>',views.delete_staff),
    # path('add_scheduler/<id>',views.add_scheduler),
    # path('add_scheduler/',views.add_scheduler),
    # path('add_scheduler_post/',views.add_scheduler_post),
    
    # path('view_scheduler/',views.view_scheduler),
    # path('view_scheduler_post/',views.view_scheduler_post),
    # path('edit_scheduler/<id>',views.edit_scheduler),
    # path('edit_scheduler_post/',views.edit_scheduler_post),
    # path('delete_scheduler/<id>',views.delete_scheduler),
    path('add_vehicle/',views.add_vehicle),
    path('add_vehicle_post/',views.add_vehicle_post),
    path('view_vehicle/',views.view_vehicle),
    path('view_vehicle_post/',views.view_vehicle_post),  
    path('edit_vehicle/<id>',views.edit_vehicle),
    path('edit_vehicle_post/',views.edit_vehicle_post),
    path('delete_vehicle/<id>',views.delete_vehicle),
    path('view_complaint/',views.view_complaint),
    path('view_complaint_post/',views.view_complaint_post),
    path('complaint_reply/<id>',views.complaint_reply),
    path('complaint_reply_post/<id>',views.complaint_reply_post),
    path('admin_view_review/', views.admin_view_review),
    path('admin_view_review_post/', views.admin_view_review_post),
    path('admin_change_password_post/',views.admin_change_password_post),
    path('admin_view_profile/',views.admin_view_profile),    
    path('staff_report1/',views.staff_report1),    
    path('view_permanent_staff/',views.view_permanent_staff),  
    path('view_permanent_staff_post/',views.view_permanent_staff_post),      
    path('view_temporary_staff/',views.view_temporary_staff),    
    path('view_temporary_staff_post/',views.view_temporary_staff_post),   
    # path('product_report1/',views.product_report1), 
    # path('product_report1_post/',views.product_report1_post), 
    # path('product_report2/<id>',views.product_report2), 
    # path('product_report2_post/',views.product_report2_post), 
    path('admin_view_duty1/<id>',views.admin_view_duty1), 
    path('admin_view_duty2/<id>',views.admin_view_duty2), 
    path('sales_report1/',views.sales_report1), 
    path('view_sales_report1/',views.view_sales_report1), 
    path('view_sales_report1_post/',views.view_sales_report1_post), 
    path('sales_report2/',views.sales_report2), 
    path('view_sales_report2/',views.view_sales_report2), 
    path('view_sales_report2_post/',views.view_sales_report2_post), 
    
    
    # Scheduler
    
    path('scheduler_home/',views.scheduler_home),
    path('view_category2/',views.view_category2),
    path('view_category2_post/',views.view_category2_post),
    path('view_product2/<id>',views.view_product2),  
    path('view_product2_post/',views.view_product2_post),
    path('edit_quantity/<id>',views.edit_quantity),  
    path('edit_quantity_post/<int:id>',views.edit_quantity_post),  
    path('view_orders/',views.view_orders),  
    path('check_payment/<id>',views.check_payment),  
    path('schedule_order/<id>',views.schedule_order),  
    path('schedule_order_post/<id>',views.schedule_order_post),  
    path('reject_order/<id>', views.reject_order),
    path('orders_history/', views.orders_history),
    path('orders_history_post/', views.orders_history_post),
    path('scheduler_change_password_post/',views.scheduler_change_password_post),
    path('scheduler_view_profile/',views.scheduler_view_profile),
    path('scheduler_edit_profile_post/',views.scheduler_edit_profile_post),
    path('add_worksite/',views.add_worksite),    
    path('add_worksite_post/',views.add_worksite_post),    
    path('view_worksite/',views.view_worksite),
    path('edit_worksite/<id>',views.edit_worksite),
    path('edit_worksite_post/',views.edit_worksite_post),
    path('delete_worksite/<id>',views.delete_worksite),
    path('view_staffs/',views.view_staffs),
    path('view_staffs_post/',views.view_staffs_post),
    path('add_duty/<id>',views.add_duty),
    path('add_duty_post/',views.add_duty_post),
    path('view_duty/',views.view_duty),
    path('view_delivery_staff/',views.view_delivery_staff),
    path('view_cancel_request/',views.view_cancel_request),
    path('view_cancel_request_post/',views.view_cancel_request_post), 
    path('cancel_confirm/<id>',views.cancel_confirm),
    path('view_return/',views.view_return),
    path('view_return_post/',views.view_return_post),
    path('schedule_return/<id>',views.schedule_return),
    path('schedule_return_post/<id>',views.schedule_return_post),
    
    
    
    
    #customer
    path('customer_home/',views.customer_home),
    path('home/',views.home),
    path('view_categories/',views.view_categories),
    path('category_sub/<int:id>',views.category_sub),
    path('view_categories1/',views.view_categories1),
    # path('view_products/<id>',views.view_products),
    path('view_products2/<id>',views.view_products2), 
    path('add_order/<id>',views.add_order), 
    path('add_order_post/<id>',views.add_order_post), 
    path('view_order/',views.view_order),
    path('view_order_post/',views.view_order_post),  
    path('send_complaint/',views.send_complaint),  
    path('send_complaint_post/',views.send_complaint_post),  
    path('view_customer_complaint/',views.view_customer_complaint),
    path('view_customer_complaint_post/',views.view_customer_complaint_post),
    path('view_replied_complaint/<id>',views.view_replied_complaint),
    path('customer_change_password/',views.customer_change_password),
    path('customer_change_password_post/',views.customer_change_password_post),
    path('customer_view_profile/',views.customer_view_profile),
    path('customer_edit_profile/',views.customer_edit_profile),
    path('customer_edit_profile_post/',views.customer_edit_profile_post),
    path('view_worksites/',views.view_worksites),
    path('add_review/<id>',views.add_review),
    path('add_review_post/<id>',views.add_review_post),
    path('cancel_order/<id>',views.cancel_order),
    path('add_return/<id>',views.add_return),
    path('add_return_post/<id>',views.add_return_post),
    path('add_to_cart_post/<int:id>',views.add_to_cart_post),
    path('view_cart/',views.view_cart),
    path('view_cart_post/',views.view_cart_post),
    path('edit_cart/<id>',views.edit_cart),
    path('edit_cart_post/<id>',views.edit_cart_post),
    path('delete_cart/<id>',views.delete_cart),
    path('cart_orders/',views.cart_orders),
    path('cart_orders1/',views.cart_orders1),
    
    #staff
    path('staff_home/',views.staff_home),
    path('staff_view_duty/',views.staff_view_duty),
    path('finish_duty/<id>',views.finish_duty),
    path('view_delivery/',views.view_delivery),
    path('confirm_delivery/<id>',views.confirm_delivery),
    path('view_returns/',views.view_returns),
    path('view_returns_post/<id>',views.view_returns_post),
    path('staff_view_profile/',views.staff_view_profile),
    path('staff_edit_profile_post/',views.staff_edit_profile_post),
    path('staff_change_password_post/',views.staff_change_password_post),
    
    
    #public
    path('signup/',views.signup),
    path('signup_post/',views.signup_post),
    path('signin/',views.signin),
    path('signin_post/',views.signin_post),
    path('public_home/',views.public_home),
    path('public_view_categories/',views.public_view_categories),
    path('public_category_sub/<id>',views.public_category_sub), 
    path('public_view_categories1/',views.public_view_categories1),
    # path('public_view_products/<id>',views.public_view_products),
    path('public_view_products2/<id>',views.public_view_products2),
    path('public_view_worksites/',views.public_view_worksites),
    
    
    #accountant
    path('accountant_home/',views.accountant_home),
    path('view_wages/',views.view_wages),
    path('view_salary/',views.view_salary),
    path('add_wage/<id>',views.add_wage),
    path('add_wage_post/<id>',views.add_wage_post),
    path('add_leave/<id>',views.add_leave),
    path('add_leave_post/<id>',views.add_leave_post),
    
    
    
    
    #admin
    path('staff_wages1/',views.staff_wages1),
    path('staff_wages1_post/',views.staff_wages1_post),
    path('staff_salary1/',views.staff_salary1),
    path('staff_salary1_post/',views.staff_salary1_post),
    
    
    
    
    #logout
    path('logout/',views.logout),
    path('admin_logout/',views.admin_logout),
        
        
        
        
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)