FROM python:3

EXPOSE 9999

WORKDIR /usr/hackithon2024

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./fast_api/ ./

CMD [ "python", "end_points.py" ]
