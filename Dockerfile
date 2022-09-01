FROM python:3.8-slim-buster

WORKDIR /code

COPY requirements.txt requirements.txt

COPY . .

RUN python -m pip install --upgrade pip

RUN pip3 install --upgrade heyoo

RUN pip3 install -r requirements.txt

CMD [ "python", "hook.py" ]

#Call to using test functions
# CMD [ "python", "examples/sending_template_message.py" ]
