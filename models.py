from torch import nn
import torch

device='cuda' if torch.cuda.is_available() else 'cpu'

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.flatten=nn.Flatten()
        self.network=nn.Sequential(
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512,512),
            nn.ReLU(),
            nn.Linear(512,10)
        )
    
    def forward(self,x):
        x=self.flatten(x)
        logits=self.network(x)
        return logits
    

def test_accuracy(model,dataloader):
    n_currects=0

    model.to(device)
    model.eval()
    for image_batch, label_batch in dataloader:
        image_batch=image_batch.to(device)
        label_batch=label_batch.to(device)
        
        with torch.no_grad():
            logits_batch=model(image_batch)

        predict_batch=logits_batch.argmax(dim=1)
        n_currects += (label_batch==predict_batch).sum().item()


    accuracy=n_currects / len(dataloader.dataset)
    return accuracy


def train(model, dataloader, loss_fn, optimizer):
    model.to(device)
    model.train()
    for image_batch, label_batch in dataloader:
        image_batch=image_batch.to(device)
        label_batch=label_batch.to(device)
        logits_batch=model(image_batch)

        loss=loss_fn(logits_batch, label_batch)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    return loss.item()


def test(model, dataloader, loss_fn):
    loss_total=0.0
    
    model.to(device)
    model.eval()
    for image_batch, label_batch in dataloader:
        image_batch=image_batch.to(device)
        label_batch=label_batch.to(device)
        
        with torch.no_grad():
            logits_batch=model(image_batch)

        loss=loss_fn(logits_batch, label_batch)
        loss_total+=loss.item()

    return loss_total / len(dataloader)