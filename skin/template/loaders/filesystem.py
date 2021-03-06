from django.contrib.sites.models import Site
from django.core.exceptions import SuspiciousFileOperation
from django.template.loaders.filesystem import Loader as BaseLoader
from django.utils._os import safe_join

from skin.conf import settings
from skin.template.loaders.util import get_site_skin


class Loader(BaseLoader):
    def get_template_sources(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name", when appended to each
        directory in "template_dirs". Any paths that don't lie inside one of the
        template dirs are excluded from the result set, for security reasons.
        """
        site_skin = get_site_skin(site=Site.objects.get_current(), name=settings.SKIN_NAME)
        if site_skin is not None:
            if not template_dirs:
                template_dirs = settings.TEMPLATE_DIRS
            for template_dir in template_dirs:
                try:
                    yield safe_join(template_dir, site_skin.path, template_name)
                except SuspiciousFileOperation:
                    # The joined path was located outside of this template_dir
                    # (it might be inside another one, so this isn't fatal).
                    pass
        else:
            pass
