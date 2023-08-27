FROM python:3.10-slim

ENV DASH_DEBUG_MODE True

WORKDIR /app

ENV OTP_SERVICE=otp
ENV OTP_PORT=8080
ENV VALHALLA_TILES=/valhalla/custom_files/valhalla_tiles.tar
ENV USE_ACTOR=URL
ENV VALHALLA_SERVICE=valhalla
ENV VALHALLA_PORT=8002
ENV ALTI_SERVICE=alti
ENV ALTI_PORT=8000
ENV ASSETS=/app/assets

# Install & use pipenv
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt && pip install gunicorn

COPY . ./

EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:80", "index:server"]