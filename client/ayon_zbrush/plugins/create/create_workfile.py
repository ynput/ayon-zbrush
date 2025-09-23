# -*- coding: utf-8 -*-
"""Creator plugin for creating workfiles."""
import ayon_api
from ayon_core.pipeline import CreatedInstance
from ayon_zbrush.api import plugin

class CreateWorkfile(plugin.ZbrushAutoCreator):
    """Workfile auto-creator."""
    identifier = "io.ayon.creators.zbrush.workfile"
    label = "Workfile"
    product_type = "workfile"
    icon = "fa5.file"

    default_variant = "Main"

    def create(self):
        variant = self.default_variant
        current_instance = next(
            (
                instance for instance in self.create_context.instances
                if instance.creator_identifier == self.identifier
            ), None)

        current_instance_folder_path = None
        if current_instance is not None:
            current_instance_folder_path = current_instance["folderPath"]

        project_entity = self.create_context.get_current_project_entity()
        folder_entity = self.create_context.get_current_folder_entity()
        task_entity = self.create_context.get_current_task_entity()

        project_name = project_entity["name"]
        folder_path = folder_entity["path"]
        task_name = task_entity["name"]
        host_name = self.create_context.host_name

        if current_instance is None:
            product_name = self.get_product_name(
                project_name=project_name,
                project_entity=project_entity,
                folder_entity=folder_entity,
                task_entity=task_entity,
                variant=variant,
                host_name=host_name,
            )
            data = {
                "task": task_name,
                "variant": variant,
                "folderPath": folder_path,
            }

            new_instance = CreatedInstance(
                self.product_type, product_name, data, self
            )
            instances_data = self.host.list_instances()
            instances_data.append(new_instance.data_to_store())
            self.host.write_instances(instances_data)
            self._add_instance_to_context(new_instance)

        elif (
            current_instance_folder_path != folder_path
            or current_instance["task"] != task_name
        ):
            # Update instance context if is not the same
            product_name = self.get_product_name(
                project_name=project_name,
                project_entity=project_entity,
                folder_entity=folder_entity,
                task_entity=task_entity,
                variant=variant,
                host_name=host_name,
            )
            current_instance["folderPath"] = folder_path
            current_instance["task"] = task_entity["name"]
            current_instance["productName"] = product_name
