import numpy as np
from scipy.io.matlab import loadmat
from mahalanobis import discriminant
from confusion_matrix import confusion_matrix
from coordinates import cart2pol, pol2cart


def load_data():

    train, test = loadmat("./test_train_data_class3.mat")["Data"][0][0]

    train = np.array(train[0])
    test = np.array(test[0])

    for i in range(train.shape[0]):
        train[i] = np.transpose(train[i])

    for i in range(test.shape[0]):
        test[i] = np.transpose(test[i])
    return train, test


def flatten_data(data, c):
    actual = np.array([], dtype=int)
    flat = np.zeros(2)

    # Flatten Test Array
    for i in range(c):
        for j in range(data[i].shape[0]):
            actual = np.append(actual, i)
            flat = np.vstack([flat, data[i][j]])

    flat = flat[1:101]

    return flat, actual


def main():

    train, test = load_data()

    prior = 1 / 3

    # Num Classes
    c = train.shape[0]
    # Num Dimensions
    d = train[0].shape[1]

    means = np.empty((c, d))
    covs = np.empty(((c, d, d)))

    ###### Part A #######
    for i in range(c):
        means[i] = np.mean(train[i], axis=0)
        covs[i] = np.cov(train[i], rowvar=0)

    predicted = np.array([], dtype=int)

    flat_test, actual = flatten_data(test, c)

    disc_values = np.zeros((100, 3))

    ####### Part B ######
    for i, point in enumerate(flat_test):
        for j in range(c):
            m = discriminant(point, means[j], covs[j], d, prior)
            disc_values[i, j] = m

    predicted = np.argmax(disc_values, axis=1)

    ####### Part C #########
    cm, acc = confusion_matrix(actual, predicted, c)

    print(cm)
    print(f"Error = {1 - acc}")

    ####### Part D ##########

    flat_train, _ = flatten_data(train, c)

    polar = cart2pol()


if __name__ == "__main__":
    main()
