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
        project_name = self.project_name
        folder_path = self.create_context.get_current_folder_path()
        task_name = self.create_context.get_current_task_name()
        host_name = self.create_context.host_name

        if current_instance is None:
            current_instance_asset = None
        else:
            current_instance_asset = current_instance["folderPath"]

        if current_instance is None:
            folder_entity = ayon_api.get_folder_by_path(
                project_name, folder_path
            )
            task_entity = ayon_api.get_task_by_name(
                project_name, folder_entity["id"], task_name
            )
            product_name = self.get_product_name(
                project_name,
                folder_entity,
                task_entity,
                variant,
                host_name,
            )
            data = {
                "task": task_entity,
                "variant": variant,
                "folderPath": folder_path
            }

            new_instance = CreatedInstance(
                self.product_type, product_name, data, self
            )
            instances_data = self.host.list_instances()
            instances_data.append(new_instance.data_to_store())
            self.host.write_instances(instances_data)
            self._add_instance_to_context(new_instance)

        elif (
            current_instance_asset != folder_path
            or current_instance["task"] != task_name
        ):
            # Update instance context if is not the same
            folder_entity = ayon_api.get_folder_by_path(
                project_name, folder_path
            )
            task_entity = ayon_api.get_task_by_name(
                project_name, folder_entity["id"], task_name
            )
            product_name = self.get_product_name(
                variant, task_entity, folder_entity, project_name, host_name
            )
            current_instance["folderPath"] = folder_path
            current_instance["task"] = task_entity
            current_instance["subset"] = product_name
