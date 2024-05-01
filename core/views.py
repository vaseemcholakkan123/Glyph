from django.views.generic import TemplateView,DetailView
from .models import *
from itertools import chain
from django.db.models import Q
from django.shortcuts import get_object_or_404




class HomePageView(TemplateView):
    template_name = 'home.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query') or self.request.POST.get('query')
        color_filter = self.request.GET.get('color')
        type_filter = self.request.GET.get('type')
        tags_filter = self.request.GET.get('tag')
        
        items = []

        # Initial queryset containing all items
        shirt_items = Shirt.objects.all()
        tshirt_items = Tshirt.objects.all()
        
        # Filter by search query
        if query:
            shirt_items = shirt_items.filter(name__icontains=query)
            tshirt_items = tshirt_items.filter(name__icontains=query)
        
        # Filter by color
        if color_filter:
            shirt_items = shirt_items.filter(color=color_filter)
            tshirt_items = tshirt_items.filter(color=color_filter)
        
        # Filter by type
        if type_filter:
            if type_filter == 'shirt':
                tshirt_items = tshirt_items.none()  # Exclude tshirts
            elif type_filter == 'tshirt':
                shirt_items = shirt_items.none()    # Exclude shirts
        
        # Filter by tags
        if tags_filter:
            tags = tags_filter.split(',')
            q_objects = Q()
            for tag_name in tags:
                q_objects |= Q(tag__name=tag_name.strip())
            shirt_items = shirt_items.filter(q_objects)
            tshirt_items = tshirt_items.filter(q_objects)
        
        # Combine the filtered results
        if type_filter:
            if type_filter == "shirt":
                items.extend(shirt_items)
            else:
                items.extend(tshirt_items)

        else:
            items.extend(chain(shirt_items, tshirt_items))


        
        context['items'] = items
        context['tags'] = Tag.objects.all()
        
        return context


    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


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
        context['tags'] = Tag.objects.all()
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


