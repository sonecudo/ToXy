#!/usr/bin/env python3

# baseado em:
#	github.com/yousefissa/Proxy-Tester

import requests, re, os, sys, base64
from colorama import Fore,Back, Style
from time import time

sites = ["http://wikipedia.org"];
ua = { "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; rv:72.0) Gecko/20100101 Firefox/72.0" };

def banner():
	print("""
	88P°888°Y88                              
	P°  888  °Y  e88 88e   Y8b Y8Y Y8b Y888P 
	    888     d888 888b   Y8b Y   Y8b Y8P  
	    888     Y888 888P  e Y8b     Y8b Y   
	    888      °88 88°  d8b Y8b     888   """+Fore.GREEN+"""by soneca"""+Style.RESET_ALL+"""
	                                  888   """+Fore.YELLOW+"""pzqcmpphmomfvih2.onion"""+Style.RESET_ALL+"""
	                                  888   
		""");
def mensagem_de_uso():
	print(
		"Uso: "+sys.argv[0]+" <modo>\n"
		"modos:\n"
		"\t-i: interativo (\"só quero um ou alguns proxies\")\n"
		"\t-a: automatico (longo)\n"
		, file=sys.stderr);
	exit(0);
def mil_seconds():
	return int(round(time() * 1000))
def salva(proxy):
	arq=open("proxies.txt", "a+");
	arq.write(proxy+"\n");
	arq.close();
def testa_proxies(proxies):
	print();

	good_proxies, bad_proxies = [], []
	print("["+Fore.GREEN+"INFO"+Style.RESET_ALL+"] Testando contra: {}".format(sites))		

	for proxy in proxies:
		# se já tenho nem testo!
		if( os.path.exists("proxies.txt") ):
			arq=open("proxies.txt", "r+");
			registro=arq.read();
			arq.close();
			if(proxy in registro):
				print("["+Fore.YELLOW+"AVISO"+Style.RESET_ALL+"] Pulando por repetição: "+str(proxy));
				continue;
		try:
			proxy_parts = proxy.split(':')
			ip, port, user, passw = proxy_parts[0], proxy_parts[
				1], proxy_parts[2], proxy_parts[3]
			proxies = {
				'http': 'http://{}:{}@{}:{}'.format(user, passw, ip, port),
				'https': 'https://{}:{}@{}:{}'.format(user, passw, ip, port)
			}
		except IndexError:
			proxies = {'http': 'http://' + proxy, 'https': 'https://' + proxy}

		for url in sites:
			start_time = mil_seconds()
			try:
				response = requests.get(url, proxies=proxies, headers=ua, timeout=2);
				if response.status_code != 200:
					print("["+Fore.YELLOW+"INFO"+Style.RESET_ALL+"] {} não é um proxy bom.".format(proxy))
					bad_proxies.append(proxy)
				else:
					print(
						"["+Fore.GREEN+"INFO"+Style.RESET_ALL+"] Proxy "+Fore.GREEN+"bom"+Style.RESET_ALL+': {} no site {} ---- {} ms'.format(proxy, url, mil_seconds() - start_time))
					#good_proxies.append(proxy);
					salva(proxy);
			except:
				print("["+Fore.YELLOW+"INFO"+Style.RESET_ALL+"] Proxy "+Fore.RED+'ruim'+Style.RESET_ALL+': {} no site {}'.format(proxy, url))
	return good_proxies;
def menu():
	print("["+Fore.GREEN+"INFO"+Style.RESET_ALL+"] (M)ais proxies ou (S)air ");
	op = input("["+Fore.GREEN+"INFO"+Style.RESET_ALL+"] Escolha: ");
	if op in "mM":
		print();
	else:
		print("["+Fore.GREEN+"INFO"+Style.RESET_ALL+"] Adeus...");
		exit(0);
