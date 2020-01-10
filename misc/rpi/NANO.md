# Jetson Nano Setup

*This guide was using a fresh `nv-jetson-nano-sd-card-image-r32.3.1.zip`*

## Tensorflow

The following is based on the [installing TensorFlow for Jetson Platform](https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html#prereqs) guide.

```bash
# install prerequisites
sudo apt-get update
sudo apt-get install python3-dev
sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev
sudo apt-get install virtualenv

# Create new virtualenv
python3 -m virtualenv -p python3 tensorflow-1.15.0
source tensorflow-1.15.0/bin/activate
pip3 install -U pip testresources setuptools

# install the following python packages
pip3 install -U numpy==1.16.1 future==0.17.1 mock==3.0.5 h5py==2.9.0 \
    keras_preprocessing==1.0.5 keras_applications==1.0.8 gast==0.2.2 \
    enum34 futures protobuf

# install the latest version of TensorFlow
export JP_VERSION=43
export TF_VERSION=1.15.0
export NV_VERSION=19.12
pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v$JP_VERSION tensorflow-gpu==$TF_VERSION+nv$NV_VERSION
```
