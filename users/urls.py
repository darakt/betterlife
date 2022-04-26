from django.urls import path

from . import handlers

urlpatterns = [
        path('', handlers.status, name='status'),
        path('create/', handlers.create, name='create'),
        path('get/<int:id>/', handlers.getAUser, name='getAUser'),
        path('update/<int:id>/', handlers.update, name='update'),
        path('delete/<int:id>/', handlers.delete, name='delete'),
    ]
