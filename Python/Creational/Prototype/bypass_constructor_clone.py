"""
Educational Prototype example focused on constructor bypass and explicit clone initialization.

Design goal:
    Show that a Prototype in Python does not rely on constructors to create new
    objects. Cloning must copy internal state faithfully and then apply
    clone-specific initialization that a constructor would normally provide.

Classical object-oriented languages:
    Languages such as C++ and Java commonly use copy constructors for this task.
    The copy constructor of every class in an inheritance hierarchy must
    participate so that the full object state is reproduced correctly.

Python copy protocol:
    Python has no copy constructors. Objects are duplicated with
    copy.copy (shallow) and copy.deepcopy (deep). Classes customize the
    behavior by implementing __copy__ and __deepcopy__; this file relies on
    the default deepcopy and keeps custom protocol hooks in
    custom_copy_protocol.py.

Allocation and initialization:
    In Python, object allocation goes through __new__ and state setup goes
    through __init__. During cloning, __new__ allocates the duplicate but
    __init__ is bypassed, so copied instances keep the exact state of the
    original. Constructor design therefore rarely determines how a Python
    Prototype is implemented.

Prototype-specific initialization:
    Some state is inherently per-instance, such as labels, counters, or
    timestamps that must not be shared between the source and its clone.
    An explicit initialization operation is needed when clone-specific state
    must be reset after the copy. Here clone() performs a deepcopy and then
    calls initialize_clone(), which resets that state without invoking
    __init__.

Trade-offs
    Explicit clone initialization keeps constructors simple and avoids
    re-running expensive construction steps for every clone. The cost is an
    additional method that must be kept in sync with the fields it resets;
    forgetting to update it can leave stale clone-specific state.
"""

import copy

from collections.abc import Sequence


class ReportTemplate:
    """
    Report template prototype demonstrating constructor bypass during cloning.
    Prototype role providing isolated cloned instances without re-executing __init__.

    Trade-offs
        The deepcopy preserves all internal state, but any new
        clone-specific field must also be added to initialize_clone();
        otherwise clones would inherit values meant to be per-instance.
    """

    constructor_call_count: int = 0

    def __init__(self, title: str, sections: Sequence[str]) -> None:
        """
        Initialize the source report template and increment constructor invocation counter.
        """

        self.title = title
        self.sections: tuple[str, ...] = tuple(sections)
        self.layout: str = f"{len(self.sections)} sections, single column"
        self.instance_label: str = "source"
        self.render_count: int = 0
        ReportTemplate.constructor_call_count += 1


    def render(self) -> str:
        """
        Simulate rendering the report, mutating the per-instance render count.
        """

        self.render_count += 1
        return (
            f"Report '{self.title}' [{self.instance_label}]"
            f" layout={self.layout} renders={self.render_count}"
        )


    def clone(self) -> "ReportTemplate":
        """
        Create a deep copy of the template and reset clone-specific instance state.
        Bypasses __init__ execution completely while ensuring clean state initialization.
        """

        cloned_template = copy.deepcopy(self)
        cloned_template.initialize_clone()
        return cloned_template


    def initialize_clone(self) -> None:
        """
        Explicitly reset per-instance state without invoking constructor logic.
        """

        self.instance_label = "clone"
        self.render_count = 0


    def describe(self) -> str:
        """
        Return structured representation of internal state for inspection and logging.
        """

        return (
            f"ReportTemplate(title={self.title!r}, sections={self.sections!r},"
            f" instance_label={self.instance_label!r},"
            f" render_count={self.render_count})"
        )


if __name__ == "__main__":
    source_template = ReportTemplate("Quarterly Summary", ["Intro", "Findings", "Next steps"])
    first_render = source_template.render()
    print(f"source render: {first_render}")

    raw_copy = copy.deepcopy(source_template)
    managed_clone = source_template.clone()

    assert ReportTemplate.constructor_call_count == 1
    assert raw_copy.instance_label == "source"
    assert raw_copy.render_count == source_template.render_count
    assert managed_clone.instance_label == "clone"
    assert managed_clone.render_count == 0

    managed_clone_render = managed_clone.render()
    print(f"managed clone render: {managed_clone_render}")
    print(f"source: {source_template.describe()}")
    print(f"raw deepcopy copy: {raw_copy.describe()}")
    print(f"managed clone: {managed_clone.describe()}")
