from rest_framework import serializers
from .models import Book, Author

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    # Custom validation to ensure the publication_year is not in the future
    def validate(self, data):
        # Validate title length
        if len(data['title']) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        
        # Validate publication year
        if data['publication_year'] > 2024:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        
        return data

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True) # Nest the BookSerializer to represent related books
    class Meta:
        model = Author
        fields = ["name", "books"]