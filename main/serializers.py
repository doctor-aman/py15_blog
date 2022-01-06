from rest_framework import serializers

from main.models import Category, Post, PostImage, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()  # ДЛЯ СОЗДАНИЯ метода get_image
    user = serializers.CharField(source='user.name')

    class Meta:
        model = Post
        fields = ['id', 'title', 'user', 'created_at', 'image']

    def get_image(self, post):
        first_image = post.pics.first()
        if first_image and first_image.image:
                return first_image.image.url  # если image есть вернет URL
        return ''  # если image то вернет пустую строку


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(),
                                              write_only=True)

    class Meta:
        model = Comment
        exclude =['user']

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        return super().create(validated_data)


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['image']


class PostSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False), write_only=True,
                                   required=False)

    class Meta:
        model = Post
        exclude = ['user']

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        images = validated_data.pop('images', [])  # по default пустой список
        post = super().create(validated_data)
        for image in images:
            PostImage.objects.create(post=post, image=image)
        return post

    def update(self, instance, validated_data):
        images = validated_data.pop('images', [])  # по default пустой список
        if images:
            for image in images:
                PostImage.objects.create(post=instance, image=image)
        return super().update(instance, validated_data)

    def to_representation(self, instance):  # выходные данные сериалайзера
        representation = super().to_representation(instance)
        representation['images'] = PostImageSerializer(instance.pics.all(), many=True).data  # Сериализируем через
                                                                                                # PostImageSerializer
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return representation
