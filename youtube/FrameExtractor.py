# misc
import os
import shutil
import math
import datetime
import numpy as np

# image operation
import cv2
from PIL import Image
import img2pdf
# import pillow

class FrameExtractor():
    '''
    Class used for extracting frames from a video file.
    '''
    def __init__(self, video_path_comp,video_path_data):
        self.video_path_comp = video_path_comp
        self.vid_cap_comp = cv2.VideoCapture(video_path_comp)
        self.video_path_data = video_path_data
        self.vid_cap_data = cv2.VideoCapture(video_path_data)
        self.n_frames = int(self.vid_cap_data.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.vid_cap_data.get(cv2.CAP_PROP_FPS))
        
    def get_video_duration(self):
        duration = self.n_frames/self.fps
        print(f'Duration: {datetime.timedelta(seconds=duration)}')
        
    def get_n_images(self, every_x_frame):
        n_images = math.floor(self.n_frames / every_x_frame) + 1
        print(f'Extracting every {every_x_frame} (nd/rd/th) frame would result in {n_images} images.')

    def img_comp(self,image1,image2):
        cv2_image1_cnvtd = cv2.cvtColor(image1,cv2.COLOR_BGR2RGB)
        cv2_image2_cnvtd = cv2.cvtColor(image2,cv2.COLOR_BGR2RGB)
        i1 = Image.fromarray(cv2_image1_cnvtd)
        i2 = Image.fromarray(cv2_image2_cnvtd)
        assert i1.mode == i2.mode, "Different kinds of images."
        assert i1.size == i2.size, "Different sizes."
        
        pairs = zip(i1.getdata(), i2.getdata())
        if len(i1.getbands()) == 1:
            # for gray-scale jpegs
            dif = sum(abs(p1-p2) for p1,p2 in pairs)
        else:
            dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
        
        ncomponents = i1.size[0] * i1.size[1] * 3
        diff_per = (dif / 255.0 * 100) / ncomponents
        return diff_per

    def output_file(self,image_list,file_name,download_path,file_ext='.pdf'):
        if file_ext == '.pdf': 
            new_image_list = []
            pdf_path  = f'{download_path}/{file_name}{file_ext}'
            for image in image_list:
                cv2_image_cnvtd = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(cv2_image_cnvtd)
                new_image_list.append(pil_image)
            # converting into chunks using img2pdf 
            new_image_list[0].save(pdf_path, save_all = True, quality=100, append_images = new_image_list[1:])
            # with open(pdf_path,"wb") as f:
	        #     f.write(img2pdf.convert(new_image_list))
        else:
            img_cnt=0
            for image in image_list:
                img_path = os.path.join(download_path,file_name, ''.join([file_name, '_', str(img_cnt), file_ext]))
                cv2.imwrite(img_path, image)
                img_cnt += 1


    def extract_distinct_frames(self, every_x_frame, file_name, dest_path, file_ext = '.pdf', tolerance=5):
        if not self.vid_cap_comp.isOpened():
            self.vid_cap_comp = cv2.VideoCapture(self.video_path_comp)
        
        if dest_path is None:
            dest_path = os.getcwd()
        else:
            if not os.path.isdir(dest_path):
                os.mkdir(dest_path)
                print(f'Created the following directory: {dest_path}')
        
        image_list = []
        frame_cnt = 0
        img_cnt = 0

        success_comp,curr_image_comp = self.vid_cap_comp.read() 
        # prev_image_comp = curr_image_comp
        curr_image_comp_bw = cv2.cvtColor(curr_image_comp,cv2.COLOR_BGR2GRAY)
        prev_image_comp_bw = curr_image_comp_bw

        success_data,curr_image_data = self.vid_cap_data.read() 

        while self.vid_cap_comp.isOpened():
            
            if not success_comp:
                break
            
            if not success_data:
                break

            if frame_cnt % every_x_frame == 0:
                curr_image_comp_bw = cv2.cvtColor(curr_image_comp,cv2.COLOR_BGR2GRAY)
                # diff_image_bw = cv2.subtract(prev_image_comp_bw,curr_image_comp_bw)
                diff_image_bw = cv2.absdiff(prev_image_comp_bw,curr_image_comp_bw)
                std_diff_image = np.std(diff_image_bw)

                if std_diff_image > tolerance:
                    image_list.append(curr_image_data)
            
                # prev_image_comp = curr_image_comp
                success_comp,curr_image_comp = self.vid_cap_comp.read() 
                success_data,curr_image_data = self.vid_cap_data.read() 
                prev_image_comp_bw = curr_image_comp_bw

            frame_cnt += 1

        self.output_file(image_list,file_name,dest_path,file_ext)

        self.vid_cap_comp.release()
        cv2.destroyAllWindows()
    def extract_frames(self, every_x_frame, file_name, dest_path=None, file_ext = '.jpg'):
        if not self.vid_cap_comp.isOpened():
            self.vid_cap_comp = cv2.VideoCapture(self.video_path_comp)
        
        if dest_path is None:
            dest_path = os.getcwd()
        else:
            if not os.path.isdir(dest_path):
                os.mkdir(dest_path)
                print(f'Created the following directory: {dest_path}')
        
        frame_cnt = 0
        img_cnt = 0

        while self.vid_cap_comp.isOpened():
            
            success,image = self.vid_cap_comp.read() 
            
            if not success:
                break
            
            if frame_cnt % every_x_frame == 0:
                img_path = os.path.join(dest_path, ''.join([file_name, '_', str(img_cnt), file_ext]))
                cv2.imwrite(img_path, image)  
                img_cnt += 1
                
            frame_cnt += 1
        
        self.vid_cap_comp.release()
        cv2.destroyAllWindows()