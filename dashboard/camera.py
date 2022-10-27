import cv2
import pandas as pd
import numpy as np
import pickle
import mediapipe as mp
import warnings 
from .models import Profile
from .models import Data
warnings.filterwarnings('ignore')
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_face_mesh = mp.solutions.face_mesh
filename = 'C:/Users/Firas Farjallah/finalized_model_Knc.sav'
model = pickle.load(open(filename, 'rb'))

class VideoCamera(object):
    def __init__(self,id):
        self.video = cv2.VideoCapture(0)
        
        self.id=Profile.objects.get(id=id)
        print(self.id)
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        LEFT_EYE=[27]
        RIGHT_EYE=[257]
        Eye_point_full = []
        LEFT_IRIS = [474,475, 476, 477]
        RIGHT_IRIS = [469, 470, 471, 472]
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)as holistic,mp_face_mesh.FaceMesh(max_num_faces=1,refine_landmarks=True,min_detection_confidence=0.5,min_tracking_confidence=0.5)as face_mesh: 
            success, frame = self.video.read()

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_h, img_w = frame.shape[:2]
            results1 = face_mesh.process(rgb_frame)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results1.multi_face_landmarks:
                mesh_points=np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) 
                for p in results1.multi_face_landmarks[0].landmark])
                (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
                (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])
                center_left = np.array([l_cx, l_cy], dtype=np.int32)
                center_right = np.array([r_cx, r_cy], dtype=np.int32)
                n = []
                n = np.concatenate((np.array(center_left)/np.array([img_w, img_h]),np.array(center_right)/np.array([img_w, img_h])))
                n = list(n)
                le = np.concatenate([mesh_points[p]/np.array([img_w, img_h]) for p in LEFT_EYE])
                ri = np.concatenate([mesh_points[p]/np.array([img_w, img_h]) for p in RIGHT_EYE])
                n1 = np.concatenate((le,ri))
                s=n-n1
                tout = np.concatenate([s])
                self.tout = list(tout)
                try:
                    e=[]
                    if results1.multi_face_landmarks :        
                        Eye_point_full.append(self.tout)
                    else:
                        Eye_point_full.append([np.nan for i in range(4)])
                except AttributeError :
                    Eye_point_full.append([np.nan for i in range(4)])
            else:
                Eye_point_full.append([np.nan for i in range(4)])
            if results1.multi_face_landmarks:
                out = model.predict([self.tout])
                out1 = model.predict_proba([self.tout])
                if out[0]=='Autism':
                    x=f"Autism {out1[0,0]*100:.2f}%"
                    y=f"Autism"
                    data = Data(profile=self.id,x1=s[0],y1=s[1],x2=s[2],y2=s[3],classe="Autism",predict=out1[0,0])
                    data.save()
                else:
                    x=f"No Autism {out1[0,1]*100:.2f}%"
                    y=f"No Autism"
                    data = Data(profile=self.id,x1=s[0],y1=s[1],x2=s[2],y2=s[3],classe="No Autism",predict=out1[0,1])
                    data.save()
                image = cv2.putText(image, x, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()

class Video(object):
    def __init__(self,ch,id):
        self.tout= [0,0,0,0]
        self.video = cv2.VideoCapture(ch)
        self.id=Profile.objects.get(id=id)
        print(self.id)
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        LEFT_EYE=[27]
        RIGHT_EYE=[257]
        Eye_point_full = []
        LEFT_IRIS = [474,475, 476, 477]
        RIGHT_IRIS = [469, 470, 471, 472]
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)as holistic,mp_face_mesh.FaceMesh(max_num_faces=1,refine_landmarks=True,min_detection_confidence=0.5,min_tracking_confidence=0.5)as face_mesh: 
            success, frame = self.video.read()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_h, img_w = frame.shape[:2]
            results1 = face_mesh.process(rgb_frame)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results1.multi_face_landmarks:
                mesh_points=np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) 
                for p in results1.multi_face_landmarks[0].landmark])
                (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
                (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])
                center_left = np.array([l_cx, l_cy], dtype=np.int32)
                center_right = np.array([r_cx, r_cy], dtype=np.int32)
                n = []
                n = np.concatenate((np.array(center_left)/np.array([img_w, img_h]),np.array(center_right)/np.array([img_w, img_h])))
                n = list(n)
                le = np.concatenate([mesh_points[p]/np.array([img_w, img_h]) for p in LEFT_EYE])
                ri = np.concatenate([mesh_points[p]/np.array([img_w, img_h]) for p in RIGHT_EYE])
                n1 = np.concatenate((le,ri))
                s=n-n1
                tout = np.concatenate([s])
                self.tout = list(tout)
                try:
                    e=[]
                    if results1.multi_face_landmarks :
                        Eye_point_full.append(self.tout)    
                    else:
                        Eye_point_full.append([np.nan for i in range(4)])
                except AttributeError :
                    Eye_point_full.append([np.nan for i in range(4)])     
            else:
                Eye_point_full.append([np.nan for i in range(4)])
            if results1.multi_face_landmarks:
                out = model.predict([self.tout])
                out1 = model.predict_proba([self.tout])
                if out[0]=='Autism':
                    x=f"Autism {out1[0,0]*100:.2f}%"
                    y=f"Autism"
                    data = Data(profile=self.id,x1=s[0],y1=s[1],x2=s[2],y2=s[3],classe="Autism",predict=out1[0,0])
                    data.save()
                else:
                    x=f"No Autism {out1[0,1]*100:.2f}%"
                    y=f"No Autism"
                    data = Data(profile=self.id,x1=s[0],y1=s[1],x2=s[2],y2=s[3],classe="No Autism",predict=out1[0,1])
                    data.save()
                image = cv2.putText(image, x, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)        
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()
def gen(cameraa):
    while True:
        frame = cameraa.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')