from __future__ import unicode_literals
from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from wagtail.snippets.models import register_snippet
import datetime


################################################################
#
# DO NOT ADD NEW CODE TO THIS APP.
# THIS IS PRESERVED FOR POSTERITY.
#
# ALL NEW CODE TAKES PLACE IN THE `network` APP AND THIS APP
# HAS BEEN DISABLED.
#
#################################################################


@register_snippet
class PersonCategory(models.Model):
    title = models.CharField(max_length=255)
    order = models.IntegerField(
        null=True, blank=True,
        help_text="Lower numbers are shown first. If left blank, it will "
                  "show up at the end."
    )

    def __str__(self):              # __unicode__ on Python 2
        # We're returning the string that populates the snippets screen. Note it returns as plain-text
        return self.title

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'People category'
        verbose_name_plural = 'People categories'


class PersonPage(Page):
    location = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    main_job_title = models.TextField(blank=True)
    academic_title = models.TextField(blank=True)
    introductory_headline = models.TextField(help_text='Introduce the topic of this page in 1-3 sentences.', blank=True)
    biography = RichTextField(blank=True)
    website = models.URLField(max_length=255, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    image_credit = models.CharField(max_length=255, blank=True, help_text="Add credit for photo if necessary. Note: add only their name 'Photo courtesy of' is hardcoded")

    @property
    def categories(self):
        categories = [
            n.category for n in self.person_category_relationship.all()
        ]
        return categories

    parent_page_types = ['PersonIndexPage']

    search_fields = Page.search_fields + [
        index.SearchField('introductory_headline'),
        index.SearchField('biography'),
        index.SearchField('location'),
        index.SearchField('phone'),
        index.SearchField('email'),
        index.SearchField('main_job_title'),
        index.SearchField('academic_title')
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('location'),
                FieldPanel('phone'),
                FieldPanel('email'),
                FieldPanel('website'),
            ],
            heading="Contact Information",
            classname="collapsible collapsed"
        ),
        FieldPanel('main_job_title'),
        FieldPanel('academic_title'),
        FieldPanel('introductory_headline'),
        FieldPanel('biography'),
        MultiFieldPanel(
            [
                ImageChooserPanel('image'),
                FieldPanel('image_credit'),
            ],
            heading="Person image"
        ),
        InlinePanel('person_category_relationship', label="Categories"),
    ]

    @property
    def person_index(self):
        # Find closest ancestor which is a blog index
        return self.get_ancestors().type(PersonIndexPage).last()

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'


class FellowPersonPage(PersonPage):
    YEAR_CHOICES = []
    for r in range(2010, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append(
            (r, "{}–{}".format(r, r + 1))
        )

    fellowship_year = models.IntegerField(
        choices=YEAR_CHOICES,
        default=datetime.datetime.now().year,
    )

    content_panels = PersonPage.content_panels + [
        FieldPanel('fellowship_year'),
    ]

    template = 'people/person_page.html'

    class Meta:
        verbose_name = 'fellow'
        verbose_name_plural = 'fellows'


class PersonIndexPage(Page):
    introductory_headline = models.TextField(help_text='Introduce the topic of this page in 1-3 sentences.', blank=True)
    listing_abstract = models.TextField(help_text='Give a brief blurb (about 1 sentence) of what this topic is about. It will appear on other pages that refer to this one.')
    body = RichTextField(blank=True)

    @property
    def fellowship_years(self):
        fellowship_years = {}
        fellows = self.get_children().live().type(FellowPersonPage).specific()
        for fellow in fellows:
            year = fellow.fellowship_year
            try:
                fellowship_years[year]
            except KeyError:
                fellowship_years[year] = []
            fellowship_years[year].append(fellow)
        return sorted(fellowship_years.items(), reverse=True)

    parent_page_types = [
        'home.HomePage',
        'standard.StandardIndexPage',
        'PersonIndexPage'
    ]

    subpage_types = ['PersonPage', 'FellowPersonPage']

    search_fields = Page.search_fields + [
        index.SearchField('introductory_headline'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('introductory_headline'),
        FieldPanel('listing_abstract'),
        FieldPanel('body'),
    ]

    @property
    def people(self):
        people = PersonPage.objects.live().child_of(self)
        return people

    @property
    def sections(self):
        sections = []
        categories = PersonCategory.objects.all()
        for category in categories:
            # Get people for category
            people = self.people.filter(person_category_relationship__category__pk=category.pk)
            if people:
                sections.append({
                    "category": category,
                    "people": people
                })
        return sections

    class Meta:
        verbose_name = 'Person List Page'


class PersonCategoryRelationship(models.Model):
    person = ParentalKey(
        'PersonPage',
        related_name='person_category_relationship',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        'PersonCategory', related_name='+', on_delete=models.CASCADE
    )

    panels = [FieldPanel('category')]


# This is basically just a different view of a PersonIndexPage
class FellowshipsIndexPage(Page):
    related_person_index_page = models.ForeignKey(
        'wagtailcore.Page',
        on_delete=models.PROTECT,
        related_name='+',
        help_text='Select the person index page to pull the list of fellows from.'
    )
    introductory_headline = models.TextField(help_text='Introduce the topic of this page in 1-3 sentences.', blank=True)
    listing_abstract = models.TextField(help_text='Give a brief blurb (about 1 sentence) of what this topic is about. It will appear on other pages that refer to this one.')
    body = RichTextField(blank=True)

    @property
    def fellowship_years(self):
        return self.related_person_index_page.fellowship_years

    content_panels = Page.content_panels + [
        PageChooserPanel('related_person_index_page', 'people.PersonIndexPage'),
        FieldPanel('introductory_headline'),
        FieldPanel('listing_abstract'),
        FieldPanel('body')
    ]
