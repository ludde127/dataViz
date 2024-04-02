from wagtail.contrib.sitemaps import Sitemap

from study_notes.models import NotePageTag
from users.models import NormalUser


class UserSitemap(Sitemap):
    def items(self):
        return (NormalUser
                .objects
                .all()
                .order_by('-user__date_joined')
                )


class TagSitemap(Sitemap):
    def items(self):
        return (NotePageTag
                .objects
                .order_by("-tag__name")
                .distinct("tag__name")
                )
