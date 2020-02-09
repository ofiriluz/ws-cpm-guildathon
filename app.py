#!/usr/bin/env python3

from aws_cdk import core

from ws_cpm_guildathon.ws_cpm_guildathon_stack import WsCpmGuildathonStack


app = core.App()
WsCpmGuildathonStack(app, "ws-cpm-guildathon")

app.synth()
