# @author: zrk
# @date: 2022-05-13
# @desc: basic neural network modules


import torch.nn as nn


class Encoder(nn.Module):
    def __init__(self, i_size, nz, nc, ndf, n_extra_layers=0, add_final_conv=True):
        super(Encoder, self).__init__()
        assert i_size % 16 == 0, "i_size has to be a multiple of 16"

        net = nn.Sequential()
        net.add_module('initial-conv-{0}-{1}'.format(nc, ndf),
                       nn.Conv2d(nc, ndf, 4, 2, 1, bias=False))
        net.add_module('initial-relu-{0}'.format(ndf), nn.LeakyReLU(0.2, inplace=True))
        c_size, c_ndf = i_size / 2, ndf

        for t in range(n_extra_layers):
            net.add_module('extra-layers-{0}-{1}-conv'.format(t, c_ndf),
                           nn.Conv2d(c_ndf, c_ndf, 3, 1, 1, bias=False))
            net.add_module('extra-layers-{0}-{1}-batchnorm'.format(t, c_ndf),
                           nn.BatchNorm2d(c_ndf))
            net.add_module('extra-layers-{0}-{1}-relu'.format(t, c_ndf),
                           nn.LeakyReLU(0.2, inplace=True))

        while c_size > 4:
            in_feat = c_ndf
            out_feat = c_ndf * 2
            net.add_module('pyramid-{0}-{1}-conv'.format(in_feat, out_feat),
                           nn.Conv2d(in_feat, out_feat, 4, 2, 1, bias=False))
            net.add_module('pyramid-{0}-batchnorm'.format(out_feat),
                           nn.BatchNorm2d(out_feat))
            net.add_module('pyramid-{0}-relu'.format(out_feat),
                           nn.LeakyReLU(0.2, inplace=True))
            c_ndf = c_ndf * 2
            c_size = c_size / 2

        if add_final_conv:
            net.add_module('final-{0}-{1}-conv'.format(c_ndf, 1),
                           nn.Conv2d(c_ndf, nz, 4, 1, 0, bias=False))

        self.net = net

    def forward(self, input_):
        return self.net(input_)


