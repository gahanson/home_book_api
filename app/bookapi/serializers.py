from rest_framework import serializers 

from .models import Book, AvailableBook

class BookSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Book
        fields = ('url','id','title', 'remote_url')

class AvailableBookSerializer(serializers.HyperlinkedModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book', write_only=True)

    class Meta:
        model = AvailableBook
        fields = ('url', 'id', 'title', 'author', 'book', 'book_id')
