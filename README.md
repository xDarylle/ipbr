# Intellegent Portrait Background Replacement

A solution for removing and replacing backgrounds for graduation photo, IDs, etc.

## Description

This is based on [MODNet: Trimap-Free Portrait Matting in Real Time](https://github.com/ZHKKKe/MODNet)

## Instruction
1. Clone this repository:
```
git clone https://github.com/xShiro2/ipbr.git
cd ipbr
```
2. Download pre-trained model from this [link](https://drive.google.com/drive/folders/1umYmlCulvIFNaqPjwod1SayFmSRHziyR) and put it into the folder `MODNet/pretrained`
3. Install the required python dependencies
```
pip install -r requirements.txt
```
4. Execute code:
```
python -m scripts.main_gui
```

