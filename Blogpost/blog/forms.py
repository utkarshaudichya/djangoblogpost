from django import forms
from blog.models import Comment, Post, UserProfile
from django.contrib.auth.models import User

class UserLoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'status')

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'status')

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
    confirm_password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Both Password must be Matched')
        else:
            return confirm_password

class EmailForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class UserEditForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class UserProfileEditForm(forms.ModelForm):
    sex = forms.ChoiceField(choices=(('male', 'Male'), ('female', 'Female')), widget=forms.RadioSelect)
    class Meta:
        model = UserProfile
        exclude = ('user',)
