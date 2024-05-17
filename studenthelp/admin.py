from django.contrib import admin
from .models import Post
from .models import Comment
from .models import Like
from .models import Housing
from .models import Transport
from .models import Event
from .models import Internship
from .models import Recommendation

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Housing)
admin.site.register(Transport)
admin.site.register(Event)
admin.site.register(Internship)
admin.site.register(Recommendation)


