from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.views.generic import TemplateView, DeleteView, ListView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Q, F
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
import math

from .models import *
from account.models import *

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request

        trending_posts = Article.objects.order_by('-views')[:3]
        latest_posts = Article.objects.order_by('-date_added')[:3]
        all_posts = Article.objects.order_by('-date_added')

        for post in all_posts:
            full_url = request.build_absolute_uri(post.get_absolute_url())
            post.facebook_share = f"https://www.facebook.com/sharer/sharer.php?u={full_url}"
            post.twitter_share = f"https://www.x.com/intent/tweet?url={full_url}&text={post.title}"
            post.linkedin_share = f"https://www.linkedin.com/sharing/share-offsite/?url={full_url}"

        context.update({
            'trending_posts': trending_posts,
            'latest_posts': latest_posts,
            'all_posts': all_posts,
            'categories': Category.objects.all(),
            'featured_authors': (
                User.objects
                .filter(article__isnull=False)
                .annotate(total_views=Sum('article__views'))
                .order_by('-total_views')[:3]
            ),
        })

        return context
    
@csrf_exempt
def subscribe_newsletter(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({"success": False, "message": "Email is required."})

            subscriber, created = NewsletterSubscription.objects.get_or_create(email=email)

            if created:
                try:
                    send_mail(
                        subject="Welcome to InkWave Newsletter",
                        message="Thanks for subscribing! You'll receive updates soon.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=True,
                    )
                except Exception as e:
                    print("Newsletter email error:", e)
                return JsonResponse({"success": True, "message": "Subscription successful! Check your email."})
            else:
                return JsonResponse({"success": False, "message": "You are already subscribed."})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid request."})

    return JsonResponse({"success": False, "message": "Invalid method."})

def search_suggestions(request):
    q = request.GET.get("q", "").strip()
    data = {
        "articles": [],
        "writers": [],
        "categories": []
    }

    if q:
        articles = Article.objects.filter(
            Q(title__icontains=q) |
            Q(category__name__icontains=q) |
            Q(writer__username__icontains=q) |
            Q(tag__name__icontains=q)
        ).distinct()[:5]
        data["articles"] = [
            {"title": a.title, "url": a.get_absolute_url()} for a in articles
        ]

        writers = User.objects.filter(username__icontains=q)[:5]
        data["writers"] = [
            {"username": w.username, "url": f"/account/profile/{w.username}/"} for w in writers
        ]

        categories = Category.objects.filter(name__icontains=q)[:5]
        data["categories"] = [
            {"name": c.name, "url": f"/category/{c.slug}/"} for c in categories
        ]

    return JsonResponse(data)

class ArticleDetailView(LoginRequiredMixin, View):
    template_name = 'blog/article_detail.html'

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)

        session_key = f'viewed_article_{article.pk}'
        if not request.session.get(session_key, False):
            Article.objects.filter(pk=article.pk).update(views=F('views') + 1)
            request.session[session_key] = True
            article.refresh_from_db()

        words = len(article.content.split())
        minutes_read = max(1, math.ceil(words / 200))

        number_of_likes = article.number_of_likes()
        comments = Comment.objects.filter(article=article).order_by('-date_added')
        total_comments = comments.count()
        liked = article.likes.filter(id=request.user.id).exists()

        related_posts = Article.objects.filter(
            writer=article.writer
        ).exclude(pk=article.pk).order_by('-date_added')[:3]

        comment_to_be_updated = None
        if 'edit' in request.GET:
            comment_to_be_updated = get_object_or_404(Comment, pk=request.GET['edit'])

        comment_to_be_replied = None
        if 'reply' in request.GET:
            comment_to_be_replied = get_object_or_404(Comment, pk=request.GET['reply'])

        context = {
            'article': article,
            'minutes_read': minutes_read,
            'number_of_likes': number_of_likes,
            'comments': comments,
            'total_comments': total_comments,
            'article_is_liked': liked,
            'related_posts': related_posts,
            'comment_to_be_updated': comment_to_be_updated,
            'comment_to_be_replied': comment_to_be_replied,
        }
        return render(request, self.template_name, context)

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        content = request.POST.get('content', '').strip()
        comment_id = request.POST.get('comment_id')
        parent_id = request.POST.get('parent_id')

        if not content:
            messages.error(request, 'Please fill out the comment field correctly.')
            return redirect('article_detail', slug=slug)

        if comment_id:
            comment = get_object_or_404(Comment, pk=comment_id)
            comment.content = content
            comment.save()
            messages.success(request, 'Comment updated successfully')

        elif parent_id:
            parent_comment = get_object_or_404(Comment, pk=parent_id)
            Comment.objects.create(
                writer=request.user,
                article=article,
                parent=parent_comment,
                content=content
            )
            messages.success(request, 'Reply added successfully')

        else:
            Comment.objects.create(
                writer=request.user,
                article=article,
                content=content
            )
            messages.success(request, 'Comment added successfully')

        return redirect('article_detail', slug=article.slug)

