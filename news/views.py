from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

# Create your views here.
from news.models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.core.paginator import Paginator

from django.contrib import messages


def user_logout(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Все ок')
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, 'Error')
    else:
        form = UserRegisterForm()

    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error')
    else:
        form = UserLoginForm()

    return render(request, 'news/login.html', {'form': form})


class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'nws'
    mixin_prop = 'hello world'
    paginate_by = 3

    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'nws'
    allow_empty = False

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


class ViewNews(DetailView):
    model = News
    # pk_url_kwarg = 'news_id'
    context_object_name = 'item'


def test1(request):
    objects = ['john', 'paul', 'george', 'ringo', 'asdasdasd0', 'asadsdasss00', 'john', 'paul', 'george', 'ringo',
               'asdasdasd0', 'asadsdasss00']
    pag = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)
    page_obj = pag.get_page(page_num)
    return render(request, 'news/test1.html', {'page_obj': page_obj, })


class CreateNews(LoginRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/add_news.html'
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        print(form)
        print(form.cleaned_data)
        return self.render_to_response(self.get_context_data(form=form))


def index(request):
    nws = News.objects.all()
    context = {
        'nws': nws,
        'title': 'список',
    }
    return render(request, 'news/index.html', context)


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)

    category = Category.objects.get(pk=category_id)
    context = {
        'nws': news,
        'category': category,
    }
    return render(request, 'news/category.html', context)


def view_news(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/home_news_list.html', {'news_item': news_item})


def add_news(request):
    form = NewsForm()
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # news = News.objects.create(**form.cleaned_data)
            news = form.save()
            return redirect(news)
    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', {'form': form})


def test(request):
    print(request)
    return HttpResponse('test')
