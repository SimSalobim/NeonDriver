def car_request(request):
    """Добавляет request в контекст моделей"""
    return {'request': request}