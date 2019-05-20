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
__version__ = "0.6"

# ttytracker_aliases.cfg: a config json that matches shortcuts with sharepoints projects and clients.
#                         for example:
#                         for example: [{"shorcut": "tools", "project": "Mantenimiento de herramientas"}, ...]
#                                       └── #tools = Mantenimiento de herramientas
#

from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from ttymetracker_credentials import *
import json
from datetime import datetime
import os
import sys

def commit_today(logbooksDir, aliasesFile):
    try:
        today_short = datetime.now().strftime("%Y-%m-%d")
        today_file = "{}/{}.md".format(logbooksDir, today_short)
        with open(today_file) as f, open("commit.tmp","w") as c:
            c.write("## Revisa tu registro de hoy {} antes de publicarlo en SharePoint.\n## Las líneas que empiezan con '##' serán ignoradas.\n".format(today_short))
            if aliasesFile: c.write("##\n## Las notas con #etiquetas configuradas en {} se completarán con sus datos correspondientes.\n".format(aliasesFile))
            c.write("## En Vim, ejecuta :Round para redondear los tiempos al cuarto de hora (ejemplo: 00:17 -> 00:15).\n")
            c.write('\n##~ Elimina esta línea para confirmar la publicación de este registro ~##\n\n')
            c.write("## DESDE - HASTA   | NOTA\n")
            lines = f.readlines()
            time = '09:00'
            for line in lines:
                i = lines.index(line)
                if i==len(lines)-1: break
                if lines[i+1]=='---\n': # if this line it's a timestamp:
                    if lines[i+2][0]=='>': # if there's a note on this timestamp:
                        previous_time = time
                        time = ''.join( line.split(' ')[4][:-3] ) # line.split(' ')[4] takes something like '09:17'
                        c.write("{} - {}: {}".format(previous_time, time, lines[i+2][2:]))
        os.system("vim commit.tmp")
    except IOError as e:
        print("\033[91m[!]\033[0m error: {}".format(e))

def push_note(ctx, start, end, project, note):
    try:
        hours = float("{0:.2f}".format((datetime.strptime(end,"%H:%M") - datetime.strptime(start,"%H:%M")).total_seconds()/3600))
        list_object = ctx.web.lists.get_by_title(sharepoint_listTitle)
        item_properties = {'__metadata': {'type': sharepoint_itemType}, 'Title': note, 'Horas': hours, 'UsuarioId': sharepoint_userid, 'ProyectoId': project['project_id']}
        #{'FirstUniqueAncestorSecurableObject': {'__deferred': {'uri': "anUrl"}}, 'RoleAssignments': {'__deferred': {'uri': "anUrl"}}, 'AttachmentFiles': {'__deferred': {'uri': "anUrl"}}, 'ContentType': {'__deferred': {'uri': "anUrl"}}, 'GetDlpPolicyTip': {'__deferred': {'uri': "anUrl"}}, 'FieldValuesAsHtml': {'__deferred': {'uri': "anUrl"}}, 'FieldValuesAsText': {'__deferred': {'uri': "anUrl"}}, 'FieldValuesForEdit': {'__deferred': {'uri': "anUrl"}}, 'File': {'__deferred': {'uri': "anUrl"}}, 'Folder': {'__deferred': {'uri': "anUrl"}}, 'LikedByInformation': {'__deferred': {'uri': "anUrl"}}, 'ParentList': {'__deferred': {'uri': "anUrl"}}, 'Properties': {'__deferred': {'uri': "anUrl"}}, 'Versions': {'__deferred': {'uri': "anUrl"}}, 'FileSystemObjectType': 0, 'Id': 121, 'ServerRedirectedEmbedUri': None, 'ServerRedirectedEmbedUrl': '', 'ContentTypeId': '0x0100B7A59ECFFA6C0C44A2DA2DA4DBD84EF1', 'Title': 'Inicio de sesión', 'ComplianceAssetId': None, 'Fecha': '2019-05-20T11:06:56Z', 'Horas': None, 'UsuarioId': None, 'UsuarioStringId': None, 'ProyectoId': None, 'ID': 121, 'Modified': '2019-05-20T11:06:56Z', 'Created': '2019-05-20T11:06:56Z', 'AuthorId': 186, 'EditorId': 186, 'OData__UIVersionString': '1.0', 'Attachments': False, 'GUID': '5182d12c-7e8a-4a31-a1a0-15168246f257'}
        item = list_object.add_item(item_properties)
        ctx.execute_query()
        print('[post] {} - {}h | {} | project: {}'.format(datetime.now().strftime("%Y-%m-%d"), hours, item.properties["Title"], project['project_name']))
    except IOError as e:
        print("\033[91m[!]\033[0m error: {}".format(e))

def push_today(ctx, aliasesFile):
    print("\033[1m[[ notas del registro de HOY {} para publicar en SharePoint: ]]\033[0m\n".format(datetime.now().strftime("%Y-%m-%d")))
    try:
        aliases = []
        if aliasesFile:
            aliases = json.load( open(aliasesFile) )
    except Exception as e:
        print("\033[91m[!]\033[0m error en {}: {}".format(aliasesFile,e))
        sys.exit()
    try:
        with open("commit.tmp") as f:
            lines = f.readlines()
            for line in lines:
                project, client, task = '""', '""', '""'
                line = line.rstrip() # remove '\n'
                if line=='##~ Elimina esta línea para confirmar la publicación de este registro ~##':
                    print('acción cancelada (porque la línea \'##~ ~##\' no fue eliminada)')
                    os.system("rm commit.tmp")
                    sys.exit()
                elif line=='' or line[:2]=='##':
                    continue
                project = {'project_name':'','project_id':None}
                for alias in aliases:
                    if "#{}".format(alias['shorcut']) in line.lower():
                        if 'project_name' in alias and 'project_id' in alias: project = {'project_name':alias['project_name'], 'project_id':alias['project_id']}
                # from '16:00:00 - 17:00:00: [x] depurar Líneas Base',
                start = line.split(' - ')[0]   # it takes 16:00
                end = line.split(' - ')[1][:5] # it takes 17:00
                note = line[15:]               # it takes '[x] depurar Líneas Base'
                push_note(ctx, start, end, project, note)
        os.system("rm commit.tmp")
    except Exception as e:
        print("\033[91m[!]\033[0m error: {}".format(e))
