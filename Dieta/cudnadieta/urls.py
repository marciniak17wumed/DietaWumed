from django.urls import path
from .views import home_view, SignUpView, kalk_view, info_view, przepisy_view, kalorie_view
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('calc/', kalk_view, name='kalk_view'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('info/', info_view, name='info'),
    path('przepisy/', przepisy_view, name='przepisy'),
    path('kalorie/', kalorie_view, name='kalorie'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
