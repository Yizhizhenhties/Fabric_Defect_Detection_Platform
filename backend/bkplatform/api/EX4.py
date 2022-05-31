import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import transforms

class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        self.cn1 = nn.Conv2d(1, 16, 3, 1)
        self.cn2 = nn.Conv2d(16, 32, 3, 1)
        self.dp1 = nn.Dropout2d(0.10)
        self.dp2 = nn.Dropout2d(0.25)
        self.fc1 = nn.Linear(4608, 64) # 4608 is basically 12 X 12 X 32
        self.fc2 = nn.Linear(64, 10)

    def forward(self, x):
        x = self.cn1(x)
        x = F.relu(x)
        x = self.cn2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dp1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dp2(x)
        x = self.fc2(x)
        op = F.log_softmax(x, dim=1)
        return op

class MyModel():
    def __init__(self):
        self.device = torch.device("cpu")
        self.model = ConvNet()
        PATH_TO_MODEL = "./api/convnet.pth"
        self.model.load_state_dict(torch.load(PATH_TO_MODEL, map_location="cpu"))
        self.model.eval()

    def run_model(self, input_tensor):
        model_input = input_tensor.unsqueeze(0)
        with torch.no_grad():
            model_output = self.model(model_input)[0]
        model_prediction = model_output.detach().numpy().argmax()
        return model_prediction

    def image_to_tensor(self, image):
        gray_image = transforms.functional.to_grayscale(image)
        resized_image = transforms.functional.resize(gray_image, (28, 28))
        input_image_tensor = transforms.functional.to_tensor(resized_image)
        input_image_tensor_norm = transforms.functional.normalize(input_image_tensor, (0.1302,), (0.3069,))
        return input_image_tensor_norm

    def process(self, img):
        input_ = self.image_to_tensor(img)
        output = self.run_model(input_)
        return output

