from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import CursorPagination


# 基础分页器
class MyPageNumberPagination(PageNumberPagination):
    page_size = 3# 每页数量
    max_page_size = 5# 可指定最大分页数
    page_size_query_param = "page_size"# 指定前端修改每页分页数量
    page_query_param = "page"# 获取第几页的对象
# 偏移分页器
class MyLimitPagination(LimitOffsetPagination):
    default_limit = 3    # 默认获取的每页数量
    limit_query_param = "limit"    # 前端修改每页数量
    offset_query_param = "offset"    # 偏移量
    max_limit = 5    # 每页最大数量
# 游标分页器
class MyCoursePagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 5
    ordering = "-price"
