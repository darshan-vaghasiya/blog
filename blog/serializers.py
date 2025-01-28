from rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    """defined PostSerializer to use blog post store, update etc."""
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'category', 'like_counts', 'comment_counts', 'view_counts',
                  'created_at']

    def validate_title(self, value):
        """
        Validate that the title is unique for the author.
        """
        author = self.context['request'].user
        if self.instance:
            # If this is an update, exclude the current instance from the check.
            if Post.objects.filter(title=value, author=author).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("You have already created a post with this title.")
        else:
            # If this is a new post creation
            if Post.objects.filter(title=value, author=author).exists():
                raise serializers.ValidationError("You have already created a post with this title.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']
        extra_kwargs = {
            'post': {'write_only': True},
        }

    def create(self, validated_data):
        author = self.context['request'].user
        post = validated_data.get('post')
        existing_comment = Comment.objects.filter(post=post, author=author).first()

        if existing_comment:
            existing_comment.content = validated_data.get('content', existing_comment.content)
            existing_comment.save()
            return existing_comment
        else:
            return super().create(validated_data)


class PostStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['like_counts', 'comment_counts', 'view_counts']
