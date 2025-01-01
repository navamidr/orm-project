from rest_framework import serializers
from sampleapp.models import Author,Book,Borrow

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields =  '__all__'

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.name')  

    class Meta:
        model = Book
        fields =  '__all__'

class BorrowSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source='book.title')

    class Meta:
        model = Borrow
        fields = '__all__'

