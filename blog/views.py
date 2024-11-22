from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import BlogPost
from .forms import CommentForm
from taggit.models import Tag

def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    tags = Tag.objects.all()
    selected_tag = request.GET.get('tag')
    if selected_tag:
        posts = posts.filter(tags__name=selected_tag)
    
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/blog_list.html', {'page_obj': page_obj, 'tags': tags, 'selected_tag': selected_tag})

def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, is_published=True)
    comments = post.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('blog_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    
    return render(request, 'blog/blog_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

@login_required
def create_blog_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        tags = request.POST['tags']
        
        post = BlogPost.objects.create(
            title=title,
            content=content,
            author=request.user,
            is_published=True  # You might want to add a draft feature later
        )
        
        for tag in tags.split(','):
            post.tags.add(tag.strip())
        
        return redirect('blog_detail', post_id=post.id)
    
    return render(request, 'blog/create_blog_post.html')