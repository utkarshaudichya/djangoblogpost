from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment, UserProfile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from taggit.models import Tag
from blog.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.db.models import Q, Count

# Create your views here.
def postListView(request, tag_slug=None):
    post_list = Post.objects.filter(status='published')
    query = request.GET.get('q')
    if query:
        post_list = Post.objects.filter(Q(title__icontains=query) | Q(author__username=query) | Q(body__icontains=query))
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = Post.objects.filter(tags__in=[tag])
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)#(last_page)
    return render(request, 'blog/post_list.html', {'post_list':post_list, 'tag':tag})

def postDetailsView(request, id, year, month, day, post, tag_slug=None):
    post = get_object_or_404(Post, slug=post, status='published', id=id)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post = Post.objects.filter(tags__in=[tag])
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    comments = post.comments.filter(active=True)
    csubmit = False
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit = False)
            new_comment.post = post
            new_comment.save()
            csubmit = True
    else:
        form = CommentForm()
    return render(request, 'blog/post_details.html', {'post':post, 'form':form, 'csubmit':csubmit, 'comments':comments, 'is_liked':is_liked})

@login_required(login_url='user_login')
def emailSendView(request, id):
    post = get_object_or_404(Post, id=id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = '{}({}) recommends you to read "{}"'.format(cd['name'], cd['email'], post.title)
            post_url = request.build_absolute_uri(post.get_absolute_url())
            message = 'Read Post at:\n{}\n\n{}\'s comments:\n{}'.format(post_url, cd['name'], cd['comment'])
            send_mail(subject, message, 'djangoblogproject@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailForm()
    return render(request, 'blog/sharebymail.html', {'form':form, 'post':post, 'sent':sent})

@login_required(login_url='user_login')
def createPostView(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            title = form.cleaned_data['title']
            slug = '-'.join(title.lower().split())
            new_post.slug = slug
            new_post.author = request.user
            new_post.save()
    else:
        form = PostCreateForm()
    return render(request, 'blog/create_blog.html', {'form':form})

def userLoginView(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                status = False
                if user.is_active:
                    status = False
                    login(request, user)
                    return HttpResponseRedirect(reverse('post_list'))
                else:
                    status = True
                    return render(request, 'blog/user_login.html', {'form':form, 'status':status})
                    #return HttpResponse("User is not active")
            else:
                status = True
                return render(request, 'blog/user_login.html', {'form':form, 'status':status})
                #return HttpResponse("User is None")
    else:
        status = False
        form = UserLoginForm()
    return render(request, 'blog/user_login.html', {'form':form, 'status':status})

def userLogoutView(request):
    logout(request)
    return redirect('post_list')

def userRegistrationView(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            form.save()
            UserProfile.objects.create(user=new_user)
            return redirect('user_login')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/user_signup.html', {'form':form})

def editProfileView(request):
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST or None, instance=request.user)
        profile_form = UserProfileEditForm(data=request.POST or None, instance=request.user.userprofile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('edit_profile'))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)
    return render(request, 'blog/edit_profile.html', {'user_form':user_form, 'profile_form':profile_form})

def likePostView(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())

def myPostView(request):
    post_list = Post.objects.filter(author=request.user)
    return render(request, 'blog/my_posts.html', {'post_list':post_list})

def postEditView(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        raise Http404()
    if request.method == 'POST':
        form = PostEditForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostEditForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})

def postDeleteView(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        raise Http404()
    post.delete()
    return redirect('my_posts')
