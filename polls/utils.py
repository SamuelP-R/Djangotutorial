from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_questions")
    is_active = models.BooleanField(default=True)  # Indica si la encuesta está activa

    def __str__(self):
        return self.question_text

python manage.py makemigrations
python manage.py migrate

from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_questions",
        default=1,  # ID del usuario que será el creador por defecto
    )
    is_active = models.BooleanField(default=True)


from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import Question

class DisableQuestionView(UserPassesTestMixin, View):
    def test_func(self):
        """
        Solo permitir acceso a administradores o creadores de la encuesta.
        """
        question = get_object_or_404(Question, pk=self.kwargs["pk"])
        return self.request.user.is_staff or question.created_by == self.request.user

    def post(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=self.kwargs["pk"])
        question.is_active = False
        question.save()
        return redirect(reverse("polls:results", kwargs={"pk": question.pk}))

class DetailView(DetailView):
    model = Question
    template_name = "polls/detail.html"
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()

        # Verificar si la encuesta está activa
        context["is_active"] = question.is_active

        # Verificar si el usuario ya votó
        if self.request.user.is_authenticated:
            context["user_has_voted"] = Voted.objects.filter(user=self.request.user, question=question).exists()
        else:
            context["user_has_voted"] = False

        return context

from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:pk>/disable/", views.DisableQuestionView.as_view(), name="disable"),
]
