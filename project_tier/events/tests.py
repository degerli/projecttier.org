from wagtail.tests.utils import WagtailPageTests
from .models import EventIndexPage, EventPage


class EventPageTests(WagtailPageTests):
    def test_can_create_under_event_index_page(self):
        """ EventPage can be created under an EventIndexPage """
        self.assertCanCreateAt(EventIndexPage, EventPage)
