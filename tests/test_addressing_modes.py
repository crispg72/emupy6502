import unittest

from unittest.mock import patch, Mock

from emupy6502.memory_controller import MemoryController
from emupy6502.registers import Registers
from emupy6502.addressing_modes import AddressingModes


def test_implied_has_no_effect():

    addressing_modes = AddressingModes()
    registers = Registers()

    with patch.object(MemoryController, 'read', return_value = None) as mock_memory_controller:
        # 'RTS' opcode is implied address mode
        count = addressing_modes.handle(0x60, registers, mock_memory_controller)
        assert count == None
        mock_memory_controller.assert_not_called()
        assert registers == Registers()

def test_immediate_loads_next_value_from_pc():

    addressing_modes = AddressingModes()
    registers = Registers()

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        mock_memory_controller.read.return_value = 0x22
        # 'LDA' 0xA9 opcode is immediate address mode
        value = addressing_modes.handle(0xA9, registers, mock_memory_controller)
        mock_memory_controller.read.assert_called_with(0)
        assert registers.pc == 1
        assert value == 0x22

def test_relative_loads_next_value_from_pc():

    addressing_modes = AddressingModes()
    registers = Registers()

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        mock_memory_controller.read.return_value = 0x22
        # 'BPL' 0x10 opcode is relative address mode
        value = addressing_modes.handle(0x10, registers, mock_memory_controller)
        mock_memory_controller.read.assert_called_with(0)
        assert registers.pc == 1
        assert value == 0x22

