# https://www.kaggle.com/datasets/nexuswho/aitex-fabric-image-database

import glob
import os
import shutil
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from dotenv import load_dotenv
from supervisely.io.fs import (
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:        
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path
    
def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count
    
def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:


    # project_name = "AITEX Fabric Image"
    defect_images_path = "/home/grokhi/rawdata/afid/Defect_images"
    defect_masks_path = "/home/grokhi/rawdata/afid/Mask_images"
    no_defect_images_path = "/home/grokhi/rawdata/afid/NODefect_images"
    ds_name = "ds"
    batch_size = 30
    masks_ext = "_mask.png"


    def create_ann(image_path):
        labels = []

        defect = sly.Tag(tag_defect)
        description_value_index = int(get_file_name(image_path).split("_")[1])
        description_value = index_to_description[description_value_index]
        obj_class = [obj_class for obj_class in obj_classes if description_value == obj_class.name][0]
        # description = sly.Tag(tag_description, value=description_value)
        fabric_code_value = get_file_name(image_path).split("_")[2]
        fabric_code = sly.Tag(tag_fabric_code, value=fabric_code_value)

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        mask_path = os.path.join(defect_masks_path, get_file_name(image_path) + masks_ext)

        if file_exists(mask_path):
            ann_np = sly.imaging.image.read(mask_path)[:, :, 0]

            obj_mask = ann_np != 0
            ret, curr_mask = connectedComponents(obj_mask.astype("uint8"), connectivity=8)
            for i in range(1, ret):
                obj_mask = curr_mask == i
                curr_bitmap = sly.Bitmap(obj_mask)
                curr_label = sly.Label(curr_bitmap, obj_class)
                labels.append(curr_label)

        return sly.Annotation(
            img_size=(img_height, img_wight), labels=labels, img_tags=[defect, fabric_code]
        )


    # obj_class = sly.ObjClass("defect", sly.Bitmap)



    tag_fabric_code = sly.TagMeta("fabric code", sly.TagValueType.ANY_STRING)
    tag_description = sly.TagMeta("defect description", sly.TagValueType.ANY_STRING)
    tag_defect = sly.TagMeta("defect", sly.TagValueType.NONE)
    tag_no_defect = sly.TagMeta("no defect", sly.TagValueType.NONE)
    tag_subfolder = sly.TagMeta("subfolder", sly.TagValueType.ANY_STRING)

    index_to_description = {
        2: "broken end",
        6: "broken yarn",
        10: "broken pick",
        16: "weft curling",
        19: "fuzzyball",
        22: "cut selvage",
        23: "crease",
        25: "warp ball",
        27: "knots",
        29: "contamination",
        30: "nep",
        36: "weft crack",
    }

    obj_classes = [sly.ObjClass(name, sly.Bitmap) for name in index_to_description.values()]

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=obj_classes,
        tag_metas=[tag_fabric_code, tag_defect, tag_no_defect, tag_subfolder],
    )
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    images_names = os.listdir(defect_images_path)

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

    for img_names_batch in sly.batched(images_names, batch_size=batch_size):
        images_pathes_batch = [
            os.path.join(defect_images_path, image_path) for image_path in img_names_batch
        ]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns_batch = [create_ann(image_path) for image_path in images_pathes_batch]
        api.annotation.upload_anns(img_ids, anns_batch)

        progress.iters_done_report(len(img_names_batch))


    def create_ann_no_defect(image_path):
        labels = []

        sub = sly.Tag(tag_subfolder, value=subfolder)

        defect = sly.Tag(tag_no_defect)
        fabric_code_value = get_file_name(image_path).split("_")[2]
        fabric_code = sly.Tag(tag_fabric_code, value=fabric_code_value)

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        return sly.Annotation(
            img_size=(img_height, img_wight), labels=labels, img_tags=[defect, fabric_code, sub]
        )


    for subfolder in os.listdir(no_defect_images_path):
        images_path = os.path.join(no_defect_images_path, subfolder)
        images_names = os.listdir(images_path)

        progress = sly.Progress(
            "Create dataset {}, add {} data".format(ds_name, subfolder), len(images_names)
        )

        for img_names_batch in sly.batched(images_names, batch_size=batch_size):
            images_pathes_batch = [
                os.path.join(images_path, image_path) for image_path in img_names_batch
            ]

            img_names_batch = [subfolder + "_" + im_name for im_name in img_names_batch]

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns_batch = [create_ann_no_defect(image_path) for image_path in images_pathes_batch]
            api.annotation.upload_anns(img_ids, anns_batch)

            progress.iters_done_report(len(img_names_batch))
    return project


