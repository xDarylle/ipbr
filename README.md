# Intellegent Portrait Background Replacement

A solution for removing and replacing backgrounds for graduation photo, IDs, etc. This is based on [MODNet: Trimap-Free Portrait Matting in Real Time](https://github.com/ZHKKKe/MODNet)

## Prerequisite
- [MODNet Pre-trained Model](https://drive.google.com/drive/folders/1umYmlCulvIFNaqPjwod1SayFmSRHziyR)
- [Pytorch](https://pytorch.org/)

## Instructions
1. Clone this repository
```
git clone https://github.com/xShiro2/ipbr.git
cd ipbr
```

2. Setup and activate virtual environment
```
python -m venv venv
venv/Scripts/activate
```

3. Download [pre-trained model](https://drive.google.com/drive/folders/1umYmlCulvIFNaqPjwod1SayFmSRHziyR) and extract contents to `MODNet/pretrained`

4. Install the required python dependencies
```
pip install -r requirements.txt
```

5. Install Pytorch seperately from [here](https://pytorch.org/)


6. Run code
```
python -m scripts.main_gui
```

