from rest_framework import pagination

class CustomPagination(pagination.PageNumberPagination):
    page_size = 40
    page_size_query_param = 'size'
    #max_page_size = 3
    page_query_param = 'page'