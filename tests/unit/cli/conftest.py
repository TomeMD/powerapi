# Copyright (c) 2023, INRIA
# Copyright (c) 2023, University of Lille
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

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
import os
import sys

import pytest
import tests.utils.cli as test_files_module
from tests.utils.cli.base_config_parser import load_configuration_from_json_file, \
    generate_cli_configuration_from_json_file
from powerapi.cli.config_parser import SubgroupConfigParser, BaseConfigParser, store_true, RootConfigParser
from powerapi.cli.parsing_manager import RootConfigParsingManager, SubgroupConfigParsingManager


@pytest.fixture(name="invalid_csv_io_stream_config")
def csv_input_output_stream_config():
    """
     Invalid configuration with csv as input and output and stream mode enabled
    """
    return load_configuration_from_json_file(file_name='csv_input_output_stream_mode_enabled_configuration.json')


@pytest.fixture
def mongodb_input_output_stream_config():
    """
    Configuration with mongodb as input and output and stream mode enabled
    """
    return load_configuration_from_json_file(file_name='mongo_input_output_stream_mode_enabled_configuration.json')


@pytest.fixture
def several_inputs_outputs_stream_config():
    """
    Configuration with several inputs and outputs and stream mode enabled
    """
    return load_configuration_from_json_file(file_name='several_inputs_outputs_stream_mode_enabled_configuration.json')


@pytest.fixture
def several_inputs_outputs_stream_mongo_without_some_arguments_config(several_inputs_outputs_stream_config):
    """
    Configuration with several inputs and outputs and stream mode enabled. Some arguments
    of mongo input/output are removed
    """
    for _, current_input in several_inputs_outputs_stream_config["input"].items():
        if current_input['type'] == 'mongodb':
            current_input.pop('uri')
            current_input.pop('db')

    for _, current_output in several_inputs_outputs_stream_config["output"].items():
        if current_output['type'] == 'mongodb':
            current_output.pop('uri')
            current_output.pop('db')
    return several_inputs_outputs_stream_config


@pytest.fixture
def several_inputs_outputs_stream_socket_without_some_arguments_config(several_inputs_outputs_stream_config):
    """
    Configuration with several inputs and outputs and stream mode enabled. Some arguments
    of socket input are removed
    """
    for _, current_input in several_inputs_outputs_stream_config["input"].items():
        if current_input['type'] == 'socket':
            current_input.pop('port')

    return several_inputs_outputs_stream_config


@pytest.fixture
def several_inputs_outputs_stream_csv_without_some_arguments_config(several_inputs_outputs_stream_config):
    """
    Configuration with several inputs and outputs and stream mode enabled. Some arguments
    of csv input/output are removed
    """
    for _, current_input in several_inputs_outputs_stream_config["input"].items():
        if current_input['type'] == 'csv':
            current_input.pop('files')

    for _, current_output in several_inputs_outputs_stream_config["output"].items():
        if current_output['type'] == 'csv':
            current_output.pop('directory')

    return several_inputs_outputs_stream_config


@pytest.fixture
def several_inputs_outputs_stream_influx_without_some_arguments_config(several_inputs_outputs_stream_config):
    """
    Configuration with several inputs and outputs and stream mode enabled. Some arguments
    of influxdb output are removed
    """
    for _, current_output in several_inputs_outputs_stream_config["output"].items():
        if current_output['type'] == 'influxdb':
            current_output.pop('port')
            current_output.pop('db')

    return several_inputs_outputs_stream_config


@pytest.fixture
def several_inputs_outputs_stream_prometheus_without_some_arguments_config(several_inputs_outputs_stream_config):
    """
    Configuration with several inputs and outputs and stream mode enabled. Some arguments
    of prometheus output are removed
    """
    for _, current_output in several_inputs_outputs_stream_config["output"].items():
        if current_output['type'] == 'prom':
            current_output.pop('metric_name')
            current_output.pop('metric_description')
            current_output.pop('aggregation_period')

    return several_inputs_outputs_stream_config


