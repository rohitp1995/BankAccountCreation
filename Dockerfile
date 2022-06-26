FROM  python:3.7
COPY . /usr/app/
EXPOSE 8501
WORKDIR /usr/app/
RUN pip install -r requirements.txt
RUN pip3 install torch==1.9.0+cpu torchvision==0.10.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install 'git+https://github.com/facebookresearch/detectron2.git'
RUN apt-get update
RUN apt install -y libgl1-mesa-glx
RUN apt-get install -y tesseract-ocr
CMD streamlit run app.py 