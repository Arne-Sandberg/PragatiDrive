from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^auth/',views.authView, name='authView'),
    url(r'^logout/',views.logout, name='logout'),
    url(r'^loggedin/',views.loggedin, name='loggedin'),
    url(r'^invalid/',views.invalid_login, name='invalid_login'),
    url(r'^tenant_admin/', views.tenant_admin,name="tenant_admin"),           
    url(r'^standard_user/', views.standard_user,name="standard_user"),
    url(r'^privileged_user/', views.privileged_user,name="privileged_user"),           
    url(r'^superuser/', views.superuser,name="superuser"),           
	url(r'^edit_privileged_rights/', views.edit_privileged_rights,name="edit_privileged_rights"),           
    url(r'^edit_standard_rights/', views.edit_standard_rights,name="edit_standard_rights"),           
    url(r'^set_privileged_rights/',views.set_privileged_rights,name="set_privileged_rights"),
    url(r'^set_standard_rights/',views.set_standard_rights,name="set_standard_rights"),
    url(r'^add_tenant/',views.add_tenant,name="add_tenant"),
    url(r'^save_tenant/',views.save_tenant,name="save_tenant"),
    url(r'^create_user/',views.create_user,name="create_user"),
    url(r'^creating_user/',views.creating_user,name="creating_user"),
    url(r'^user_created/',views.user_created,name="user_created"),
    url(r'^edit_tenant/(?P<tenant>[0-9]+)/$',views.edit_tenant,name="edit_tenant"),
    url(r'^update_tenant/(?P<tenant>[0-9]+)/$',views.update_tenant,name="update_tenant"),
    url(r'^delete_file_p/',views.delete_file_p,name="delete_file_p"),
    url(r'^delete_file_s/',views.delete_file_s,name="delete_file_s"),
]