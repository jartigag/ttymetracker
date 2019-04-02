#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ##########
# # ttymetracker: terminal time tracker
# ##########
#
# this module for ttymetracker copies your tasks to your 
# MS SharePoint sheet
# usage: python3 ttymetracker.py logbooksDir --modules sharepoint 

__author__ = "@jartigag"
__version__ = "0.5"

import urllib.request, urllib.parse
from ttymetracker_credentials import *
import json

# this is awesome!!! => https://curl.trillworks.com

### TODO ###
#
#todo1: post task with the minimal data and headers

post_data = {
    "formValues": [
    {
      "FieldName": "Title",
      "FieldValue": "prueba desde modules/ttymetracker_sharepoint.py",
      "HasException": False,
      "ErrorMessage": None
    },
    {
      "FieldName": "Fecha",
      "FieldValue": "01/04/2019",
      "HasException": False,
      "ErrorMessage": None
    },
    {
      "FieldName": "Horas",
      "FieldValue": "1",
      "HasException": False,
      "ErrorMessage": None
    },
    {
      "FieldName": "Usuario",
      "FieldValue": "[{\"Key\":\"i:0#.f|membership|{}\",\"DisplayText\":\"%s\",\"IsResolved\":true,\"Description\":\"{}\",\"EntityType\":\"User\",\"EntityData\":{\"IsAltSecIdPresent\":\"False\",\"Title\":\"\",\"Email\":\"%s\",\"MobilePhone\":\"\",\"ObjectId\":\"14308d04-61bc-40d2-98b1-fee3accf077d\",\"Department\":\"\"},\"MultipleMatches\":[],\"ProviderName\":\"Tenant\",\"ProviderDisplayName\":\"Espacio empresarial\"}]",
      "HasException": False,
      "ErrorMessage": None
    },
    {
      "FieldName": "Proyecto",
      "FieldValue": "9;#Otros",
      "HasException": False,
      "ErrorMessage": None
    },
    {
      "FieldName": "ContentType",
      "FieldValue": "Elemento",
      "HasException": False,
      "ErrorMessage": None
    }],
    "bNewDocumentUpdate": False,
    "checkInComment": None
    }

post_data = json.dumps(str(post_data).replace("{","{{").replace("}","}}") % (sharepoint_email, sharepoint_display_name) ).encode('utf8') #format(sharepoint_email, sharepoint_display_name).encode('utf8')
print(post_data)
req = urllib.request.Request(sharepoint_url, headers=sharepoint_headers, data=post_data)
ans = urllib.request.urlopen(req)
print(ans)

