"""
MAL-Toolbox Attack Graph Node Dataclass
"""

from dataclasses import dataclass
from typing import Any, List, Optional, ForwardRef

from maltoolbox.attackgraph import attacker

@dataclass
class AttackGraphNode:
    id: str = None
    type: str = None
    asset: Any = None
    name: str = None
    ttc: dict = None
    defense_status: dict = None
    children: List[ForwardRef('AttackGraphNode')] = None
    parents: List[ForwardRef('AttackGraphNode')] = None
    existence_status: bool = None
    is_reachable: bool = None
    is_traversable: bool = None
    compromised_by: List[ForwardRef('Attacker')] = None
    extra: dict = None
    mitre_info: str = None

    def to_dict(self):
        node_dict = {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'ttc': self.ttc,
            'children': [child.id for child in self.children],
            'parents': [parent.id for parent in self.parents],
            'compromised_by': ['Attacker:' + attacker.id for attacker in \
                self.compromised_by]
        }

        if self.asset != None:
            node_dict['asset'] = self.asset.metaconcept + ':' \
                + str(self.asset.id)
        if self.defense_status != None:
            node_dict['defense_status'] = str(self.defense_status)
        if self.existence_status != None:
            node_dict['existence_status'] = str(self.existence_status)
        if self.mitre_info != None:
            node_dict['mitre_info'] = str(self.mitre_info)

        return node_dict
