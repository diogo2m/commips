import argparse

# --------------------------------------------------------------------
# ----------------------    HELPER FUNCTIONS    ----------------------
# --------------------------------------------------------------------


def verify_line_size(line: list, LINE_SIZE: int) -> None:
    if len(line) != LINE_SIZE:
        raise Exception("Tamanho da linha inválido")


def checking_syntax(word: str, expected_word: str) -> None:
    # Checking if the command is correct
    if word != expected_word:
        raise Exception(
            f'Sintaxe inválida. Esperava-se "{expected_word}", mas foi fornecido "{word}".'
        )


def getting_register_or_immediate(word: str, registers: list, imm: int) -> list:
    try:
        if imm:
            raise Exception("Mais de um imediato foi fornecido")
        imm = int(word)
        imm = f'{imm}'
    except:
        registers.append(word)

    return [registers, imm]


def getting_register(word: str, registers: list, imm: int) -> list:
    try:
        imm = int(word)
        raise Exception("Um imediato foi fornecido quando se esperava um registrador")
    except:
        registers.append(word)

    return registers


def identifying_operation(possible_operations: object, operation: str) -> str:
    # Identifying operation
    if possible_operations.get(operation):
        opcode = possible_operations[operation]
    else:
        raise Exception(
            f'Operação "{operation}" inválida. Operações esperadas: {possible_operations}'
        )

    return opcode


# -------------------------------------------------------------------
# ---------------------- TRANSLATION FUNCTIONS ----------------------
# -------------------------------------------------------------------


def translate_logical_operation(line: list) -> str:
    # Constant for the expected size of the line
    LINE_SIZE = 6

    # Dictionary mapping logical operation keywords to their assembly counterparts
    logical_operations = {"nor": "NOR", "e": "AND", "ou": "OR", "xor": "XOR"}

    # Verify that the line has the expected size
    verify_line_size(line, LINE_SIZE)

    # Initialize lists for registers and immediate values
    registers = []
    imm = None

    # Process the first word in the line (usually a register or immediate value)
    registers, imm = getting_register_or_immediate(line[1], registers, imm)

    # Identify the opcode (assembly operation) based on the keyword in the second word
    opcode = identifying_operation(logical_operations, line[2])

    # Process the third word (usually a register or immediate value)
    registers, imm = getting_register_or_immediate(line[3], registers, imm)

    # Check if the command is correct (e.g., syntax check)
    checking_syntax(line[4], "em")

    # Process the last word (usually a register or immediate value)
    registers = getting_register(line[5], registers, imm)

    # Return the assembly code based on the number of registers and immediate values
    if len(registers) == 2:
        return f"{opcode}I ${registers[1]}, ${registers[0]}, #{imm}"

    elif len(registers) == 3:
        return f"{opcode} ${registers[2]}, ${registers[0]}, ${registers[1]}"

    else:
        raise Exception("Erro de sintaxe desconhecido.")


def translate_arithmetic(line: list) -> list:
    LINE_SIZE = 6

    # Dictionary mapping arithmetic operation keywords to their assembly counterparts
    arithmetic_operations = {
        "adicionar": "ADD",
        "subtrair": "SUB",
        "multiplicar": "MULT",
    }

    # Verify that the line has the expected size
    verify_line_size(line, LINE_SIZE)

    # Initialize lists for registers and immediate values
    registers = []
    imm = None

    # Identify the opcode (assembly operation) based on the keyword in the first word
    opcode = identifying_operation(arithmetic_operations, line[0])

    # Process the second word (usually a register or immediate value)
    registers, imm = getting_register_or_immediate(line[1], registers, imm)

    # Check if the command is correct (e.g., syntax check)
    checking_syntax(line[2], "e")

    # Process the third word (usually a register or immediate value)
    registers, imm = getting_register_or_immediate(line[3], registers, imm)

    # Check if the command is correct (e.g., syntax check)
    checking_syntax(line[4], "em")

    # Process the fourth word (usually a register or immediate value)
    registers = getting_register(line[5], registers, imm)

    # Return the assembly code based on the number of registers and immediate values
    if len(registers) == 2:
        return f"{opcode}I ${registers[1]}, ${registers[0]}, #{imm}"

    elif len(registers) == 3:
        return f"{opcode} ${registers[2]}, ${registers[0]}, ${registers[1]}"

    else:
        raise Exception("Erro de sintaxe desconhecido.")


