# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtaildocs.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0028_merge'),
        ('standard', '0003_auto_20160620_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='StandardPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, to='wagtailcore.Page', primary_key=True, serialize=False, parent_link=True)),
                ('introductory_headline', models.TextField(help_text='Introduce the topic of this page in 1-3 sentences.')),
                ('overview', wagtail.wagtailcore.fields.RichTextField(help_text='Give a general overview of what this topic is about. Limit yourself to 3 paragraphs.')),
                ('body', wagtail.wagtailcore.fields.StreamField((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='fa-paragraph')), ('heading', wagtail.wagtailcore.blocks.TextBlock(template='blocks/heading.html', icon='fa-header')), ('smaller_heading', wagtail.wagtailcore.blocks.TextBlock(template='blocks/smaller_heading.html', icon='fa-header')), ('smallest_heading', wagtail.wagtailcore.blocks.TextBlock(template='blocks/smallest_heading.html', icon='fa-header')), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.TextBlock(required=False))))), ('download', wagtail.wagtaildocs.blocks.DocumentChooserBlock(icon='fa-download')), ('accordion', wagtail.wagtailcore.blocks.StructBlock((('panels', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.TextBlock(help_text='The headline to display when the accordion panel is closed.')), ('body', wagtail.wagtailcore.blocks.RichTextBlock(help_text='The inner content of this accordion panel. It is initially hidden.'))), label='Panel'))),))), ('notice', wagtail.wagtailcore.blocks.StructBlock((('message', wagtail.wagtailcore.blocks.RichTextBlock(help_text='Write the message text.')), ('indicator', wagtail.wagtailcore.blocks.ChoiceBlock(help_text='Choose what type of notice this is.', required=False, choices=[('', 'Standard'), ('success', 'Success'), ('alert', 'Alert'), ('warning', 'Warning')])))))))),
                ('listing_abstract', models.TextField(help_text='Give a brief blurb (about 1 sentence) of what this topic is about. It will appear on other pages that refer to this one.')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]