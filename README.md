# Image Encoder / Decoder

## Description
This uses invisible-watermark to apply an invisible watermark to images.
See https://github.com/shieldmnt/invisible-watermark

## Installation
1. Clone the repo
2. Navigate to ./src
3. Run the command `pipenv install -r requirements.txt`
    - If you don't have pipenv, install it using `pip install --user pipenv`
4. Activate the environment using `pipenv shell`

## Running
To encode, run `encode.py input-folder output-folder message`
To decode, run `decode.py input-file`
QUOTATION MARKS ARE NOT NECESSARY
If you're getting an error relating to blind_watermark, make sure to run `pipenv shell`

## Misc.
https://github.com/guofei9987/blind_watermark - looks more accurate and can embed any number of characters, but the length of the embedded string is not consistent and is needed to decode.