class Decoder(nn.Module):
    def __init__(self, i_size, nz, nc, ngf, n_extra_layers=0):
        super(Decoder, self).__init__()
        assert i_size % 16 == 0, "i_size has to be a multiple of 16"

        c_ngf, ti_size = ngf // 2, 4
        while ti_size != i_size:
            c_ngf = c_ngf * 2
            ti_size = ti_size * 2

        main = nn.Sequential()
        # input is Z, going into a convolution
        main.add_module('initial-{0}-{1}-convt'.format(nz, c_ngf),
                        nn.ConvTranspose2d(nz, c_ngf, 4, 1, 0, bias=False))
        main.add_module('initial-{0}-batchnorm'.format(c_ngf),
                        nn.BatchNorm2d(c_ngf))
        main.add_module('initial-{0}-relu'.format(c_ngf),
                        nn.ReLU(True))

        c_size, _ = 4, c_ngf
        while c_size < i_size // 2:
            main.add_module('pyramid-{0}-{1}-convt'.format(c_ngf, c_ngf // 2),
                            nn.ConvTranspose2d(c_ngf, c_ngf // 2, 4, 2, 1, bias=False))
            main.add_module('pyramid-{0}-batchnorm'.format(c_ngf // 2),
                            nn.BatchNorm2d(c_ngf // 2))
            main.add_module('pyramid-{0}-relu'.format(c_ngf // 2),
                            nn.ReLU(True))
            c_ngf = c_ngf // 2
            c_size = c_size * 2

        # Extra layers
        for t in range(n_extra_layers):
            main.add_module('extra-layers-{0}-{1}-conv'.format(t, c_ngf),
                            nn.Conv2d(c_ngf, c_ngf, 3, 1, 1, bias=False))
            main.add_module('extra-layers-{0}-{1}-batchnorm'.format(t, c_ngf),
                            nn.BatchNorm2d(c_ngf))
            main.add_module('extra-layers-{0}-{1}-relu'.format(t, c_ngf),
                            nn.ReLU(True))

        main.add_module('final-{0}-{1}-convt'.format(c_ngf, nc),
                        nn.ConvTranspose2d(c_ngf, nc, 4, 2, 1, bias=False))
        main.add_module('final-{0}-tanh'.format(nc),
                        nn.Tanh())
        self.main = main

    def forward(self, input_):
        return self.main(input_)


class SimpleAutoEncoder(nn.Module):
    def __init__(self, input_size=128, embed_size=32, output_size=128, in_channel=1, ngf=32, out_channel=1):
        super(SimpleAutoEncoder, self).__init__()
        self.input_size = input_size
        self.embed_size = embed_size
        self.output_size = output_size

        enc_list = []
        dec_list = []

        # how many layers?
        count = 0
        while embed_size < input_size:
            embed_size *= 2
            count += 1

        in_c = in_channel
        for _ in range(count):
            enc_list += [
                nn.Conv2d(in_c, ngf, 3, 1, 1),
                nn.BatchNorm2d(ngf),
                nn.ReLU(True),
                nn.MaxPool2d(2, 2),
            ]
            in_c = ngf
            ngf += ngf

        for i in range(count):
            ngf //= 2
            out_c = out_channel if i == count - 1 else ngf // 2
            dec_list += [
                nn.UpsamplingBilinear2d(scale_factor=2),
                nn.Conv2d(ngf, out_c, 3, 1, 1),
                nn.BatchNorm2d(out_c),
                nn.ReLU(True),
            ]
        dec_list = dec_list[:-2]

        self.net_enc = nn.Sequential(*tuple(enc_list))
        self.net_dec = nn.Sequential(*tuple(dec_list))

    def forward(self, x):
        x = self.net_enc(x)
        x = self.net_dec(x)
        return x


class SimpleSegmentation(nn.Module):
    def __init__(self, size, in_feature):
        super(SimpleSegmentation, self).__init__()
        self.net = nn.Conv2d(in_feature, 1, 3, 1, 1)
        self.act = nn.Sigmoid()

    def forward(self, x):
        x = self.net(x)
        x = self.act(x)
        return x


class NetG(nn.Module):
    def __init__(self, i_size, nz, nc, ngf, extra_layers):
        super(NetG, self).__init__()
        self.encoder1 = Encoder(i_size, nz, nc, ngf, extra_layers)
        self.decoder  = Decoder(i_size, nz, nc, ngf, extra_layers)
        self.encoder2 = Encoder(i_size, nz, nc, ngf, extra_layers)

    def forward(self, x):
        latent_i = self.encoder1(x)
        gen_img  = self.decoder(latent_i)
        latent_o = self.encoder2(gen_img)
        return gen_img, latent_i, latent_o


class NetD(nn.Module):
    def __init__(self, i_size, nc, ngf, extra_layers):
        super(NetD, self).__init__()
        model  = Encoder(i_size, 1, nc, ngf, extra_layers)
        layers = list(model.net.children())

        self.features = nn.Sequential(*layers[:-1])
        self.classifier = nn.Sequential(layers[-1])
        self.classifier.add_module('Sigmoid', nn.Sigmoid())

    def forward(self, img):
        features = self.features(img)
        real_or_fake = self.classifier(features)
        real_or_fake = real_or_fake.view(-1, 1).squeeze(1)
        return real_or_fake, features


# class NetC(nn.Module):
#     def __init__(self, opt):
#         super(NetC, self).__init__()
#         i_size = int(opt.nz ** 0.5)
#
#         model = Encoder(i_size, 1, 1, opt.ngf, opt.ngpu, opt.extralayers)
#         layers = list(model.main.children())
#
#         self.features_io = nn.Sequential(*layers[:-1])
#         self.classifier_io = nn.Sequential(layers[-1])
#         self.classifier_io.add_module('Sigmoid', nn.Sigmoid())
#
#     def forward(self, z):
#         features_io = self.features_io(z)
#         features_io = features_io
#         classifier_io = self.classifier_io(features_io)
#         classifier_io = classifier_io.view(-1, 1).squeeze(1)
#         return classifier_io
