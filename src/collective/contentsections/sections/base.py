from collective.contentsections import _
from plone import schema
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from Products.Five.browser import BrowserView
from zope.interface import implementer


class ISection(model.Schema):
    """Shared base marker interface and schema for Sections"""

    title = schema.TextLine(
        title=_("Section title"),
        required=True,
    )
    hide_title = schema.Bool(
        title=_("Hide section title in page"),
        required=False,
        default=False,
    )
    background_image = NamedBlobImage(
        title="Image de fond",
        required=False,
    )
    css_width = schema.Choice(
        title="Largeur de la section",
        required=False,
        vocabulary="collective.contentsections.SectionWidths",
    )
    css_classes = schema.TextLine(
        title="Classes CSS",
        required=False,
    )

    model.fieldset(
        "layout",
        label="Layout",
        fields=["hide_title", "css_width", "background_image", "css_classes"],
    )


@implementer(ISection)
class Section(Container):
    """Shared base class for Sections"""

    def canSetDefaultPage(self):
        return False

    @property
    def main_editing_view_name(self):
        return "@@edit"


class SectionView(BrowserView):
    """Section view"""

    def __call__(self):
        page = self.context.__parent__
        url = f"{page.absolute_url()}#section-{self.context.id}"
        self.request.response.redirect(url)


def reindex_parent_page(section, event):
    page = section.__parent__
    if page is not None:
        page.reindexObject()
