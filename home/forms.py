from django import forms
from .models import Quiz, Question, Answer, User, UserQuiz
from django.contrib import admin
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm


class QuizForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(QuizForm, self).__init__(*args, **kwargs)
        current_user = User.objects.filter(
            id=self.request.user.id)
        self.fields['created_by'] = forms.ModelChoiceField(queryset=current_user, initial=current_user.first(),
                                                           required=True, widget=forms.HiddenInput())

    class Meta:
        model = Quiz
        fields = ('name', 'desc', 'created_by')


class UserQuizForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(UserQuizForm, self).__init__(*args, **kwargs)
        user = User.objects.filter(groups__name__in=['partecipant'])
        quiz = Quiz.objects.filter(created_by=self.request.user.id)
        self.fields['user'] = forms.ModelChoiceField(queryset=user,
                                                     required=True, label='Partecipant')
        self.fields['quiz'] = forms.ModelChoiceField(queryset=quiz,
                                                     required=True)

    class Meta:
        model = UserQuiz
        fields = ['user', 'quiz']


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(QuestionForm, self).__init__(*args, **kwargs)
        quiz = Quiz.objects.filter(created_by=self.request.user.id)
        self.fields['quiz'] = forms.ModelChoiceField(queryset=quiz,
                                                     required=True)

    class Meta:
        model = Question
        fields = ('content', 'quiz')


class InvitationForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(InvitationForm, self).__init__(*args, **kwargs)


# Custom allauth signup form to add partecipant custom group
class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        partecipant_group = Group.objects.get(name='partecipant')
        partecipant_group.user_set.add(user)
        return user
