import cv2 
import os 
import pandas as pd
import numpy as np

class ETL_Pipeline:
    '''
    The extract function receives a source directory ( the video path) and returns extracted images frames for detection. 
    
    Params:
        source_directpry (string): path to video 
        fps (int): frames per second we want to extract from video
    '''
    def extract(self, source_directory, fps):
        cam = cv2.VideoCapture(source_directory)
        frames = []
        if not os.path.exists('video_frames'): 
            os.makedirs('video_frames')
        current_frame = 0
        frame_interval = fps
        while(True):
            ret, frame = cam.read() 
            if ret: 
                if current_frame % (frame_interval * int(cam.get(cv2.CAP_PROP_FPS))) == 0:
                    frame_name = os.path.join('video_frames', f'frame{current_frame}.jpg')
                    print('Creating...', frame_name)
                    cv2.imwrite(frame_name, frame) 
                    frames.append(str(frame_name))
                current_frame += 1
            else: 
                break
        cam.release() 
        cv2.destroyAllWindows() 
        self.df = pd.DataFrame([str(path) for path in frames])
        print("Extracted dataframe head: ", self.df.head())
        return self.df
    '''
    The transform function performs any data cleansing and transformations. It accepts the intial dataframe and returns a processed dataframe.
     Params:
       df (dataframe): Initial datframe
    '''
    def transform(self, df):
        frames = []
        for i, row in df.iterrows():
            print(row[0])
            # New feature: In the exploratory analysis, better performance was seen from the model when grayscale was applied to the image
            gray_frame = cv2.cvtColor(cv2.imread(row[0]), cv2.COLOR_BGR2GRAY)
            cv2.imwrite(row[0], gray_frame)
        return df

    '''
    The load function saves a dataframe to a csv file.
    Params:
        df( dataframe): dataframe to save
    '''
    def load(self, df):
        self.df_blob.to_csv('video_frame_inputs.csv', index=False)
        print("Saved network inputs to video_frame_inputs.csv!")
        return self.df_blob











