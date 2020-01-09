# UGATIT - Model Training Tutorial

Selfie2Anime was a successful use of Image-to-Image translation using UGATIT. In this post we learn how to setup a development environment capable of running UGATIT, then train out own variation of a model.

Detailed tutorial for training and inference are outlined in the [blog](.blog/README.md)

## Setup

### Pip

```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

### Conda

```bash
conda env create -f environment.yml
conda activate UGATIT
```

## Usage

```bash
├── dataset
   └── YOUR_DATASET_NAME
       ├── trainA
           ├── xxx.jpg (name, format does not matter)
           ├── yyy.png
           └── ...
       ├── trainB
           ├── zzz.jpg
           ├── www.png
           └── ...
       ├── testA
           ├── aaa.jpg
           ├── bbb.png
           └── ...
       └── testB
           ├── ccc.jpg
           ├── ddd.png
           └── ...
```

### Train

```bash
python main.py --dataset YOUR_DATASET_NAME
```

If the memory of gpu is **not sufficient**, set `--light` to **True**

* But it may **not** perform well
* paper version is `--light` to **False**

### Test

```bash
python main.py --dataset YOUR_DATASET_NAME --phase test --light True
```

### Test Video

Make sure to set your video device in the `State` class of `main.py` if you have a unique setup.

By default it'll use the first video device attached

```bash
python main.py --dataset YOUR_DATASET_NAME --phase video --light True
```

### Test Process Endpoint [WIP]

```bas
python main.py --dataset YOUR_DATASET_NAME --phase web --light True
```

POST to `http://0.0.0.0:5000/process` with the following data format

```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...."
}
```

## Common Errors

### No module named 'tensorflow.contrib'

Version 2.0 of Tensorflow isn't supported, you might need to change the `environment.yaml` to the following

```yaml
name: UGATIT
dependencies:
  - python=3.5
  - matplotlib
  - numpy
  - pip
  - pip:
    - opencv-python
    - Pillow
#    - tensorflow==1.15.0 # CPU support
    - tensorflow-gpu==1.15.0
```

## Citation

If you find the code useful for your research, please cite their paper:

```
@article{kim2019u,
  title={U-GAT-IT: Unsupervised Generative Attentional Networks with Adaptive Layer-Instance Normalization for Image-to-Image Translation},
  author={Kim, Junho and Kim, Minjae and Kang, Hyeonwoo and Lee, Kwanghee},
  journal={arXiv preprint arXiv:1907.10830},
  year={2019}
}
```

## Attribution

* [Junho Kim](http://bit.ly/jhkim_ai), Minjae Kim, Hyeonwoo Kang, Kwanghee Lee
* [U-GAT-IT: Unsupervised Generative Attentional Networks with Adaptive Layer-Instance Normalization for Image-to-Image Translation](https://arxiv.org/abs/1907.10830)
