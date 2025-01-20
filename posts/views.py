from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/home.html', {'posts': posts})



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if Like.objects.filter(author=request.user, post=post).exists():
        Like.objects.filter(author=request.user, post=post).delete()
    else:
        Like.objects.create(author=request.user, post=post)
    return redirect('home')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment
from .forms import CommentEditForm

# Edit Comment
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure the comment belongs to the current user
    if comment.author != request.user:
        return redirect('home')  # You can redirect to an error page or a custom view

    if request.method == 'POST':
        form = CommentEditForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id)  # Redirect to the post details page
    else:
        form = CommentEditForm(instance=comment)

    return render(request, 'posts/edit_comment.html', {'form': form})

# Delete Comment

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure the comment belongs to the current user
    if comment.author != request.user:
        return redirect('home')  # You can redirect to an error page or a custom view

    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', post_id=comment.post.id)  # Redirect to the post details page

    return render(request, 'posts/confirm_delete.html', {'comment': comment})

