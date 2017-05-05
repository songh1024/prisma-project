from __future__ import print_function
import sys,os
sys.path.insert(0, 'src')
from utils import save_img, get_img, exists, list_files
import tensorflow as tf
import transform
import numpy as np

def style_transfer(style,image_path):
    if image_path == None:
        return None
    batch_size = 1
    root_dir = os.path.abspath('')
    checkpoint_dir = os.path.join(root_dir,'style',style)
    device_t = '/gpu:0'
    img_shape = get_img(image_path).shape

    g = tf.Graph()
    soft_config = tf.ConfigProto(allow_soft_placement=True)
    soft_config.gpu_options.allow_growth = True
    with g.as_default(), g.device(device_t), tf.Session(config=soft_config) as sess:
        batch_shape = (batch_size,) + img_shape
        img_placeholder = tf.placeholder(tf.float32, shape=batch_shape, name='img_placeholder')
        preds = transform.net(img_placeholder)
        saver = tf.train.Saver()

        if os.path.isdir(checkpoint_dir):
            ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
            else:
                raise Exception("No checkpoint found...")
        else:
            saver.restore(sess, checkpoint_dir)

        X = np.zeros(batch_shape, dtype=np.float32)
        img = get_img(image_path)
        X[0] = img
        _preds = sess.run(preds, feed_dict={img_placeholder: X})

        return _preds[0]

if __name__ == '__main__':
    style = 'wave.ckpt'
    image_path = 'images/chicago.jpg'
    style_transfer(style,image_path)
