import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Define paths and load resources
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKING_DIR = BASE_DIR

with open(os.path.join(WORKING_DIR, 'Transmitter/models/features.pkl'), 'rb') as f:
    features = pickle.load(f)

with open(os.path.join(BASE_DIR, 'Transmitter/models/captions.txt'), 'r') as f:
    next(f)
    captions_doc = f.read()

# Create mapping of image to captions
mapping = {}
for line in captions_doc.split('\n'):
    tokens = line.split(',')
    if len(tokens) < 2:
        continue
    image_id, caption = tokens[0], tokens[1:]
    image_id = image_id.split('.')[0]
    caption = " ".join(caption)
    if image_id not in mapping:
        mapping[image_id] = []
    mapping[image_id].append(caption)

def clean(mapping):
    import re
    for key, captions in mapping.items():
        for i in range(len(captions)):
            caption = captions[i]
            caption = caption.lower()
            caption = re.sub(r'[^a-z]+', ' ', caption)
            caption = re.sub(r'\s+', ' ', caption).strip()
            caption = 'startseq ' + " ".join([word for word in caption.split() if len(word) > 1]) + ' endseq'
            captions[i] = caption

clean(mapping)

# Tokenize the text
all_captions = [caption for captions in mapping.values() for caption in captions]
tokenizer = Tokenizer()
tokenizer.fit_on_texts(all_captions)
vocab_size = len(tokenizer.word_index) + 1

def idx_to_word(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

def predict_caption(model, image, tokenizer, max_length):
    in_text = 'startseq'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], max_length)
        yhat = model.predict([image, sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = idx_to_word(yhat, tokenizer)
        if word is None:
            break
        in_text += " " + word
        if word == 'endseq':
            break
    return in_text

# Load VGG16 model
vgg_model = VGG16()
vgg_model = Model(inputs=vgg_model.inputs, outputs=vgg_model.layers[-2].output)

# Load the pre-trained captioning model
try:
    model = tf.keras.models.load_model('Transmitter/models/best_model.h5')
except IOError:
    raise Exception("Captioning model file not found or is corrupted")

def generate_caption(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    feature = vgg_model.predict(image, verbose=0)
    caption = predict_caption(model, feature, tokenizer, 35)
    return caption[8:len(caption)-7]

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python caption_generator.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    caption = generate_caption(image_path)
    print(caption)
