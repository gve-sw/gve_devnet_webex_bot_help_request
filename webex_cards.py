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


# The card seen by the Radiologist requesting help
def get_help_card(avatar, help_space):
    help_card = {
        "type": "AdaptiveCard",
        "body": [
            {
                "type": "ColumnSet",
                "columns": [
                    {
                        "type": "Column",
                        "items": [
                            {
                                "type": "Image",
                                "style": "Person",
                                "url": avatar,
                                "size": "Medium",
                                "height": "50px"
                            }
                        ],
                        "width": "auto"
                    },
                    {
                        "type": "Column",
                        "width": "stretch",
                        "style": "emphasis",
                        "items": [
                            {
                                "type": "TextBlock",
                                "weight": "Bolder",
                                "text": "What can I do?",
                                "horizontalAlignment": "Center",
                                "wrap": True,
                                "color": "Default",
                                "size": "Medium",
                                "spacing": "Small"
                            }
                        ]
                    }
                ]
            },
            {
                "type": "TextBlock",
                "text": "Here are my available commands. Click one to begin!",
                "wrap": True
            },
            {
                "type": "ActionSet",
                "actions": [
                    {
                        "type": "Action.Submit",
                        "id": "request",
                        "title": "Request help from PA",
                        "data": {
                            "callback_keyword": "request"
                        }
                    },
                ],
                "horizontalAlignment": "Left",
                "spacing": "Large"
            }
        ],
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.2"
    }

    # If we are in the PA space, disable commands and change message
    if help_space:
        help_card['body'][-1]["isVisible"] = False
        help_card['body'][-2]['text'] = 'Please click "Accept" on a Radiologist request to create a 1-1 space. This ' \
                                        'will also remove the request card. '

    return help_card


# The card seen by the Radiologist requesting help
def get_request_card(avatar):
    request_card = {
        "type": "AdaptiveCard",
        "body": [
            {
                "type": "ColumnSet",
                "columns": [
                    {
                        "type": "Column",
                        "items": [
                            {
                                "type": "Image",
                                "style": "Person",
                                "url": avatar,
                                "size": "Medium",
                                "height": "50px"
                            }
                        ],
                        "width": "auto"
                    },
                    {
                        "type": "Column",
                        "width": "stretch",
                        "style": "emphasis",
                        "items": [
                            {
                                "type": "TextBlock",
                                "weight": "Bolder",
                                "text": "Request a PA for Assistance",
                                "horizontalAlignment": "Center",
                                "wrap": True,
                                "color": "Default",
                                "size": "Medium",
                                "spacing": "Small"
                            }
                        ]
                    }
                ]
            },
            {
                "type": "TextBlock",
                "text": "Please enter additional details for your request. Including this information helps us serve you quicker!",
                "wrap": True
            },
            {
                "type": "Input.Text",
                "isMultiline": True,
                "placeholder": "What can I help you with? (optional)",
                "id": "information",
                "maxLength": 1500,
            },
            {
                "type": "ActionSet",
                "actions": [
                    {
                        "type": "Action.Submit",
                        "id": "submit",
                        "title": "Submit",
                        "data": {
                            "callback_keyword": "submit"
                        }
                    }
                ],
                "horizontalAlignment": "Left",
                "spacing": "Large"
            }
        ],
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.2"
    }

    return request_card


# The card seen by the PA to respond to the Radiologist's request
def get_response_card(requester, requester_id, requester_firstname, details, request_id, avatar):
    response_card = {
        "type": "AdaptiveCard",
        "body": [
            {
                "type": "ColumnSet",
                "columns": [
                    {
                        "type": "Column",
                        "items": [
                            {
                                "type": "Image",
                                "style": "Person",
                                "url": avatar,
                                "size": "Medium",
                                "height": "50px"
                            }
                        ],
                        "width": "auto"
                    },
                    {
                        "type": "Column",
                        "items": [
                            {
                                "type": "TextBlock",
                                "weight": "Bolder",
                                "text": "New Radiologist Request",
                                "horizontalAlignment": "Center",
                                "wrap": True,
                                "color": "Default",
                                "size": "Medium",
                                "spacing": "Small"
                            }
                        ],
                        "width": "stretch",
                        "style": "emphasis"
                    }
                ]
            },
            {
                "type": "ColumnSet",
                "columns": [
                    {
                        "type": "Column",
                        "width": 35,
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": "Requester:",
                            }
                        ]
                    },
                    {
                        "type": "Column",
                        "width": 65,
                        "items": [
                            {
                                "type": "TextBlock",
                                "color": "Light",
                                "text": requester
                            }
                        ],
                        "id": "name"
                    }
                ],
                "spacing": "Padding",
                "horizontalAlignment": "Center",
                "id": "requester"
            },
            {
                "type": "ColumnSet",
                "columns": [
                    {
                        "type": "Column",
                        "width": 35,
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": "ID:",
                            }
                        ]
                    },
                    {
                        "type": "Column",
                        "width": 65,
                        "items": [
                            {
                                "type": "TextBlock",
                                "color": "Light",
                                "text": request_id
                            }
                        ],
                        "id": "unique_id"
                    }
                ],
                "spacing": "Padding",
                "horizontalAlignment": "Center",
                "id": "request"
            },
            {
                "type": "Container",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": "Request Details:",
                        "wrap": True,
                    },
                    {
                        "type": "TextBlock",
                        "text": details,
                        "id": "details",
                        "wrap": True,
                        "color": "Light"
                    },
                ]
            },
            {
                "type": "Input.Text",
                "value": requester_firstname,
                "id": "requester_firstname",
                "isVisible": False
            },
            {
                "type": "Input.Text",
                "value": requester_id,
                "id": "requester_id",
                "isVisible": False
            },
            {
                "type": "Input.Text",
                "value": request_id,
                "id": "request_id",
                "isVisible": False
            },
            {
                "type": "ActionSet",
                "actions": [
                    {
                        "type": "Action.Submit",
                        "id": "submit",
                        "title": "Accept",
                        "data": {
                            "callback_keyword": "accept"
                        }
                    }
                ],
                "horizontalAlignment": "Left",
                "spacing": "Large"
            }
        ],
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.2"
    }

    return response_card
