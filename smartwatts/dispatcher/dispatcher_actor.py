# Copyright (C) 2018  University of Lille
# Copyright (C) 2018  INRIA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from smartwatts.actor import Actor, SocketInterface
from smartwatts.handler import PoisonPillMessageHandler
from smartwatts.report import Report
from smartwatts.message import PoisonPillMessage, StartMessage
from smartwatts.dispatcher import StartHandler, DispatcherState
from smartwatts.dispatcher import FormulaDispatcherReportHandler


class NoPrimaryGroupByRuleException(Exception):
    """
    Exception raised when user want to get the primary group_by rule on a
    formula dispatcher that doesn't have one
    """


class DispatcherActor(Actor):
    """
    DispatcherActor class herited from Actor.

    Route message to the corresponding Formula, and create new one
    if no Formula exist for this message.
    """

    def __init__(self, name, formula_init_function, route_table, verbose=False,
                 timeout=None):
        """
        :param str name: Actor name
        :param func formula_init_function: Function for creating Formula
        :param route_table: initialized route table of the DispatcherActor
        :type route_table: smartwatts.dispatcher.state.RouteTable
        :param bool verbose: Allow to display log
        :param bool timeout: Define the time in millisecond to wait for a
                             message before run timeout_handler
        """
        Actor.__init__(self, name, verbose, timeout)

        # (func): Function for creating Formula
        self.formula_init_function = formula_init_function

        # (smartwatts.DispatcherState): Actor state
        self.state = DispatcherState(Actor._initial_behaviour,
                                     SocketInterface(name, timeout),
                                     self._create_factory(), route_table)

    def setup(self):
        """
        Check if there is a primary group by rule. Set define
        StartMessage, PoisonPillMessage and Report handlers
        """
        Actor.setup(self)
        if self.state.route_table.primary_group_by_rule is None:
            raise NoPrimaryGroupByRuleException()

        self.add_handler(Report, FormulaDispatcherReportHandler())
        self.add_handler(PoisonPillMessage, PoisonPillMessageHandler())
        self.add_handler(StartMessage, StartHandler())

    def terminated_behaviour(self):
        """
        Override from Actor.

        Kill each formula before terminate
        """
        for name, formula in self.state.get_all_formula():
            self.log('kill ' + str(name))
            formula.send_data(PoisonPillMessage())
            formula.join()

    def _create_factory(self):
        """
        Create the full Formula Factory

        :return: Formula Factory
        :rtype: func(formula_id, context) -> Formula
        """
        # context = self.state.socket_interface.context
        formula_init_function = self.formula_init_function
        verbose = self.verbose

        def factory(formula_id, context):
            formula = formula_init_function(str(formula_id), verbose)
            formula.connect_data(context)
            formula.connect_control(context)
            return formula

        return factory
