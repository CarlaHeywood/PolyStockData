FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /var/www/PolyStockData.py

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000
EXPOSE 8000

CMD [ "python3", "polygon/manage.py", "runserver", "0.0.0.0:8000"]