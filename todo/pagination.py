from rest_framework.pagination import PageNumberPagination


from todo.views import * 
class PaginationDemo(PageNumberPagination):
    page_size=2
    max_page_size=3
    page_size_query_param="page"

