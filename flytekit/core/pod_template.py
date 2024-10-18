from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Optional, cast

import flytekit.core.utils
from flytekit.exceptions import user as _user_exceptions
from flytekit.models import task as task_models
from google.protobuf.struct_pb2 import Struct

if TYPE_CHECKING:
    from kubernetes.client import V1PodSpec

PRIMARY_CONTAINER_DEFAULT_NAME = "primary"


@dataclass(init=True, repr=True, eq=True, frozen=False)
class PodTemplate(object):
    """Custom PodTemplate specification for a Task."""

    pod_spec: Optional["V1PodSpec"] = None
    primary_container_name: str = PRIMARY_CONTAINER_DEFAULT_NAME
    labels: Optional[Dict[str, str]] = None
    annotations: Optional[Dict[str, str]] = None

    def __post_init__(self):
        if self.pod_spec is None:
            from kubernetes.client import V1PodSpec

            self.pod_spec = V1PodSpec(containers=[])
        if not self.primary_container_name:
            raise _user_exceptions.FlyteValidationException("A primary container name cannot be undefined")

def convert_podtemplate_to_model(
    pod_template: Optional[PodTemplate] = None,
) -> task_models.PodTemplate:
    from kubernetes.client import ApiClient, V1PodSpec
    print(pod_template.pod_spec)
    print(ApiClient().sanitize_for_serialization(cast(PodTemplate, pod_template).pod_spec))
    return task_models.PodTemplate(primary_container_name=pod_template.primary_container_name, labels=pod_template.labels, annotations=pod_template.annotations, pod_spec=ApiClient().sanitize_for_serialization(cast(PodTemplate, pod_template).pod_spec))