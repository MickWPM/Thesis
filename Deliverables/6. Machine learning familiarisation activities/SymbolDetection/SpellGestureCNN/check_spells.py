import cv2
import load_data
import train_spells as train
import numpy as np
from keras.models import load_model

_, _, _, _, TEST_IMAGES = load_data.GetImages()
#model = train.TrainSpellsModel()
#model = train.TrainSpellsModel(True)
model = load_model("D:/Programming/PythonTests/SpellGestureCNN/spell_model.h5")
 
for image in TEST_IMAGES:
    img_predict = image.reshape(1, 32, 32, 1)
    Data = img_predict.astype('float32')
    Data /=255
    #prediction = model.predict_proba(Data, verbose=1)
    prediction_prob = model.predict(Data)
    prediction = model.predict(img_predict)
    img = cv2.resize(image,(512,512))
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,500)
    fontScale              = .35
    fontColor              = (255,0,0)
    lineType               = 1

    preds = ["V1", "V2", "E"]
    #pred_text = preds[np.argmax(prediction)]
    pred_text = preds[np.argmax(prediction_prob)]
    if np.max(prediction_prob) < 0.9:
        pred_text = 'Fail'
    cv2.putText(img,'Prediction: ' + pred_text + ' (' + str(prediction) + ')' + ' (' + str(prediction_prob) + ')', 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)

    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()