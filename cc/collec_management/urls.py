from django.urls import path

from . import views

urlpatterns = [
    path("about/", views.about, name="about"),
    path('collection/<int:id>',views.d_collection, name='d_collection'),
    path("all", views.liste_collections, name="liste_collections"),
    path('new', views.new_collection, name='new_collection'),
    path("delete/<int:id>", views.delete_collection_confirmation, name="delete_collection_confirmation"),
    path("change/<int:id>",views.edit_collection,name="edit_collection"),
    path("", views.main, name="main"),
    path('collection/<int:id_collection>/element/add/', views.add_element, name="add_element"),
    path('element/delete/<int:element_id>/', views.delete_element, name="delete_element"),
    path('element/<int:id>',views.d_element, name='d_element'),
    path('element/edit/<int:id>', views.edit_element, name="edit_element"),

    path('accounts/login/', views.login_user, name="login"),
    path('accounts/logout/', views.logout_user, name="logout"),
]
