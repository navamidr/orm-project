
from django.urls import path
from .views import AuthorDetail,BookDetail,BookDetailView,BookCopyView,BookAuthor,BookList,AuthorBook,BookAvailablity,BorrowDetail,BorrowUpdate

urlpatterns = [
    path('authordetails/',AuthorDetail.as_view(),name='authordetails'),
    path('bookdetail/',BookDetail.as_view(),name='bookdetails'),
    path('book/<str:title>/',BookDetailView.as_view(),name='bookdetailview'),
    path('bookcopy/<str:title>/',BookCopyView.as_view(),name='bookcopy'),
    path('bookvalues/',BookAuthor.as_view(),name='bookvalues'),
    path('bookvaluelist/',BookList.as_view(),name='bookvaluelist'),
    path('bookauthor/',AuthorBook.as_view(),name='bookauthor'),
    path('bookstatus/',BookAvailablity.as_view(),name='bookstatus'),
    path('borrowdetail/',BorrowDetail.as_view(),name='borrowdetail'),
    path('borrowupdate/<str:title>/',BorrowUpdate.as_view(),name='borrowupdate'),
    # path('borrowbook/',BorrowBook.as_view(),name='borrowbook'),
]