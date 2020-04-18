from alpine:latest

RUN apk add --no-cache python3-dev \
                    gcc \
                    libc-dev \
                    linux-headers \
                    mariadb-dev \
                    python3-dev \
	&& pip3 install --upgrade pip

WORKDIR /main

COPY . /main

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["main.py"]
