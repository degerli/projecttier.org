import json
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler
from wagtail.admin.rich_text.converters.contentstate import ContentstateConverter
from wagtail.core import hooks
from wagtail.core.templatetags.wagtailcore_tags import richtext
from draftjs_exporter.dom import DOM
from django.urls import path, include
from . import urls


# Register the app URLs Wagtail's /admin/
# https://docs.wagtail.io/en/latest/reference/hooks.html#register-admin-urls
@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        path('draftailmodal/', include(urls))
    ]


# https://docs.wagtail.io/en/latest/reference/hooks.html#register-rich-text-features
@hooks.register('register_rich_text_features')
def register_tip_feature(features):
    features.default_features.append('tip')
    """
    Registering the `tip` feature, which uses the `tip` Draft.js entity type,
    and is stored as HTML with a `<span data-tip>` tag.
    """
    feature_name = 'tip'
    type_ = 'TIP'

    control = {
        'type': type_,
        'label': 'ⓘ',
        'description': 'Tip',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.EntityFeature(
            control,
            js=['js/tip.js'],
            css={'all': ['css/tip.css']}
        )
    )

    features.register_converter_rule('contentstate', feature_name, {
        # Note here that the conversion is more complicated than for blocks and inline styles.
        'from_database_format': {'span[data-tip]': TipEntityElementHandler(type_)},
        'to_database_format': {'entity_decorators': {type_: tip_entity_decorator}},
    })


def tip_entity_decorator(props):
    """
    Draft.js ContentState to database HTML.
    Converts the tip entities into a span tag.
    """
    tip = props['tip']

    # HACK: Convert to JSON string if necessary.
    # Without this it's inconsistent for some reason.
    if type(tip) is dict:
        tip = json.dumps(tip)

    tip_html = ContentstateConverter(features=[
        'h2', 'h3', 'bold', 'italic', 'ol', 'ul', 'link', 'image', 'embed'
    ]).to_database_format(tip)
    tip_html = richtext(tip_html)  # apply |richtext filter
    return DOM.create_element('span', {
        'data-tip': tip_html,
    }, props['children'])


class TipEntityElementHandler(InlineEntityElementHandler):
    """
    Database HTML to Draft.js ContentState.
    Converts the span tag into a tip entity, with the right data.
    """
    mutability = 'IMMUTABLE'

    def get_attribute_data(self, attrs):
        """
        Take the ``tip`` value from the ``data-tip`` HTML attribute.
        """
        tip_json = ContentstateConverter(features=[
            'h2', 'h3', 'bold', 'italic', 'ol', 'ul', 'link', 'image', 'embed'
        ]).from_database_format(attrs['data-tip'])
        return {
            'tip': json.loads(tip_json),
        }
