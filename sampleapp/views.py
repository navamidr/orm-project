from django.shortcuts import render
from .models import Author,Book,Borrow
from .serializer import AuthorSerializer,BookSerializer,BorrowSerializer
from rest_framework.response import Response
from django.db.models import F, Case, When, Value, Sum, Count
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound,ValidationError
from rest_framework import status
from django.utils.timezone import now
# creation get and post

class AuthorDetail(APIView):
    def get(self,request):
        objuser = Author.objects.all()
        serializer = AuthorSerializer(objuser,many = True)
        return Response(serializer.data)
    
    
    def post(self,request):
        data=request.data
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
# book creation get and post

class BookDetail(APIView):
    def get(self,request):
        objuser = Book.objects.all()
        serializer = BookSerializer(objuser,many = True)
        return Response(serializer.data)
    
    
    def post(self,request):
        data=request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

class BookDetailView(APIView):
    def get(self, request, title):
        try:
            book = Book.objects.get(title=title)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except book.DoesNotExist:
            raise NotFound(f"Book with title '{title}' not found.")
        

class BookCopyView(APIView):
    def get(self,request,title):
        total_copy = Book.objects.filter(title=title).aggregate(total=Sum('copies'))['total']
        if total_copy is None:
            total_copy = 0
        return Response({'title':title,'total_copy':total_copy})
    
class BookAuthor(APIView):
    def get(self,request):
        books = Book.objects.values('title','author__name')
        book_data = list(books)
        return Response({'Books':book_data})
    
class BookList(APIView):
    def get(self,request):
        title = Book.objects.values_list('title',flat=True)
        titles = list(title)
        return Response({'title':titles})
    
class AuthorBook(APIView):
    def get(self,request):
        authors = Author.objects.annotate(book_count=Count('book'))
        authors_data = [{ 'id':author.id,'name':author.name,'book_count':author.book_count,}
        for author in authors ]
        return Response({'authors':authors_data})
    



class BookAvailablity(APIView):
    def get(self,request):

        books = Book.objects.annotate(
            status=Case(
                When(copies__gt=0, then=Value("Available")),
                default=Value("Out of Stock")
            )
        )
        books_data = [{'title':book.title,'status':book.status}
        for book in books]
        return Response({'books':books_data})
        



class BorrowDetail(APIView):
    def get(self,request):
        objuser = Borrow.objects.all()
        serializer = BorrowSerializer(objuser,many = True)
        return Response(serializer.data)

    def post(self,request,):
        data = request.data
        serializer = BorrowSerializer(data=data)
        if serializer.is_valid():
            book = serializer.validated_data['book']
            if book.copies <= 0:
                raise ValidationError(f"No copies available for the book: {book.title}")
            book.copies -= 1
            book.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BorrowUpdate(APIView):
    def post(self,request,title):
        
        updatebook = Borrow.objects.filter(book__title=title,return_date__isnull=True).update(return_date=now())
        if updatebook == 0:
            return Response({'message': f"No pending transactions found for the book '{title}'."}, status=200)
        
        book = Book.objects.filter(title=title).first()
        if book:
            book.copies += updatebook
            book.save()
        return Response({'message': f"Updated return date for {updatebook} transaction(s) for the book '{title}'."})




      



















