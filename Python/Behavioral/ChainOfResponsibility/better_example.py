from __future__ import annotations
from typing import Optional, List

from abc import ABC, abstractmethod


class ComponentWithContextualHelpInterface(ABC):
    
    @abstractmethod
    def show_help(self):
        pass


class AbstractComponent(ComponentWithContextualHelpInterface):
    
    tooltip_text: Optional[str] = None
    _container: Optional[AbstractContainer] = None
    
    def show_help(self):
        if self.tooltip_text is not None:
            print(f'Showing tooltip: "{self.tooltip_text}"')
        elif self._container is not None:
            self._container.show_help()
        else:
            print('There is no hint in any component level !!!')


class AbstractContainer(AbstractComponent):
    
    _children: List[AbstractComponent] = []
    
    def add(self, child: AbstractComponent):
        self._children.append(child)
        child._container = self


class Button(AbstractComponent):
    pass


class Panel(AbstractContainer):
    
    modal_help_text: Optional[str] = None
    
    def show_help(self):
        if self.modal_help_text is not None:
            print(f'Showing a modal window with the help text: "{self.modal_help_text}"')
        else:
            return super().show_help()


class Dialog(AbstractContainer):
    
    wiki_page_url: Optional[str] = None
    
    def show_help(self):
        if self.wiki_page_url is not None:
            print(f'Opening the wiki help page: "{self.wiki_page_url}"')
        else:    
            return super().show_help()


# Client code
if __name__ == "__main__":
    
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
    
    def print_all():
        print('\nDialog help:')
        dialog.show_help()
        print('\nPanel help:')
        panel.show_help()
        print('\nButton help (OK):')
        ok.show_help()
        print('\nButton help (CANCEL):')
        cancel.show_help()
    
    print_all()

    print('\n\nDeleting wiki_page_url ...')
    dialog.wiki_page_url = None
    print_all()
    
    print('\n\nDeleting modal_help_text ...')
    dialog.wiki_page_url = "http://..."
    panel.modal_help_text = None
    print_all()
    
    print('\n\nDeleting OK button tooltip_text ...')
    dialog.wiki_page_url = "http://..."
    panel.modal_help_text = "This panel does ..."
    ok.tooltip_text = None
    print_all()
    
    print('\n\nDeleting "OK button tooltip_text" and "panel modal_help_text" ...')
    panel.modal_help_text = None
    ok.tooltip_text = None
    print_all()
