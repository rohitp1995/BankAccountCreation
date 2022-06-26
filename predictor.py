from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.utils.visualizer  import Visualizer
from detectron2.data.datasets import register_coco_instances
import cv2 as cv
import os
import sys
from log.logger import Logger

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

class Predict:
    
    def __init__(self, image_file, coco_file):
    
        self.image_file = image_file
        self.model_cfg = get_cfg()
        self.coco_file = coco_file
        self.log_obj = Logger('Generatedlogs')
        self.logger = self.log_obj.logging()


    def get_prediction(self):
        
        try:
            self.logger.info('Started prediction')
            self.model_cfg.merge_from_file('config.yaml')
            predictor = DefaultPredictor(self.model_cfg)
            im = cv.imread(self.image_file)
            
            outputs = predictor(im)
            output_list = sorted(outputs['instances'].pred_classes.cpu().tolist())

            ## visualizing and saving graph
            v = Visualizer(im[:, :, ::-1], scale=1.2)
            v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
            predicted_image = v.get_image()
            im_rgb = cv.cvtColor(predicted_image, cv.COLOR_RGB2BGR)
            # os.makedirs('uploads', exist_ok= True)
            # cv.imwrite(f'uploads/{self.image_file}_OD.jpg', im_rgb)
            
            return output_list
        
        except Exception as e:
                print(e)
                self.logger.error('Error while Prediction: ' + str(e))
                sys.exit(1) 
