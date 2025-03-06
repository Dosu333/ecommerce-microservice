from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math

DEFAULT_PAGE = 1

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):
        """Paginate MongoDB query results."""
        page_size = int(request.query_params.get(self.page_size_query_param, 20))
        current_page = int(request.query_params.get('page', DEFAULT_PAGE))

        total_items = queryset.collection.count_documents({}) 

        if total_items == 0:
            return []

        self.page = queryset.skip((current_page - 1) * page_size).limit(page_size)

        # Store metadata
        self.total_items = total_items
        self.page_size = page_size
        self.current_page = current_page
        
        return list(self.page)
    
    def get_paginated_response(self, data):
        """Return a structured paginated response."""
        from_item = ((self.current_page - 1) * self.page_size) + 1 if self.total_items > 0 else 0
        to_item = min(self.current_page * self.page_size, self.total_items) if self.total_items > 0 else 0

        return Response({
            'from': from_item,
            'to': to_item,
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.total_items,
            'total_pages': math.ceil(self.total_items / self.page_size) if self.total_items > 0 else 0,
            'current_page': self.current_page,
            'page_size': self.page_size,
            'results': data
        })

    def get_next_link(self):
        """Manually generate next page URL."""
        if (self.current_page * self.page_size) >= self.total_items:
            return None
        return f"?page={self.current_page + 1}&page_size={self.page_size}"

    def get_previous_link(self):
        """Manually generate previous page URL."""
        if self.current_page <= 1:
            return None
        return f"?page={self.current_page - 1}&page_size={self.page_size}"
