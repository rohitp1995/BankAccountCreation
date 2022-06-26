import os
import sys
import detectron2
from detectron2.utils.logger import setup_logger
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data.datasets import register_coco_instances
from detectron2.data import MetadataCatalog, DatasetCatalog

setup_logger()

class Train:

    def __init__(self, image_dir, coco_file, model_name):
    
        self.image_dir = image_dir
        self.coco_file = coco_file
        self.model_name = model_name
        self.model_cfg = get_cfg()
        self.log_obj = Logger('Generatedlogs')
        self.logger = self.log_obj.logging()


    def trainmodel(self):

        try:
            self.logger.info('Started training the model')
            register_coco_instances("sample", {}, self.coco_file, self.image_dir)
            sample_metadata = MetadataCatalog.get("sample")
            dataset_dicts = DatasetCatalog.get("sample")

            self.model_cfg.merge_from_file("config.yaml")
            os.makedirs(self.model_cfg.OUTPUT_DIR, exist_ok=True)
            self.model_cfg.WEIGHTS  = model_zoo.get_checkpoint_url(self.model_name)
            trainer = DefaultTrainer(self.model_cfg)
            trainer.resume_or_load(resume=False)
            trainer.train()

        except Exception as e:
            self.logger.error('Error while training the model: ' + str(e))
            sys.exit(1) 


if __name__ == '__main__':

    Trainer = Train('aadhar_images', 'coco/output.json', 'COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml')
    Trainer.trainmodel()