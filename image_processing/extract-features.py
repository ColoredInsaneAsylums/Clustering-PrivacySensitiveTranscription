import argparse
import cv2
import os
import _pickle as pickle

from descriptors import SIFT, SURF, HOG, ORB

# run image filtering and HOG feature extraction
def main(desc_name):
    print('[INFO] Working...')

    # image directory
    path = './images/'

    # track HOG feature vectors and corresponding images
    features = {}

    # image dimensions
    width = 128
    height = 64

    # feature descriptor
    if desc_name == 'SIFT':
        descriptor = SIFT()
    elif desc_name == 'SURF':
        descriptor = SURF()
    elif desc_name == 'HOG':
        descriptor = HOG()
    elif desc_name == 'ORB':
        descriptor = ORB()

    # evaluate image files
    print('[INFO] Reshaping images and computing ' + desc_name + ' features')
    for filename in os.listdir(path):
        im = cv2.imread(path + filename, cv2.COLOR_BGR2GRAY)

        # resize image and compute features
        im = cv2.resize(im, (width,height))
        v = descriptor.compute(im)

        features[filename] = v

    # save data
    print('[INFO] Saving features and corresponding image name to \'features/' + desc_name + '_features.pickle\'')
    with open('./features/' + desc_name + '_features.pickle', 'wb') as handle:
        pickle.dump(features, handle)

if __name__ == '__main__':
    # require name of descriptor to use
    parser = argparse.ArgumentParser(description='Extract image feature vectors using feature descriptors (i.e., SIFT, SURF, HOG, ORB).')
    parser.add_argument('-d', '--descriptor', required=True,
                        choices=['SIFT', 'SURF', 'HOG', 'ORB'],
                        nargs=1, action='store', type=str, dest='desc_name',
                        help='The name of the descriptor to use (i.e., SIFT, SURF, HOG, ORB)')

    args = vars(parser.parse_args())
    desc_name = args['desc_name'][0]

    main(desc_name)