@pytest.fixture
def several_inputs_outputs_stream_opentsdb_without_some_arguments_config(several_inputs_outputs_stream_config):
    """
    Configuration with several inputs and outputs and stream mode enabled. Some arguments
    of opentsdb output are removed
    """
    for _, current_output in several_inputs_outputs_stream_config["output"].items():
        if current_output['type'] == 'opentsdb':
            current_output.pop('metric_name')
            current_output.pop('port')
            current_output.pop('uri')

    return several_inputs_outputs_stream_config


@pytest.fixture
def several_inputs_outputs_stream_virtiofs_without_some_arguments_config(several_inputs_outputs_stream_config):
    """
    Configuration with several inputs and outputs and stream mode enabled. Some arguments
    of virtiofs output are removed
    """
    for _, current_output in several_inputs_outputs_stream_config["output"].items():
        if current_output['type'] == 'virtiofs':
            current_output.pop('vm_name_regexp')
            current_output.pop('root_directory_name')
            current_output.pop('vm_directory_name_prefix')
            current_output.pop('vm_directory_name_suffix')

    return several_inputs_outputs_stream_config


@pytest.fixture
def several_inputs_outputs_stream_filedb_without_some_arguments_config(several_inputs_outputs_stream_config):
    """
    Configuration with several inputs and outputs and stream mode enabled. Some arguments
    of filedb output are removed
    """
    for _, current_output in several_inputs_outputs_stream_config["output"].items():
        if current_output['type'] == 'filedb':
            current_output.pop('filename')

    return several_inputs_outputs_stream_config


@pytest.fixture
def csv_io_postmortem_config(invalid_csv_io_stream_config):
    """
    Valid configuration with csv as input and output and stream mode disabled
    """
    invalid_csv_io_stream_config["stream"] = False
    return invalid_csv_io_stream_config


@pytest.fixture
def csv_io_postmortem_config_without_optional_arguments(csv_io_postmortem_config):
    """
    Valid configuration with csv as input and output without optional arguments, i.e.,
    stream, verbose, and name model for inputs and outputs
    """
    csv_io_postmortem_config.pop('stream')
    csv_io_postmortem_config.pop('verbose')

    for current_input_name in csv_io_postmortem_config['input']:
        csv_io_postmortem_config['input'][current_input_name].pop('model')
        csv_io_postmortem_config['input'][current_input_name].pop('name')

    for current_ouput_name in csv_io_postmortem_config['output']:
        csv_io_postmortem_config['output'][current_ouput_name].pop('model')
        csv_io_postmortem_config['output'][current_ouput_name].pop('name')

    return csv_io_postmortem_config


@pytest.fixture
def config_without_input(csv_io_postmortem_config):
    """
    Invalid configuration without inputs
    """
    csv_io_postmortem_config.pop('input')

    return csv_io_postmortem_config


@pytest.fixture
def config_without_output(csv_io_postmortem_config):
    """
    Invalid configuration without inputs
    """
    csv_io_postmortem_config.pop('output')

    return csv_io_postmortem_config


@pytest.fixture()
def subgroup_parser():
    """
    A subgroup parser with one argument "-a"
    """
    parser = SubgroupConfigParser('test')
    parser.add_argument('a', is_flag=True)
    return parser


@pytest.fixture
def create_empty_files_from_config(invalid_csv_io_stream_config: dict):
    """
    Create on the module path the files that are indicated on csv input.
    When they are no longer required, those files are erased
    """
    for _, input_config in invalid_csv_io_stream_config['input'].items():
        if input_config['type'] == 'csv':
            list_of_files = input_config['files'].split(",")
            for file_str in list_of_files:
                if os.path.isfile(file_str) is False:
                    with open(file_str, 'w') as file:
                        file.close()

    yield

    for _, input_config in invalid_csv_io_stream_config['input'].items():
        if input_config['type'] == 'csv':
            list_of_files = input_config['files']
            for file_str in list_of_files:
                if os.path.isfile(file_str):
                    os.remove(file_str)


@pytest.fixture
def base_config_parser():
    """
    Return a BaseConfigParser with mandatory and optional arguments
    """

    parser = BaseConfigParser()

    parser.add_argument('arg1', 'argument1', 'argumento1', default_value=3, argument_type=int, is_mandatory=False)

    parser.add_argument('argumento2', 'arg2', argument_type=str, is_mandatory=True)

    parser.add_argument('arg3', 'argument3', argument_type=bool, is_mandatory=False)

    parser.add_argument('dded', 'arg4', argument_type=float, is_mandatory=True)

    parser.add_argument('arg5', '5', default_value='default value', argument_type=str, help_text='help 5')

    return parser


