from django.contrib import admin
from .models import Post, Comment, Vote


def make_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status='p')
    if rows_updated == 1:
        message_bit = "Published Article"
    else:
        message_bit = "Published Articles"
    modeladmin.message_user(request, "{} article {}".format(rows_updated, message_bit))


make_published.short_description = "Publish Selected Articles"


def make_draft(modeladmin, request, queryset):
    rows_updated = queryset.update(status='d')
    if rows_updated == 1:
        message_bit = "Drafed Article"
    else:
        message_bit = "Drafed Articles"
    modeladmin.message_user(request, "{} article {}".format(rows_updated, message_bit))


make_draft.short_description = "Draft Selected Articles"


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'status', 'publish')
    list_filter = ('publish', 'status')
    search_fields = ('body', )
    prepopulated_fields = {'slug': ('body',)}
    ordering = ['-status', '-publish']
    actions = [make_published, make_draft]

admin.site.register(Post, PostAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'created', 'is_reply')
    raw_id_fields = ('user', 'post', 'reply')


admin.site.register(Vote)