class ArticleLikeView(LoginRequiredMixin, View):
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            messages.success(request, 'Article unliked successfully')
        else:
            article.likes.add(request.user)
            messages.success(request, 'Article liked successfully')
        return redirect(reverse_lazy('article_detail', kwargs={'slug': article.slug}))

class ArticleCreateView(LoginRequiredMixin, View):
    template_name = 'blog/article_create.html'

    def get(self, request):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})

    def post(self, request):
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_ids = request.POST.getlist('categories')
        tags = request.POST.get('tags', '')
        featured_image = request.FILES.get('featured_image')

        if Article.objects.filter(title__iexact=title).exists():
            categories = Category.objects.all()
            return render(request, self.template_name, {
                'categories': categories,
                'error': f'An article with the title "{title}" already exists.',
                'title': title,
                'content': content,
                'selected_categories': category_ids,
                'tags': tags,
            })
        
        if not title or not content:
            messages.error(request, "Title and content are required.")
            return redirect('article_create')

        article = Article.objects.create(
            writer=request.user,
            title=title,
            content=content,
            image=featured_image
        )

        if category_ids:
            article.category.set(category_ids)

        if tags:
            article.tag.add(*[tag.strip() for tag in tags.split(',') if tag.strip()])

        messages.success(request, "Article created successfully!")
        return redirect('article_detail', slug=article.slug)

class ArticleEditView(LoginRequiredMixin, View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        categories = Category.objects.all()
        return render(request, 'blog/article_edit.html', {
            'article': article,
            'categories': categories,
            'selected_categories': article.category.all(),
            'tags': ', '.join(article.tag.names())
        })

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)

        new_title = request.POST.get('title').strip()
        new_content = request.POST.get('content')

        if Article.objects.exclude(pk=article.pk).filter(title__iexact=new_title).exists():
            messages.error(request, "An article with this title already exists. Please choose another title.")
            categories = Category.objects.all()
            return render(request, 'blog/article_edit.html', {
                'article': article,
                'categories': categories,
                'selected_categories': article.category.all(),
                'tags': ', '.join(article.tag.names())
            })

        article.title = new_title
        article.content = new_content

        if 'featured_image' in request.FILES:
            article.image = request.FILES['featured_image']

        article.save()

        category_ids = request.POST.getlist('categories')
        article.category.set(category_ids)

        tags_input = request.POST.get('tags', '')
        tag_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
        article.tag.set(tag_list)

        messages.success(request, 'Article updated successfully!')
        return redirect('article_detail', slug=article.slug)

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = "blog/article_delete.html"
    context_object_name = "article"
    
    def get_success_url(self):
        messages.success(self.request, 'Article deleted successfully.')
        return reverse_lazy('home')
    
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_delete.html"
    context_object_name = "comment"

    def get_success_url(self):
        messages.success(self.request, 'Comment deleted successfully.')
        return reverse_lazy("article_detail", kwargs={"slug": self.object.article.slug})

class CategoryArticleListView(ListView):
    model = Article
    template_name = "blog/category_article_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Article.objects.filter(category=self.category).order_by('-date_added')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        articles_qs = Article.objects.filter(category=self.category).order_by('-date_added')

        paginator = Paginator(articles_qs, 6)
        page = self.request.GET.get('page')
        articles = paginator.get_page(page)

        context["articles"] = articles
        context['category'] = self.category
        return context
