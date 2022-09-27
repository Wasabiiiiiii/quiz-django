from django.contrib import admin
from django import forms
from .models import Quiz, Question, Answer, UserQuiz, UserAnswer, User


class QuizForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        current_user = User.objects.filter(
            id=self.request.user.id)
        self.fields['created_by'] = forms.ModelChoiceField(queryset=current_user,
                                                           required=True)

    class Meta:
        model = Quiz
        fields = '__all__'


@ admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    form = QuizForm

    def get_queryset(self, request):
        qs = super(QuizAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(created_by=request.user.id)

    def get_form(self, request, *args, **kwargs):
        form = super(QuizAdmin, self).get_form(request, *args, **kwargs)
        form.current_user = request.user
        form.request = request
        return form


class AnswerInLine(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInLine]


admin.site.register(Question, QuestionAdmin)
# admin.site


class QuizForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        current_user = User.objects.filter(
            id=self.request.user.id)
        self.fields['created_by'] = forms.ModelChoiceField(queryset=current_user,
                                                           required=True)

    class Meta:
        model = Quiz
        fields = '__all__'


class UserQuizAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserQuizAdminForm, self).__init__(*args, **kwargs)
        self.fields['score'] = forms.CharField()
        self.fields['score'].initial = "5"

    class Meta:
        model = UserQuiz
        fields = ['score']


@admin.register(UserQuiz)
class UserQuizAdmin(admin.ModelAdmin):
    form = UserQuizAdminForm
    list_display = ('quiz', 'is_complete',  'score')


admin.site.register(UserAnswer)
