from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db import OperationalError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import multiprocessing.connection
from .models import Feedback, Car
from .forms import SignUpForm, LoginForm
import os
import requests
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



from django.db import OperationalError, ProgrammingError

def home(request):
    cars = Car.objects.all()

    return render(request, 'main/home.html', {
        'cars': cars,
        'user': request.user  # Добавьте эту строку
    })



@csrf_exempt
@require_http_methods(["POST"])
@login_required
def toggle_like(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    user = request.user
    liked = False

    if car.likes.filter(id=user.id).exists():
        car.likes.remove(user)
    else:
        car.likes.add(user)
        liked = True

    likes_count = car.likes.count()

    # Отправка обновления через WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "likes",
        {
            "type": "like.update",
            "car_id": car_id,
            "likes_count": likes_count
        }
    )

    return JsonResponse({
        'status': 'success',
        'liked': liked,
        'likes_count': likes_count
    })
def get_likes(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return JsonResponse({
        'liked': car.user_has_liked(request.user),
        'likes_count': car.likes_count
    })


def cars(request):
    # Получаем конкретные машины по имени
    car1 = Car.objects.filter(name="KUZANAGI CT-3X").first()
    car2 = Car.objects.filter(name="QUADRA TURBO-R V-TECH").first()

    return render(request, 'main/cars.html', {
        'car1': car1,
        'car2': car2
    })


class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'main/register.html', {'form': form})


def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        feedback_entry = Feedback.objects.create(name=name, email=email, message=message)

        # Telegram отправка
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        text = f"Новое сообщение!\nИмя: {name}\nEmail: {email}\nСообщение: {message}"

        try:
            requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": text},
                timeout=5
            )
        except Exception as e:
            print(f"Ошибка отправки: {e}")

        return redirect('home')
    return render(request, 'main/feedback.html')