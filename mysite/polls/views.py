from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from django.db import connection
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # FIX: validate password strength. This uses Django’s built-in password validation system to checks
        # the strength of the password and prevents users from creating accounts with weak or common passwords.
        try:
            validate_password(password)
        except ValidationError as e:
            return HttpResponse(" ".join(e.messages), status=400)

        User.objects.create_user(username=username, password=password)
        return HttpResponse("User created")

    return render(request, "polls/signup.html")

def search(request):
    query = request.GET.get("q", "")
    # FLAW: vulnerable to SQL injection
    # with connection.cursor() as cursor:
    #     sql = "SELECT id, question_text, pub_date FROM polls_question WHERE question_text LIKE '%" + query + "%'"
    #     cursor.execute(sql)
    #     rows = cursor.fetchall()

    # to fix the code above you can see the vulnerable code is in comment
    # the fix uses ORM query system that prevents user input from being interpreted as SQL code.
    rows = Question.objects.filter(
        question_text__icontains=query
    ).values_list("id", "question_text", "pub_date")

    output = "<h1>Search results</h1>"
    output += f"<p>Search term: {query}</p>"
    output += "<ul>"
    for row in rows:
        output += f"<li>{row[1]}</li>"
    output += "</ul>"

    return HttpResponse(output)

def get_queryset(self):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]
    
    #This code makes polls that are dated to show in future to not show before the day
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())



class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    # FIX: Only allow access to polls that have already been published
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))