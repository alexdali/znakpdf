from io import BytesIO
from os import remove
from random import randint
from shutil import copyfileobj

import fitz
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from pylibdmtx.pylibdmtx import decode


app = FastAPI()


@app.post("/decodefile/")
async def create_upload_file(file: UploadFile = File(...)):
    zoom = 2
    w = 148
    h = 148
    temp_file = f'/tmp/temp{randint(0, 100)}.pdf'
    xys = [(444, 72, 592, 220),
           (1060, 72, 1060 + w, 72 + h),
           (444, 416, 592, 416 + h),
           (1060, 416, 1060 + w, 416 + h),
           (444, 760, 592, 760 + h),
           (1060, 760, 1060 + w, 760 + h)]
    codes = []

    try:
        with open(temp_file, "wb") as buffer:
            copyfileobj(file.file, buffer)
            mat = fitz.Matrix(zoom, zoom)
            doc = fitz.open(temp_file)

            for i, page in enumerate(doc.pages()):
                codes.append([])
                pix = page.getPixmap(matrix=mat, alpha=True)
                bytes_image = pix.getImageData("png")
                image = Image.open(BytesIO(bytes_image))

                for xy in xys:
                    try:
                        cropped = image.crop(xy)
                        codes[i].append(decode(cropped.convert('L'))[0].data.decode('utf-8')[0:31])
                    except IndexError:
                        pass

        remove(temp_file)
    except:
        return {"Error"}

    return {"codes": codes,
            "n:": len(codes)}
