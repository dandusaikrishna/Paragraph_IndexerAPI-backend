from django.urls import path
from .views import UserRegistrationView, UserLoginView, ParagraphView, SearchView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('paragraphs/', ParagraphView.as_view(), name='paragraphs'),
    path('search/', SearchView.as_view(), name='search'),
]
