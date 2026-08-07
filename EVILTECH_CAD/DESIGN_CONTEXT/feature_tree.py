"""Feature-tree presentation helpers for EvilTech CAD."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class FeatureTreeNode:
    """A node in a design-context feature tree."""

    name: str
    node_type: str
    children: list["FeatureTreeNode"] = field(default_factory=list)

    def add_child(self, node: "FeatureTreeNode") -> None:
        """Append a child node."""
        self.children.append(node)


class DesignFeatureTree:
    """A tree model for UI-facing feature presentation."""

    def __init__(self, root_name: str = "Design") -> None:
        self.root = FeatureTreeNode(name=root_name, node_type="root")

    def flatten(self) -> list[str]:
        """Return a pre-order list of node names."""
        names: list[str] = []

        def visit(node: FeatureTreeNode) -> None:
            names.append(node.name)
            for child in node.children:
                visit(child)

        visit(self.root)
        return names
