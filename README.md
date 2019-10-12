# UGATIT - Model Training Tutorial

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
python main.py --dataset YOUR_DATASET_NAME --phase test
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
