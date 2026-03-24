import numpy as np
import matplotlib.pyplot as plt


def get_gmm_data(n, means, covs, alpha):
    """
    生成 GMM 随机样本，这里采用了比较直观的方法，即首先根据 alpha 概率随机选择样本所属的高斯分布，
    然后再根据该高斯分布的参数生成随机生成最终的样本。这种方法相对比较低效，需要 n 次循环。

    Parameters
    ----------
    n : int
        生成随机样本的个数。
    means : list of 1D array
        各个高斯分布的均值，必须使用 list 来存放，或者使用 m x k 的二维矩阵，m 为高斯分布的个数。
    covs : list of 2D array
        各个高斯分布的协方差矩阵，必须使用 list 来存放，或者使用使用 m x k x k 的三维矩阵，k 为样本的维数。
    alpha : list or 1D array
        样本属于各个高斯分布的概率，总和必须为 1。

    Returns
    -------
    k x n 的二维数组，其中 k 为样本维数，可以从 means 推导。
    注意，为了方便进行矩阵的运算，脚本中所有样本都以列向量的形式存在，即每一列代表一个样本。
    """
    models = len(alpha)
    xs = []
    for i in range(n):
        j = np.random.choice(range(models), p=alpha)
        xs.append(np.random.multivariate_normal(means[j].reshape(-1), covs[j]))
    return np.array(xs).T


def gauss_prob(x, mean, cov):
    """
    根据给定 mean, cov 的高斯分布的概率密度函数计算样本 x 的概率密度。注意只适用于单高斯分布。

    Parameters
    ----------
    x : scalar or array
        可以为单个样本，也可以为多个样本。样本既可以是标量，也可以是列向量（单个样本也应该是 k x 1 的形式）。
    mean : scalar or array
        scalar 代表单变量的随机分布，array 代表多变量的随机分布。
        可以以行向量或列向量形式输入，list 形式也可以，实际上包括 scalar 都会首先被转换为 k x 1 的列向量形式。
    cov : scalar or 2D array
        如果 mean 是 scalar, cov 也必须为 scalar，否则应该为 k x k 的二维矩阵。

    Returns
    -------
    如果 x 是单个 scalar 样本，那么也返回一个 scalar，否则都返回一个 shape 为 (n,) 的 1D array。
    """
    return_scalar = True if np.shape(x) is () else False
    mean = np.reshape(mean, [-1, 1])
    dim = mean.shape[0]
    x = np.reshape(x, [dim, -1])
    cov = np.reshape(cov, [dim, dim])

    # 参考多维的高斯概率密度函数公式，注意这里可以一次性求得所有样本的概率密度
    tmp = (x - mean).T
    tmp = np.sum(tmp.dot(np.linalg.inv(cov)) * tmp, axis=1)
    prob = ((2 * np.pi) ** dim * np.linalg.det(cov)) ** (-0.5) * np.exp(-0.5 * tmp)

    if return_scalar:
        prob = prob[0]
    return prob


def gmm_em(xs, models):
    """
    基于 EM 算法估计 GMM 参数的具体实现。

    Parameters
    ----------
    xs : 2D array
        已有的样本，应该为 k x n 的形式，k 为样本维数，n 为样本数量。
        注意即便 k=1 样本也应该使用列向量的形式，因为代码大部分采用了矩阵运算。
    models : int
        高斯分布个数。

    Returns
    -------
    alpha : 1D array
        样本属于各个高斯分布的概率
    means : lsit of 1D array
        各个高斯分布的均值，以 list 形式存储
    covs : list of 2D array
        各个高斯分布的协方差矩阵，以 list 形式存储
    """
    # 根据样本的总体均值和协方差矩阵随机初始化各个高斯分布的参数，这种方式仅供参考
    dims, n = xs.shape[:2]
    mean = np.mean(xs, axis=1, keepdims=True)
    cov = (xs - mean).dot((xs - mean).T) / n
    alpha = np.random.rand(models) + 0.1
    alpha = alpha / np.sum(alpha)

    means, covs = [], []
    rnd_range = (np.max(xs, axis=1) - np.min(xs, axis=1)) * 0.8  # 样本数据的范围乘以一个缩放系数
    for i in range(models):
        means.append(mean.ravel() + (np.random.rand(dims) - 0.5) * rnd_range)  # 总体均值加上一个随机数
        covs.append(np.copy(cov))  # 直接使用总体协方差矩阵
    means, covs = np.array(means), np.array(covs)

    """ EM 算法流程 """
    for epoch in range(100):
        # 根据各个高斯分布的参数求得每个样本属于各个高斯分布的后验概率，即 E step
        probs = np.array([gauss_prob(xs, _mean, _cov) for _mean, _cov in zip(means, covs)])
        post_probs = np.diag(alpha).dot(probs)
        post_probs = post_probs / np.sum(post_probs, axis=0)

        # 根据求得的后验概率更新各个高斯分布的参数，即 M step
        new_alpha = np.sum(post_probs, axis=1)
        new_means = xs.dot(post_probs.T) / new_alpha
        new_covs = []
        for i in range(models):
            tmp = xs - new_means[:, [i]]
            new_covs.append(tmp.dot(np.diag(post_probs[i])).dot(tmp.T) / new_alpha[i])
        new_alpha = new_alpha / n
        new_means = new_means.T
        new_covs = np.array(new_covs)

        # 判断参数的更新是否停滞，这里使用了无穷阶范数，即 max(abs(x))，也可以改为 2nd 范数
        diff_alpha = np.linalg.norm(np.ravel(alpha - new_alpha), np.inf)
        diff_means = np.linalg.norm(np.ravel(means - new_means), np.inf)
        diff_covs = np.linalg.norm(np.ravel(covs - new_covs), np.inf)

        alpha = new_alpha
        means = new_means
        covs = new_covs

        if diff_alpha <= 1e-3 and diff_means <= 1e-3 and diff_covs <= 1e-3:
            print('Solved in {} epoches.'.format(epoch))
            break
    return alpha, list(means), list(covs)


if __name__ == '__main__':
    means = [np.array([5, 6]), np.array([1, 2])]
    covs = [np.array([[1, 0.1], [0.1, 0.5]]), np.array([[0.8, 1.2], [1.2, 3.5]])]
    alpha = np.array([0.3, 0.7])
    n = 2000

    xs = get_gmm_data(n, means, covs, alpha)
    # plt.scatter(xs[0], xs[1])
    # plt.show()

    _alpha, _means, _covs = gmm_em(xs, 2)
    print(_alpha)
    print(_means)
    print(_covs)

