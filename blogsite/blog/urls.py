from django.urls import path
from . import views


app_name = "blog"

urlpatterns = [
    # path("", views.post_list, name="post_list"),
    path("", views.get_dashboard, name="blog_wave"),
    path("contact/", views.get_contact_blog, name="contact"),
    path("category/", views.get_category, name="category"),
    path("about/", views.get_about, name="about"),
    path("<int:post_id>/post", views.get_post_by_id, name="single_post"),
    # path("", views.PostListView.as_view(), name="post_list"),
    # path(
    #     "<int:year>/<int:month>/<int:day>/<slug:post>/",
    #     views.post_detail,
    #     name="post_detail",
    # ),
    # path("<int:post_id>/share/", views.post_share, name="post_share"),
    # path("<int:post_id>/comment/", views.post_comment, name="post_comment"),
    # path("tag/<slug:tag_slug>/", views.post_list, name="post_list_by_tag"),
]
