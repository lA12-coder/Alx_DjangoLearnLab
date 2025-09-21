from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = "Create initial groups (Editors, Viewers, Admins) and assign permissions."

    def handle(self, *args, **options):
        # get content type for Book model
        ct = ContentType.objects.get_for_model(Book)

        # fetch custom permissions by codename (they exi
        # st after migrations)
        perms = {}
        for codename in ['can_view', 'can_create', 'can_edit', 'can_delete']:
            try:
                perms[codename] = Permission.objects.get(content_type=ct, codename=codename)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Permission {codename} not found. Run migrations first."))
                return

        # Create or update groups
        viewers, _ = Group.objects.get_or_create(name='Viewers')
        editors, _ = Group.objects.get_or_create(name='Editors')
        admins, _ = Group.objects.get_or_create(name='Admins')

        # Assign permissions
        viewers.permissions.set([perms['can_view']])

        editors.permissions.set([perms['can_view'], perms['can_create'], perms['can_edit']])

        # Admins get all custom permissions plus Django model-level perms if desired
        admins.permissions.set([perms['can_view'], perms['can_create'], perms['can_edit'], perms['can_delete']])

        self.stdout.write(self.style.SUCCESS('Groups created/updated: Viewers, Editors, Admins'))
