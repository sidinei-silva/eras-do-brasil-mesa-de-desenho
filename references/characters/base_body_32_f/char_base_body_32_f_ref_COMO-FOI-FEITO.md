# Boneco base 32 px, feminino (f): como foi feito

Cópia do `char_base_body_32_v3_ref.aseprite` com pixels **só removidos ou recoloridos**, nunca acrescentados para
fora. Camadas (`sombra`, `pele`, `roupa`, `linhas`, `brilho`, `guia` oculta), tags (`idle_down`, `idle_up`,
`idle_side`), 6 quadros de 400 ms, pivô (32, 56) e as linhas da guia (topo y25, queixo y34, ombro y36,
cintura y44, joelho y51, chão y56) iguais à v3.

Coordenadas abaixo são do quadro 1, 3 e 5. Nos quadros 2, 4 e 6 (respiração) tudo de y25 a y48 está 1 px abaixo,
como na v3.

## Ordem das camadas (de baixo para cima)

`sombra` → `pele` → `roupa` → `linhas` → `brilho` → `guia` (oculta). Atenção: `brilho` fica **acima** das
linhas, então um brilho que caia em cima do contorno aparece por cima dele. Por isso o brilho do ombro mudou de lugar.

## O que mudou

**Frente e costas (quadros 1–4)**

- Ombros: o contorno da curva do ombro entrou 1 px dos dois lados em 3 linhas. Fica uma diagonal 1-1-1
  (x27 → x26 → x25 → x24 da esquerda; x37 → x38 → x39 → x40 da direita), em vez da v3 (x26 → x25 → x24).
  O braço, de y38 para baixo, não mudou.
- Brilho da camisa no ombro: de x26 para x28 em y36 (o x26 virou contorno).
- Cintura: x28 e x36 viram contorno em y42–y44. Na frente e nas costas a cintura fica escondida pelo braço,
  então isso aparece como o contorno de dentro do braço mais grosso, não como mudança de silhueta.
- Quadril (y45–y49), pernas e pés: iguais.

**Só frente (quadros 1–2)**

- Queixo: mandíbula em diagonal (x27 → x28 em y32, x29 em y33, x30 em y34; espelhado na direita). Saem do corpo
  x28 e x36 em y33 e x29 e x35 em y34.
- Sobrancelha de 1 px em `#5A3426`, y29: x29–x30 e x34–x35. Olhos iguais à v3.

**Lado (quadros 5–6)**

- Queixo: a ponta recua 1 px (contorno em x35, y33; x36 em y32 vira contorno). Sai do corpo: x36 y33 e x35 y34.
- Sobrancelha: x34–x35, y29.
- Peito: 1 px de `#B89976` em x35, y39 (sombra embaixo do peito). Contorno da frente, das costas e do quadril igual.

**Cor (todos os quadros)**

- Sombra do calção: `#5A3426` (sombra da pele) → `#3D261C` (terra e madeira). Agora o calção não divide tom com a pele.

## À mão

- Ombros e queixo: **Borracha** (E) de 1 px nos cantos e **Lápis** (B) com `#1A1515` para fechar o contorno 1 px
  para dentro. Confira com a **Varinha** (W) na camada `linhas` que o contorno da cabeça ficou fechado.
- Sombra do calção: **Substituir cor** (Shift+R) só na camada `roupa`, em todos os quadros.
- Respiração: faça no quadro 1 e repita no 2 com 1 px a menos em y (ou copie o quadro e desça y25–y48 com a
  **Seleção** + setas).

## O que muda entre os quadros

Igual à v3: no quadro par, y25–y48 desce 1 px; y50–y56 não mudam.
