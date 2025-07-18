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

# An inline admin to manage results directly from the Calendar page
class RaceResultInline(admin.TabularInline):
    model = RaceResult
    # Fields to display in the inline form
    fields = ('driver', 'points', 'status')
    # Provides extra empty slots to add new results easily
    extra = 3
    # Optional: adds a raw_id_fields widget for the driver, useful if you have many drivers
    raw_id_fields = ('driver',)


class CalendarAdmin(admin.ModelAdmin):
    list_display = ['circuit', 'country', 'from_date', 'to_date', 'status']
    list_filter = ['status', 'from_date']
    search_fields = ['circuit', 'country']
    inlines = [RaceResultInline]

class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'team')
    search_fields = ('name', 'team')
    
class RaceResultAdmin(admin.ModelAdmin):
    list_display = ('race', 'get_race_date', 'driver', 'points', 'status')
    list_filter = ('race__circuit', 'driver__team', 'status')
    search_fields = ('race__circuit', 'driver__name')
    
    # Correctly order by the date on the related Calendar model, then by points
    ordering = ('race__from_date', '-points')

    # Custom method to display the race date in the list view
    def get_race_date(self, obj):
        return obj.race.from_date
    
    get_race_date.short_description = 'Race Date'
    get_race_date.admin_order_field = 'race__from_date' # Makes the column sortable

admin.site.register(TopLeaderboard, TopLeaderboardAdmin)
admin.site.register(ConstructorsLeaderboard, ConstructorsLeaderboardAdmin)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Chat_post, Chat_postAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(RaceResult, RaceResultAdmin)
