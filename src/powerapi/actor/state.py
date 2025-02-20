# Copyright (c) 2018, INRIA
# Copyright (c) 2018, University of Lille
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from powerapi.exception import UnknownMessageTypeException
from powerapi.actor.supervisor import Supervisor


class State:
    """
    A basic state class that encapsulate basic actor values :

    :attr:`initialized <powerapi.actor.state.State.initialized>`
    :attr:`alive <powerapi.actor.state.State.alive>`
    :attr:`behaviour <powerapi.actor.state.State.behaviour>`
    :attr:`handlers <powerapi.actor.state.State.handlers>`
    :attr:`supervisor <powerapi.actor.state.State.supervisor>`
    """

    def __init__(self, actor):
        """
        :param powerapi.Actor actor: Actor
        """
        #: (bool): True if the actor is initialized and can handle all
        #: message, False otherwise
        self.initialized = False
        #: (bool): True if the actor is alive, False otherwise
        self.alive = True
        #: ([(type, powerapi.handler.abstract_handler.AbstractHandler)]):
        #: mapping between message type and handler that the mapped handler
        #: must handle
        self.handlers = []
        #: (powerapi.actor.supervisor.Supervisor): object that supervise actors
        #: that are handle by this actor
        self.supervisor = Supervisor()
        #: (powerapi.Actor): Actor
        self.actor = actor

    def get_corresponding_handler(self, msg):
        """
        Return the handler corresponding to the given message type

        :param Object msg: the received message
        :return: the handler corresponding to the given message type
        :rtype: powerapi.handler.AbstractHandler

        :raises UnknowMessageTypeException: if no handler could be find
        """
        for (msg_type, handler) in self.handlers:
            if isinstance(msg, msg_type):
                return handler
        raise UnknownMessageTypeException()

    def add_handler(self, message_type, handler):
        """
        Map a handler to a message type

        :param type message_type: type of the message that the handler can
                                  handle
        :param handler: handler that will handle all messages of the given type
        :type handler: powerapi.handler.AbstractHandler
        """
        self.handlers.append((message_type, handler))

    def reinit(self):
        """
        Reinitialize the state
        """
