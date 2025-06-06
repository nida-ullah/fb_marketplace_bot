from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MarketplacePostForm
from .models import MarketplacePost

# Create your views here.


def create_post(request):
    if request.method == 'POST':
        form = MarketplacePostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post scheduled successfully!')
            return redirect('post_list')
    else:
        form = MarketplacePostForm()

    return render(request, 'postings/create_post.html', {'form': form})


def post_list(request):
    posts = MarketplacePost.objects.all().order_by('-scheduled_time')
    return render(request, 'postings/post_list.html', {'posts': posts})
