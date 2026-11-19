# d20 de interface v2: como foi feito

Referência de estudo, não arte final. Tela 64×64, transparente; o dado cabe na caixa 48×48 (x8–55, y8–55).
Cores: só Terra e madeira + Palha da P1 e o contorno `#1A1515`. A guia usa `#C070F0` (da P1, só porque fica oculta).

## Geometria

Hexágono T(32,8) · UR(52,18) · LR(52,45) · B(32,55) · LL(12,45) · UL(12,18). Triângulo P(32,20) · L(21,42) · R(43,42).

| Face | Cantos | Onde fica | Cor no idle |
| --- | --- | --- | --- |
| 1 | P UL T | cima-esquerda | `#B89976` (mais clara) |
| 2 | P T UR | cima-direita | `#A8703E` |
| 3 | P UL L | vizinha esquerda, **2** | `#7C5A3A` |
| 4 | L UL LL | lateral esquerda | `#B89976` |
| 5 | L LL B | baixo-esquerda | `#A8703E` |
| 6 | L B R | vizinha de baixo, **8** | `#7C5A3A` |
| 7 | R B LR | baixo-direita | `#3D261C` (mais escura) |
| 8 | R LR UR | lateral direita | `#7C5A3A` |
| 9 | P UR R | vizinha direita, **14** | `#7C5A3A` |
| frente | P L R | vazia | `#A8703E` |

## Camadas, na ordem de trabalho

Pilha no arquivo, de baixo para cima: faces → linhas → numeros → brilho → guia (oculta).

1. **guia**: a caixa 48×48. *À mão:* **Retângulo** de 1 px de (8,8) a (55,55).
2. **linhas**: as 18 linhas em `#1A1515`. *À mão:* **Lápis** de 1 px + **Shift+clique**. Desenhe só a metade
   esquerda, com cada linha saindo do canto de cima (T, P) ou de baixo (B), e espelhe com
   **Edit > Flip Horizontal** num selecionado da metade, encaixando em x=32. Assim as pontas ficam simétricas.
   Confira os degraus: bordas do hexágono 2-2-2, P→L e P→R 1:2 (dois pixels por degrau na vertical).
3. **faces**: 4 tons. *À mão:* **Balde**, contíguo, conectividade 4, "sample all layers", na camada abaixo das linhas.
   A cor da face continua por baixo das linhas, sem buraco. Isso ajuda na troca de paleta e no giro.
4. **numeros**: `#F0E2B6`, fonte 3×5 à mão (**Lápis**). "2" em (20,24), "14" em (39,24) com 1 px entre os
   dígitos, "8" em (31,44). Frente vazia.
5. **brilho**: `#D8B67A`, 5 px (**Lápis**). 3 px logo abaixo da borda T–UL em (18,16), (20,15), (22,14),
   seguindo o degrau 2:1, e 2 px na ponta do triângulo, em (32,22) e (32,23).

## Quadros

| Quadro | Tag | O que é |
| --- | --- | --- |
| 1 | `idle` | dado parado, com números e brilho |
| 2 | `spin` | 0°: igual ao 1, sem números e sem brilho |
| 3 | `spin` | 20° horário em torno de (32; 31,5) |
| 4 | `spin` | 40° horário, reduzido a 97% para não sair da caixa |

`spin` roda para a frente em laço, 80 ms por quadro.

**O que muda entre os quadros:** a luz fica parada (cima-esquerda) e a cor de cada face é recalculada pela posição
dela. Face de fora: até 60° da luz é `#B89976`, até 105° `#A8703E`, até 157° `#7C5A3A` e acima disso `#3D261C`.
Vizinhas da frente ficam em `#7C5A3A`; a frente fica sempre em `#A8703E`.

| Face | Q2 (0°) | Q3 (20°) | Q4 (40°) |
| --- | --- | --- | --- |
| 1 cima-esq. | clara | clara | média clara |
| 2 cima-dir. | média clara | média clara | média |
| 4 lat. esq. | clara | clara | clara |
| 5 baixo-esq. | média clara | média clara | média clara |
| 7 baixo-dir. | **escura** | média | média |
| 8 lat. dir. | média | **escura** | **escura** |

A face escura passa da 7 para a 8, porque a 8 desce girando para baixo à direita.

*À mão:* duplique o quadro (**Alt+D**), desenhe a guia girada, refaça as linhas com lápis + Shift e repinte com o
balde. Não use **Rotation (Ctrl+Shift+R)** no pixel pronto: o RotSprite entorta as linhas.
