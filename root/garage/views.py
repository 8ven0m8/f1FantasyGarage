from django.shortcuts import render, redirect, get_object_or_404
from .models import TopLeaderboard, ConstructorsLeaderboard, Calendar, Chat_post, Vote, Comments, RaceResult, Driver
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import PostForm, UserRegistrationForm, ProfileForm, CommentForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
from django.views.generic import ListView, DetailView

# Create your views here.
def garage_home(request):
    leaderdata = TopLeaderboard.objects.all().order_by('-points')
    constructordata = ConstructorsLeaderboard.objects.all().order_by('-points')
    year = timezone.now().year
    past = Calendar.objects.filter(status='previous').last()
    next_race = Calendar.objects.filter(status='next').last()
    upcoming = Calendar.objects.filter(status='upcoming').last()
    return render(request, 'garage/garage.html', {'leaderdata':leaderdata, 
                                                  'year':year, 
                                                  'constructordata':constructordata,
                                                  'next_race':next_race,
                                                  'upcoming':upcoming,
                                                  'past':past,
                                                  })

def leaderboard(request):
    driversboard = TopLeaderboard.objects.all().order_by('-points')
    constructorboard = ConstructorsLeaderboard.objects.all().order_by('-points')
    races = Calendar.objects.all().order_by('-from_date')


    first_place = driversboard[0] if len(driversboard) > 0 else None
    second_place = driversboard[1] if len(driversboard) > 1 else None
    third_place = driversboard[2] if len(driversboard) > 2 else None

    first_c = constructorboard[0] if len(constructorboard) > 0 else None
    second_c = constructorboard[1] if len(constructorboard) > 1 else None
    third_c = constructorboard[2] if len(constructorboard) > 2 else None

    return render(request, 'garage/leaderboard.html', {'driversboard':driversboard,
                                                       'constructorboard': constructorboard,
                                                       'first_place': first_place,
                                                       'second_place': second_place,
                                                       'third_place': third_place,
                                                       'first_c': first_c,
                                                       'second_c': second_c,
                                                       'third_c': third_c,
                                                       'races': races,
                                                       })

def chat(request):
    posts = Chat_post.objects.all().order_by('-created_at')

    if request.user.is_authenticated:
        for post in posts:
            vote = post.votes.filter(user=request.user).first()
            post.user_vote = vote.value if vote else 0
    return render(request, 'garage/chat.html', {'posts':posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('chat')
    else:
        form = PostForm()
    return render(request, 'garage/create_post.html', {'form':form})

@login_required
def vote_post(request, post_id, vote_type):
    post = get_object_or_404(Chat_post, id=post_id)

    if vote_type not in ['upvote', 'downvote']:
        return redirect('chat')

    vote_value = 1 if vote_type == "upvote" else -1

    vote, created = Vote.objects.get_or_create(
        post=post,
        user=request.user,
        defaults={'value': vote_value}
    )

    if not created:
        vote.value = vote_value
        vote.save()

    return redirect('chat') 

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Chat_post, pk=post_id, user = request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('chat')
    else:
        form = PostForm(instance=post)
    return render(request, 'garage/create_post.html', {'form':form})

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Chat_post, pk=post_id, user = request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('chat')
    return render(request, 'garage/post_confirm_delete.html', {'post':post})

def register(request):
    if request.user.is_authenticated:
        return redirect('garage_home')

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()

           
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

           
            login(request, user)
            return redirect('garage_home')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()

    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def comments(request, post_id):
    post = get_object_or_404(Chat_post, pk=post_id)
    comments = Comments.objects.filter(post=post, parent=None).order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('comment', post_id=post.id)
    else:
        form = CommentForm()
    replyform = ReplyForm()

    if request.user.is_authenticated:
            vote = post.votes.filter(user=request.user).first()
            post.user_vote = vote.value if vote else 0

    return render(request, 'garage/comments.html', {'post':post,
                                                    'comments':comments,
                                                    'form':form,
                                                    'replyform': replyform
                                                    })

@login_required
def edit_comments(request, post_id, comment_id):
    post = get_object_or_404(Chat_post, pk=post_id)
    comment_to_edit = get_object_or_404(Comments, pk=comment_id, user = request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment_to_edit)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.parent = comment_to_edit.parent
            comment.pk = comment_to_edit.pk          
            comment.save()
            return redirect('comment', post_id=post.id)
    else:
        form = CommentForm(instance = comment_to_edit)

    return render(request, 'garage/edit_comment.html', {'post':post,
                                                        'form':form,
                                                        'comment_to_edit': comment_to_edit,
                                                    })

@login_required
def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Chat_post, pk=post_id)
    comment_to_delete = get_object_or_404(Comments, pk=comment_id, user = request.user)
    if request.method == 'POST':
        comment_to_delete.delete()
        return redirect('comment', post_id = post.id)
    

def profile(request):
    posts = Chat_post.objects.all().filter(user=request.user).order_by('-created_at')
    comments = Comments.objects.all().filter(user=request.user).order_by('-created_at')
    if request.user.is_authenticated:
        for post in posts:
            vote = post.votes.filter(user=request.user).first()
            post.user_vote = vote.value if vote else 0

    upvoted_posts = Chat_post.objects.filter(
        votes__user=request.user,
        votes__value=1
    )
    return render(request, 'garage/profile.html', {'posts':posts, 'comments':comments, 'upvoted_posts':upvoted_posts})

@login_required
def reply_to_comment(request, comment_id):
    parent_comment = get_object_or_404(Comments, id=comment_id)
    post = parent_comment.post

    if request.method == 'POST':
        replyform = ReplyForm(request.POST)
        if replyform.is_valid():
            reply = replyform.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.parent = parent_comment
            reply.save()
            return redirect('comment', post_id=post.id)
    else:
        replyform = ReplyForm()

    return render(request, 'garage/comments.html', {
        'replyform': replyform,
        'parent_comment': parent_comment,
    })

@login_required
def edit_reply_to_comment(request, post_id, comment_id):
    reply_to_edit = get_object_or_404(Comments, pk=comment_id, user=request.user)
    post = get_object_or_404(Chat_post, pk=post_id)

    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=reply_to_edit)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.parent = reply_to_edit.parent
            reply.pk = reply_to_edit.pk
            reply.save()
            return redirect('comment', post_id=post.id)
    else:
        form = ReplyForm(instance=reply_to_edit)

    return render(request, 'garage/edit_reply.html', {
        'post': post,
        'form': form,
        'reply_to_edit': reply_to_edit,
    })

@login_required
def delete_reply_to_comment(request, post_id, comment_id):
    reply_to_delete = get_object_or_404(Comments, pk=comment_id, user=request.user, post__id = post_id)
    post = get_object_or_404(Chat_post, pk=post_id)

    if request.method == 'POST':
        reply_to_delete.delete()
        return redirect('comment', post_id=post_id)

@login_required
def update_profile_image(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # or wherever your profile page is
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'garage/change_profile_picture.html', {'form': form})

def search_view(request):
    query = request.GET.get('q')
    posts = []
    if query:
        posts = Chat_post.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(user__username__icontains=query) | Q(flair__icontains=query))
    return render(request, 'garage/search_result.html', {'posts': posts})

def DetailRaceResult(request, circuit_name):
    race_result = RaceResult.objects.all().filter(race__circuit__iexact=circuit_name).order_by('position')
    race = Calendar.objects.filter(circuit__iexact=circuit_name).get()
    return render(request, 'garage/race_result.html', {'race_result': race_result,
                                                       'race': race,
                                                       })
    



    

