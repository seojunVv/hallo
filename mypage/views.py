from django.contrib.auth.decorators import login_required
from mypage.models import UserProfile, Article, ClickCount
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from mypage.forms import Form
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


@login_required
def ranking_kr(request, username):
    user = User.objects.get(username=username)
    top_click_counts = ClickCount.objects.order_by('-click_count')[:30]
    click_count_obj, created = ClickCount.objects.get_or_create(user=user)
    click_count = click_count_obj.click_count
    my_rank = ClickCount.objects.filter(click_count__gt=click_count).count() + 1
    house_ranks = ClickCount.objects.filter(house_click__gt=0).order_by('-house_click')
    my_house_rank = house_ranks.filter(user__userprofile__house=user.userprofile.house).count() + 1
    if user.userprofile.house == 'Poseidon':
        my_house_click_count = click_count_obj.poseidon_click
    elif user.userprofile.house == 'Athena':
        my_house_click_count = click_count_obj.athena_click
    elif user.userprofile.house == 'Apollo':
        my_house_click_count = click_count_obj.apollo_click
    elif user.userprofile.house == 'Artemis':
        my_house_click_count = click_count_obj.artemis_click
    

    context = {
        'username': username,
        'click_count': click_count,
        'top_click_counts': top_click_counts,
        'my_rank': my_rank,
        'my_house_rank': my_house_rank,
        'my_house_click_count': my_house_click_count,
    }
    return render(request, 'mypage/kr/ranking.html', context)

def get_click_count(request, username):
    user = User.objects.get(username=username)
    click_count_obj, created = ClickCount.objects.get_or_create(user=user)
    click_count = click_count_obj.click_count
    return render(request, 'mypage/kr/click_count.html', {'click_count': click_count})
@login_required
def update_click_count(request, username):
    if request.method == 'POST':
        user = request.user
        click_count_obj, created = ClickCount.objects.get_or_create(user=user)
        click_count_obj.click_count += 1
        if user.userprofile.house == 'Poseidon':
            click_count_obj.poseidon_click += 1
        elif user.userprofile.house == 'Athena':
            click_count_obj.athena_click += 1
        elif user.userprofile.house == 'Apollo':
            click_count_obj.apollo_click += 1
        elif user.userprofile.house == 'Artemis':
            click_count_obj.artemis_click += 1
        click_count_obj.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
@login_required
def mainpage(request, username):
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('user_view')
    users = User.objects.get(username=username)
    article_list = Article.objects.filter(user=users)
    
    context = {
        'user': user,
        'username' : username,
        'candy' : len(article_list)
    }
    return render(request, 'mypage/kr/mainpage.html', context)

@login_required
def mypage_eg(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('user_view')
    users = User.objects.get(username=username)
    article_list = Article.objects.filter(user=users)
    
    context = {
        'user': user,
        'username' : username,
        'candy' : len(article_list),
    }
    return render(request, 'mypage/eg/mainpage_eg.html', context)
@login_required
def inside_pumpkin_eg(request, username,page_num):
    user = request.user
    users = User.objects.get(username=username)
    article_list = Article.objects.filter(user=users)
    articles_per_page = 4
    start_index = (page_num - 1) * articles_per_page
    end_index = start_index + articles_per_page
    paginated_article_list = article_list[start_index:end_index]
    max_pages = (len(article_list) + articles_per_page - 1) // articles_per_page
    max_pages_minus_one = max_pages - 1
    if request.user.username == username:

        
        
        context = {
            'user': user,
            'username': username,
            'article_list': paginated_article_list,
            'max_pages': max_pages,
            'max_pages_minus_one': max_pages_minus_one,
            'range' : range(1,max_pages+1)
        }
        return render(request, 'mypage/eg/inside_pumpkin_eg.html', context)
    else:
        japp_context = {
            'user': user,
            'username': username,
            'article_list': paginated_article_list,
            'max_pages': max_pages,
            'max_pages_minus_one': max_pages_minus_one,
            'range' : range(1,max_pages+1)
        }
        return render(request, 'mypage/eg/inside_pumpkin_notme_eg.html', japp_context)
@login_required
def inside_pumpkin(request, username, page_num):
    user = request.user
    users = User.objects.get(username=username)
    article_list = Article.objects.filter(user=users)
    articles_per_page = 4
    start_index = (page_num - 1) * articles_per_page
    end_index = start_index + articles_per_page
    paginated_article_list = article_list[start_index:end_index]
    max_pages = (len(article_list) + articles_per_page - 1) // articles_per_page
    max_pages_minus_one = max_pages - 1
    if request.user.username == username:

        context = {
            'user': user,
            'username': username,
            'article_list': paginated_article_list,
            'max_pages': max_pages,
            'max_pages_minus_one': max_pages_minus_one,
            'range' : range(1,max_pages+1)
        }
        return render(request, 'mypage/kr/inside_pumpkin.html', context)
    else:
        japp_context = {
            'user': user,
            'username': username,
            'article_list': paginated_article_list,
            'max_pages': max_pages,
            'max_pages_minus_one': max_pages_minus_one,
            'range' : range(1,max_pages+1)
        }
        return render(request, 'mypage/kr/inside_pumpkin_notme.html', japp_context)
@login_required
def write(request, username):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = User.objects.get(username=username)
            article.save()
            user = request.user
            profile = UserProfile.objects.get(user=user)
            language = profile.language
            if language == 'ko':
                return redirect('mypage_kr', username)
            else:
                return redirect('mypage_eg', username)
    else:
        form = Form()
                                                                                                                                                        
    return render(request, 'write.html', {'form': form})

@login_required
def user_list(request, username):
    user = User.objects.get(username=username)
    article_list = Article.objects.filter(user=user)
    return render(request, 'list.html', {'article_list': article_list})

@login_required
def user_view(request, username, num):
    try:
        article = Article.objects.get(id=num, user=User.objects.get(username=username))
        return render(request, 'view.html', {'article': article})
    except Article.DoesNotExist:
        return redirect('user_list', username=username)