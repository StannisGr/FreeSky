from django.urls import path
from .views import SingInView, SingUpView, ProfileView, DeleteDocumentView, DeletePaymentView

urlpatterns = [
    path('signin/', SingInView.as_view(), name='sign_in'),
    path('signup/', SingUpView.as_view(), name='sign_up'),
    path('profile/', ProfileView.as_view(), name='profile'),
	path('profile/settings/delete/doc/<int:document_pk>', DeleteDocumentView.as_view(), name='delete_doc'),
	path('profile/settings/delete/pay/<int:payment_pk>', DeletePaymentView.as_view(), name='delete_pay'),
]
