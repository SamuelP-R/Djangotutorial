from django.contrib.auth import get_user_model
from .models import Response

def has_responded(user, question):
    User = get_user_model()
    try:
        response = Response.objects.get(question=question, user=user)
        return True
    except Response.DoesNotExist:
        return False
