FROM python:3.10-slim

ENV DASH_DEBUG_MODE True

WORKDIR /alti

ENV BD_ALTI_PATH_DALLES=/alti/assets/BDALTIV2/1_DONNEES_LIVRAISON_2021-10-00008/BDALTIV2_MNT_25M_ASC_LAMB93_IGN69_D038
ENV BD_ALTI_PATH_SPECS=/alti/assets/BDALTIV2/3_SUPPLEMENTS_LIVRAISON_2021-10-00008/BDALTIV2_MNT_25M_ASC_LAMB93_IGN69_D038

# Install & use pipenv
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY . ./

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]