'''
curl 'https://myCompany.sharepoint.com/sites/administracion2/_api/web/GetList(@a1)/AddValidateUpdateItemUsingPath()?@a1=%27%2Fsites%2Fadministracion2%2FLists%2FHoras%5FJA%27'
-H 'origin: https://myCompany.sharepoint.com'
-H 'accept-encoding: gzip, deflate, br'
-H 'accept-language: es-ES,es;q=0.9,en;q=0.8'
-H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
-H 'content-type: application/json;odata=verbose'
-H 'accept: application/json;odata=verbose'
-H 'referer: https://myCompany.sharepoint.com/sites/administracion2/Lists/Horas_JA/AllItems.aspx'
-H 'authority: myCompany.sharepoint.com'
-H 'cookie: rtFa=Cc4Dy8GkhNh5AtzI85WhdtGj0obIQ7VUbRIM/AawJrMmQUI3RDg4QjMtMjcwOS00NEYyLUFBMTctQTRFMzQ5RTBCOEI0x4AY2iVYfqY5NuCXvlLrY4QlYqpMuWwAa8XsNrBGj6yMwA9qRXFX4+jY2R+SnzY85GE1O+S6IBD4TtuirY6SMZJAGBgRfu9XexlTWvTCzGfVFBi1X+ybgjoVZU6ohVRw+zcx+8NAN96w0KxZfZBnJXQpEqW/Wg000fX3+umnXDMEELawDAgRnkAS2t7J7j9MUbJGBZ6kQiw93H04hXqv1HUtV7YOj6OA/LFliJv0bmhEzWZcX8a4x7NvoNFLvBBz/T5hXyQGVqEBJYEUZJVONQDeNZCMZWaZRHoapaVk/vRGAktrDcBv4AU9sgteKr/jOyJcLcxtnaehwD4mIOFywkUAAAA=; FedAuth=77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U1A+VjUsMGguZnxtZW1iZXJzaGlwfDEwMDMyMDAwMzc5ZTVjODhAbGl2ZS5jb20sMCMuZnxtZW1iZXJzaGlwfGphdmllci5hcnRpZ2FAbmF1ZGl0LmVzLDEzMTk2OTY5MDIzMDAwMDAwMCwxMzE5MTkzMTgxOTAwMDAwMDAsMTMxOTkxMTQ4ODEzMjIyMzI0LDAuMC4wLjAsMyxhYjdkODhiMy0yNzA5LTQ0ZjItYWExNy1hNGUzNDllMGI4YjQsLFYyITEwMDMyMDAwMzc5RTVDODghMTMxOTY5NjkwMjMsMDNhMmNlOWUtMjAwZi04MDAwLTQzNjItZmI0MTA2ZThhMmJiLDQ2MDRjZjllLWMwY2MtODAwMC05ZTEwLTE4ZmU1MjVkMjJhYywsMCwxMzE5ODY4NjQ4MTMyMjIzMjQsMTMxOTg5NDIwODEzMjIyMzI0LCxNUy9KTEtHZEpQem4xREJaV1VqK1pXMHZmZEpMNmtqVG1adkVWdG1hRU9vaEdzUFhWcVJLVTIrU1IvZjhIUnZNUzdPMGlwV1ZkUjdJS2R6VGRITFl2Vm0wZ1J6SEFZVzZoU2svYVh3b0Q0S25ZUmR3bDUrQjF3THE2c1J0aE15Smc5ZEs5Nzg5WVJvMzN2MXdvTHdpRTNtSnU1WVVTODdaZXRqMTNrdEFxWE9zVW4wU3dnS1NyOHUrclpJQTBSU2x1b2UvNmVEUWJYejJWY3VzQko3NTJGWXdzUG9GSWgxV0NKcjJGWWlBR1ZxT1ljMjRYeU55M0ZOM2VaL1V0VW9xVHQyVXJySjl3d0VFM2ZPVzBjQ0NzQTRWUVMrbFE0bUhxd1l1OU9Iais0Tlk4b3lYNDF3L2xVMHVSV04vREduOVV6eVpaSS9HK21pejVPaHNENGxJQmc9PTwvU1A+; FeatureOverrides_enableFeatures=; FeatureOverrides_disableFeatures=; WSS_FullScreenMode=false'
-H 'x-sp-requestresources: listUrl=%2Fsites%2Fadministracion2%2FLists%2FHoras%5FJA'
-H 'x-requestdigest: 0x9900593CF90DF1D73419392C46CBA0AACEFDB0A430048A56AB8F90CF18AF25512CE4DA2AC84023348EE43D5413CE1966881CD56E159F27E1A1BA76037DB22A85,02 Apr 2019 13:31:08 -0000'
--data-binary '{
    "listItemCreateInfo":
    {
        "__metadata":
        {
            "type": "SP.ListItemCreationInformationUsingPath"
        },
        "FolderPath":
        {
            "__metadata":
            {
                "type": "SP.ResourcePath"
            },
            "DecodedUrl": "/sites/administracion2/Lists/Horas_JA"
        }
    },
    "formValues": [
    {
        "FieldName": "Title",
        "FieldValue": "ZZ",
        "HasException": false,
        "ErrorMessage": null
    },
    {
        "FieldName": "Fecha",
        "FieldValue": "02/04/2019",
        "HasException": false,
        "ErrorMessage": null
    },
    {
        "FieldName": "Horas",
        "FieldValue": "1",
        "HasException": false,
        "ErrorMessage": null
    },
    {
        "FieldName": "Usuario",
        "FieldValue": "[{\"Key\":\"i:0#.f|membership|myemail@myCompany.com\",\"DisplayText\":\"Jartigag\",\"IsResolved\":true,\"Description\":\"myemail@myCompany.com\",\"EntityType\":\"User\",\"EntityData\":{\"IsAltSecIdPresent\":\"False\",\"Title\":\"\",\"Email\":\"myEmail@myCompany.com\",\"MobilePhone\":\"\",\"ObjectId\":\"14308d04-61bc-40d2-98b1-fee3accf077d\",\"Department\":\"\"},\"MultipleMatches\":[],\"ProviderName\":\"Tenant\",\"ProviderDisplayName\":\"Espacio empresarial\"}]",
        "HasException": false,
        "ErrorMessage": null
    },
    {
        "FieldName": "Proyecto",
        "FieldValue": "19;#Administración",
        "HasException": false,
        "ErrorMessage": null
    },
    {
        "FieldName": "ContentType",
        "FieldValue": "Elemento",
        "HasException": false,
        "ErrorMessage": null
    }],
    "bNewDocumentUpdate": false,
    "checkInComment": null
}'
--compressed
'''







