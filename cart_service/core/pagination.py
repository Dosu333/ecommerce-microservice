from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math
from django.conf import settings

DEFAULT_PAGE = 1


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    
    def paginate_queryset(self, queryset, request, view=None):
        page_size = request.query_params.get(self.page_size_query_param, None)
        if page_size is None:
            self.page_size = queryset.count() if queryset.count() > 0 else 20 # Set page_size to total count of queryset
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        size = int(self.request.query_params.get('page_size', self.page_size))
        current_page = int(self.request.query_params.get('page', DEFAULT_PAGE))
        
        total_items = self.page.paginator.count if self.page else 0
        from_item = ((current_page - 1) * size) + 1 if total_items > 0 else 0
        to_item = min(current_page * size, total_items) if total_items > 0 else 0
        
        return Response({
            'from': from_item,
            'to': to_item,
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': total_items,
            'total_pages': math.ceil(total_items / size) if total_items > 0 else 0,
            'current_page': current_page,
            'page_size': size,
            'results': data
        })


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000
    
    def paginate_queryset(self, queryset, request, view=None):
        page_size = request.query_params.get(self.page_size_query_param, None)
        if page_size is None:
            self.page_size = queryset.count()  # Set page_size to total count of queryset
        return super().paginate_queryset(queryset, request, view)