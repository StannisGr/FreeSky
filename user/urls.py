from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.SingInView.as_view(), name='sign_in'),
    path('signup/', views.SingUpView.as_view(), name='sign_up'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
	path('profile/settings/delete/doc/<int:document_pk>', views.DeleteDocumentView.as_view(), name='delete_doc'),
	path('profile/settings/delete/pay/<int:payment_pk>', views.DeletePaymentView.as_view(), name='delete_pay'),
    # path('logout', views.get_sing_up),
]
