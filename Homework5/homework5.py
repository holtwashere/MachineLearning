import numpy as np
from data import load_data, flatten_data
from mahalanobis import discriminant
from confusion_matrix import confusion_matrix
from coordinates import cart2pol, pol2cart
from plot import plot_data
from polar_descriminant import mu_estimate


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

    flat_test, labels_test = flatten_data(test, c)

    disc_values = np.zeros((100, 3))

    ####### Part B ######

    for i, point in enumerate(flat_test):
        for j in range(c):
            m = discriminant(point, means[j], covs[j], d, prior)
            disc_values[i, j] = m

    predicted = np.argmax(disc_values, axis=1)

    ####### Part C #########

    cm, acc = confusion_matrix(labels_test, predicted, c)

    print("Part C Covariance Matrix")
    print(cm)
    print(f"Error = {1 - acc}")

    ####### Part D ##########

    flat_train, labels_train = flatten_data(train, c)

    plot_data(flat_train.T[0], flat_train.T[1], labels_train, c)
    plot_data(flat_test.T[0], flat_test.T[1], labels_test, c)

    r_train, theta_train = cart2pol(flat_train)

    r_test, theta_test = cart2pol(flat_test)

    plot_data(r_train, theta_train, labels_train, c)
    plot_data(r_test, theta_test, labels_test, c)

    means = np.empty(c)
    covs = np.empty(c)
    posterior = np.zeros(c)

    disc_values = np.empty((r_test.shape[0], c))

    for i in range(c):
        means[i], covs[i] = mu_estimate(
            r_train[labels_train == i], 0, 100, .25)

    for i, pt in enumerate(r_test):
        for j in range(c):
            disc_values[i, j] = discriminant(
                pt, means[j], covs[j], d, prior)

    predicted = np.argmax(disc_values, axis=1)

    cm, acc = confusion_matrix(labels_test, predicted, c)

    print("Part D Covariance Matrix")
    print(cm)
    print(f"Error = {1 - acc}")


if __name__ == "__main__":
    main()