@pytest.fixture
def root_config_parser_with_mandatory_and_optional_arguments():
    """
    Return a RootConfigParser with mandatory and optional arguments
    """

    parser = RootConfigParser()

    parser.add_argument('a', argument_type=bool, is_flag=True, action=store_true)

    parser.add_argument('argument1', 'arg1', default_value=3, argument_type=int, is_mandatory=False)

    parser.add_argument('argumento2', '2', argument_type=str, is_mandatory=True)

    parser.add_argument('arg3', 'argument3', argument_type=bool, is_mandatory=False)

    parser.add_argument('d', 'arg4', argument_type=float, is_mandatory=True)

    parser.add_argument('arg5', '5', default_value='default value', argument_type=str,
                        help_text='help 5')

    return parser


@pytest.fixture
def root_config_parser_with_subgroups(root_config_parser_with_mandatory_and_optional_arguments):
    """
     Return a RootConfigParser with subgroups
    """

    root_config_parser_with_mandatory_and_optional_arguments.add_simple_argument_prefix(argument_prefix='TEST_')

    root_config_parser_with_mandatory_and_optional_arguments.add_subgroup(subgroup_type='g1', prefix='TEST_G1_')

    root_config_parser_with_mandatory_and_optional_arguments.add_subgroup(subgroup_type='g2', prefix='TEST_G2_')

    subgroup_parser_g1 = SubgroupConfigParser(name='type1')
    subgroup_parser_g1.add_argument('1', 'a1', argument_type=str, is_mandatory=True)
    subgroup_parser_g1.add_argument('2', 'a2', argument_type=bool, default_value=True)
    subgroup_parser_g1.add_argument('3', 'a3', argument_type=str, default_value=69)
    subgroup_parser_g1.add_argument('n', 'name', argument_type=str)
    root_config_parser_with_mandatory_and_optional_arguments.add_subgroup_parser(subgroup_type='g1',
                                                                                 subgroup_parser=subgroup_parser_g1)

    subgroup_parser_g2 = SubgroupConfigParser(name='type2')
    subgroup_parser_g2.add_argument('1', 'a1', argument_type=float, is_mandatory=False)
    subgroup_parser_g2.add_argument('2', 'a2', argument_type=str)
    subgroup_parser_g2.add_argument('3', 'a3', argument_type=str)
    subgroup_parser_g2.add_argument('4', 'a4', argument_type=str)
    subgroup_parser_g2.add_argument('n', 'name', argument_type=str)
    root_config_parser_with_mandatory_and_optional_arguments.add_subgroup_parser(subgroup_type='g2',
                                                                                 subgroup_parser=subgroup_parser_g2)

    return root_config_parser_with_mandatory_and_optional_arguments


@pytest.fixture
def base_config_parser_no_mandatory_arguments():
    """
    Return a BaseConfigParser without mandatory arguments
    """
    parser = BaseConfigParser()

    parser.add_argument('arg1', default_value=4, argument_type=int)

    parser.add_argument('arg2', argument_type=str)

    parser.add_argument('arg3', argument_type=bool)

    parser.add_argument('arg4', argument_type=int)

    parser.add_argument('arg5', argument_type=int)

    return parser


@pytest.fixture
def base_config_parser_str_representation():
    """
    Return expected representation for a BaseConfigParser used in unit tests
    """
    return ' --arg1, --argument1, --argumento1 : \n' + \
        ' --argumento2, --arg2 : \n' + \
        ' --arg3, --argument3 : \n' + \
        ' --dded, --arg4 : \n' + \
        ' --arg5, -5 : help 5\n'


@pytest.fixture
def root_config_parsing_manager():
    """
    Return a RootConfigParsingManager with a flag argument 'a'
    """
    parser_manager = RootConfigParsingManager()
    parser_manager.add_argument_to_cli_parser('a', argument_type=bool, is_flag=True, action=store_true)
    parser_manager.add_subgroup_to_cli_parser(name='sub')

    return parser_manager


