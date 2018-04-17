import numpy as np
from data import load_data, flatten_data
from mahalanobis import discriminant
from confusion_matrix import confusion_matrix
from coordinates import cart2pol, pol2cart
from plot import plot_data


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

    flat_train, labels_train = flatten_data(train, c)
    labels_test = actual

    r_train, theta_train = cart2pol(flat_train)

    r_test, theta_test = cart2pol(flat_test)
    plot_data(r_train, theta_train, labels_train, c)
    plot_data(r_test, theta_test, labels_test, c)


if __name__ == "__main__":
    main()
