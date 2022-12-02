import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def preprocessImage(img):
    # Copying input image
    import numpy as np

    im_width = 512
    im_height = 512
    split_ratio = 0.2

    im = img.copy()

    if im.size[0] > im.size[1]:
        wpercent = (im_width / float(im.size[0]))
        hsize = int((float(im.size[1]) * float(wpercent)))
        im = im.resize((im_width, hsize), Image.ANTIALIAS)
    else:

        hpercent = (im_height / float(im.size[1]))
        wsize = int((float(im.size[0]) * float(hpercent)))
        im = im.resize((wsize, im_height), Image.ANTIALIAS)

    new_size = im.size
    preprocessImg = Image.new("RGB", (im_width, im_height))
    # # Pasting resized image by keeping aspect ratio to target image
    preprocessImg.paste(im, ((im_width - new_size[0]) // 2, (im_height - new_size[1]) // 2))

    preprocessImg = np.asarray(preprocessImg)/255.0

    canvas = np.zeros((1, 512, 512, 3), dtype=np.float32)
    canvas[0] = preprocessImg

    return canvas


# Preprocessing test images
# def preprocess_test(image):
#     import tensorflow as tf
#     img = preprocessImage(image)
#     preprocessImg = tf.reshape(img, [-1, 512, 512, 3])
#     # img = image.resize((512, 512))
#
#     img = img/255.0
#     return img

def dice_coef(y_true, y_pred, smooth=1):
    from keras import backend as K
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)

def dice_coef_loss(y_true, y_pred):
    return 1-dice_coef(y_true, y_pred)

def predict_image(image):
    from keras.models import load_model
    model = load_model('my_model2.hdf5', custom_objects={'dice_coef':dice_coef, 'dice_coef_loss':dice_coef_loss})
    preds_test = model.predict(image)

    preds_test_t = (preds_test > 0.5).astype(np.uint8)

    return preds_test_t


def plot_sample(image, prediction, ix=None):
    import io
    from PIL import Image
    import matplotlib.pyplot as plt

    # fig, ax = plt.subplots(1, 1)

    plt.figure(figsize=(5,5))
    plt.imshow(image, cmap='seismic', aspect='auto',vmin=0, vmax=255)
    plt.axis('off')
    plt.contour(prediction.squeeze(), colors='#eb0e1d', levels=[0.8])

    plt.savefig('temp.png', format='png', bbox_inches='tight', pad_inches=0)

    return Image.open('temp.png')


def predict(image):
    import matplotlib.pyplot as plt

    preprocessed_image = preprocessImage(image)
    prediction = predict_image(preprocessed_image)
    draw_prediction = plot_sample(preprocessed_image[0], prediction)

    # Saving prediction contour
    plt.figure(figsize=(5, 5))
    plt.imshow(prediction.squeeze(), cmap='gray')
    plt.axis("off")
    plt.savefig("D:\Front end\pred_mask\Image Mask.png", format='png', bbox_inches='tight', pad_inches=0)

    return draw_prediction