def processa(source):
	saida=[];

	#tipo 12.123.1.123:54321
	if( re.findall(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{1,5}", source) ):
		match = re.findall(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{1,5}", source);
		for cada in match:
			if cada not in saida:
				saida.append(cada);

	#tipo Proxy('MTIuMTIzLjEuMTIzOjU0MzIxCg==') |> http://proxy-list.org/english/index.php?p=2
	if( re.findall(r"Proxy\(\'(.*)\'\)", source) ):
		print("["+Fore.GREEN+"INFO"+Style.RESET_ALL+"] Obfucado com base64.");
		match = re.findall(r"Proxy\(\'(.*)\'\)", source);
		for cada in match:
			proxy = base64.b64decode(cada).decode();
			if proxy not in saida:
				saida.append(proxy);

	print("["+Fore.GREEN+"INFO"+Style.RESET_ALL+"] "+str(len(saida))+" proxies diferentes" );
	return saida;

urls=[]
# Escolha os sites que deseja escanear
urls+=[
		"http://aliveproxy.com/fastest-proxies/",
		"http://aliveproxy.com/anonymous-proxy-list",
		"http://aliveproxy.com/fr-proxy-list",
		"http://aliveproxy.com/proxy-list-port-3128",
		"http://aliveproxy.com/proxy-list-port-80",
		"http://aliveproxy.com/proxy-list-port-8080",
		"http://aliveproxy.com/ru-proxy-list",
		"http://atomintersoft.com/products/alive-proxy/proxy-list",
		"http://atomintersoft.com/products/alive-proxy/proxy-list?ap=9",
		"http://atomintersoft.com/products/alive-proxy/proxy-list/3128",
		"http://atomintersoft.com/proxy_list_domain_com",
		"http://atomintersoft.com/proxy_list_port_3128",
		"http://atomintersoft.com/proxy_list_port_80",

		#obfusca com base64
		"http://best-proxy.com/english/search.php?search=anonymous-and-elite&country=any&type=anonymous-and-elite&port=any&ssl=any",
		"http://best-proxy.com/english/search.php?search=anonymous-and-elite&country=any&type=anonymous-and-elite&port=any&ssl=any&p=2",
		"http://best-proxy.com/english/search.php?search=anonymous-and-elite&country=any&type=anonymous-and-elite&port=any&ssl=any&p=3",


		#"http://rootjazz.com/proxies/proxies.txt", #403
		#"http://www.my-proxy.com/free-proxy-list.html", #70
		#"http://www.proxyblind.org/anonymous-proxy.shtml", #49
		#"http://www.proxyblind.org/free-proxy.shtml",
		#"http://www.proxyblind.org/proxy-list.shtml",
		#"http://www.proxyblind.org/ssl.shtml",
		#"spys.me/proxy.txt" #300
		#"https://github.com/clarketm/proxy-list/blob/master/proxy-list.txt", #300

		#esconde porta com js + recaptcha
		#"http://free-proxy-list.net/",
		#"http://free-proxy-list.net/anonymous-proxy.html",
		#"http://free-proxy-list.net/uk-proxy.html",

		# js
		#"http://multiproxy.org/anon_proxy.htm",

		#ip separado da porta ip :porta
		#"http://www.ip-adress.com/proxy_list/?k=time&d=desc",
	];
#obfusca com base64
urls.append("http://proxy-list.org/english/index.php" );
for num in range(2, 11):
	urls.append("http://proxy-list.org/english/index.php?p=" + str(num));
# ip longe da porta
for c in range(1, 30):
	if(c<=9):
		urls.append("http://nntime.com/proxy-list-0"+str(c)+".htm")
	else:
		urls.append("http://nntime.com/proxy-list-"+str(c)+".htm")


if __name__ == '__main__':

	banner();
	if(len(sys.argv)!=2):
		mensagem_de_uso();

	# gerencia argumentos
	if(sys.argv[1]=="-i"):
		print("["+Fore.GREEN+"INFO"+Style.RESET_ALL+"] Modo interativo");
		interativo = True;
	elif(sys.argv[1]=="-a"):
		print("["+Fore.GREEN+"INFO"+Style.RESET_ALL+"] Modo Automático "+Fore.YELLOW+"(recomendado rodar em background)"+Style.RESET_ALL);
		interativo = False;
	else:
		print("["+Fore.RED+"ERRO"+Style.RESET_ALL+"] Modo Desconhecido");
		mensagem_de_uso();
		exit(0);

	# informação
	print(
			"["+Fore.GREEN+"INFO"+Style.RESET_ALL+"] Proxies operantes serão salvos em "+
			Fore.YELLOW+"proxies.txt"+Style.RESET_ALL
		);
	print("["+Fore.GREEN+"INFO"+Style.RESET_ALL+"] Monitore em tempo-real com: tail -f proxies.txt\n");

	# confere existência do arquivo proxies.txt
	if( os.path.exists("proxies.txt") ):
		print( "["+Fore.YELLOW+"AVISO"+Style.RESET_ALL+"] Arquivo "+Fore.YELLOW+"proxies.txt"+Style.RESET_ALL+" já existe!", file=sys.stderr);
		exit(0);

	for x in range(len(urls)):
		proxies = []
		try:
			response = requests.get(urls[x], headers=ua, timeout=10);
		except:
			print("["+Fore.RED+"ERRO"+Style.RESET_ALL+"] Ocorreu um erro em "+urls[x] );
			continue

		# resposta vazia
		html = response.text;
		if not html:
			print("["+Fore.YELLOW+"AVISO"+Style.RESET_ALL+"] Resposta vazia de "+urls[x] );
			continue;

		print("["+Fore.GREEN+"INFO"+Style.RESET_ALL+"] Pegando de "+urls[x]);
		
		proxies+=processa(html);
		if(len(proxies)>=1):
			testa_proxies(proxies); #retorna só proxies operantes
		if(interativo):
			menu();