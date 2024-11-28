from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, Optional, cast

from kubernetes.client import ApiClient

from flytekit.exceptions import user as _user_exceptions
from flytekit.models import task as task_models

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

    def _serialize_pod_spec(self) -> Dict[str, Any]:
        if self.pod_spec is None:
            return {}
        from kubernetes.client import ApiClient, V1PodSpec
        containers = cast(V1PodSpec, self.pod_spec).containers

        final_containers = []
        for container in containers:
            # In the case of the primary container, we overwrite specific container attributes
            # with the values given to ContainerTask.
            # The attributes include: image, command, args, resource, and env (env is unioned)
            final_containers.append(container)
        cast(V1PodSpec, self.pod_spec).containers = final_containers
        return ApiClient().sanitize_for_serialization(self.pod_spec)

def convert_pod_template_to_model(podtemplate: Optional[PodTemplate] = None) -> task_models.PodTemplate:
    breakpoint()
    if podtemplate is None:
        return None
    return task_models.PodTemplate(
        primary_container_name=podtemplate.primary_container_name,
        labels=podtemplate.labels,
        annotations=podtemplate.annotations,
        pod_spec=podtemplate.pod_spec,
    )
