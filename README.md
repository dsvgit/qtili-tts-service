## Install

```bash
git clone https://github.com/dsvgit/qtili-tts-service.git
cd qtili-tts-service
source ./bootstrap.sh # it will reboot machine at the end

# after reboot
cd qtili-tts-service
source ./setup_venv.sh # could show some errors (error: invalid command 'bdist_wheel') 

# download models
cd models
wget -i download-models.txt
for i in *.zip; do unzip "$i" -d "${i%%.zip}"; done
cd ..

# download vocoders
cd vocoders
wget -i download-vocoders.txt
for i in *.zip; do unzip "$i" -d "${i%%.zip}"; done
cd ..

python3 service.py

```

## Python

python3 -m pip install -r requirements.txt

## Links

- pip installing deps: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
- espnet2_tutorial_2021_CMU_11751_18781: https://colab.research.google.com/github/espnet/notebook/blob/master/espnet2_tutorial_2021_CMU_11751_18781.ipynb#scrollTo=41alrKGO4d3v
- espnet2_tutorial_2021_CMU_11751_18781: https://github.com/espnet/notebook/blob/master/espnet2_tutorial_2021_CMU_11751_18781.ipynb
- espnet getting started: https://www.assemblyai.com/blog/getting-started-with-espnet/
- installing deps: https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-20-04-server
- installing deps "bdist_wheel": https://bobbyhadz.com/blog/python-error-invalid-command-bdist-wheel
- espnet docs: https://espnet.github.io/espnet/installation.html
- Running espnet as a service: https://www.youtube.com/watch?v=ooEIfR3aw44
- My TTS Service: https://github.com/espnet/espnet/blob/2e8a588a6910e8cd2ee095ca05ebc374125399e6/MyTTsService.py

## Curl
```
curl localhost:3000 --output test.wav
curl -F "vocabulary_file=@vocabulary.csv" localhost:3000/vocabulary
curl -F "vocabulary_file=@vocabulary.csv" localhost:3000/vocabulary --output audio.zip
unzip audio.zip -d audio
```

## Required libs

`libsndfile1-dev`
