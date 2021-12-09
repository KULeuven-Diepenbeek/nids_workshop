# Workshop - Network Intrusion Detection System

This GitHub repository is used in the [ESnS](https://iiw.kuleuven.be/onderzoek/ess) workshop: **Network Intrusion Detection System (NIDS)**. In this workshop the participants are guided through an introduction to NIDS using Python. 

## How to join ?

Inspired by an online [blog-post](https://towardsdatascience.com/tools-for-sharing-jupyter-notebooks-online-28c8d4ff821c), these notebooks will by shared through [Binder](https://mybinder.org/). Binder allows to generate an executable environment that can be used by everyone.

If you prefer running the exercises on your own system, we provide two alternatives:
* If you have docker installed, and are able to [run it without root](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user), you can simply start you own docker container by executing *run_docker.sh*:
```$ ./run_docker.sh```
* If you prefer to run everything natively, we have provided an *environment.yml* file that contains all necessary Python packages. You can choose to use it directly with *conda*, or to manually check that all the packages are installed.

## Feedback

As with all workshops, learning <s>can</s> should happen bidirectionally. If you have any feedback for us (interesting improvements, possible typos, ...) you can find our coordinates on our [contact page](https://iiw.kuleuven.be/onderzoek/ess/contactform).

## Installation notes

Install instructions pip (linux):

* sudo pip install jupyterlab
* sudo pip install numpy matplotlib sklearn
* sudo pip install torch==1.10.0+cpu torchvision==0.11.1+cpu torchaudio==0.10.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

## Todo

* <s>add UDP frames to the dataset</s>
* <s>add ARP frames to the dataset, or any other EtherType</s>
* <s>create a private repo with solutions</s>
* verify that all links to "next notebook" are correct
* verify that all **expected solution values** are correct (wrt the used dataset)
* rename this repo so it sits closer to the solution-repo name
