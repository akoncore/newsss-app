from django.db.models import (
    Model,
    CharField,
    IntegerField,
    BooleanField,
    ForeignKey,
    CASCADE,
    TextField,
    DateTimeField,
    Index
) 
from django.conf import settings


class Comment(Model):
    post = ForeignKey(
        'main.Post',
        on_delete=CASCADE,
        related_name='comments'
    )
    author = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name='comments'
    )
    parent = ForeignKey(
        'self',
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    content = TextField()
    is_active = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'comments'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']
        indexes =[
            Index(fields=['post','-created_at']),
            Index(fields=['author','-created_at']),
            Index(fields=['parent','-created_at'])
        ]
        
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    
    @property
    def replies_count(self):
        return self.replies.filter(is_active = True).count()
    
    @property
    def is_reply(self):
        return self.parent is not None
    