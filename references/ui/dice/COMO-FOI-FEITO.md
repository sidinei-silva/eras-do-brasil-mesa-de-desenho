# Dados de dano (d4, d6, d8, d10, d12): como foi feito

Referência de estudo, não arte final. Segue o d20 v2 (`ui_d20_v2_ref.aseprite`, nesta pasta; notas em `COMO-FOI-FEITO-d20.md`), mas na escala dos **dados de dano: 32 px** (Janela
de teste, na direção de arte). Tela 48×48, transparente; o dado cabe na caixa 32×32 (x8–39, y8–39), com a mesma
margem de 8 px do d20. Centro de giro (24; 23,5).
Cores: Terra e madeira + Palha da P1 e o contorno `#1A1515`. A guia usa `#C070F0` (oculta).

Gerados por `ui_dice_ref_gen.py` (geometria → linhas → faces → números → brilho), que grava o `.aseprite` direto.
Rodar de novo: `python3 -I ui_dice_ref_gen.py .` nesta pasta.

## Geometria (quadro idle)

| Dado | Silhueta | Frente (vazia) | Faces com número |
| --- | --- | --- | --- |
| d4 | tetraedro de lado: T(24,8) L(9,36) F(28,39) R(39,31) | T L F | direita: **3** |
| d6 | cubo oblíquo, deslocamento (8,−8) | quadrado (9,17)–(30,39) | topo **2**, lado direito **3** |
| d8 | hexágono de 6 pontas, x 11–37 | triângulo T(24,8) LL(11,31) LR(37,31) | esquerda **3**, direita **5**, baixo **7** |
| d10 | losango de 6 pontas, x 9–39 | pipa T(24,8) FL(16,23) FC(24,30) FR(32,23) | baixo-esq. **3**, baixo-dir. **7** |
| d12 | decágono r=15,5 | pentágono r=7,5 | **9** **5** / **11** **3** / **7** (as 5 vizinhas) |

## Camadas, na ordem de trabalho

Pilha no arquivo, de baixo para cima: faces → linhas → numeros → brilho → guia (oculta). Igual ao d20.

1. **guia**: a caixa 32×32. *À mão:* **Retângulo** de 1 px de (8,8) a (39,39).
2. **linhas**: as arestas em `#1A1515`, 1 px. *À mão:* **Lápis** + **Shift+clique** de vértice a vértice, sempre
   do vértice de cima para o de baixo (assim os degraus das duas metades ficam iguais). No d8, d10 e d12 desenhe só a
   metade esquerda e espelhe em x=24 (**Edit > Flip Horizontal**). O d4 e o d6 não são simétricos.
3. **faces**: **Balde**, contíguo, conectividade 4, "sample all layers". A cor da face continua por baixo da linha.
4. **numeros**: `#F0E2B6`, a mesma fonte 3×5 do d20. Cada algarismo tem 1 px de folga reta da linha (na diagonal pode
   encostar). Frente vazia: o resultado vem do código.
5. **brilho**: `#D8B67A`, 3 px logo dentro da borda de fora mais voltada para cima-esquerda, e 2 px sob o vértice de
   cima da frente (só quando cabem dentro da frente).

## Quadros

| Quadro | Tag | O que é |
| --- | --- | --- |
| 1 | `idle` | parado, com números e brilho |
| 2 | `spin` | 0°: igual ao 1, sem números e sem brilho |
| 3 | `spin` | 20° horário em torno de (24; 23,5) |
| 4 | `spin` | 40° horário, a 97% |

`spin` em laço, 80 ms por quadro. A luz fica parada e cada face é repintada pela direção dela (do centro do dado ao
centro da face) contra a luz de cima-esquerda: até 60° `#B89976`, até 105° `#A8703E`, até 157° `#7C5A3A`, acima
disso `#3D261C`. A frente fica sempre `#A8703E`.

Diferença do d20: lá as vizinhas da frente ficam fixas em `#7C5A3A`. Aqui **todas** as faces de fora seguem a regra
do ângulo, porque no d8 e no d12 todas são vizinhas da frente e o dado ficaria chapado.

*À mão:* duplique o quadro (**Alt+D**), gire os vértices na guia, refaça as linhas com lápis + Shift e repinte com o
balde. Não use **Rotation** no pixel pronto.
