from django.urls import path

from . import handlers

urlpatterns = [
        path('', handlers.status, name='status'),
        path('create/', handlers.create, name='create'), # born to disappear
        path('create/superuser/', handlers.createSuperuser, name='createSuperuser'),
        path('create/org_admin/', handlers.createOrgAdmin, name='createOrgAdmin'),
        path('create/org_member/', handlers.createOrgMember, name='createOrgMember'),
        path('create/proj_owner/', handlers.createProjOwner, name='createProjOwner'),
        path('create/proj_member/', handlers.createProjMember, name='createProjMember'),
        path('get/<int:id>/', handlers.getAUser, name='getAUser'),
        path('update/<int:id>/', handlers.update, name='update'),
        path('delete/<int:id>/', handlers.delete, name='delete'),
    ]