@pytest.fixture
def root_config_parsing_manager_with_mandatory_and_optional_arguments():
    """
    Return a RootConfigParsingManager with several arguments, some of them are mandatory
    """
    parser_manager = RootConfigParsingManager()

    parser_manager.add_simple_argument_prefix_to_cli_parser(argument_prefix='TEST_')

    parser_manager.add_subgroup_to_cli_parser(name='input', prefix='TEST_INPUT_')

    parser_manager.add_subgroup_to_cli_parser(name='output', prefix='TEST_OUTPUT_')

    parser_manager.add_argument_to_cli_parser('a', argument_type=bool, is_flag=True, action=store_true)

    parser_manager.add_argument_to_cli_parser('1', 'argument1', default_value=3, argument_type=int, is_mandatory=False)

    parser_manager.add_argument_to_cli_parser('argumento2', '2', argument_type=str, is_mandatory=True)

    parser_manager.add_argument_to_cli_parser('arg3', 'argument3', argument_type=bool, is_mandatory=False)

    parser_manager.add_argument_to_cli_parser('d', 'arg4', argument_type=float, is_mandatory=True)

    parser_manager.add_argument_to_cli_parser('arg5', '5', default_value='default value', argument_type=str,
                                              help_text='help 5')

    i1_type_subgroup_parser_manager = SubgroupConfigParsingManager(name="i1_type")
    i1_type_subgroup_parser_manager.add_argument_to_cli_parser('model', 'm', argument_type=str, is_mandatory=True)
    i1_type_subgroup_parser_manager.add_argument_to_cli_parser('db', 'd', argument_type=str, is_mandatory=False)
    i1_type_subgroup_parser_manager.add_argument_to_cli_parser('port', 'p', argument_type=int, is_mandatory=False)
    i1_type_subgroup_parser_manager.add_argument_to_cli_parser('name', 'n', argument_type=str, is_mandatory=False,
                                                               default_value='my_i1_instance')

    parser_manager.add_subgroup_parser(subgroup_name="input", subgroup_parser=i1_type_subgroup_parser_manager)

    o1_type_subgroup_parser_manager = SubgroupConfigParsingManager(name="o1_type")
    o1_type_subgroup_parser_manager.add_argument_to_cli_parser('model', 'm', argument_type=str, is_mandatory=True)
    o1_type_subgroup_parser_manager.add_argument_to_cli_parser('db', 'd', argument_type=str, is_mandatory=False)
    o1_type_subgroup_parser_manager.add_argument_to_cli_parser('name', 'n', argument_type=str, is_mandatory=False,
                                                               default_value='my_o1_instance')
    o1_type_subgroup_parser_manager.add_argument_to_cli_parser('collection', 'c', argument_type=str)

    parser_manager.add_subgroup_parser(subgroup_name="output", subgroup_parser=o1_type_subgroup_parser_manager)

    o2_type_subgroup_parser_manager = SubgroupConfigParsingManager(name="o2_type")
    o2_type_subgroup_parser_manager.add_argument_to_cli_parser('model', 'm', argument_type=str, is_mandatory=True)
    o2_type_subgroup_parser_manager.add_argument_to_cli_parser('db', 'd', argument_type=str, is_mandatory=False)
    o2_type_subgroup_parser_manager.add_argument_to_cli_parser('name', 'n', argument_type=str, is_mandatory=False,
                                                               default_value='my_o2_instance')
    o2_type_subgroup_parser_manager.add_argument_to_cli_parser('collection', 'c', argument_type=str)

    parser_manager.add_subgroup_parser(subgroup_name="output", subgroup_parser=o2_type_subgroup_parser_manager)

    return parser_manager


@pytest.fixture
def test_files_path():
    return test_files_module.__path__[0]


@pytest.fixture()
def cli_configuration(config_file: str):
    """
    Load in sys.argv a configuration with arguments extracted from a json file
    """
    # config_file = 'root_manager_basic_configuration.json'
    sys.argv = generate_cli_configuration_from_json_file(file_name=config_file)

    yield None

    sys.argv = []


@pytest.fixture()
def empty_cli_configuration():
    sys.argv = []

    yield None

    sys.argv = []
