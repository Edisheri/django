from django.views.decorators.cache import cache_page, never_cache

from catalog.apps import CatalogConfig
from django.urls import path

from catalog.views import ProductListView, contacts, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, published_toggle, CategoryListView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    # path('<int:pk>/products_by_category/', ProductByCategoryView.as_view(), name='products_by_category'),
    path('contacts/', contacts, name='contacts'),
    path('<int:pk>/view_product/', cache_page(60)(ProductDetailView.as_view()), name='view_product'),
    path('create_product/', never_cache(ProductCreateView.as_view()), name='create_product'),
    path('<int:pk>/edit_product/', ProductUpdateView.as_view(), name='edit_product'),
    path('<int:pk>/product/', ProductDeleteView.as_view(), name='delete_product'),
    path('<int:pk>/published/', published_toggle, name='published_toggle')
]
