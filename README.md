# learnseeker-ocr
An Optical Character Recognition for extracting both Handwriting and Text from Paper Records

## Python Version
3.8.5

## Set Up
1. Install Python 3.8.5
2. Install pip
3. Clone this repository
4. Change directory to this repository
5. Run `pip install -r ./requirements.txt`
6. Run either of the following
- `jupyter notebook` for viewing `./learning` progress
- `export FLASK_APP=main.py; export FLASK_ENV=development; export CAPTURE_PHRASE=False; flask run` for starting up flask. (Refer to [Environment Variable](#Environment_Variables))
- `./development_start` for quick starting a development application

## Libraries
- Flask
- Pytest
- Jupyter Notebook
- PDF2Image
- Pillow
- TensorFlow
- tqdm 
- SymspellPy
- Coverage
- Numpy
- OpenCV2
- PyTesseract
- Calamari
- Kraken

## Environment Variables
1. `FLASK_APP` (`main.py`)
Identifies app entrypoint
2. `FLASK_ENV` (`development` | `production`)
Set the running environment
3. `CAPTURE_PHRASE` (`True` | `False`)
Set whether should the `text_recognise` endpoint save images `./assets/phrases`

