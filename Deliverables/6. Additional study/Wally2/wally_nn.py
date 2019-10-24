import wally_nn_setup as wally_setup
import cv2
from keras.models import load_model
from keras import backend as K

MODEL = None


#This method needs to be replaced by a prediction using a trained NN based off the passed img
def analyse_sub_img(img):
    global MODEL
    if MODEL is None:
        #TODO: Load model from disk - CHECK IF IT EXISTS
        MODEL = load_model('wally_model.h5')
        #MODEL = wally_setup.Train_Wally()
        print("Model 'loaded from disk'")


    img_predict = img.reshape(1, 60, 60, 3)
    pred=MODEL.predict(img_predict)
    prediction = pred[0]
    
    return prediction > 0.99

def get_predict_data(img):
    IMAGE_SHAPE= (60, 60, 3)
    img_rows, img_cols, channels = IMAGE_SHAPE[0], IMAGE_SHAPE[1], IMAGE_SHAPE[2]
    if K.image_data_format() == 'channels_first':
        img = img.reshape(1, channels, img_rows, img_cols)
    else:
        img = img.reshape(1, img_rows, img_cols, channels)
    return img

LOAD_MODEL = False

if __name__ == "__main__": 
    print("TODO: Create, train and save NN. In load_model, load saved model from dist")
    
    if LOAD_MODEL:
        MODEL = load_model('wally_model.h5')
    else:
        MODEL = wally_setup.Train_Wally()
    print(MODEL.summary())

    if False:
        images, _, labels, _ = wally_setup.get_training_data()

        for i in range(0, len(labels)):
            img_predict = images[i].reshape(1, 60, 60, 3)
            Data = img_predict.astype('float32')
            Data /=255
            
            pred=MODEL.predict(img_predict)
            prediction = pred[0]

            cv2.imshow("Image",images[i])
            print("Category " + str(i) + ": " + str(labels[i]))
            print("prediction " + str(i) + ": " + str(prediction))
            cv2.waitKey(0)
        cv2.destroyAllWindows()



    # pred=MODEL.predict(images)

    # for i in range(0, len(labels)):
    #     img_predict = images[i].reshape(1, 60, 60, 3)
    #     Data = img_predict.astype('float32')
    #     Data /=255

    #     #data = get_predict_data(images[i])
    #     cv2.imshow("Image",images[i])
    #     print("Category " + str(i) + ": " + str(labels[i]))
    #     prediction = pred[i]
    #     print("prediction " + str(i) + ": " + str(prediction))
    #     cv2.waitKey(0)
    # cv2.destroyAllWindows()

