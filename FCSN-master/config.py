import pprint


class Config():
    """Config class"""
    def __init__(self, **kwargs):

        # Path
        self.data_path = 'F:/data/ydata-tvsum50-v1_1/fcsn_tvsum.h5'
        self.save_dir = 'F:/data/ydata-tvsum50-v1_1/save_dir'
        self.score_dir = 'F:/data/ydata-tvsum50-v1_1/score_dir'
        self.log_dir = 'F:/data/ydata-tvsum50-v1_1/log_dir'

        # Model
        self.mode = 'train'
        self.gpu = True
        self.n_epochs = 5
        self.n_class = 2
        self.lr = 1e-3
        self.momentum = 0.9
        self.batch_size = 5

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        config_str = 'Configurations\n' + pprint.pformat(self.__dict__)
        return config_str


if __name__ == '__main__':
    config = Config()
    print(config)
