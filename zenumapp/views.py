import http
from django.shortcuts import render, redirect
from .models import Question, Answer
from django.http import *
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, forms
from django.contrib import messages

from .forms import CreateUserForm, CreateProfileForm
from .models import Profile, generate_random, Rating


def tag(request):
    return render(request, "include/tag.html")


def question(request, i: int):
    return render(request, "include/question.html")


def ask(request):
    if request.user.is_authenticated:
        return render(request, "ask.html", {'user': Profile.objects.get_user(request.user)})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect...')

        context = {}
        return render(request, 'registration/login.html', context)


def signup_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                user_name = form.cleaned_data.get('username')
                Profile.objects.create(user=user)
                messages.success(request, 'Account was created for ' + user_name)

                return redirect('login')

        context = {'form': form}
        return render(request, 'registration/signup.html', context)


def profile(request):
    if request.user.is_authenticated:
        user = Profile.objects.get_user(request.user)
        form = CreateProfileForm(instance=user)

        if request.method == 'POST':
            form = CreateProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
            else:
                redirect('home')

        context = {'form': form, 'user': user}

        return render(request, 'profile.html', context)
    else:
        return redirect('home')


def tags(request, tag_name):
    question_with_tag = Question.objects.select_by_tag(tag_name)
    return render(request, "tags.html", {'questions': question_with_tag, 'tag_to_find': tag_name})


def questions(request, pk):
    question_to_show = Question.objects.filter(id=pk)[0]
    answers = question_to_show.get_answers()
    rating = Rating.objects.filter(question=question_to_show)
    full_rating = 0
    for rate in rating:
        if rate.up_vote:
            full_rating += 1
        else:
            full_rating -= 1
    return render(request, "questions.html", {'question': question_to_show,
                                              'answers': answers,
                                              'rating': full_rating})


def home(request):
    all_questions = Question.objects.all()
    most_common_tags = Question.tags.most_common()[:25]

    page = request.GET.get('page', 1)
    paginator = Paginator(all_questions, 10)
    page_range = paginator.get_elided_page_range(number=page)
    try:
        p_questions = paginator.page(page)
    except PageNotAnInteger:
        p_questions = paginator.page(1)
    except EmptyPage:
        p_questions = paginator.page(paginator.num_pages)

    # generate_random(10, 100, 10)

    if request.user.is_authenticated:
        user = Profile.objects.get_user(request.user)
        return render(request, "index.html", {'questions': p_questions,
                                              'tags': most_common_tags,
                                              'page_range': page_range,
                                              'user': user})
    else:
        return render(request, "index.html", {'questions': p_questions,
                                              'tags': most_common_tags,
                                              'page_range': page_range})
