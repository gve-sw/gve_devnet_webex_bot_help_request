# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Trevor Maco <tmaco@cisco.com>"
__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import sys
import random
import string

from webex_bot.models.command import Command
from webex_bot.models.response import Response
from webexteamssdk import WebexTeamsAPI, ApiError
from config import *
from webex_cards import *

# Define WebexTeamsSDK Entry point
api = WebexTeamsAPI(access_token=BOT_TOKEN)

# Get Webex PA Help Space Room ID
rooms = api.rooms.list(type='group')
roomID = ''

for room in rooms:
    if room.title == HELP_SPACE:
        roomID = room.id
        break

# If room doesn't exist, raise error
if roomID == '':
    print('Error: PA Help Space room not found. Please ensure the configured room exists!')
    sys.exit(1)

# Get Avatar for cards
avatar = api.people.me().avatar


class HelpCommand(Command):
    def __init__(self):
        super().__init__(
            help_message="Help Command",
            delete_previous_message=False
        )

    def execute(self, message, attachment_actions, activity):
        response = Response()
        help_space = False

        # We are in help space
        if attachment_actions.roomId == roomID:
            help_space = True

        # Define card attachment with proper format
        response.attachments = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": get_help_card(avatar, help_space=help_space)
        }

        response.text = 'Something has gone wrong'
        return response


class RequestPA(Command):
    def __init__(self):
        super().__init__(
            command_keyword="request",
            help_message="Request help from PA Space",
            delete_previous_message=False
        )

    def execute(self, message, attachment_actions, activity):
        response = Response()

        # Disabled requests command in Help Space (can't globally disable, it needs to be callable)
        if attachment_actions.roomId == roomID:
            response.text = 'Error: requests not allowed in the Help Space! Please use "help" command to see valid ' \
                            'commands. '
            return response

        # Define card attachment with proper format
        response.attachments = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": get_request_card(avatar)
        }

        # Fallback text
        response.text = "Something has gone wrong"

        return response


class PostToPASpace(Command):
    def __init__(self):
        super().__init__(
            card_callback_keyword="submit",
            help_message="Post card request to PA space",
            delete_previous_message=True
        )

    def execute(self, message, attachment_actions, activity):
        response = Response()

        # Attempting to call submit command directly
        if not hasattr(attachment_actions, 'inputs'):
            response.text = 'Error: Command is reserved and not callable. Please use "help" command to see valid ' \
                            'commands. '
            return response

        # Populate request card with requestor information
        person = api.people.get(attachment_actions.personId)
        details = attachment_actions.inputs['information']
        request_id = ''.join(random.choices(string.digits, k=10))

        if details == '':
            details = 'N/A'

        # Define card attachment with proper format
        attachments = [{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": get_response_card(person.displayName, person.id, person.firstName, details, request_id, avatar)
        }]

        try:
            # Post message with card to Help Space
            api.messages.create(roomId=roomID, text='A new Radiologist request has been submitted.',
                                attachments=attachments)
            response.text = "Request successfully submitted. Once the request is accepted, a 1-1 Webex Space will " \
                            "be created between you and the accepting PA!"
        except ApiError as e:
            response.text = "There was an error with submitting the request {}. Please try again.".format(e)

        return response


class AcceptRequest(Command):
    def __init__(self):
        super().__init__(
            card_callback_keyword="accept",
            help_message="Accept Radiologist request posted to PA space",
            delete_previous_message=True
        )

    def execute(self, message, attachment_actions, activity):
        response = Response()

        # Attempting to call accept command directly
        if not hasattr(attachment_actions, 'inputs'):
            response.text = 'Error: Command is reserved and not callable. Please use "help" command to see valid ' \
                            'commands. '
            return response

        # Generate unique 1-1 room name
        requester_firstname = attachment_actions.inputs['requester_firstname']
        accepter_firstname = api.people.get(attachment_actions.personId).firstName
        request_id = attachment_actions.inputs['request_id']

        room_title = '{} - {} Help Request ({})'.format(requester_firstname, accepter_firstname, request_id)

        # Create 1-1 Room with Radiologist and PA, add them to the room, remove the bot from the room
        try:
            new_room = api.rooms.create(title=room_title)

            accepter_id = attachment_actions.personId
            requester_id = attachment_actions.inputs['requester_id']

            # Add members
            api.memberships.create(roomId=new_room.id, personId=accepter_id)
            api.memberships.create(roomId=new_room.id, personId=requester_id)

            # Remove bot
            members = api.memberships.list(new_room.id)

            for member in members:
                if member.personDisplayName == BOT_NAME:
                    api.memberships.delete(member.id)

            response.text = "Request {} accepted, 1-1 space successfully created.".format(request_id)

        except ApiError as e:
            response.text = "There was an error with creating or adding members to the 1-1 room {}. Please try again.".format(
                e)

        return response
