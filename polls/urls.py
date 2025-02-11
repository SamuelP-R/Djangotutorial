from django.urls import include, path
from . import views
from .views import AllResultsView


app_name = "polls"
urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/5/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # ex: /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    
    path('accounts/', include('django.contrib.auth.urls')),

    path("<int:question_id>/delete-vote/", views.DeleteVoteView.as_view(), name="delete_vote"),

    path("<int:pk>/disable/", views.DisableQuestionView.as_view(), name="disable"),

    path("<int:pk>/enable/", views.EnableQuestionView.as_view(), name="enable"),

    path('allresults/', AllResultsView.as_view(), name='all_results'),
]