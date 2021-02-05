import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
import os
from torch.autograd import Variable
import transforms as transforms
from models import *
import cv2
import sqlite3
import time


cut_size = 44


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


transform_test = transforms.Compose([
    transforms.TenCrop(cut_size),
    transforms.Lambda(lambda crops: torch.stack([transforms.ToTensor()(crop) for crop in crops])),
])



net = VGG('VGG19')
checkpoint = torch.load(os.path.join('FER2013_VGG19', 'PrivateTest_model.t7'))
net.load_state_dict(checkpoint['net'])
net.cuda()
net.eval()


cap = cv2.VideoCapture(0)

conn = create_connection('emotion_correlation.db')

while True:
    ret, frame = cap.read()
    cv2.imwrite('current.jpg', frame)
    
    raw_img = Image.open('current.jpg')
    gray = raw_img.convert('L')
    gray = gray.resize((48,48))

    gray.save('current_final.jpg')

    gray = np.array(gray)
    gray = gray.astype(np.uint8)

    img = gray[:, :, np.newaxis]

    img = np.concatenate((img, img, img), axis=2)
    img = Image.fromarray(img)
    inputs = transform_test(img)

    class_names = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

    ncrops, c, h, w = np.shape(inputs)

    inputs = inputs.view(-1, c, h, w)
    inputs = inputs.cuda()
    inputs = Variable(inputs, volatile=True)
    outputs = net(inputs)

    outputs_avg = outputs.view(ncrops, -1).mean(0)  # avg over crops

    score = F.softmax(outputs_avg)
    _, predicted = torch.max(outputs_avg.data, 0)

    print("Emotion: {0}".format(class_names[int(predicted.cpu().numpy())]))

    sql = "INSERT INTO emotions(emotion) VALUES({0})".format(int(predicted.cpu().numpy()))
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    time.sleep(1)

