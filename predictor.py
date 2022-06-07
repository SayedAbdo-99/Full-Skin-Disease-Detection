################################################### to get rid of warnings
import warnings
import os
import tensorflow as tf

import sys,getopt
import tensorflow
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.metrics import categorical_accuracy, top_k_categorical_accuracy
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import Dense, Dropout
import cv2

###################################################
class Predictor():
    def __init__(self):
        warnings.filterwarnings('ignore',category=FutureWarning)
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        tf.get_logger().warning('test')
        tf.get_logger().setLevel('ERROR')
        tf.get_logger().warning('test')

    def top_3_accuracy(self,y_true, y_pred):
        return top_k_categorical_accuracy(y_true, y_pred, k=3)

    def top_2_accuracy(sefl,y_true, y_pred):
        return top_k_categorical_accuracy(y_true, y_pred, k=2)

    ###################################################
    def modelGenerator(self,modeltype):
        self.clsNumbers=4
        self.class_labels = {'Psoriasis':0,'Measles':1,'Melanoma':2,'Ringworm':3}
        self.ModelCheckpoint='ModelCheckpoint_Skin_Disease.h5'
        
        if modeltype=='cancer':
            self.clsNumbers=7
            self.class_labels={'Actinic Keratoses and Intraepithelial Carcinoma':0, 'Basal Cell Carcinoma':1, 'Benign Keratosis':2, 'Dermatofibroma':3, '(MEL) Malignant Neoplasm':4, 'Melanocytic Nevi':5, 'Vascular Skin Lesions':6}
            self.ModelCheckpoint='ModelCheckpoint_Cancer.h5'
        
        mobile = tensorflow.keras.applications.mobilenet.MobileNet()

        x = mobile.layers[-6].output
        x = Dropout(0.25)(x)
        predictions = Dense(self.clsNumbers, activation='softmax')(x)#4
        model = Model(inputs=mobile.input, outputs=predictions)
        for layer in model.layers[:-23]:
            layer.trainable = False

        model.compile(Adam(learning_rate=0.01), loss='categorical_crossentropy', metrics=[categorical_accuracy, self.top_2_accuracy, self.top_3_accuracy])

        model.load_weights(self.ModelCheckpoint)
        return model,self.class_labels

    def TestImage(self,path,modeltype='cancer'):
        model,class_labels=self.modelGenerator(modeltype)
        img = image.load_img(path,target_size=(224, 224))
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = tensorflow.keras.applications.mobilenet.preprocess_input(img_data)
        features = np.array(model.predict(img_data))
        y_classes = features #.argmax(axis=-1)
        
        cls=class_labels
        out=y_classes[0]
        k=0
        for i in cls:
            cls[i]=out[k]
            k=k+1
        #print(cls)
        newcls={n: v for n, v in sorted(cls.items(), key=lambda item: item[1],reverse=True)}
        #print(newcls)

        return newcls

'''
inputfile = 'C:\\xampp\\htdocs\\skd2\\assets\\samplepic.jpg'
p=Predictor()
x = p.TestImage(inputfile)
print(x)
'''
'''
predictor=Predictor()
cancerResult = predictor.TestImage(path='C:\\xampp\\htdocs\\skd2\\assets\\samplepic.jpg',modeltype='cancer')
skinResult=predictor.TestImage(path='C:\\xampp\\htdocs\\skd2\\assets\\samplepic.jpg',modeltype='skin')
print(str(round(list(cancerResult.values())[0])*100)+" %")
print(skinResult.keys())
'''
