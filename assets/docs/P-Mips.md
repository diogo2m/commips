# Sintaxe da linguagem

## Operações lógicas:

**Formato de comandos:**
1. operar registrador1 `<operação>` registrador2 em registrador3
2. operar registrador1 `<operação>` imm em registrador3
3. operar imm `<operação>` registrador1 em registrador3

**Operação:** e, ou, nor, xor

**Tabela em comandos Assembly:**
| NOME  | PARÂMETROS        | DESCRIÇÃO                  | OPERAÇÃO               |
| ----- | ----------------- | -------------------------- | ---------------------- |
| NOR   | rd,rs,rt          | Nor                        | rd=~(rs\|rt)           |
| NORI  | rd,rs,imm         | Nor imediato               | rd=~(rs\|imm)          |
| AND   | rd,rs,rt          | E                          | rd=rs&rt               |
| ANDI  | rd,rs,imm         | E imediato                 | rd=rs&imm              |
| OR    | rd,rs,rt          | Ou                         | rd=rs rt               |
| ORI   | rt,rs,imm         | Ou imediato                | rt=rs imm              |
| XOR   | rd,rs,rt          | Ou exclusivo               | rd=rs^rt               |
| XORI  | rt,rs,imm         | Ou exclusivo imediato      | rt=rs^imm              |



<hr>

## Operações aritméticas:

**Formato de comandos:**
1. `<operação>` registrador1 e registrador2 em registrador3
2. `<operação>` registrador1 e imm em registrador3
3. `<operação>` imm e registrador1 em registrador3

**Operação:** adicionar, subtrair, multiplicar

**Tabela em comandos Assembly:**
| NOME  | PARÂMETROS        | DESCRIÇÃO                  | OPERAÇÃO               |
| ----- | ----------------- | -------------------------- | ---------------------- |
| ADD   | rd,rs,rt          | Adicionar                  | rd=rs+rt               |
| ADDI  | rd,rs,imm         | Adicionar imediato         | rd=rs+imm              |
| SUB   | rd,rs,rt          | Subtrair                   | rd=rs-rt               |
| SUBI  | rd,rs,rt          | Subtrair imediato          | rd=rs-imm              |
| MULT  | rs,rt,rd          | Multiplicar                | rd=rs*rt               |
| MULTI | rs,imm,rd         | Multiplicar imediato       | rd=rs*imm              |



<hr>

## Saltos

### Saltos não-condicionais
1. pular para linha registrador1
2. pular para linha imm

**Tabela em comandos Assembly:**
| NOME  | PARÂMETROS        | DESCRIÇÃO                  | OPERAÇÃO               |
| ----- | ----------------- | -------------------------- | ---------------------- |
| J     | offset(rs)        | Salto                      | pc=pc_upper(rs<<2)     |
| JI    | offset(imm)       | Salto imediato             | pc=pc_upper(imm<<2)    |



<hr>

### Salto condicional
1. pular para linha reg1 se reg2 igual zero
2. pular para linha imm se registrador1 igual zero

**Tabela em comandos Assembly:**
| NOME  | PARÂMETROS        | DESCRIÇÃO                  | OPERAÇÃO               |
| ----- | ----------------- | -------------------------- | ---------------------- |
| JZ    | offset(rs),rt     | Salto condicional          | if(rt==0) pc+=offset*4 |
| JZI   | offset(imm),rt    | Salto condicional imediato | if(rt==0) pc+=offset*4 |



<hr>

## Acesso de memória

### Carregar

**Formato de comandos:**
1. carregar registrador1 em registrador3
2. carregar imm em registrador3
3. carregar registrador1[imm] em registrador3
4. carregar registrador1[registrador2] em registrador3

**Tabela em comandos Assembly:**
| NOME  | PARÂMETROS        | DESCRIÇÃO                  | OPERAÇÃO               |
| ----- | ----------------- | -------------------------- | ---------------------- |
| LW    | rt,offset(rs),rd  | Carregar palavra           | rt=mem(offset+rd)      |
| LWI   | rt,offset(rs),imm | Carregar palavra imediato  | rt=mem(offset+imm)     |
| SW    | rt,offset(rs),rd  | Salvar palavra             | mem(offset+rd)=rt      |
| SWI   | rt,offset(rs),imm | Salvar palavra imediato    | mem(offset+imm)=rt     |



<hr>

## Salvar

**Formato de comandos:**
1. salvar registrador1 em registrador3
2. salvar imm em registrador3
3. salvar registrador1 em registrador3[imm]
4. salvar registrador1 em registrador3[registrador3]

**Tabela em comandos Assembly:**
| NOME  | PARÂMETROS        | DESCRIÇÃO                  | OPERAÇÃO               |
| ----- | ----------------- | -------------------------- | ---------------------- |
| SW    | rt,offset(rs),rd  | Salvar palavra             | mem(offset+rd)=rt      |
| SWI   | rt,offset(rs),imm | Salvar palavra imediato    | mem(offset+imm)=rt     |

