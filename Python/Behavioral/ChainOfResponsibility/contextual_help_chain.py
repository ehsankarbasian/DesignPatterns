from __future__ import annotations
from typing import List, Optional

from abc import ABC, abstractmethod


class ComponentWithContextualHelpInterface(ABC):

    @abstractmethod
    def show_help(self) -> None:
        raise NotImplementedError


class AbstractComponent(ComponentWithContextualHelpInterface):
    """
    Design goal:
        Provide contextual help for UI-like components using parent delegation as a chain.
    Key decisions:
        Encapsulate tooltip and parent reference in instance state to avoid class-level leaks;
        delegate help lookup upwards to parent container if local tooltip is missing;
        print fallback message when reaching root without help text.
    Trade-offs:
        Couples contextual help resolution to the structural containment hierarchy.
    """

    def __init__(self, tooltip_text: Optional[str] = None) -> None:
        self.tooltip_text: Optional[str] = tooltip_text
        self._parent: Optional[AbstractContainer] = None

    def show_help(self) -> None:
        if self.tooltip_text is not None:
            print(f'Showing tooltip: "{self.tooltip_text}"')
            return

        if self._parent is not None:
            self._parent.show_help()
            return

        print("No contextual help is available for this component.")


class AbstractContainer(AbstractComponent):
    """
    Design goal:
        Represent composite components that can nest children and chain help requests.
    Key decisions:
        Initialize empty instance list for children and bind parent reference upon addition.
    Trade-offs:
        Maintains two-way association between containers and child components.
    """

    def __init__(self, tooltip_text: Optional[str] = None) -> None:
        super().__init__(tooltip_text)
        self._children: List[AbstractComponent] = []

    def add(self, child: AbstractComponent) -> None:
        self._children.append(child)
        child._parent = self


class Button(AbstractComponent):
    pass


class Panel(AbstractContainer):
    """
    Design goal:
        Provide modal help text specific to panel containers before parent delegation.
    Key decisions:
        Store modal_help_text in instance state and resolve before delegating to superclass.
    Trade-offs:
        Prioritizes modal help over parent container resolution.
    """

    def __init__(
        self,
        tooltip_text: Optional[str] = None,
        modal_help_text: Optional[str] = None,
    ) -> None:
        super().__init__(tooltip_text)
        self.modal_help_text: Optional[str] = modal_help_text

    def show_help(self) -> None:
        if self.modal_help_text is not None:
            print(f'Showing a modal window with the help text: "{self.modal_help_text}"')
            return
        super().show_help()


class Dialog(AbstractContainer):
    """
    Design goal:
        Provide wiki page URL help for dialog windows as highest structural container.
    Key decisions:
        Store wiki_page_url in instance state and intercept show_help before ancestor chain.
    Trade-offs:
        Wiki page help resolution supersedes nested component delegation.
    """

    def __init__(
        self,
        tooltip_text: Optional[str] = None,
        wiki_page_url: Optional[str] = None,
    ) -> None:
        super().__init__(tooltip_text)
        self.wiki_page_url: Optional[str] = wiki_page_url

    def show_help(self) -> None:
        if self.wiki_page_url is not None:
            print(f'Opening the wiki help page: "{self.wiki_page_url}"')
            return
        super().show_help()


def build_sample_ui() -> tuple[Dialog, Panel, Button, Button]:
    dialog = Dialog()
    panel = Panel()
    ok = Button()
    cancel = Button()

    panel.add(ok)
    panel.add(cancel)
    dialog.add(panel)

    dialog.wiki_page_url = "http://..."
    panel.modal_help_text = "This panel does ..."
    ok.tooltip_text = "This is an OK button that does ..."
    cancel.tooltip_text = "This is a CANCEL button that does ..."

    return dialog, panel, ok, cancel


def print_all(dialog: Dialog, panel: Panel, ok: Button, cancel: Button) -> None:
    print("\nDialog help:")
    dialog.show_help()
    print("\nPanel help:")
    panel.show_help()
    print("\nButton help (OK):")
    ok.show_help()
    print("\nButton help (CANCEL):")
    cancel.show_help()


if __name__ == "__main__":
    dialog, panel, ok, cancel = build_sample_ui()

    print_all(dialog, panel, ok, cancel)

    print("\n\nDeleting wiki_page_url ...")
    dialog.wiki_page_url = None
    print_all(dialog, panel, ok, cancel)

    print("\n\nDeleting modal_help_text ...")
    dialog.wiki_page_url = "http://..."
    panel.modal_help_text = None
    print_all(dialog, panel, ok, cancel)

    print("\n\nDeleting OK button tooltip_text ...")
    dialog.wiki_page_url = "http://..."
    panel.modal_help_text = "This panel does ..."
    ok.tooltip_text = None
    print_all(dialog, panel, ok, cancel)

    print('\n\nDeleting "OK button tooltip_text" and "panel modal_help_text" ...')
    panel.modal_help_text = None
    ok.tooltip_text = None
    print_all(dialog, panel, ok, cancel)