'''
curl 'https://myCompany.sharepoint.com/sites/administracion2/_api/web/GetList(@a1)/AddValidateUpdateItemUsingPath()?@a1=%27%2Fsites%2Fadministracion2%2FLists%2FHoras%5FJA%27'
-H 'origin: https://myCompany.sharepoint.com'
-H 'accept-encoding: gzip, deflate, br'
-H 'content-type: application/json;odata=verbose'
-H 'accept: application/json;odata=verbose'
-H 'authority: myCompany.sharepoint.com'
-H 'cookie: MicrosoftApplicationsTelemetryDeviceId=b6b4bfbd-79e4-6a45-f44f-cf3b794498d0;
MicrosoftApplicationsTelemetryFirstLaunchTime=1548974821466;
rtFa=5c5aYaUAtjBm2yFpZUufKjO9xk1ODDRGLDbft0My+comQUI3RDg4QjMtMjcwOS00NEYyLUFBMTctQTRFMzQ5RTBCOEI0JCbMbwH2GCysGtMIgafAkfoCaB2gfTxLcsO1eLnrLCpKYz3+FItD+xQz6gMp6tcx37LATWvBqPcpRAa8B5NgcSehFRRAifsU+ztLHoZYsstGOvuGz6qpK1ZVM1p0EHVkN1vw7tPqP3xZUgnp5QyuZYhys9IKVFzhNZd6XR0+02AZIEtImt/3rVyYiufqe9X1NpNu0JGlTSapK5ZLKgYI7Qs7v9MmeBGx/rGoUCiXY5zzeoLOox392OCnwRm/0vS88GZmvPGLmli/r0sg14X0WyFdgN+8vBb/sKk2zel83miMJE7anSRQOqeQw4g3HGClr5o3eewAK4xUDM+7Pyy740UAAAA=;
FedAuth=77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U1A+VjUsMGguZnxtZW1iZXJzaGlwfDEwMDMyMDAwMzc5ZTVjODhAbGl2ZS5jb20sMCMuZnxtZW1iZXJzaGlwfGphdmllci5hcnRpZ2FAbmF1ZGl0LmVzLDEzMTkyNzM1NzAyMDAwMDAwMCwxMzE5MTkzMTgxOTAwMDAwMDAsMTMxOTc5NzU1NTg5MDc0ODMwLDAuMC4wLjAsMyxhYjdkODhiMy0yNzA5LTQ0ZjItYWExNy1hNGUzNDllMGI4YjQsLFYyITEwMDMyMDAwMzc5RTVDODghMTMxOTI3MzU3MDIsMWNhN2M5OWUtMzA1YS04MDAwLTllMTAtMTA5MzRkMjMyMzk3LGJiYzVjYTllLWIwZWUtODAwMC00MzYyLWZhMzkwMmY3ZjE5MywsMCwxMzE5NzI0NjYxMjU0NzI3MjMsMTMxOTc1MDIyMTI1NDcyNzIzLCxDTGdoTjNTYlJZeHJzUUEvUW9ZWUJSNWQ5anMxdjJjREVQV0dKaVlhNnpjK05jalJXT29HMUdFRk5RRi9EcmV5bXM0dThveC9nVUEwbGUyYXFxSkNUeGlEbldRSGh2eEtxTnZxY3JtNGhYa0luOURxMUx5enZVRkpObnk2OEF4djM5eWMweEFDRWhQaWthZmdwRnYzbUlzTW1MZE5UQ0ttM1BoekZpaGRLTEUxemc2T20vTndtUVI4ci95QTF3ZVBwVVRHYlA3bTVMTjg5M0ZvRTJMZTBiSFhYdFF6cUlOSlM4eXdReHNNbUdoQ1ArWlRpVmdSRmZyQTk2MzZTaHExNVhaeVN5eklJZVhsazBtbWRJSlV5TjBmV2dMeWw4d0NYNngxVVJCM01LckZoaDNtdTlUOFNrMXB4cWpYOVFKb0FXTWcxbGd2VzNxM1ViL2ZJSmhyK1E9PTwvU1A+'
-H 'x-sp-requestresources: listUrl=%2Fsites%2Fadministracion2%2FLists%2FHoras%5FJA'
-H 'x-requestdigest: 0xC3D680541EA4A9018E3B74FB7CEAFEB7608BDD6161E2CF8A560145CF180947C7331347FA09263B2BAF515CFFA43014AD637435B7B3DC4873BEE0361D7D0317DF,20 Mar 2019 11:42:29 -0000'
--data-binary '{
"listItemCreateInfo":
{
  "__metadata":
  {
    "type": "SP.ListItemCreationInformationUsingPath"
  },
  "FolderPath":
  {
    "__metadata":
    {
      "type": "SP.ResourcePath"
    },
    "DecodedUrl": "/sites/administracion2/Lists/Horas_JA"
  }
},
"formValues": [
{
  "FieldName": "Title",
  "FieldValue": "prueba desde curl quitando headers",
  "HasException": false,
  "ErrorMessage": null
},
{
  "FieldName": "Fecha",
  "FieldValue": "20/03/2019",
  "HasException": false,
  "ErrorMessage": null
},
{
  "FieldName": "Horas",
  "FieldValue": "5",
  "HasException": false,
  "ErrorMessage": null
},
{
  "FieldName": "Usuario",
  "FieldValue": "[{\"Key\":\"i:0#.f|membership|jartigag@example.com\",\"DisplayText\":\"Jartigag\",\"IsResolved\":true,\"Description\":\"jartigag@example.com\",\"EntityType\":\"User\",\"EntityData\":{\"IsAltSecIdPresent\":\"False\",\"Title\":\"\",\"Email\":\"jartigag@example.com\",\"MobilePhone\":\"\",\"ObjectId\":\"14308d04-61bc-40d2-98b1-fee3accf077d\",\"Department\":\"\"},\"MultipleMatches\":[],\"ProviderName\":\"Tenant\",\"ProviderDisplayName\":\"Espacio empresarial\"}]",
  "HasException": false,
  "ErrorMessage": null
},
{
  "FieldName": "Proyecto",
  "FieldValue": "9;#Otros",
  "HasException": false,
  "ErrorMessage": null
},
{
  "FieldName": "ContentType",
  "FieldValue": "Elemento",
  "HasException": false,
  "ErrorMessage": null
}],
"bNewDocumentUpdate": false,
"checkInComment": null
}'
--compressed; echo

{
    "d":
    {
        "AddValidateUpdateItemUsingPath":
        {
            "__metadata":
            {
                "type": "Collection(SP.ListItemFormUpdateValue)"
            },
            "results": [
            {
                "ErrorMessage": null,
                "FieldName": "Title",
                "FieldValue": "prueba desde curl",
                "HasException": false,
                "ItemId": 0
            },
            {
                "ErrorMessage": null,
                "FieldName": "Fecha",
                "FieldValue": "20/03/2019",
                "HasException": false,
                "ItemId": 0
            },
            {
                "ErrorMessage": null,
                "FieldName": "Horas",
                "FieldValue": "5",
                "HasException": false,
                "ItemId": 0
            },
            {
                "ErrorMessage": null,
                "FieldName": "Usuario",
                "FieldValue": "[{\"Key\":\"i:0#.f|membership|jartigag@example.com\",\"DisplayText\":\"Jartigag\",\"IsResolved\":true,\"Description\":\"jartigag@example.com\",\"EntityType\":\"User\",\"EntityData\":{\"IsAltSecIdPresent\":\"False\",\"Title\":\"\",\"Email\":\"jartigag@example.com\",\"MobilePhone\":\"\",\"ObjectId\":\"14308d04-61bc-40d2-98b1-fee3accf077d\",\"Department\":\"\"},\"MultipleMatches\":[],\"ProviderName\":\"Tenant\",\"ProviderDisplayName\":\"Espacio empresarial\"}]",
                "HasException": false,
                "ItemId": 0
            },
            {
                "ErrorMessage": null,
                "FieldName": "Proyecto",
                "FieldValue": "9;#Otros",
                "HasException": false,
                "ItemId": 0
            },
            {
                "ErrorMessage": null,
                "FieldName": "ContentType",
                "FieldValue": "Elemento",
                "HasException": false,
                "ItemId": 0
            },
            {
                "ErrorMessage": null,
                "FieldName": "Id",
                "FieldValue": "10",
                "HasException": false,
                "ItemId": 0
            }]
        }
    }
}
'''
