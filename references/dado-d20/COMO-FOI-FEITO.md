# d20 de interface: como foi feito

Referência de estudo, não arte final. Tela 64×64, fundo transparente, paleta Terra e madeira + Palha (P1).

## Nomes usados aqui

Cantos do hexágono: **B** (32,4) topo · **C** (56,16) · **F** (56,47) · **E** (32,59) base · **D** (8,47) · **A** (8,16).
Triângulo da frente: **P** (32,18) ponta · **L** (19,44) esquerdo · **R** (45,44) direito.

Faces (numeração usada abaixo):

| # | Cantos | Onde fica | Cor no quadro 1 |
| --- | --- | --- | --- |
| 1 | P A B | cima-esquerda | clara `#B89976` |
| 2 | P B C | cima-direita | média clara `#A8703E` |
| 3 | P A L | vizinha esquerda (**2**) | média clara `#A8703E` |
| 4 | L A D | lateral esquerda | clara `#B89976` |
| 5 | L D E | baixo-esquerda | média `#7C5A3A` |
| 6 | L E R | vizinha de baixo (**8**) | escura `#3D261C` |
| 7 | R E F | baixo-direita | escura `#3D261C` |
| 8 | R F C | lateral direita | média `#7C5A3A` |
| 9 | P C R | vizinha direita (**14**) | escura `#3D261C` |
| T | P L R | frente (vazia) | média `#7C5A3A` |

## Camadas, na ordem de trabalho

Pilha no arquivo, de baixo para cima: faces → linhas → numeros → brilho → guia (oculta).

1. **guia** (no arquivo fica no topo, oculta). Linhas da geometria em magenta `#FF00FF`.
   *À mão:* **Lápis** de 1 px, clique no ponto inicial e **Shift+clique** no final (linha reta). Faça as 6 bordas
   do hexágono, depois as 3 do triângulo, depois as 9 arestas. Deixe a camada com ~50% de opacidade enquanto trabalha.
2. **linhas**: as mesmas 18 linhas, agora em `#1A1515`, 1 px.
   *À mão:* lápis + **Shift** de novo, por cima da guia. Nas diagonais 2:1 (bordas do hexágono, P→L, P→R) confira se
   os degraus são todos de 2 px. Nos cantos onde 3–4 linhas se encontram (A, C, L, R) vão sobrar "bolos" de pixel:
   limpe com a **Borracha** até ficar uma junção de 1 px.
3. **faces**: 4 tons, um por face.
   *À mão:* **Balde** com **"Sample: All Layers"** (ou "sample all layers") e **contiguous** ligado, pixel connectivity
   de 4. Pinte na camada `faces` (que fica abaixo de `linhas`): o balde enxerga as linhas pretas e para nelas.
   Clique uma vez em cada face. Perto dos cantos A, C e L
   aparecem pedacinhos de face isolados pelas linhas (o quadro 1 tem 12 regiões para 10 faces): eles levam um clique cada.
4. **numeros**: `#F0E2B6`, fonte 3×5 desenhada à mão.
   *À mão:* **Lápis** de 1 px. "2" em (18,24), "14" em (41,24) (1 px de espaço entre os dígitos), "8" em (31,46).
   O triângulo T fica vazio: o resultado entra por cima no motor.
5. **brilho**: `#D8B67A`, 5 pixels.
   *À mão:* **Lápis**. 3 pixels logo abaixo da borda A–B, em (15,14), (17,13), (19,12), seguindo o degrau 2:1, e
   2 pixels na ponta do triângulo, em (32,20) e (32,21).

## Luz

Vem de cima à esquerda. A regra puramente por posição deixava T igual a três vizinhas (5, 6, 9). No quadro 1, troquei
para manter **T diferente das três vizinhas** e **os números em faces escuras** (contraste com o creme):
6 e 9 viram escuras, e 4 sobe para clara.

## Giro (quadros 2–4, tag `spin`, 80 ms, em laço)

Todo o dado gira em torno do centro (32; 31,5), no sentido horário: 0°, 20°, 40°. Sem números e sem brilho.
As cores **não** acompanham as faces: são recalculadas pela posição de cada face em relação à luz, que fica parada.
Por isso a cor clara "escorrega".

| Face | Q1 (parado) | Q2 (0°) | Q3 (20°) | Q4 (40°) |
| --- | --- | --- | --- | --- |
| 1 cima-esq. | clara | **clara** | média clara | média clara |
| 2 cima-dir. | média clara | média clara | média | média |
| 3 viz. esq. | média clara | média clara | média clara | média clara |
| 4 lat. esq. | clara | média clara | **clara** | **clara** |
| 5 baixo-esq. | média | média | média clara | média clara |
| 6 viz. baixo | escura | média | média | média |
| 7 baixo-dir. | escura | escura | escura | escura |
| 8 lat. dir. | média | escura | escura | escura |
| 9 viz. dir. | escura | média | média | média |
| T frente | média | média | média | média |

Leitura: do Q2 para o Q3 a clara pula da face 1 (topo) para a face 4 (lateral esquerda), que subiu girando até o
lado da luz. Do Q3 para o Q4 a atribuição é a mesma, mas as faces já estão 20° adiante, então a mancha clara anda
junto com o dado.

*À mão:* duplique o quadro (**Alt+D** / New Frame), desenhe a guia girada, refaça as linhas com lápis + Shift
e repinte com o balde. Não gire com **Rotation (Ctrl+Shift+R)** em cima do pixel pronto: o RotSprite entorta as linhas.