def translate_memory_access(line: list) -> list:
    LINE_SIZE = 4

    # Dictionary mapping memory operation keywords to their assembly counterparts
    memory_operations = {
        "carregar": "LW",
        "salvar": "SW",
    }

    # Verify that the line has the expected size
    verify_line_size(line, LINE_SIZE)

    # Initialize lists for registers and immediate values
    registers = []
    imm = None

    # Identify the opcode (assembly operation) based on the keyword in the first word
    opcode = identifying_operation(memory_operations, line[0])

    # Process the second word (usually a register or immediate value)
    registers, imm = getting_register_or_immediate(line[1], registers, imm)

    # Check if the command is correct (e.g., syntax check)
    checking_syntax(line[2], "em")

    # Process the third word (usually a register or immediate value)
    registers = getting_register(line[3], registers, imm)

    # Return the assembly code based on the number of registers and immediate values
    if len(registers) == 1:
        return f"{opcode}I ${registers[0]}, #{imm}"

    elif len(registers) == 2:
        return f"{opcode} ${registers[1]}, ${registers[0]}"

    else:
        raise Exception("Erro de sintaxe desconhecido.")


def translate_conditional_jump(line: list) -> list:

    code = translate_jump(line[:4]).split(" ")

    if code == "":
        raise Exception("Erro de sintaxe desconhecido.")

    # Check if the command is correct (e.g., syntax check)
    checking_syntax(line[4], "se")

    registers = []
    imm = None

    # Process the fifth word (usually a register or immediate value)
    registers = getting_register(line[5], registers, imm)

    # Check if the command is correct (e.g., syntax check)
    checking_syntax(line[6], "igual")
    checking_syntax(line[7], "zero")

    return f"JZ ${registers[0]} {code[1]}"


def translate_jump(line: list) -> str:
    LINE_SIZE = 4

    if len(line) != 4:
        if len(line) == 8:
            return translate_conditional_jump(line)
        raise Exception("Erro de sintaxe desconhecido.")

    registers = []
    imm = None

    # Check if the command is correct (e.g., syntax check)
    checking_syntax(line[0], "pular")
    checking_syntax(line[1], "para")
    checking_syntax(line[2], "linha")

    # Process the fourth word (usually a register or immediate value)
    registers, imm = getting_register_or_immediate(line[3], registers, imm)

    # Return the assembly code based on the number of registers and immediate values
    if len(registers) == 0:
        return f"JI #{imm}"

    elif len(registers) == 1:
        return f"J ${registers[0]}"

    else:
        raise Exception("Erro de sintaxe desconhecido.")


def instruction_code_to_hex(code: list) -> list:

    operations = {
        "ADD": 1,
        "ADDI": 2,
        "SUB": 3,
        "SUBI": 4,
        "MULT": 5,
        "MULTI": 6,
        "AND": 7,
        "ANDI": 8,
        "OR": 9,
        "ORI": 10,
        "NOR": 11,
        "NORI": 12,
        "XOR": 13,
        "XORI": 14,
        "LW": 15,
        "LWI": 16,
        "SW": 17,
        "SWI": 18,
        "J": 19,
        "JI": 20,
        "JZ": 21,
        "JZI": 22,
    }

    memory_address = 0

    registers = {}
    new_code = []

    for line in code:
        new_line = ""
        line = line.split(" ")
        new_line += hex(operations[line[0]])
        for word in line[1:]:
            if word:
                if word[0] == '$':
                    if word not in registers:
                        registers[word] = memory_address
                        memory_address += 1
                    new_line += f' {hex(registers[word])}'
                elif word[0] == "#":
                    new_line += f' {hex(int(word[1:].rsplit(",")[0]))}'

        new_code.append(new_line)

    return new_code

