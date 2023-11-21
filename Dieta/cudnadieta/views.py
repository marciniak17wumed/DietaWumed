from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .forms import CalorieEntryForm
from django.contrib.auth import logout


def home_view(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def kalk_view(request):
    if request.method == 'POST':
        form = CalorieEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()

            # Algorytm dietetyczny
            plan_diety = calculate_plan_diety(entry)

            return render(request, 'calc.html', {'form': form, 'plan_diety': plan_diety})
    else:
        form = CalorieEntryForm()
    return render(request, 'calc.html', {'form': form})



def calculate_plan_diety(entry):
    # Współczynniki modyfikujące bazowe kalorie w zależności od wieku
    wspolczynniki_wieku = {
        '18-29': 1.0,
        '30-59': 0.95,
        '60+': 0.9,
    }

    # Współczynniki modyfikujące bazowe kalorie w zależności od płci
    wspolczynniki_plci = {
        'K': 0.9,  # dla kobiet
        'M': 1.0,  # dla mężczyzn
    }

    # Współczynniki modyfikujące bazowe kalorie w zależności od aktywności
    wspolczynniki_aktywnosci = {
        'niska': 1.2,
        'umiarkowana': 1.5,
        'wysoka': 1.8,
    }

    # Współczynniki modyfikujące bazowe kalorie w zależności od celu
    wspolczynniki_celu = {
        'schudnac': 0.8,
        'utrzymanie_masy': 1.0,
        'przytyc': 1.2,
    }

    # Współczynniki procentowe dla białka, węglowodanów i tłuszczu
    proteiny_procent = 0.3
    weglowodany_procent = 0.5
    tluszcze_procent = 0.2

    # Proporcja kalorii przypisywanych do każdego posiłku
    proporcja_posilkow = {'śniadanie': 0.3, 'drugie_sniadanie': 0.2, 'podwieczorek': 0.1, 'obiad': 0.3, 'kolacja': 0.1}

    wiek = entry.wiek
    waga = entry.waga
    wzrost = entry.wzrost
    plec = entry.plec
    aktywnosc = entry.aktywnosc
    cel = entry.cel

    if 18 <= wiek <= 29:
        wiek_group = '18-29'
    elif 30 <= wiek <= 59:
        wiek_group = '30-59'
    else:
        wiek_group = '60+'

    # Obliczenia bazowych kalorii
    bazowe_kalorie = int((10 * waga) + (6.25 * wzrost) - (5 * wiek) + 5) * wspolczynniki_wieku[wiek_group] * \
                     wspolczynniki_plci[plec]

    # Modyfikacja bazowych kalorii na podstawie aktywności, celu
    bazowe_kalorie = int(bazowe_kalorie * wspolczynniki_aktywnosci[aktywnosc] * wspolczynniki_celu[cel])

    # Inicjalizacja słownika planu diety
    plan_diety = {
        'śniadanie': {'proteiny': 0, 'weglowodany': 0, 'tluszcze': 0, 'kalorie': 0},
        'drugie_sniadanie': {'proteiny': 0, 'weglowodany': 0, 'tluszcze': 0, 'kalorie': 0},
        'podwieczorek': {'proteiny': 0, 'weglowodany': 0, 'tluszcze': 0, 'kalorie': 0},
        'obiad': {'proteiny': 0, 'weglowodany': 0, 'tluszcze': 0, 'kalorie': 0},
        'kolacja': {'proteiny': 0, 'weglowodany': 0, 'tluszcze': 0, 'kalorie': 0},
        'kalorie': 0,  # Dodaj inicjalizację dla klucza 'kalorie'
    }

    # Oblicz kalorie, proteiny, węglowodany i tłuszcze dla każdego posiłku
    for posilek in plan_diety.keys():
        # Sprawdź, czy klucz istnieje w słowniku proporcja_posilkow
        if posilek in proporcja_posilkow:
            # Utwórz unikalną strukturę dla każdego posiłku
            plan_diety[posilek] = {
                'kalorie': int(bazowe_kalorie * proporcja_posilkow[posilek]),
                'proteiny': int((bazowe_kalorie * proporcja_posilkow[posilek]) * proteiny_procent / 4),
                'weglowodany': int((bazowe_kalorie * proporcja_posilkow[posilek]) * weglowodany_procent / 4),
                'tluszcze': int((bazowe_kalorie * proporcja_posilkow[posilek]) * tluszcze_procent / 9),
            }
            plan_diety['kalorie'] += plan_diety[posilek]['kalorie']

    return plan_diety




class CustomLoginView(LoginView):
    template_name = 'login.html'

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def info_view(request):
    return render(request, 'info.html')

def przepisy_view(request):
    return render(request, 'przepisy.html')

def kalorie_view(request):
    return render(request, 'kalorie.html')