def test_zero_page_calls_read_correctly():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xa5 0x22 and value at [0x0022] = 1
        mock_memory_controller.read.side_effect = [0x22, 1]
        # 'LDA' 0xA5 opcode is zero page address mode
        value = addressing_modes.handle(0xA5, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 2
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(0x22)
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert registers.pc == 2
        assert value == 1

def test_absolute_jmp_calls_read_correctly():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xa5 0x22 and value at [0x0022] = 1
        mock_memory_controller.read.side_effect = [0x22, 0x23, 1]
        # 'JMP' 0x4c opcode is absolute address mode
        value = addressing_modes.handle(0x4C, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 2
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(2)
        assert registers.pc == 3
        assert value == 0x2322

def test_absolute_calls_read_correctly():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xa5 0x22 and value at [0x0022] = 1
        mock_memory_controller.read.side_effect = [0x22, 0x23, 1]
        # 'LDA' 0xad opcode is absolute address mode
        value = addressing_modes.handle(0xAD, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 3
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(2)
        assert mock_memory_controller.read.call_args_list[2] == unittest.mock.call(0x2322)
        assert registers.pc == 3
        assert value == 1

def test_zero_page_x_index_calls_read_correctly():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode
    registers.x_index = 3

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xB5 0x03 and value at [0x06] = 1
        mock_memory_controller.read.side_effect = [3, 1]
        # 'LDA' 0xB5 opcode is zero page x indexed address mode
        value = addressing_modes.handle(0xB5, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 2
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(6)
        assert registers.pc == 2
        assert value == 1

def test_zero_page_x_index_deals_with_wraparound():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode
    registers.x_index = 0xff

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xB5 0x03 and value at [0x02] = 1
        mock_memory_controller.read.side_effect = [3, 1]
        # 'LDA' 0xB5 opcode is zero page x indexed address mode
        value = addressing_modes.handle(0xB5, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 2
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(2)
        assert registers.pc == 2
        assert value == 1

def test_zero_page_y_index_calls_read_correctly():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode
    registers.y_index = 3

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xB6 0x03 and value at [0x06] = 1
        mock_memory_controller.read.side_effect = [3, 1]
        # 'LDX' 0xB6 opcode is zero page x indexed address mode
        value = addressing_modes.handle(0xB6, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 2
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(6)
        assert registers.pc == 2
        assert value == 1

def test_zero_page_y_index_deals_with_wraparound():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode
    registers.y_index = 0xff

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xB6 0x03 and value at [0x02] = 1
        mock_memory_controller.read.side_effect = [3, 1]
        # 'LDX 0xB6 opcode is zero page x indexed address mode
        value = addressing_modes.handle(0xB6, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 2
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(2)
        assert registers.pc == 2
        assert value == 1

def test_indirect():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode
    registers.y_index = 0xff

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0x6C 0x03 0xf0 and value at [0xf003] = 0x1234
        mock_memory_controller.read.side_effect = [3, 0xf0, 0x34, 0x12]
        # 'JMP' 0x6C opcode uses indirect addressing
        value = addressing_modes.handle(0x6C, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 4
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(2)
        assert mock_memory_controller.read.call_args_list[2] == unittest.mock.call(0xf003)
        assert mock_memory_controller.read.call_args_list[3] == unittest.mock.call(0xf004)
        assert registers.pc == 3
        assert value == 0x1234

def test_zp_index_indirect_x():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode
    registers.x_index = 0x3

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xA1 0x03 and value at [0x06] = 0x1234
        mock_memory_controller.read.side_effect = [3, 0x34, 0x12]
        # 'LDA' 0xA1 opcode uses indirect addressing
        value = addressing_modes.handle(0xA1, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 3
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(6)
        assert mock_memory_controller.read.call_args_list[2] == unittest.mock.call(7)
        assert registers.pc == 2
        assert value == 0x1234

def test_zp_index_indirect_x_wraparound_1():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode
    registers.x_index = 0xff

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xA1 0x03 and value at [0xff] = 0x12, [0x00] = 0x34
        mock_memory_controller.read.side_effect = [3, 0x34, 0x12]
        # 'LDA' 0xA1 opcode uses indirect addressing
        value = addressing_modes.handle(0xA1, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 3
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(2)
        assert mock_memory_controller.read.call_args_list[2] == unittest.mock.call(3)
        assert registers.pc == 2
        assert value == 0x1234

def test_zp_index_indirect_x_wraparound_2():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode
    registers.x_index = 0xfe

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xA1 0x03 and value at [0xff] = 0x12, [0x00] = 0x34
        mock_memory_controller.read.side_effect = [1, 0x34, 0x12]
        # 'LDA' 0xA1 opcode uses indirect addressing
        value = addressing_modes.handle(0xA1, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 3
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(0xff)
        assert mock_memory_controller.read.call_args_list[2] == unittest.mock.call(0)
        assert registers.pc == 2
        assert value == 0x1234

def test_absolute_x():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode
    registers.x_index = 0x3
    AddressingModes.cycle_count = 0

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xBD 0xc000 
        mock_memory_controller.read.side_effect = [0, 0xc0]
        # 'LDA' 0xBD opcode uses indirect addressing
        value = addressing_modes.handle(0xBD, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 2
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(2)
        assert registers.pc == 3
        assert value == 0xc003
        assert AddressingModes.cycle_count == 0

def test_absolute_x_page_boundary():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode
    registers.x_index = 0x3
    AddressingModes.cycle_count = 0

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xBD 0xc000 
        mock_memory_controller.read.side_effect = [0xfe, 0xc0]
        # 'LDA' 0xBD opcode uses indirect addressing
        value = addressing_modes.handle(0xBD, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 2
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(2)
        assert registers.pc == 3
        assert value == 0xc101
        assert AddressingModes.cycle_count == 1

def test_absolute_y():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode
    registers.y_index = 0x3
    AddressingModes.cycle_count = 0

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xB9 0xc000 
        mock_memory_controller.read.side_effect = [0, 0xc0]
        # 'LDA' 0xB9 opcode uses indirect addressing
        value = addressing_modes.handle(0xB9, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 2
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(2)
        assert registers.pc == 3
        assert value == 0xc003
        assert AddressingModes.cycle_count == 0

def test_absolute_y_page_boundary():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode
    registers.y_index = 0x3
    AddressingModes.cycle_count = 0

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xB9 0xc000 
        mock_memory_controller.read.side_effect = [0xfe, 0xc0]
        # 'LDA' 0xB9 opcode uses indirect addressing
        value = addressing_modes.handle(0xB9, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 2
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(2)
        assert registers.pc == 3
        assert value == 0xc101
        assert AddressingModes.cycle_count == 1

def test_indirect_indexed_y():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode
    registers.y_index = 0x3
    AddressingModes.cycle_count = 0

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xB1 0x2a  memory at 0x2a = [0x28, 0x40]
        mock_memory_controller.read.side_effect = [0x2a, 0x28, 0x40]
        # 'LDA' 0xB9 opcode uses indirect addressing
        value = addressing_modes.handle(0xB1, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 3
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(0x2a)
        assert mock_memory_controller.read.call_args_list[2] == unittest.mock.call(0x2b)
        assert registers.pc == 2
        assert value == 0x402b
        assert AddressingModes.cycle_count == 0

def test_indirect_indexed_y_zp_boundary():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode
    registers.y_index = 0x3
    AddressingModes.cycle_count = 0

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xB1 0xff  memory at 0xff = [0x28, 0x40]
        mock_memory_controller.read.side_effect = [0xff, 0x28, 0x40]
        # 'LDA' 0xB9 opcode uses indirect addressing
        value = addressing_modes.handle(0xB1, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 3
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(0xff)
        assert mock_memory_controller.read.call_args_list[2] == unittest.mock.call(0x00)
        assert registers.pc == 2
        assert value == 0x402b
        assert AddressingModes.cycle_count == 0

def test_indirect_indexed_y_page_boundary():

    addressing_modes = AddressingModes()
    registers = Registers()
    registers.pc = 1 #fake loading of opcode
    registers.y_index = 0x3
    AddressingModes.cycle_count = 0

    with patch.object(MemoryController, 'read') as mock_memory_controller:

        # we're mocking 0xB1 0x2a  memory at 0x2a = [0xfe, 0x40]
        mock_memory_controller.read.side_effect = [0x2a, 0xfe, 0x40]
        # 'LDA' 0xB9 opcode uses indirect addressing
        value = addressing_modes.handle(0xB1, registers, mock_memory_controller)
        assert mock_memory_controller.read.call_count == 3
        assert mock_memory_controller.read.call_args_list[0] == unittest.mock.call(1)
        assert mock_memory_controller.read.call_args_list[1] == unittest.mock.call(0x2a)
        assert mock_memory_controller.read.call_args_list[2] == unittest.mock.call(0x2b)
        assert registers.pc == 2
        assert value == 0x4101
        assert AddressingModes.cycle_count == 1