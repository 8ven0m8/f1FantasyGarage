from django.contrib import admin
from .models import TopLeaderboard, ConstructorsLeaderboard, Calendar, Chat_post, Comments, Driver, RaceResult
import nested_admin

# Register your models here.
class TopLeaderboardAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'points']
    ordering = ['-points', '-name']

class ConstructorsLeaderboardAdmin(admin.ModelAdmin):
    list_display = ['name', 'points']
    ordering = ['-points', '-name']

class CalendarAdmin(admin.ModelAdmin):
    list_display = ['circuit', 'country', 'from_date', 'to_date', 'status']
    list_filter = ['status', 'from_date']
    search_fields = ['circuit', 'country']

class CommentsAdmin(admin.TabularInline):
    model = Comments
    extra = 1

class Chat_postAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'flair', 'title')
    inlines = [CommentsAdmin]

class ReplyInline(nested_admin.NestedTabularInline):
    model = Comments
    fk_name = 'parent'  # this shows replies to a comment
    extra = 1

class CommentInline(nested_admin.NestedTabularInline):
    model = Comments
    fk_name = 'post'
    inlines = [ReplyInline]  # allow replies inside comment
    extra = 1

class Driver_Admin(admin.ModelAdmin):
    list_display = ('name', 'team')

class RaceResult_Admin(admin.ModelAdmin):
    list_display = ('race',)
    ordering = ['-points']

admin.site.register(TopLeaderboard, TopLeaderboardAdmin)
admin.site.register(ConstructorsLeaderboard, ConstructorsLeaderboardAdmin)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Chat_post, Chat_postAdmin)
admin.site.register(Driver, Driver_Admin)
admin.site.register(RaceResult, RaceResult_Admin)
