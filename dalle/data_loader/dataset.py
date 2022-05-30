from PIL import Image
from typing import Optional
import torchvision.transforms as transforms
import pytorch_lightning as pl
from torch.utils.data import Dataset





class CustomDataset(Dataset):
    def __init__(self, img_paths_label, transform):
        self.X = img_paths_label['path']
        self.y = img_paths_label['label']
        self.transform = transform

    def __getitem__(self, index):
        # image = Image.open(self.X.iloc[index])
        try:
            image = Image.open(self.X.iloc[index]).convert('RGB')
            label = self.y.iloc[index]
            if self.transform:
                image = self.transform(image)
            return image, label
        except:
            print(f'Image load error : {self.X.iloc[index]}')

    def __len__(self):
        return len(self.X)


class CustomDataModule(pl.LightningDataModule):
    def __init__(self,
                config,
                 data_dir: Optional[str] = None,
                 image_resolution: int = 256,
                 train_batch_size: int = 2,
                 valid_batch_size: int = 32,
                 num_workers: int = 8,
                 pin_memory: bool = True):
        
        super().__init__()
        self.config = config
        self.data_dir = data_dir
        self.image_resolution = image_resolution
        self.train_batch_size = train_batch_size
        self.valid_batch_size = valid_batch_size
        self.num_workers = num_workers
        self.pin_memory = pin_memory

        self.train_transform = transforms.Compose(
            [transforms.Resize(image_resolution),
             transforms.RandomCrop(image_resolution),
             transforms.ToTensor(),
             transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])]
        )
        self.valid_transform = transforms.Compose(
            [transforms.Resize(image_resolution),
             transforms.CenterCrop(image_resolution),
             transforms.ToTensor(),
             transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])]
        )

    def setup(self, stage=None):
        self.trainset = CustomDataset(self.config.train, self.config.data_transforms['train'])
        self.validset = CustomDataset(self.config.valid, self.config.data_transforms['val'])