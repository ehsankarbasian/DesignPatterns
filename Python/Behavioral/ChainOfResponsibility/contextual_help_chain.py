from __future__ import annotations
from typing import Optional, List

from abc import ABC, abstractmethod


class ComponentWithContextualHelpInterface(ABC):
    
    @abstractmethod
    def show_help(self) -> None:
        raise NotImplementedError


class AbstractComponent(ComponentWithContextualHelpInterface):
    """
    Design goal:
    Provide contextual help for UI-like components, using parent delegation as a chain.

    Key decisions:
    - Each component optionally owns a tooltip text.
    - If a component cannot provide help, it delegates to its parent container.
    - The chain terminates with a clear fallback message when no help is available.

    Trade-offs:
    - Delegation via a parent pointer is simple and matches UI containment,
      but it couples help resolution to the containment tree structure.
    """

    tooltip_text: Optional[str] = None
    _parent: Optional[AbstractContainer] = None

    def show_help(self) -> None:
        if self.tooltip_text is not None:
            print(f'Showing tooltip: "{self.tooltip_text}"')
            return

        if self._parent is not None:
            self._parent.show_help()
            return

        print("No contextual help is available for this component.")


class AbstractContainer(AbstractComponent):

    def __init__(self) -> None:
        self._children: List[AbstractComponent] = []

    def add(self, child: AbstractComponent) -> None:
        self._children.append(child)
        child._parent = self


class Button(AbstractComponent):
    pass


class Panel(AbstractContainer):

    modal_help_text: Optional[str] = None

    def show_help(self) -> None:
        if self.modal_help_text is not None:
            print(f'Showing a modal window with the help text: "{self.modal_help_text}"')
            return
        super().show_help()


class Dialog(AbstractContainer):

    wiki_page_url: Optional[str] = None

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

    print('\n\nDeleting wiki_page_url ...')
    dialog.wiki_page_url = None
    print_all(dialog, panel, ok, cancel)

    print('\n\nDeleting modal_help_text ...')
    dialog.wiki_page_url = "http://..."
    panel.modal_help_text = None
    print_all(dialog, panel, ok, cancel)

    print('\n\nDeleting OK button tooltip_text ...')
    dialog.wiki_page_url = "http://..."
    panel.modal_help_text = "This panel does ..."
    ok.tooltip_text = None
    print_all(dialog, panel, ok, cancel)

    print('\n\nDeleting "OK button tooltip_text" and "panel modal_help_text" ...')
    panel.modal_help_text = None
    ok.tooltip_text = None
    print_all(dialog, panel, ok, cancel)
