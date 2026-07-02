from __future__ import annotations

from pyscrape.mixins import SelectionMixin


def test_selection_mixin_css_delegates_to_cssselect() -> None:
    class Selector(SelectionMixin):
        def cssselect(self, css):  # noqa: ANN001
            return [css]

    assert Selector().css("a.link") == ["a.link"]
