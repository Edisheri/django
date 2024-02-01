from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version, Category
from django.shortcuts import render, get_object_or_404, redirect

from catalog.services import get_cached_category_list


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'object_list': get_cached_category_list(),
        'title': 'Категории товаров',
    }


# class ProductByCategoryView(ListView):
#     model = Product
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         queryset = queryset.filter(category_id=self.kwargs.get('category.id'))
#         return queryset
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super().get_context_data(*args, **kwargs)
#         category_item = Category.objects.get(pk=self.kwargs.get('pk'))
#         context_data['category_pk'] = category_item.pk
#         context_data['title'] = f'Продукты категории {category_item.name}'
#         return context_data



class ProductListView(ListView):
    model = Product
    extra_context = {
        'title': "Каталог продуктов",
        'current_user': settings.AUTH_USER_MODEL,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='moderator') or self.request.user.is_staff:
            return queryset
        return queryset.filter(is_published=True)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя клиента: {name}\nКонтактный телефон: {phone}\nСообщение: {message}')
        # with open('info.txt', 'a', encoding='utf8') as file:
        #     file.write(f'Имя клиента: {name}\nКонтактный телефон: {phone}\nСообщение: {message}\n')
    return render(request, 'catalog/contacts.html')


class ProductDetailView(DetailView):
    model = Product
    extra_context = {
        'title': "Карточка продукта",
    }


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    # permission_required = 'catalog.change_product'
    success_url = reverse_lazy('catalog:home')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        version_formset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = version_formset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = version_formset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    # permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('catalog:home')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


@login_required
@permission_required('catalog.set_is_published')
def published_toggle(request, pk):
    prod_item = get_object_or_404(Product, pk=pk)
    if prod_item.is_published:
        prod_item.is_published = False
    else:
        prod_item.is_published = True
    prod_item.save()
    return redirect(reverse('catalog:home'))
