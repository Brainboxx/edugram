from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment
from core.models import Post
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)


@login_required(login_url='login')
def add_comment(request, post_pk):

    if request.method == 'POST':
        user = request.user
        content = request.POST['content']
        post_id = post_pk

        if not post_id:
            return HttpResponseBadRequest("Post ID is required.")

        comment = Comment.objects.create(post_id=post_id, username=user, content=content)
        comment.save()

        return redirect('/')
    else:
        return render(request, 'core/signup.html')


def view_comments(request, post_id):
    comments = Comment.objects.filter(post_id=post_id)
    return render(request, 'comments/view_comments.html', {'comments': comments})

