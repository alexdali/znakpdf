from io import BytesIO

import fitz
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import PlainTextResponse
from pylibdmtx.pylibdmtx import decode

app = FastAPI()

zoom = 2
w = 148
h = 148
xys = [(444, 72, 444 + w, 72 + h),
       (1060, 72, 1060 + w, 72 + h),
       (444, 416, 444 + w, 416 + h),
       (1060, 416, 1060 + w, 416 + h),
       (444, 760, 444 + w, 760 + h),
       (1060, 760, 1060 + w, 760 + h)]


async def parse_pdf(file):
    codes = []

    try:
        file_bytes = await file.read()
        mat = fitz.Matrix(zoom, zoom)
        doc = fitz.open("pdf", file_bytes)

        for i, page in enumerate(doc.pages()):
            pix = page.getPixmap(matrix=mat, alpha=True)
            bytes_image = pix.getImageData("png")
            image = Image.open(BytesIO(bytes_image))

            for xy in xys:
                try:
                    cropped = image.crop(xy)
                    t = decode(cropped.convert('L'))[0].data.decode('utf-8')
                    codes.append(t)
                except IndexError:
                    pass
        doc.close()
    except Exception as e:
        print(e)
        return "Error"

    return {"codes": codes,
            "n": len(codes)}


@app.post("/decodefile/")
async def create_upload_file(file: UploadFile = File(...)):
    codes = await parse_pdf(file)
    return codes


@app.post("/decodefiletotext/", response_class=PlainTextResponse)
async def create_upload_file(file: UploadFile = File(...)):
    codes = await parse_pdf(file)
    return '\n'.join(codes['codes']) + '\n' + str(codes['n'])
