from uuid import uuid4
from os.path import abspath, join
from os import getcwd, mkdir
import io
import shutil

from fastapi import FastAPI, File, Form, UploadFile, Body, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
import uvicorn
from speech import make_text2speech, make_vocoder, generate_file, save_file

# args
device = "cpu"
port = 3000

# paths
working_dir = getcwd()
output_path = abspath("output")

# models
model_names = [
    "kaztts_female1_tacotron2_train.loss.ave",
    "kaztts_female2_tacotron2_train.loss.ave",
    "kaztts_female3_tacotron2_train.loss.ave",
    "kaztts_male1_tacotron2_train.loss.ave",
    "kaztts_male2_tacotron2_train.loss.ave"
]

vocoder_names = [
    "parallelwavegan_female1_checkpoint",
    "parallelwavegan_female2_checkpoint",
    "parallelwavegan_female3_checkpoint",
    "parallelwavegan_male1_checkpoint",
    "parallelwavegan_male2_checkpoint",
]

models = list(map(lambda model_name: make_text2speech(working_dir, abspath(join("models", model_name)), device), model_names))
vocoders = list(map(lambda vocoder_name: make_vocoder(working_dir, abspath(join("vocoders", vocoder_name)), device), vocoder_names))

# fasstapi
app = FastAPI()

api_keys = [
    "HMIkzWppQHfbQrU76sRIkKsX"
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )

@app.get('/api/text', dependencies=[Depends(api_key_auth)])
def index(model = "0", text = "тест"):
    wav = generate_file(models[int(model)], vocoders[int(model)], text)

    file_name = str(uuid4()) + ".wav"
    file_path = join(output_path, file_name)

    save_file(file_path, wav)

    return FileResponse(file_path)

@app.post('/api/vocabulary', dependencies=[Depends(api_key_auth)])
async def vocabulary(vocabulary_file: UploadFile, model: str = Form()):
    contents = await vocabulary_file.read()
    string = contents.decode("UTF-8")

    vocabulary_dir_name = str(uuid4())
    vocabulary_dir_path = join(output_path, vocabulary_dir_name)
    mkdir(vocabulary_dir_path)

    for line in string.splitlines():
        file_name = line + ".wav"
        file_path = join(vocabulary_dir_path, file_name)

        wav = generate_file(models[int(model)], vocoders[int(model)], "@" + line + "@")

        save_file(file_path, wav)

    shutil.make_archive(vocabulary_dir_path, 'zip', vocabulary_dir_path)

    return FileResponse(vocabulary_dir_path + ".zip")


app.mount("/", StaticFiles(directory="site", html = True), name="site")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
