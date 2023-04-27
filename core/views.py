from django.shortcuts import render, redirect
import cv2
from django.contrib import messages
import shutil
import os
import random
from PIL import Image

def handle_uploaded_file(f):
    dirName = f.name.split('.')[0]
    dirId = ''
    for i in range(0,5):
        dirId += str(random.randint(0,8))
    dirFinalName = dirName + dirId
    os.mkdir(f"media/uploads/{dirFinalName}/")
    with open(f"media/uploads/{dirFinalName}/{f}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return dirFinalName

def zip_files(dname):
    shutil.make_archive(f"media/zip/{dname}", "zip", f"media/processed/{dname}")
    return f"media/zip/{dname}.zip"

def image_process(filename, dirname, operation):
    image = cv2.imread(f"media/uploads/{dirname}/{filename}")
    if operation == 'cjpg':
        fnamewithext = f"{str(filename).split('.')[0]}.jpg"
        os.mkdir(f"media/processed/{dirname}")
        newFilename = f"media/processed/{dirname}/{fnamewithext}"
        print(newFilename)
        cv2.imwrite(newFilename, image)
        zip_url = zip_files(dirname)
        return zip_url
    if operation == 'cpng':
        fnamewithext = f"{str(filename).split('.')[0]}.png"
        os.mkdir(f"media/processed/{dirname}")
        newFilename = f"media/processed/{dirname}/{fnamewithext}"
        print(newFilename)
        cv2.imwrite(newFilename, image)
        zip_url = zip_files(dirname)
        return zip_url
    
    if operation == 'cwebp':
        fnamewithext = f"{str(filename).split('.')[0]}.webp"
        os.mkdir(f"media/processed/{dirname}")
        newFilename = f"media/processed/{dirname}/{fnamewithext}"
        print(newFilename)
        cv2.imwrite(newFilename, image)
        zip_url = zip_files(dirname)
        return zip_url
    
    if operation == 'cpdf':
        img = Image.open(f"media/uploads/{dirname}/{filename}")
        cnvrt_to_pdf = img.convert('RGB')
        os.mkdir(f"media/processed/{dirname}")
        cnvrt_to_pdf.save(f"media/processed/{dirname}/{filename.name.split('.')[0]}.pdf")
        zip_url = zip_files(dirname)        
        return zip_url
    
    if operation == 'cgray':
        os.mkdir(f"media/processed/{dirname}")
        newFilename = f"media/processed/{dirname}/{filename}"
        grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(newFilename, grayImg)
        zip_url = zip_files(dirname)
        return zip_url
    
    
def home(request):
    if request.POST:
        file = request.FILES['file']
        operation = request.POST.get('operation')
        dirname = handle_uploaded_file(file)
        image = image_process(file, dirname, operation)
        messages.success(request, f'Image Processed successfully. <a href="{image}" target="_blank">Click here</a> to download the image')
        return redirect('home')
    return render(request, 'index.html')
