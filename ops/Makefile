COMPOSE_MAIN = docker-compose
COMPOSE_CERTBOT = certbot-docker-compose

all: enc_main dec_main stop start
deploy: dec_main sto start

start:
	docker compose -f ${COMPOSE_MAIN}.dec.yml up -d --build
stop:
	docker compose -f ${COMPOSE_MAIN}.dec.yml down
cert: dec_certbot
	docker compose -f ${COMPOSE_CERTBOT}.dec.yml up

enc: enc_main enc_certbot

enc_main:
	sops -e ${COMPOSE_MAIN}.dec.yml > ${COMPOSE_MAIN}.enc.yml
enc_certbot:
	sops -e ${COMPOSE_CERTBOT}.dec.yml > ${COMPOSE_CERTBOT}.enc.yml

dec: dec_main dec_certbot

dec_main:
	sops -d ${COMPOSE_MAIN}.enc.yml > ${COMPOSE_MAIN}.dec.yml
dec_certbot:
	sops -d ${COMPOSE_CERTBOT}.enc.yml > ${COMPOSE_CERTBOT}.dec.yml
