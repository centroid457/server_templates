# RELEASE HISTORY

********************************************************************************
## TODO
1. add full logger for requests (with time+body) save in file  

********************************************************************************
## FIXME
1. ...  

********************************************************************************
## NEWS

0.2.17 (2024/04/25 17:03:25)
------------------------------
- [Client] try add logger-aux  

0.2.16 (2024/04/25 10:50:25)
------------------------------
- [Client] big ref  

0.2.15 (2024/04/24 18:07:18)
------------------------------
- [TestClient]:  
	- separate Test__RequestItem/Stack  
	- some fix  

0.2.14 (2024/04/24 15:40:54)
------------------------------
- [test server_aiohttp] add skip ReqCheckStr_Os.bool_if__LINUX()  

0.2.13 (2024/04/24 15:19:36)
------------------------------
- [URL] separate url + tests  

0.2.12 (2024/04/24 14:35:11)
------------------------------
- [FastApi] add time.sleep into server.start  

0.2.11 (2024/04/24 11:24:04)
------------------------------
- [FastApi] zero fix  

0.2.9 (2024/04/22 12:45:02)
------------------------------
- [FastApi] add param data into init ServerFastApi_Thread  

0.2.8 (2024/04/22 12:33:02)
------------------------------
- [FastApi] try move all to one class ServerFastApi_Thread  

0.2.7 (2024/04/22 11:38:53)
------------------------------
- [FastApi] add first variant server  

0.2.6 (2024/03/29 14:37:45)
------------------------------
- [AIOHTTP] add Exx__LinuxPermition/Exx__AiohttpServerOtherError  

0.2.5 (2024/03/29 12:04:18)
------------------------------
- [FASTAPI] try add - not worked  

0.2.4 (2024/03/29 10:21:22)
------------------------------
- [LINUX]:  
	- [LAN]zero add explicit localhost for server! - DELETE BACK+COMMENT!  

0.2.3 (2024/03/29 09:56:33)
------------------------------
- [LINUX]:  
	- zero add explicit localhost for server!  
	- [thread] try move App into main thread  

0.2.2 (2024/03/05 18:10:37)
------------------------------
- zero renames Client_RequestItem/Client_RequestsStack  

0.2.1 (2024/02/15 18:06:28)
------------------------------
- zero fix prints  

0.1.15 (2024/02/14 17:39:04)
------------------------------
- add http_client.py (move from testplans)  

0.1.14 (2024/02/13 16:21:30)
------------------------------
- add _response_get_json__converted_to_html  

0.1.13 (2024/02/13 14:51:56)
------------------------------
- zero clear not used attrs  

0.1.12 (2024/02/13 11:30:23)
------------------------------
- add response_post_converted_to_get  

0.1.11 (2024/02/08 13:14:27)
------------------------------
- add logger (print) for client POSTs!=fix exx if ROUTE not exists  

0.1.10 (2024/02/08 12:58:17)
------------------------------
- add logger (print) for client POSTs!=add status  

0.1.9 (2024/02/08 12:41:14)
------------------------------
- add logger (print) for client POSTs!  

0.1.8 (2024/02/07 19:16:24)
------------------------------
- fix url slashes strip=last  

0.1.7 (2024/02/07 17:57:43)
------------------------------
- fix url slashes strip  

0.1.6 (2024/02/07 17:39:19)
------------------------------
- add post_json  

0.1.5 (2024/02/06 16:55:51)
------------------------------
- remove ServerAiohttp_Example to testplans - keep only bare server!  

0.1.4 (2024/02/06 10:50:50)
------------------------------
- fix html_block__api_index  

0.1.3 (2024/02/06 10:37:55)
------------------------------
- switch to QTread  
- separate ServerAiohttp_Example from BASE  

0.1.2 (2024/02/05 18:37:00)
------------------------------
- add request as parameter into html_create to show ip/host in html  

0.1.1 (2024/02/05 17:45:18)
------------------------------
- log remote IP  
- log request statuscode  

0.1.0 (2024/02/05 16:12:22)
------------------------------
- add decorator__log_request_response  

0.0.12 (2024/02/05 15:09:59)
------------------------------
- clean links for all except GET requests in index  
- use json responses for POST  

0.0.11 (2024/02/05 13:22:40)
------------------------------
- add port number setting  

0.0.10 (2024/02/05 11:28:41)
------------------------------
- separate get/post and use _route_groups as dict  

0.0.9 (2024/02/02 17:50:14)
------------------------------
- separate html_create method for full pages  

0.0.8 (2024/02/02 15:43:36)
------------------------------
- use automated setup_routes by listing names response__*  
- add response__info_json/+html  

0.0.7 (2024/01/30 13:12:48)
------------------------------
- fix start with no config file=second  

0.0.6 (2024/01/30 13:01:50)
------------------------------
- fix start with no config file  

0.0.5 (2024/01/30 12:31:41)
------------------------------
- apply as thread  

0.0.4 (2024/01/29 18:55:34)
------------------------------
- finish fix keep all pkgs_internal in setup/build pypi  

0.0.3 (2024/01/29 18:38:57)
------------------------------
- try fix import internal packages (before it is not keep it)=in setup  

0.0.2 (2024/01/29 18:22:02)
------------------------------
- try fix import internal packages (before it is not keep it)  

0.0.1 (2024/01/26 17:19:01)
------------------------------
- try simple aiohttp

********************************************************************************
