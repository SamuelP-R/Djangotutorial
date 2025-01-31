from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import F
from django.views.generic import DetailView
from .models import Choice, Question, Voted
from django.views import generic
from django.utils import timezone
from django.contrib import messages

# Create your views here.
#First view 
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
    Return the last five published questions (not including those set to be
    published in the future).
    """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
        :5
    ]


class DetailView(DetailView):
    model = Question
    template_name = "polls/detail.html"
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()

        # Verificar si el usuario ha votado en esta pregunta
        user_has_voted = Voted.objects.filter(
            user=self.request.user, question=question
        ).exists() if self.request.user.is_authenticated else False

        print(f'Usuario: {self.request.user}, Ha votado: {user_has_voted}')  # 👀 Ver en consola

        context["user_has_voted"] = user_has_voted
        return context
 

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # si el user ya voto en esa pregunta
    if request.user.is_authenticated:
        existing_vote = Voted.objects.filter(user=request.user, question=question).first()
        if existing_vote:
            messages.error(request, 'Ya votaste y no se puede votar otra vez')
            return redirect('polls:results', question.id)
    
    if request.method == "POST":
        choice_id = request.POST.get('choice')

        #Obtener la opcion seleccionada
        if not choice_id:
            messages.error(request, 'No se selecciono una opcion')
            return redirect('polls:detail', question.id)
    
        choice = get_object_or_404(Choice, pk=choice_id)

        #Guardar el voto
        Voted.objects.create(user=request.user, question=question, choice=choice)
        choice.votes = choice.votes +1
        choice.save()

        messages.success(request, 'Se registro el Voto')
        return redirect('polls:results', question.id)
    
    return redirect('polls:detail', question.id)


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)