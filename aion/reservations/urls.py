from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('tos/', views.tos, name='tos'),
    path('privacy', views.privacy, name='privacy'),
    path('contact/', views.contact, name='contact'),
    path('contact-success', views.contact_success, name='contact_success'),
    
    # Account urls
    path('accounts/profile/', views.update_profile, name='update-profile'),
    
    # Logged in URLS
    path('home/', views.home, name='home'),
    
    # Reserve a school resource
    path('my-resources/', views.my_resources, name='my_resources'),
    
    # Reservation Management
    path('todays-reservations', views.todays_reservations, name='todays_reservations'),
    path('manage-reservations', views.manage_reservations, name='manage_reservations'),
    path('reserve-resource/<resource_id>/', views.reserve_resource, name='reserve_resource'),
    
    # Building Administration
    path('building-admin/', views.building_admin, name='building_admin'),
    # Resources
    path('new-resource/', views.new_resource, name='new_resource'),
    path('edit-resources/', views.edit_resources, name='edit_resources'),
    path('edit-resource/<resource_id>/', views.edit_resource, name='edit_resource'),
    path('delete-resource/<resource_id>/', views.delete_resource, name='delete_resource'),
    # Blocks
    path('new-block/', views.new_time_block, name='new_time_block'),
    path('edit-blocks/', views.edit_time_blocks, name='edit_time_blocks'),
    path('edit-block/<time_block_id>/', views.edit_time_block, name='edit_time_block'),
    path('delete-block/<time_block_id>/', views.delete_time_block, name='delete_time_block'),
    # Make Building Admins
    path('select-school-users/', views.select_school_users, name='select_school_users'),
    path('edit-school-admin/<profile_id>/', views.edit_school_admin, name='edit_school_admin'),
    # Announcements
    path('announcements/', views.announcements, name='announcements'),
    path('new-annoucement/', views.new_announcement, name='new_announcement'),
    path('edit-announcements/', views.edit_announcements, name='edit_announcements'),
    path('edit-announcement/<announcement_id>', views.edit_announcement, name='edit_announcement'),
    path('delete-announcement/<announcement_id>', views.delete_announcement, name='delete_announcement'),
    # Bulk Reservations
    path('bulk-reservation/', views.bulk_reservation, name='bulk_reservation'),
    # path('bulk-reservation/confirmation', views.bulk_reservation_confirm, name='bulk_reservation_confirm'),
    
    # Ajax request URLs
    path('ajax/cancel-reservation/', views.ajax_cancel_reservation, name='ajax_cancel_reservation'),
    path('ajax/get-reservations/', views.ajax_get_reservations, name='ajax_get_reservations'),
    path('ajax/make-reservation/', views.ajax_make_reservation, name='ajax_make_reservation'),
    path('ajax/bookmark/', views.ajax_bookmark, name='ajax_bookmark'),

]
