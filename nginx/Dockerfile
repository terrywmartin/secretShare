FROM nginx:1.21-alpine

# install certbot
#RUN add-apt-repository ppa:certbot/certbot
#RUN apt-get update -y
#RUN apt-get install -y certbot python-certbot-nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d