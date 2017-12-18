import cv2
import numpy
import os
import _pickle as pickle

# run image filtering and HOG feature extraction
def main():
    print('[INFO] Working...')

    # image directory
    path = './images/'

    # track HOG feature vectors and corresponding images
    features = {}
    h_features = []

    # load images in black/white
    ims = {filename: cv2.imread(path + filename, 0) for filename in os.listdir(path)}

    # find largest image dimensions and align to block size and stride
    print('[INFO] Calculating image window size...')
    height = max([im.shape[0] for im in ims.values()])
    width = max([im.shape[1] for im in ims.values()])

    height += 8 - (height % 8)
    width += 8 - (width % 8)

    # HOG feature descriptor
    hog = cv2.HOGDescriptor(_winSize = (width,height),
                            _blockSize = (16,16),
                            _blockStride = (8,8),
                            _cellSize = (8,8),
                            _nbins = 9)

    # evaluate image files
    print('[INFO] Reshaping images and computing HOG features...')
    div = lambda n: (n // 2, n // 2 + 1) if n % 2 else (n // 2, n // 2)
    for filename, im in ims.items():
        # compute padding
        im_h, im_w = im.shape[:2]
        t, b = div(height - im_h)
        l, r = div(width - im_w)

        # pad image with whitespace and compute features
        im = cv2.copyMakeBorder(im, top=t, bottom=b, left=l, right=r,
                                borderType=cv2.BORDER_CONSTANT,
                                value=[255, 255, 255])
        h = hog.compute(im)

        features[filename] = h
        h_features.append(h)

    # save data
    print('[INFO] Saving HOG features and corresponding image name to \'features.pickle\'.')
    with open('features.pickle', 'wb') as handle:
        pickle.dump(features, handle)

    print('[INFO] Saving HOG feature vectors to \'hog_features.csv\'.')
    numpy.savetxt('hog_features.csv',
                  numpy.array(h_features),
                  delimiter=',')

if __name__ == '__main__':
    main()
