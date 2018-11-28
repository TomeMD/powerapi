import multiprocessing


import setproctitle
import pytest
import zmq
from mock import Mock, patch

from smartwatts.message import UnknowMessageTypeException, PoisonPillMessage
from smartwatts.actor import Actor


class DummyActor(Actor):
    def _post_handle(self, result):
        pass

    def setup(self):
        pass


ACTOR_NAME = 'dummy_actor'
VERBOSE_MODE = False
PULL_SOCKET_ADDRESS = 'ipc://@' + ACTOR_NAME

@pytest.fixture()
def dummy_actor():
    """ Return a dummy actor"""
    actor = DummyActor(name=ACTOR_NAME, verbose=VERBOSE_MODE)

    return actor



def test_actor_initialisation(dummy_actor):
    """ test actor attributes initialization"""
    assert dummy_actor.alive is True
    assert dummy_actor.pull_socket_address == PULL_SOCKET_ADDRESS
    assert dummy_actor.name == ACTOR_NAME


def test_communication_setup(dummy_actor):
    """test if zmq context and sockets are correctly initialized and if the proc
    title is correctly set after the run function was call

    """

    dummy_actor._communication_setup()

    assert isinstance(dummy_actor.context, zmq.Context)

    assert isinstance(dummy_actor.pull_socket, zmq.Socket)
    assert dummy_actor.pull_socket.closed is False
    assert dummy_actor.pull_socket.get(zmq.TYPE) == zmq.PULL
    assert (dummy_actor.pull_socket.get(zmq.LAST_ENDPOINT).decode("utf-8") ==
            PULL_SOCKET_ADDRESS)

    assert setproctitle.getproctitle() == ACTOR_NAME

#######################
# HANDLE MESSAGE TEST #
#######################

def test_handle_unknow_message_type(dummy_actor):
    """test to handle a message with no handle bind to its type

    must raise an UnknowMessageTypeException

    """
    with pytest.raises(UnknowMessageTypeException):
        dummy_actor._handle_message("toto")

def test_handle_poison_pill_message(dummy_actor):
    """test to handle a PoisonPillMessage

    after handle this message, the self.alive boolean must be set to False

    """
    dummy_actor._handle_message(PoisonPillMessage())
    assert dummy_actor.alive is False