def instruction_code_to_line_hex(code: list) -> list:

    opcode = {
        "ADD": 0,
        "ADDI": 1,
        "SUB": 0,
        "SUBI": 1,
        "MULT": 0,
        "MULTI": 1,
        "AND": 0,
        "ANDI": 1,
        "OR": 0,
        "ORI": 1,
        "NOR": 0,
        "NORI": 1,
        "XOR": 0,
        "XORI": 1,
        "LW": 2,
        "LWI": 3,
        "SW": 4,
        "SWI": 5,
        "JZ": 6,
        "J": 7,
    }

    aluop = {
        "ADD": 0,
        "ADDI": 0,
        "SUB": 1,
        "SUBI": 1,
        "MULT": 2,
        "MULTI": 2,
        "AND": 3,
        "ANDI": 3,
        "OR": 4,
        "ORI": 4,
        "NOR": 5,
        "NORI": 5,
        "XOR": 6,
        "XORI": 6,
        "JZ": 7,
        "LW": 0,
        "LWI": 0,
        "SW": 0,
        "SWI": 0,
        "J": 0,
    }

    memory_address = 0

    instruction_format = {
        "instruction_bit_size": 32,
        "opcode_bit_size": 3,
        "register_bit_size": 5,
        "immediate_bit_size": 16,
        "aluop_bit_size": 3
    }

    registers = {}
    new_code = []

    for i, line in enumerate(code):
        new_line = 0
        line = line.split(" ")
        if opcode.get(line[0], -1) == -1:
            raise Exception(f'Erro na linha {i}: Comando "{line[0]}" não disponível na arquitetura') 
        new_line += opcode[line[0]] ^ 2**(instruction_format["instruction_bit_size"] - instruction_format["opcode_bit_size"])
        new_line += aluop[line[0]]
        for j, word in enumerate(line[1:]):
            if word:
                if word[0] == '$':
                    if word not in registers:
                        registers[word] = memory_address
                        memory_address += 1
                    new_line += registers[word] * 2**(instruction_format["instruction_bit_size"] - instruction_format["opcode_bit_size"] - (instruction_format["register_bit_size"]*(j+1)))

                elif word[0] == "#":
                    new_line += int(word[1:].rsplit(",")[0]) * 2**(instruction_format["instruction_bit_size"] - instruction_format["opcode_bit_size"] - (instruction_format["register_bit_size"]*(j)) - instruction_format["immediate_bit_size"])


        new_code.append(hex(new_line).split("0x")[-1])

    return new_code



def translate_to_instruction_code(high_level_code: list, HEX: bool = False) -> list:

    operations = {
        "operar": translate_logical_operation,
        "adicionar": translate_arithmetic,
        "subtrair": translate_arithmetic,
        "multiplicar": translate_arithmetic,
        "carregar": translate_memory_access,
        "salvar": translate_memory_access,
        "pular": translate_jump,
    }

    translated_code = []
    for i, line in enumerate(high_level_code):
        if line:
            line = line.split(" ")
            if operations.get(line[0]):
                try:
                    translated_code.append(operations[line[0]](line))
                except Exception as e:
                    print(f"Erro na linha {i}: {e}")
                    exit(1)
            else:
                raise Exception(
                    f'Erro, comando "{line[0]}" na linha {i} não existe na lista de comandos validos'
                )
        
    return translated_code


def print_code(code: list) -> None:
    for line in code:
        print(line)


def load_code(path: str) -> list:
    code = []

    try:
        with open(path, "r") as file:
            for line in file:
                code.append(line.rsplit("\n")[0])
    except:
        raise Exception("Arquivo não pôde ser aberto.")

    return code


def input_code() -> list:
    code = []
    line = ""

    line = input()
    while line != "fim":
        code.append(line)
        line = input()

    return code


def main(args: list) -> None:
    if args.input:
        code = load_code(args.input)
    else:
        code = input_code()

    instruction_code = translate_to_instruction_code(code)

    if args.HEXADECIMAL:
        instruction_code = instruction_code_to_hex(instruction_code)

    if args.LINE_HEX:
        instruction_code = instruction_code_to_line_hex(instruction_code)



    if args.output:
        with open(args.output, "w") as file:
            for line in instruction_code:
                file.write(line + "\n")
    else:
        print("\nCodigo em linguagem de instrução\n")
        print_code(instruction_code)


if __name__ == "__main__":
    args = argparse.ArgumentParser(
        prog="Commips",
        description="Compilador de linguagem de alto nível em português para linguagem de instrução",
        epilog="",
    )
    args.add_argument(
        "-H",
        "--HEXADECIMAL",
        action="store_true",
        help="Compilar para código de máquina em hexadecimal",
    )
    args.add_argument(
        "-L",
        "--LINE-HEX",
        action="store_true",
        help="Compilar a linha de código para hexadecimal",
    )
    args.add_argument(
        "-i",
        "--input",
        help="O caminho para o arquivo com as instruções em alto nível.",
    )
    args.add_argument(
        "-o",
        "--output",
        help="O caminho para o arquivo de saída em linguagem de instrução.",
    )
    main(args.parse_args())
