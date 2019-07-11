# train_models.py
import os
import pickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture
from extract_feature import extract_features
import warnings
import librosa

warnings.filterwarnings("ignore")

# path to training data
source = r'voice_list.txt'

# path where training speakers will be saved
dest = "universal_model\\"
speaker_paths = open(source, 'r')
# train_file = "development_set_enroll.txt"
features = np.asarray(())
for speaker in speaker_paths:
    print('speaker ' + str(speaker))
    for root, dirs, files in os.walk(str(speaker).replace('\n', '')):
        count = 0
        for file in files:
            if count == 10:
                break
            if file.endswith('.m4a'):
                print('file ' + str(file))
                file_path = os.path.join(root, file)
                audio, sr = librosa.core.load(file_path)
                vector = extract_features(audio, sr)
                if features.size == 0:
                    features = vector
                else:
                    features = np.vstack((features, vector))

                count += 1
ubm = GaussianMixture(n_components=512, max_iter=200, covariance_type='diag', n_init=3)
ubm.fit(features)

# dumping the trained gaussian model
picklefile = "ubm.gmm"
pickle.dump(ubm, open(dest + picklefile, 'wb'))
print('modeling completed for ubm with data point = '+ str(features.shape))
features = np.asarray(())

# file_paths = []
# for root, dirs, files in os.walk(source):
#     for file in files:
#         if file.endswith('.wav'):
#             file_paths.append(os.path.join(root, file))
#
# print(len(file_paths))
# features = np.asarray(())
# for wav_file in file_paths:
#     sr, audio = read(wav_file)
#
#     vector = extract_features(audio, sr)
#
#     if features.size == 0:
#         features = vector
#     else:
#         features = np.vstack((features, vector))
#
# ubm = GaussianMixture(n_components=128, max_iter=200, covariance_type='diag', n_init=3)
# ubm.fit(features)
#
# # dumping the trained gaussian model
# picklefile = "ubm.gmm"
# pickle.dump(ubm, open(dest + picklefile, 'wb'))
# print('modeling completed for ubm with data point = '+ str(features.shape))
# features = np.asarray(())
#
# count = 1
#
# # Extracting features for each speaker (5 files per speakers)
# features = np.asarray(())
# for path in file_paths:
#     path = path.strip()
#     print(path)
#
#     # read the audio
#     sr, audio = read(source + path)
#
#     # extract 40 dimensional MFCC & delta MFCC features
#     vector = extract_features(audio, sr)
#
#     if features.size == 0:
#         features = vector
#     else:
#         features = np.vstack((features, vector))
#     # when features of 5 files of speaker are concatenated, then do model training
#     if count == 5:
#         gmm = GaussianMixture(n_components=16, max_iter=200, covariance_type='diag', n_init=3)
#         gmm.fit(features)
#
#         # dumping the trained gaussian model
#         picklefile = path.split("-")[0] + ".gmm"
#         pickle.dump(gmm, open(dest + picklefile, 'wb'))
#         print('+ modeling completed for speaker:', picklefile, " with data point = ", features.shape)
#         features = np.asarray(())
#         count = 0
#     count = count + 1
