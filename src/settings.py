from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "AFID"
PROJECT_NAME_FULL: str = "AFID: A Public Fabric Image Database for Defect Detection"
HIDE_DATASET = False  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.CC0_1_0()
APPLICATIONS: List[Union[Industry, Domain, Research]] = [Industry.Textile(), Domain.SurfaceDefectDetection()]
CATEGORY: Category = Category.Manufacturing()

CV_TASKS: List[CVTask] = [CVTask.InstanceSegmentation(), CVTask.SemanticSegmentation(), CVTask.ObjectDetection(), CVTask.Classification()]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.InstanceSegmentation()]

RELEASE_DATE: Optional[str] = None  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = 2019

HOMEPAGE_URL: str = "https://www.aitex.es/afid/"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 7918311
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/afid"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = {
    "defect_images.zip": "https://newweb.aitex.es/wp-content/uploads/2019/07/Defect_images.7z",
    "nodefect_images.zip": "https://newweb.aitex.es/wp-content/uploads/2019/07/NODefect_images.7z",
    "mask_images.zip": "https://newweb.aitex.es/wp-content/uploads/2019/07/Mask_images.7z",
}
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = {
    "broken end": [230, 25, 75],
    "broken yarn": [60, 180, 75],
    "broken pick": [255, 225, 25],
    "weft curling": [0, 130, 200],
    "fuzzyball": [245, 130, 48],
    "cut selvage": [145, 30, 180],
    "crease": [70, 240, 240],
    "warp ball": [240, 50, 230],
    "knots": [210, 245, 60],
    "contamination": [250, 190, 212],
    "nep": [0, 128, 128],
    "weft crack": [220, 190, 255],
}

# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
# Use dict key to specify name for a button
PAPER: Optional[Union[str, List[str], Dict[str, str]]] = "https://riunet.upv.es/bitstream/handle/10251/154810/Silvestre-Blanes?sequence=1"
BLOGPOST: Optional[Union[str, List[str], Dict[str, str]]] = None
REPOSITORY: Optional[Union[str, List[str], Dict[str, str]]] = {"Kaggle":"https://www.kaggle.com/datasets/nexuswho/aitex-fabric-image-database"}

CITATION_URL: Optional[str] = "https://www.aitex.es/afid/"
AUTHORS: Optional[List[str]] = ["Javier Silvestre-Blanes", "Teresa Albero-Albero", "Ignacio Miralles", "Rubén Pérez-Llorens", "Jorge Moreno"]
AUTHORS_CONTACTS: Optional[List[str]] = ["info@aitex.es"]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = [ "Universitat Politècnica de València, Spain", "AITEX, Spain"]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = ["https://www.upv.es/", "https://www.aitex.es/?lang=en"]

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with string value to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = {"classification image sets": ['defect', 'no defect'], "__POSTTEXT__":"Additionally, ***fabric code*** information is provided"}
TAGS: Optional[List[str]] = None


SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL or PROJECT_NAME,
        "hide_dataset": HIDE_DATASET,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["blog"] = BLOGPOST
    settings["repository"] = REPOSITORY
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["authors_contacts"] = AUTHORS_CONTACTS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
