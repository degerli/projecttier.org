from django.core.management.base import BaseCommand, CommandError
from taggit.models import Tag

class Command(BaseCommand):
    args = 'none'
    help = 'all tag names'

    def handle(self, *args, **options):

        # Get all tags
        tags = Tag.objects.all()
        count = tags.count()

        # Get all related fields to Tag
        rel = [f for f in Tag._meta.get_fields() if f.auto_created and not f.concrete]

        # Loop through tags
        for i, tag in enumerate(tags):
            # Skip tag names that are already lowercase
            if tag.name == tag.name.lower():
                continue
            # Get lowercase version of tag
            tag_lc, created = Tag.objects.get_or_create(name=tag.name.lower())
            # Loop through related fields
            for r in rel:

                # taglist = getattr(tag, r.related_name)
                taglist = getattr(r.related_model, r.field.name)
                import pdb; pdb.set_trace()
                # fn = r.field.name
                # taglist = getattr(tag, getattr(r.related_model, fn).field.name)
                for t in taglist.all():
                    setattr(t, r.field.name, tag_lc)
                    t.save()
            self.stdout.write('Lowercasing %d/%d\n' % (i+1, count))
            tag.delete()
