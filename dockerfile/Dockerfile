FROM jupyter/base-notebook

WORKDIR app

RUN pip install numpy
RUN pip install matplotlib
RUN pip install sklearn
RUN pip install torch==1.10.0+cpu torchvision==0.11.1+cpu torchaudio==0.10.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

#RUN pip install cpuonly
#RUN pip install torch

#RUN mkdir -p app
#WORKDIR app
#RUN pwd
#RUN jupyter notebook

