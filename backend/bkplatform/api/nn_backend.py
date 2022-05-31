import PIL.Image
import api.model as model
import api.fdd_configs as fdd_configs
import api.networks as networks
import torch
import torch.nn.functional as F
import torchvision
import numpy as np


class Backend:
    def __init__(self):
        self.device = torch.device("cpu")

        cfg = fdd_configs.FddConfig()
        fdd_model = model.make_fdd_model(self.device, cfg.lr, cfg.beta1, cfg.i_size,
                                         cfg.nz, cfg.nc, cfg.ngf, cfg.extra_layers)  # fabrics defect detection model
        net_gen = fdd_model.net_gen
        epoch = 1400
        net_gen.load_state_dict(torch.load(f'./api/checkpoint/gen/net_{epoch}.pth', map_location='cpu'))
        net_gen.eval()

        ae_net = networks.SimpleAutoEncoder().to(self.device)
        epoch = 150
        ae_net.load_state_dict(torch.load(f'./api/checkpoint/ae/{epoch}.pth', map_location='cpu'))
        ae_net.eval()

        seg_net = networks.SimpleSegmentation(32, 64).to(self.device)
        epoch = 100
        seg_net.load_state_dict(torch.load(f'./api/checkpoint/seg/{epoch}.pth', map_location='cpu'))
        seg_net.eval()

        self.net_gen = net_gen
        self.ae_net = ae_net
        self.seg_net = seg_net

        self.transform = torchvision.transforms.Compose([
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Resize(128),
            torchvision.transforms.CenterCrop(128),
            torchvision.transforms.Normalize((0.5,), (0.5,))
        ])
        self.to_pil = torchvision.transforms.ToPILImage()
        red = torch.tensor((1.0, 0.0, 0.0), device=self.device)[..., None, None]
        self.red = torch.broadcast_to(red, (3, 128, 128))

    def process(self, image: PIL.Image.Image, th1=0.0012, th2=0.04) -> (bool, PIL.Image.Image):
        input_ = self.transform(image).to(self.device)
        input_ = input_[None, ...]
        if input_.shape[1] == 1:
            input_ = torch.cat([input_, input_, input_], dim=1)

        with torch.no_grad():
            _, latent_i, latent_o = self.net_gen(input_)
            b_diff = ((latent_i - latent_o) ** 2).mean(dim=(1, 2, 3))
            score = b_diff[0].item()
            print(score)
            is_normal = score < th1
            is_fabric = score < th2
            input_ = input_[:, 0: 1, ...]
            feature = self.ae_net.net_enc(input_)
            mask = self.seg_net(feature)
            mask = F.interpolate(mask, scale_factor=4, mode='bicubic', align_corners=True)

        mask = torch.cat([mask, mask, mask], dim=1)[0]
        input_ = (input_ + 1.0) * 0.5

        if is_normal: mask = mask.zero_()
        weight = (mask.clone() - 0.25)
        weight[weight < 0.0] = 0.0
        heat = input_[0] * (1.0 - weight) + self.red * weight

        mask = mask.permute((1, 2, 0)).cpu().numpy()
        mask = np.clip(mask, 0, 1)

        heat = heat.permute((1, 2, 0)).cpu().numpy()
        heat = np.clip(heat, 0, 1)

        pil_mask = PIL.Image.fromarray(np.uint8(mask*255), 'RGB')
        pil_heat = PIL.Image.fromarray(np.uint8(heat*255), 'RGB')
        return is_fabric, is_normal, pil_mask, pil_heat


