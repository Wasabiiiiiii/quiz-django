from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.contrib.auth import authenticate,  login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import QuizForm, QuestionForm, UserQuizForm, InvitationForm
from django.forms import inlineformset_factory
from django.views import View
from invitations.utils import get_invitation_model
from django.core.mail import send_mail
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


class indexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            quiz = UserQuiz.objects.filter(user=self.request.user.id)
            context = {'quiz': quiz}
        else:
            return render(request, "index.html")
        return render(request, "index.html", context)


class quizView(View):
    def get(self, request, myid):
        quiz = UserQuiz.objects.get(quiz=myid, user=self.request.user.id)
        return render(request, "quiz.html", {'quiz': quiz})


class quizdataView(View):
    def get(self, request, myid):
        quiz = UserQuiz.objects.get(quiz=myid, user=self.request.user.id)
        questions = []
        for q in Question.objects.filter(quiz=myid):
            answers = []
            for a in Answer.objects.filter(question=q.id):
                print(a)
                answers.append(a.content)
            questions.append({str(q): answers})
        return JsonResponse({
            'data': questions,
        })


class quizsaveView(View):
    def post(self, request, myid):
        if request.is_ajax():
            questions = []
            data = request.POST
            data_ = dict(data.lists())

            data_.pop('csrfmiddlewaretoken')

            for k in data_.keys():
                print('key: ', k)
                question = Question.objects.get(content=k, quiz=myid)
                questions.append(question)

            user = request.user
            quiz = UserQuiz.objects.get(quiz=myid, user=self.request.user.id)

            score = 0
            marks = []
            correct_answer = None

            for q in questions:
                a_selected = request.POST.get(q.content)

                if a_selected != "":
                    question_answers = Answer.objects.filter(question=q)
                    for a in question_answers:
                        if a_selected == a.content:
                            UserAnswer.objects.create(user=user, answer=a)
                            if a.correct:
                                score += 1
                                correct_answer = a.content
                        else:
                            if a.correct:
                                correct_answer = a.content
                    marks.append(
                        {str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
                else:
                    marks.append({str(q): 'not answered'})
            final_score = (
                score / Question.objects.filter(quiz=myid).count()) * 100
            UserQuiz.objects.filter(quiz=myid, user=self.request.user.id).update(
                is_complete=True, score=final_score)
            return JsonResponse({'is_complete': True, 'score': final_score, 'marks': marks})


class addquizView(View):
    def get(self, request):
        if request.user.groups.filter(name='creator').exists():
            form = QuizForm(request=request)
            return render(request, "add_quiz.html", {'form': form, 'request': request})
        else:
            return HttpResponse('Unauthorized', status=401)

    def post(self, request):
        form = QuizForm(data=request.POST,  request=request)
        if form.is_valid():
            ##
            # Checking if quiz with the same name is already added
            ##
            present = Quiz.objects.filter(name=request.POST['name']).exists()
            if not present:
                quiz = form.save(commit=False)
                quiz.save()
                obj = form.instance
                return redirect(reverse('add_question'))
        return redirect(reverse('index'))


class adduserquizView(View):
    def get(self, request):
        if request.user.groups.filter(name='creator').exists():
            form = UserQuizForm(request=request)
            return render(request, "add_user_quiz.html", {'form': form, 'request': request})
        else:
            return HttpResponse('Unauthorized', status=401)

    def post(self, request):
        form = UserQuizForm(data=request.POST,  request=request)
        if form.is_valid():
            ##
            # Checking if user is already added
            ##
            present = UserQuiz.objects.filter(
                user=request.POST['user'], quiz=request.POST['quiz']).exists()
            if not present:
                quiz = form.save()
                quiz.save()
                obj = form.instance
                return render(request, "add_user_quiz.html", {'obj': obj, 'user_added': True})
        return render(request, "index.html",)


class addquestionView(View):

    def get(self, request, ):
        if request.user.groups.filter(name='creator').exists():
            questions = Question.objects.filter(
                quiz__created_by=request.user.id).order_by('-id')
            form = QuestionForm(request=request)
            return render(request, "add_question.html", {'form': form, 'questions': questions})
        else:
            return HttpResponse('Unauthorized', status=401)

    def post(self, request):
        questions = Question.objects.filter(
            quiz__created_by=request.user.id).order_by('-id')
        form = QuestionForm(request.POST, request=request)
        if form.is_valid():
            form.save()
        return render(request, "add_question.html", {'form': form, 'questions': questions})


class deletequestionView(View):

    def get(self, request, myid):
        if request.user.groups.filter(name='creator').exists():
            question = Question.objects.get(id=myid)
            return render(request, "delete_question.html", {'question': question})
        else:
            return HttpResponse('Unauthorized', status=401)

    def post(self, request, myid):
        question = Question.objects.get(id=myid)
        question.delete()
        return redirect('/add_question')


class addoptionView(View):

    def get(self, request, myid):
        if request.user.groups.filter(name='creator').exists():
            question = Question.objects.get(id=myid)
            QuestionFormSet = inlineformset_factory(
                Question, Answer, fields=('content', 'correct', 'question'), extra=4)
            formset = QuestionFormSet(instance=question)
            return render(request, "add_options.html", {'formset': formset, 'question': question})
        else:
            return HttpResponse('Unauthorized', status=401)

    def post(self, request, myid):
        question = Question.objects.get(id=myid)
        QuestionFormSet = inlineformset_factory(
            Question, Answer, fields=('content', 'correct', 'question'), extra=4)
        formset = QuestionFormSet(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            alert = True
            return render(request, "add_options.html", {'alert': alert})
        return render(request, "add_options.html", {'formset': formset, 'question': question})


class resultsView(View):

    def get(self, request):
        if request.user.groups.filter(name="creator"):
            marks = UserQuiz.objects.filter(quiz__created_by=request.user.id)
            answers = UserAnswer.objects.filter(
                answer__question__quiz__created_by=request.user.id)
        else:
            marks = UserQuiz.objects.filter(user=request.user.id)
            answers = UserAnswer.objects.filter(user=request.user.id)
        return render(request, "results.html", {'marks': marks, 'answers': answers})

    def post(self, request):
        if request.is_ajax():
            data = request.POST.get('quiz', None)
            print(data)
            marks = UserQuiz.objects.all()
            return render(request, "results.html", {'marks': marks})
        else:
            marks = UserQuiz.objects.all()
            return render(request, "results.html", {'marks': marks})


class invitationView(View):
    def get(self, request):
        if request.user.groups.filter(name="creator"):
            form = InvitationForm(request=request)
            return render(request, "invitation.html", {'form': form, 'request': request})
        else:
            return HttpResponse('Unauthorized', status=401)

    def post(self, request):
        Invitation = get_invitation_model()
        form = InvitationForm(data=request.POST,  request=request)
        try:
            if form.is_valid():
                invite = Invitation.create(
                    request.POST['email'], inviter=request.user)
                invite.send_invitation(request)
            return render(request, "invitation.html", {'sent': True})
        except IntegrityError as e:
            return render(request, "invitation.html", {'not_unique': True})


class sendResultsView(View):
    def get(self, request, my_id, user_id):
        if request.user.groups.filter(name="creator"):
            if Quiz.objects.filter(
                    id=my_id, created_by=self.request.user.id).exists():
                results = UserQuiz.objects.get(
                    quiz=my_id, user=user_id, is_complete=True)
                if results is not None:
                    email = User.objects.get(id=user_id).email
                    send_mail("Quiz Results", "You made a score of {}".format(results.score), "admin@example.com",
                              [email])
            else:
                return HttpResponse('Unauthorized', status=401)
            return JsonResponse({'score_sent': True})
        else:
            return HttpResponse('Unauthorized', status=401)

    def post(self, request, my_id, user_id):
        return HttpResponse('Unauthorized', status=401)
