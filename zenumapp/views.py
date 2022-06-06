import http

import taggit.utils
from django.shortcuts import render, redirect
from .models import Question, Answer
from django.http import *
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, forms
from django.contrib import messages

from .forms import CreateUserForm, CreateProfileForm, CreateVoteForm
from .models import Profile, Rating


def tag(request):
    if request.user.is_authenticated:
        return render(request, "include/tag.html", {'user': Profile.objects.get_user(request.user)})
    else:
        return render(request, "include/tag.html")


def question(request):
    return render(request, "include/question.html")


def vote_answer(request):
    if request.user.is_authenticated:
        answer_id = request.POST.get('answer_id')
        answer_vote = int(request.POST.get('vote'))

        if answer_vote == 1:
            if (Rating.objects.filter(up_vote=True, down_vote=False, user=request.user,
                                      answer_id=answer_id).exists()):
                answer_vote = Rating.objects.update_or_create(user=request.user,
                                                              answer_id=answer_id,
                                                              defaults={'up_vote': False, 'down_vote': False})
            else:
                answer_vote = Rating.objects.update_or_create(user=request.user,
                                                              answer_id=answer_id,
                                                              defaults={'up_vote': True, 'down_vote': False})
        elif answer_vote == -1:
            if (Rating.objects.filter(up_vote=False, down_vote=True, user=request.user,
                                      answer_id=answer_id).exists()):
                answer_vote = Rating.objects.update_or_create(user=request.user,
                                                              answer_id=answer_id,
                                                              defaults={'up_vote': False, 'down_vote': False})
            else:
                answer_vote = Rating.objects.update_or_create(user=request.user,
                                                              answer_id=answer_id,
                                                              defaults={'up_vote': False, 'down_vote': True})
        else:
            answer_vote = Rating.objects.update_or_create(user=request.user,
                                                          answer_id=answer_id,
                                                          defaults={'up_vote': False, 'down_vote': False})

        rating = Rating.objects.filter(answer_id=answer_id)

        full_rating = 0
        for rate in rating:
            if rate.up_vote:
                full_rating += 1
            elif rate.down_vote:
                full_rating -= 1

        return JsonResponse({'full_rating': full_rating})


def is_right(request):
    if request.user.is_authenticated:
        ans_id = request.POST.get('answer_id')
        Answer.objects.filter(id=ans_id).update(is_right=True)
        return JsonResponse({'status': 'ok'})


def ask(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST.get("title")
            text = request.POST.get("text")
            n_tags = request.POST.get("tags")

            n_tags = taggit.utils.parse_tags(n_tags)

            new_q = Question.objects.create(question_title=title, question_text=text, user=request.user, views=0,
                                            is_hot=False)

            for n_tag in n_tags:
                new_q.tags.add(n_tag)

            messages.info(request, "Successfully created!")
        return render(request, "ask.html", {'user': Profile.objects.get_user(request.user)})
    else:
        return redirect("login")


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
    if request.user.is_authenticated:
        return render(request, "tags.html", {'questions': question_with_tag, 'tag_to_find': tag_name,
                                             'user': Profile.objects.get_user(request.user)})
    else:
        return render(request, "tags.html", {'questions': question_with_tag, 'tag_to_find': tag_name})


def questions(request, pk):
    question_to_show = Question.objects.all().filter(id=pk)

    if not question_to_show:
        raise Http404("Question not found")

    question_to_show = question_to_show[0]

    answers = question_to_show.get_answers()

    if request.method == 'POST':
        answer = request.POST.get("answer")
        Answer.objects.create(answer_text=answer, question=question_to_show, user=request.user, is_right=False)

    page = request.GET.get('page', 1)
    paginator = Paginator(answers, 5)
    page_range = paginator.get_elided_page_range(number=page)
    try:
        p_answers = paginator.page(page)
    except PageNotAnInteger:
        p_answers = paginator.page(1)
    except EmptyPage:
        raise Http404("No such page. There are only {} pages.".format(paginator.num_pages))

    rating = Rating.objects.filter(question=question_to_show)

    full_rating = 0
    for rate in rating:
        if rate.up_vote:
            full_rating += 1
        elif rate.down_vote:
            full_rating -= 1

    if request.user.is_superuser:
        Profile.objects.update_or_create(user=request.user)

    if request.user.is_authenticated:
        return render(request, "questions.html", {'question': question_to_show,
                                                  'answers': p_answers,
                                                  'rating': full_rating,
                                                  'user': Profile.objects.get_user(request.user),
                                                  'page_range': page_range})
    else:
        return render(request, "questions.html", {'question': question_to_show,
                                                  'answers': p_answers,
                                                  'rating': full_rating,
                                                  'page_range': page_range})


def vote(request):
    if request.user.is_authenticated:
        question_id = request.POST.get('question_id')
        question_vote = int(request.POST.get('vote'))

        if question_vote == 1:
            if (Rating.objects.filter(up_vote=True, down_vote=False, user=request.user,
                                      question_id=question_id).exists()):
                question_vote = Rating.objects.update_or_create(user=request.user,
                                                                question_id=question_id,
                                                                defaults={'up_vote': False, 'down_vote': False})
            else:
                question_vote = Rating.objects.update_or_create(user=request.user,
                                                                question_id=question_id,
                                                                defaults={'up_vote': True, 'down_vote': False})
        elif question_vote == -1:
            if (Rating.objects.filter(up_vote=False, down_vote=True, user=request.user,
                                      question_id=question_id).exists()):
                question_vote = Rating.objects.update_or_create(user=request.user,
                                                                question_id=question_id,
                                                                defaults={'up_vote': False, 'down_vote': False})
            else:
                question_vote = Rating.objects.update_or_create(user=request.user,
                                                                question_id=question_id,
                                                                defaults={'up_vote': False, 'down_vote': True})
        else:
            question_vote = Rating.objects.update_or_create(user=request.user,
                                                            question_id=question_id,
                                                            defaults={'up_vote': False, 'down_vote': False})

        rating = Rating.objects.filter(question_id=question_id)

        full_rating = 0
        for rate in rating:
            if rate.up_vote:
                full_rating += 1
            elif rate.down_vote:
                full_rating -= 1

        return JsonResponse({'full_rating': full_rating})


def home(request, is_hot):
    if is_hot:
        all_questions = Question.objects.all().filter(is_hot=True)
    else:
        all_questions = Question.objects.all()

    most_common_tags = Question.tags.most_common()[:25]

    page = request.GET.get('page', 1)
    paginator = Paginator(all_questions, 7)
    page_range = paginator.get_elided_page_range(number=page)
    try:
        p_questions = paginator.page(page)
    except PageNotAnInteger:
        p_questions = paginator.page(1)
    except EmptyPage:
        raise Http404("No such page. There are only {} pages.".format(paginator.num_pages))

    # generate_random(10, 100, 10)

    if request.user.is_superuser:
        Profile.objects.update_or_create(user=request.user)

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
