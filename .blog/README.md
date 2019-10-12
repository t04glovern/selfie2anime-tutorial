# Building your own UGATIT Model

## Preface

[Selfie2Anime](https://selfie2anime.com/) was a successful use of Image-to-Image translation using [UGATIT](https://github.com/taki0112/UGATIT); a project by Junho Kim, Minjae Kim, Hyeonwoo Kang and Kwanghee Lee. This however isn't the only combination of images that could be swapped. The combinations are literally limitless, and in this post I'd like to describe how you can create your very own alternate variation.

The work that's required to train your own version of this project is described at a high level below:

* [Development Environment Setup](#Development-Environment-Setup)
* [Dataset Collection & Preparation](#Dataset-Collection-&-Preparation)
* [Model Training](#Model-Training)
* [Model Inference](#Model-Inference)

---

## Development Environment Setup

---

### Base Requirements

You should be able to make use of either AWS SageMaker or Google Colab, however for people who are planning on training or performing inference locally the following requirements are good to have setup

* Clone the tutorial respository at [https://github.com/t04glovern/x2x-tutorial](https://github.com/t04glovern/x2x-tutorial)
* [AWS CLI Setup](https://aws.amazon.com/cli/) and authenticated with an account (Optional)
* [GCP SDK Setup](https://cloud.google.com/sdk/) and authenticated with a project (Optional)
* Python Environment:
  * Anaconda is highly recommended. For more information on setup, checkout my post on [Repeatable Data Science - Anaconda Environments](https://devopstar.com/2019/07/29/repeatable-data-science-anaconda-environments/)
  * Alternatively Pip with Python3.5 is advisable
* **CUDA GPU is required** for this tutorial.
  * tensorflow-gpu will be installed as part of dependencies.
  * Inference *should* work on CPU however training will not.
* [Docker Community](https://docs.docker.com/install/) is also recommended a container deployment sounds awesome to you.

### Requirement Install

The following steps cover each of the different variations of development environments you might be working with.

#### Local Environment [Requirements]

If you are running locally open up a shell and run one of the following sets of commands.

**NOTE**: *Depending on if you decided to use Anaconda or not will define what commands to use*

```bash
# Anaconda
conda env create -f environment.yml
conda activate UGATIT

# Pip / Python3.5
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

---

## Dataset Collection & Preparation

---

Collecting and preparing datasets for use is the most difficult part of this project. Let's take a look at what was used for the training of selfie2anime created with UGATIT:

* **selfie2anime**
  * selfie - photos of females as training data and test data. The size of the training dataset is 3400, and that of the test dataset is 100, with the image size of 256 x 256.
  * anime - selecting only female character images and removing monochrome images manually, collected two datasets of female anime face images, with the sizes of 3400 and 100 for training and test data respectively
    * made use of [nagadomi/lbpcascade_animeface](https://github.com/nagadomi/lbpcascade_animeface) to extract the faces
* **horse2zebra**
  * training - 1,067 (horse), 1,334 (zebra)
  * test - 120 (horse), 140 (zebra)
* **photo2portrait**
  * training - 6,452 (photo), and 1,811 (vangogh)
  * test - 751 (photo), and 400 (vangogh)

This gives us a lot of information about roughly how much data we should compile to get reasonably successful results.

### Dataset Folder Structure

The datasets you decide to use should be put into the `dataset` folder of the project and follow the structure seen below

```bash
├── dataset
   └── DATASET_NAME
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

**You need to ensure that images are cropped down** to an appropriate size before using them. To do this programmatically, edit `resize.py` and ensure the DATASET_NAME matches your one

```python
paths = [
    "dataset/DATASET_NAME/testA/"
    "dataset/DATASET_NAME/testB/"
    "dataset/DATASET_NAME/trainA/"
    "dataset/DATASET_NAME/trainB/"
]
```

Once you have images in the four folders above you can run the following python file to resize all the images down to 256*256

```python
python resize.py
```

### Selfie2Anime Example

Let's walk through an example of how the datsets for selfie2anime was compiled. We needed two datasets:

**NOTE**: *I can't directly provide these datasets to use for Licensing reasons, however you are able to download them yourself from the links*.

* Selfie Dataset - [https://www.crcv.ucf.edu/data/Selfie](https://www.crcv.ucf.edu/data/Selfie)
* Anime Dataset - [https://www.gwern.net/Danbooru2018](https://www.gwern.net/Danbooru2018)

These datasets are much bigger then was necessary so a portion of each were taken for each. 

**NOTE**: An important thing to keep in mind is that only female anime characters were used. This means a lot of hand picked items had to be singled out. When deciding on what to use in your dataset ensure there's some level of consistency.

![Selfie2Anime Dataset Count](img/selfie2anime-dataset-count.png)

---

## Model Training

---

We should now be in a good position to begin training out model. **This process is very time consuming** but rewarding.

## Model Inference
