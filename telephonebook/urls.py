from .views import *
from django.urls import path, include

from rest_framework import routers
router = routers.DefaultRouter()
router.register('person', PersonViewSet)

urlpatterns = router.urls

person_list_view = PersonViewSet.as_view({
    "get": "list",
    "post": "create"

})

urlpatterns = [
    path('api/', include(router.urls)),
    path('generic/person/', PersonListView.as_view()),
    path('generic/person/<int:id>/', PersonListView.as_view()),
    path('', index, name='index'),
    path('create/', create, name='create'),
    path('<int:id>/', details, name='details'),
    path('<int:id>/editPerson/', editPerson, name='editPerson'),
    path('<int:id>/editInfo/', editInfo, name='editInfo'),
    path('<int:id>/delete/', delete, name='delete'),


]