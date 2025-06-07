from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Feedback, Car
from .forms import SignUpForm, LoginForm
import os
import requests
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def home(request):
    try:
        car1 = Car.objects.get_or_create(name="Kusanagi CT-3X")[0]
        car2 = Car.objects.get_or_create(name="Quadra Turbo-R V-Tech")[0]
    except Car.DoesNotExist:
        # Если машины не найдены, создаем пустые объекты
        car1 = Car.objects.get_or_create(name="Kusanagi CT-3X")[0]
        car2 = Car.objects.get_or_create(name="Quadra Turbo-R V-Tech")[0]

    # Добавляем информацию о лайках
    if request.user.is_authenticated:
        car1.user_has_liked_value = car1.user_has_liked(request.user)
        car2.user_has_liked_value = car2.user_has_liked(request.user)
    else:
        car1.user_has_liked_value = False
        car2.user_has_liked_value = False

    return render(request, 'main/home.html', {
        'car1': car1,
        'car2': car2,
        'user': request.user
    })

import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def toggle_like(request, car_id):
    try:
        car = get_object_or_404(Car, id=car_id)
        user = request.user

        if car.likes.filter(id=user.id).exists():
            car.likes.remove(user)
            liked = False
        else:
            car.likes.add(user)
            liked = True

        likes_count = car.likes.count()

        # Всегда возвращаем JSON-ответ
        response_data = {
            'status': 'success',
            'liked': liked,
            'likes_count': likes_count
        }

        try:
            channel_layer = get_channel_layer()
            if channel_layer:
                async_to_sync(channel_layer.group_send)(
                    "likes_group",
                    {
                        "type": "like_update",
                        "car_id": car_id,
                        "likes_count": likes_count,
                        "user_has_liked": liked
                    }
                )
        except Exception as e:
            logger.error(f"Redis error: {str(e)}")
            # Добавляем информацию об ошибке в ответ
            response_data['redis_error'] = str(e)

        return JsonResponse(response_data)

    except Exception as e:
        logger.error(f"Error in toggle_like: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

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

def get_likes(request, car_id):
    try:
        car = get_object_or_404(Car, id=car_id)
        return JsonResponse({
            'liked': car.user_has_liked(request.user),
            'likes_count': car.likes.count()
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
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