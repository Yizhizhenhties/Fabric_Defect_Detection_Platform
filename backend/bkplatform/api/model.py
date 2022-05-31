# @author: zrk
# @date: 2022-05-13
# @desc: defines a model for defect detection


import torch
import torch.nn as nn
import torch.utils.data.dataloader as torch_loader
from torch.optim import Optimizer, Adam
from api.networks import NetG, NetD
from tqdm import tqdm


def _weights_init(mod):
    class_name = mod.__class__.__name__
    if class_name.find('Conv') != -1:
        mod.weight.data.normal_(0.0, 0.02)
    elif class_name.find('BatchNorm') != -1:
        mod.weight.data.normal_(1.0, 0.02)
        mod.bias.data.fill_(0)


class FddModel:
    def __init__(self, net_gen: NetG, net_dis: NetD, opt_gen: Optimizer, opt_dis: Optimizer,
                 device, w_adv=1, w_con=50, w_enc=1):
        self.net_gen = net_gen
        self.net_dis = net_dis
        self.opt_gen = opt_gen
        self.opt_dis = opt_dis
        self.l_adv = nn.MSELoss()
        self.l_con = nn.L1Loss()
        self.l_enc = nn.MSELoss()
        self.l_bce = nn.BCELoss()
        self.w_adv = w_adv
        self.w_con = w_con
        self.w_enc = w_enc
        self.device = device

    def set_train(self):
        self.net_gen.train()
        self.net_dis.train()

    def set_eval(self):
        self.net_gen.eval()
        self.net_dis.eval()

    def train_once(self, real_img: torch.Tensor):
        batch_size = real_img.shape[0]
        real_label = torch.ones(size=(batch_size,),  dtype=torch.float32, device=real_img.device)
        fake_label = torch.zeros(size=(batch_size,), dtype=torch.float32, device=real_img.device)

        # generator forward
        fake_img, latent_i, latent_o = self.net_gen(real_img)

        # discriminator forward
        class_real, fea_real = self.net_dis(real_img)
        class_fake, fea_fake = self.net_dis(fake_img.detach())

        # generator backward
        self.opt_gen.zero_grad()
        err_g_adv = self.l_adv(fea_real, fea_fake)
        err_g_con = self.l_con(fake_img, real_img)
        err_g_enc = self.l_enc(latent_i, latent_o)
        err_g = err_g_adv * self.w_adv + err_g_con * self.w_con + err_g_enc * self.w_enc
        err_g.backward(retain_graph=True)
        self.opt_gen.step()

        # discriminator backward
        self.opt_dis.zero_grad()
        err_d_real = self.l_bce(class_real, real_label)
        err_d_fake = self.l_bce(class_fake, fake_label)
        err_d = (err_d_real + err_d_fake) * 0.5
        err_d.backward()
        self.opt_dis.step()

        return err_g.item(), err_d.item()

    def train_one_epoch(self, loader: torch_loader.DataLoader, d_threshold=1e-5, progress_bar=True):
        iter_ = tqdm(loader) if progress_bar else loader
        g_ls = []
        d_ls = []
        for image, index in iter_:
            image = image.to(self.device)
            err_g, err_d = self.train_once(image)
            g_ls.append(err_g)
            d_ls.append(err_d)
            if err_d < d_threshold:
                self.net_dis.apply(_weights_init)
        return g_ls, d_ls


class SegModel:
    pass


def make_seg_model():
    pass


def make_fdd_model(device, lr=0.0002, beta1=0.5, i_size=128, nz=1024, nc=3, ngf=16, extra_layers=0):
    net_gen = NetG(i_size, nz, nc, ngf, extra_layers).to(device)
    net_dis = NetD(i_size, nc, ngf, extra_layers).to(device)
    opt_gen = Adam(net_gen.parameters(), lr, betas=(beta1, 0.999))
    opt_dis = Adam(net_dis.parameters(), lr, betas=(beta1, 0.999))

    net_gen.apply(_weights_init)
    net_dis.apply(_weights_init)

    return FddModel(net_gen, net_dis, opt_gen, opt_dis, device)
