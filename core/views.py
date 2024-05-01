from django.views.generic import TemplateView,DetailView
from .models import Shirt,Tshirt
from itertools import chain
from django.db.models import Q
from django.shortcuts import get_object_or_404




class HomePageView(TemplateView):
    template_name = 'home.html'
    extra_context = {'items' : list(chain(Shirt.objects.all(), Tshirt.objects.all()))}



class ItemDetailView(DetailView):
    template_name = 'detail.html'
    model = None
    context_object_name = 'item'

    def get_queryset(self):
        item_type = self.kwargs.get('item_type')
        id = self.kwargs.get('pk')
        if item_type == 'shirt':
            self.model = Shirt
        elif item_type == 'tshirt':
            self.model = Tshirt
        return self.model.objects.filter(pk=id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object

        # Fetching tags related to the current item
        tags = item.tag.all()

        # Fetching recommended products with shared tags and same color
        recommended_shirts = Shirt.objects.filter(
            Q(tag__in=tags) | Q(color=item.color)
        ).exclude(pk=item.pk).distinct()
        recommended_tshirts = Tshirt.objects.filter(
            Q(tag__in=tags) | Q(color=item.color)
        ).exclude(pk=item.pk).distinct()

        # Combining and ordering recommended products by type
        if item.type == 'shirt':
            recommended_products = list(recommended_shirts) + list(recommended_tshirts)
        else:
            recommended_products = list(recommended_tshirts) + list(recommended_shirts)



        context['recommended_products'] = recommended_products
        return context
    

class TryOnView(TemplateView):
    template_name = 'try_on.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_type = self.kwargs.get('item_type')
        pk = self.kwargs.get('pk')
        
        if item_type == 'shirt':
            item = get_object_or_404(Shirt, pk=pk)
        elif item_type == 'tshirt':
            item = get_object_or_404(Tshirt, pk=pk)
        else:
            item = None
        
        images = []
        images.append(item.image.url)
        for item in self.get_recommends(item):
            images.append(item.image.url)

        context['images'] = images
        return context
    
    def get_recommends(self,item):

        # Fetching tags related to the current item
        tags = item.tag.all()

        # Fetching recommended products with shared tags and same color
        recommended_shirts = Shirt.objects.filter(
            Q(tag__in=tags) | Q(color=item.color)
        ).exclude(pk=item.pk).distinct()
        recommended_tshirts = Tshirt.objects.filter(
            Q(tag__in=tags) | Q(color=item.color)
        ).exclude(pk=item.pk).distinct()

        # Combining and ordering recommended products by type
        if item.type == 'shirt':
            recommended_products = list(recommended_shirts) + list(recommended_tshirts)
        else:
            recommended_products = list(recommended_tshirts) + list(recommended_shirts)

        return recommended_products


