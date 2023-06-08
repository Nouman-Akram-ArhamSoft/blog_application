from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, Category
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag


def get_dashboard(request):
    categories = Category.objects.all()
    posts = Post.objects.all()
    filtered_posts = {}
    for category in categories:
        if category.title == "Business":
            filtered_posts["business_posts"] = category.posts.filter(
                title="Business"
            )
        elif category.title == "Culture":
            filtered_posts["culture_posts"] = category.posts.filter(title="Culture")
        elif category.title == "Sport":
            filtered_posts["sport_posts"] = category.posts.filter(title="Sport")
        elif category.title == "Food":
            filtered_posts["food_posts"] = category.posts.filter(title="Food")
        elif category.title == "Politics":
            filtered_posts["politics_posts"] = category.posts.filter(
                title="Politics"
            )
        elif category.title == "Celebrity":
            filtered_posts["celebrity_posts"] = category.posts.filter(
                title="Celebrity"
            )
        elif category.title == "Startups":
            filtered_posts["startup_posts"] = category.posts.filter(title="Startups")
        elif category.title == "Travel":
            filtered_posts["business_posts"] = category.posts.filter(title="Travel")

    print({"categories": categories, "posts": posts}.update(filtered_posts))

    return render(
        request, "blog/zenblog/index.html", {"categories": categories, "posts": posts}.update(filtered_posts)
    )


def get_contact_blog(request):
    return render(request, "blog/zenblog/contact.html")


def get_category(request):
    categories = Category.objects.all()
    return render(request, "blog/zenblog/category.html", {"categories": categories})


def get_about(request):
    return render(request, "blog/zenblog/about.html")


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommend you read " f"{post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )

            import os

            send_mail(subject, message, os.environ.get("EMAIL_HOST_USER"), [cd["to"]])

            sent = True
    else:
        form = EmailPostForm()

    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )


# class PostListView(ListView):
#     """
#     Alternative post list view
#     """

#     queryset = Post.published.all()
#     context_object_name = "posts"
#     paginate_by = 3
#     template_name = "blog/post/list.html"


def post_list(request, tag_slug=None):
    _post_list = Post.published.all()
    tags = None
    if tag_slug:
        tags = get_object_or_404(Tag, slug=tag_slug)
        post_list = _post_list.filter(tags__in=[tags])

    paginator = Paginator(_post_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)

    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)

    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/post/list.html", {"posts": posts, "tags": tags})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(
        request,
        "blog/post/detail.html",
        {"post": post, "comments": comments, "form": form},
    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    form = CommentForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(
        request,
        "blog/post/comment.html",
        {"post": post, "form": form, "comment": comment},
    )
