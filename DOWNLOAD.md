Dataset **AFID** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://www.dropbox.com/scl/fi/rvwop9w8liyask0xfy6g6/afid-DatasetNinja.tar?rlkey=c25dv5fyz3dsse6i0v3oxry3c&dl=1)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='AFID', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be downloaded here:

- [defect_images.zip](https://newweb.aitex.es/wp-content/uploads/2019/07/Defect_images.7z)
- [nodefect_images.zip](https://newweb.aitex.es/wp-content/uploads/2019/07/NODefect_images.7z)
- [mask_images.zip](https://newweb.aitex.es/wp-content/uploads/2019/07/Mask_images.7z)
