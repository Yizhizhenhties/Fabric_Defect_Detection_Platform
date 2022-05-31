# @author: zrk
# @date: 2022-05-13
# @desc: configuration file that defines hyper-parameters of the model & data loader


class FddConfig:
    def __init__(self):
        self.batch_size = 64
        self.lr = 0.0002
        self.beta1 = 0.5
        self.i_size = 128
        self.nz = 1024
        self.nc = 3
        self.ngf = 16
        self.extra_layers = 0

    def dump_str(self):
        return ''.join([f'{k}: {v}\n' for k, v in self.__dict__.items()])

    def dump_to_file(self, filename):
        with open(filename, 'w') as f:
            f.writelines(self.dump_str())

