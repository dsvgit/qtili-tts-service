import os

import torch
import numpy
import soundfile as sf
from espnet2.bin.tts_inference import Text2Speech
from parallel_wavegan.utils import load_model

def make_text2speech(working_dir, model_path, device):
    os.chdir(model_path)
    text2speech = Text2Speech.from_pretrained(
        train_config="exp/tts_train_raw_char/config.yaml",
        model_file="exp/tts_train_raw_char/train.loss.ave_5best.pth",
        device=device,
        speed_control_alpha=1,
#         threshold=1,
#         use_att_constraint=True,
#         forward_window=1000,
#         backward_window=2000
    )
    text2speech.spc2wav = None  # Disable griffin-lim
    os.chdir(working_dir)
    return text2speech

def make_vocoder(working_dir, vocoder_path, device):
    os.chdir(vocoder_path)
    vocoder = load_model("checkpoint-400000steps.pkl").to(device).eval()
    vocoder.remove_weight_norm()
    os.chdir(working_dir)
    return vocoder

def generate_file(text2speech, vocoder, text):
    with torch.no_grad():
        output_dict = text2speech(text.lower())
        feat_gen = output_dict['feat_gen']
        wav = vocoder.inference(feat_gen)
    return wav

def save_file(file_path, wav):
    fs = 22050
    sf.write(file_path, wav.view(-1).cpu().numpy(), fs, "PCM_16")
