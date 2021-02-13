If you want generate a new ssl key and cert, which you should, you need to use something like openssl

On linux run command
openssl req -newkey rsa:2048 -nodes -keyout ssl.key -x509 -days 365 -out ssl.crt

On windows and mac, I do not know, so you may need to find this out your self.
