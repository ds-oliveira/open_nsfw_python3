#!/usr/bin/env python
"""
Copyright 2016 Yahoo Inc.
Licensed under the terms of the 2 clause BSD license. 
Please see LICENSE file in the project root for terms.
"""

import numpy as np
from PIL import Image
import io
import caffe


class NSFWClassifier:
    def __init__(self):
        """
        Classification model used for sexual content prediction.

        classifier = NSFWClassifier()

        Methods
        -------
        get_score : returns the sexual content score of a given image.
        """
        self.model_def = "deploy.prototxt"
        self.pretrained_model = "resnet_50_1by2_nsfw.caffemodel"

    def resize_image(self, data, sz=(256, 256)):

        im = Image.open(data)
        if im.mode != "RGB":
            im = im.convert('RGB')
        imr = im.resize(sz, resample=Image.BILINEAR)
        fh_im = data
        imr.save(fh_im, format='JPEG')
        fh_im.seek(0)
        return io.BytesIO(fh_im.read())

    def caffe_preprocess_and_compute(self, pimg, caffe_transformer=None, caffe_net=None, output_layers=None):

        if caffe_net is not None:

            # Grab the default output names if none were requested specifically.
            if output_layers is None:
                output_layers = caffe_net.outputs

            img_data_rs = self.resize_image(pimg, sz=(256, 256))
            image = caffe.io.load_image(img_data_rs)

            H, W, _ = image.shape
            _, _, h, w = caffe_net.blobs['data'].data.shape
            h_off = max((H - h) / 2, 0)
            w_off = max((W - w) / 2, 0)
            crop = image[int(h_off):int(h_off) + int(h),
                         int(w_off):int(w_off) + int(w), :]
            transformed_image = caffe_transformer.preprocess('data', crop)
            transformed_image.shape = (1,) + transformed_image.shape

            input_name = caffe_net.inputs[0]
            all_outputs = caffe_net.forward_all(
                blobs=output_layers, **{input_name: transformed_image})

            outputs = all_outputs[output_layers[0]][0].astype(float)
            return outputs
        else:
            return []

    def get_score(self, filepath):
        """
        Returns the sexual content score of a given image.

        score = get_score('image1.jpg')

        Parameters
        ----------
        filepath : the relative local path of the image file.
        """
        with open(filepath, 'rb') as f:
            image_data = io.BytesIO(f.read())

        # Pre-load caffe model.
        nsfw_net = caffe.Net(str(self.model_def),  # pylint: disable=invalid-name
                             str(self.pretrained_model), caffe.TEST)

        # Load transformer
        # Note that the parameters are hard-coded for best results
        caffe_transformer = caffe.io.Transformer(
            {'data': nsfw_net.blobs['data'].data.shape})
        # move image channels to outermost
        caffe_transformer.set_transpose('data', (2, 0, 1))
        # subtract the dataset-mean value in each channel
        caffe_transformer.set_mean('data', np.array([104, 117, 123]))
        # rescale from [0, 1] to [0, 255]
        caffe_transformer.set_raw_scale('data', 255)
        caffe_transformer.set_channel_swap(
            'data', (2, 1, 0))  # swap channels from RGB to BGR

        # Classify.
        scores = self.caffe_preprocess_and_compute(
            image_data, caffe_transformer=caffe_transformer, caffe_net=nsfw_net, output_layers=['prob'])

        # Scores is the array containing SFW / NSFW image probabilities
        # scores[1] indicates the NSFW probability
        return scores[1]
