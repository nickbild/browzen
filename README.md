# BrowZen

BrowZen correlates your emotional states with the web sites you visit to give you actionable insights about how you spend your time browsing the web.

<p align="center">
<img src="https://raw.githubusercontent.com/nickbild/browzen/main/media/browzen_demo_short.gif">
</p>

## How It Works

<p align="center">
<img src="https://raw.githubusercontent.com/nickbild/browzen/main/media/browzen.jpg">
</p>

A webcam attached to an NVIDIA Jetson Xavier NX captures periodic images of the user of the computer as a background process.  These images are classified (see [classify_emotion.py](https://github.com/nickbild/browzen/blob/main/classify_emotion.py)) by a VGG19 convolutional neural network that has been [pretrained](https://github.com/WuJie1010/Facial-Expression-Recognition.Pytorch) to recognize seven emotional states ("Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", and "Neutral").  Observations (emotional state, datetime stamp) are recorded in an SQLite3 database.  For privacy protection, images are destroyed after classification, and all processing takes place locally—nothing is sent to the cloud.

Next, [analysis.py](https://github.com/nickbild/browzen/blob/main/analysis.py) connects to the SQLite3 database that stores web history in Chrome/Chromium and correlates web site visit times with the database of emotional state observations created by the classification step.  The result of the analysis, the sum of each emotional state observed while visiting each web site, is stored in an SQLite3 database table.

Finally, the analysis results are used to generate a web dashboard ([generate_dashboard.py](https://github.com/nickbild/browzen/blob/main/generate_dashboard.py)) to provide a simple way to visualize, on average, how each web site one visits impacts their emotional state.  The web dashboard ([dashboard.html](https://github.com/nickbild/browzen/blob/main/dashboard.html)) relies on only HTML5 and JavaScript.

## Media

Demo Video:
[YouTube](https://www.youtube.com/watch?v=xNUKsig8W3w)

The web dashboard, giving an overview of emotional reactions during visits to various websites ([high resolution](https://raw.githubusercontent.com/nickbild/browzen/main/media/browzen_dashboard.png)):
![Dashboard](https://raw.githubusercontent.com/nickbild/browzen/main/media/browzen_dashboard_sm.png)

Classifying emotions in real-time ([high resolution](https://raw.githubusercontent.com/nickbild/browzen/main/media/classification.jpg)):
![Classification](https://raw.githubusercontent.com/nickbild/browzen/main/media/classification_sm.jpg)

Jetson Xavier NX ([high resolution](https://raw.githubusercontent.com/nickbild/shaides_v2/master/media/jetson_nx.jpg)):
![Jetson](https://raw.githubusercontent.com/nickbild/shaides_v2/master/media/jetson_nx_sm.jpg)

## Future Direction

It may be useful to create a browser plugin that displays a small, always-visible icon representing past emotions experienced when visiting the current website.  This would serve as a quick reminder of past experiences that may modify current behavior.

I would like to also explore other areas, beyond web browsing, where this idea may be helpful.

## Bill of Materials

- 1 x NVIDIA Jetson Xavier NX
- 1 x USB webcam

## About the Author

[Nick A. Bild, MS](https://nickbild79.firebaseapp.com/#!/)
