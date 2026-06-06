from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DefaultPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        page_size = request.query_params.get(self.page_size_query_param)

        if page_size == '-1':
            return None

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Lista de resultados',
            'data': data,
            'pagination': {
                'current_page': self.page.number,
                'page_size': self.get_page_size(self.request),
                'total_pages': self.page.paginator.num_pages,
                'total_items': self.page.paginator.count,
            },
        }, status=status.HTTP_200_OK)
