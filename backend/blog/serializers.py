from rest_framework import serializers
from .models import Post, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')
    featured_image = serializers.ImageField(use_url=True)
    category = CategorySerializer()  # Use a nested serializer to return category details

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'featured_image', 'category', 'author', 'created_at', 'updated_at', 'published']
