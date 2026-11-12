# Boneco base 32 px, v3: como foi feito

Parte da **v1** (`COMO-FOI-FEITO.md`), não da v2. Frente e costas (quadros 1–4) são a v1 sem mudança
(0 px de diferença na folha). Só o lado (quadros 5–6) foi redesenhado. Camadas, tags, 400 ms, pivô (32, 56),
guia e as 8 cores da v1 iguais.

**O Mana Seed não foi usado como medida.** A licença da demo (`references/third_party/mana_seed/NO AI, NO
EXCEPTIONS.txt`) proíbe usar a arte junto de IA generativa, então nenhuma imagem dela foi aberta. As larguras
vêm de proporção anatômica comum (adulto, de perfil), escalada pela frente da v1.

## A escala

Frente da v1: 17 px com os braços (x24–x40), ombro a ombro ≈ 48 cm num adulto → **≈ 2,8 cm por pixel**.
Tronco sem braços na frente: 11 px (x27–x37).

| Parte (de perfil)     | Medida real (aprox.) | Esperado em px | v1  | v3   |
| --------------------- | -------------------- | -------------- | --- | ---- |
| tronco (peito–costas) | 23–26 cm             | 8–9 + contorno | 9–10, com degrau no peito | **10 (x28–x37), reto** |
| braço (braço/antebraço) | 9–11 cm            | 3–4            | 4 (x30–x33) | **4 (x31–x34)** |
| perna (coxa)          | 15–17 cm             | 5–6            | 6 (x29–x34) | 6 (x29–x34), igual |

A cabeça da v1 é ~25% maior que a real (estilo); o tronco ficou na escala real, sem esse exagero.

## O que mudou no lado

- **Frente do tronco reta**: x36 no ombro (y36) e x37 de y37 até a barra do calção (y49). Na v1 o peito saía
  para x37 só em y37–y40 e voltava para x36; esse degrau sumiu. O calção agora tem a mesma frente da camisa
  (x37), sem entrar 1 px.
- **Costas retas**: x28 do ombro (y35) até a barra (y49), sem bumbum saliente.
- **Braço centrado no tronco**: contorno de trás em x31 (era x30), miolo x32–x33, borda da frente em x34
  separada do peito só pelo tom (`#B89976` na manga, `#5A3426` na pele). Ficam 2 px de camisa atrás do braço
  (x29–x30) e 2 na frente (x35–x36), em vez de 1 e 3.
- **Mão**: y46–y48, polegar em x35 (y46) passando por cima da borda do braço; fundo da mão em x32–x34, y48.
- Cabeça, nuca, orelha, pernas e pés: iguais à v1.

*À mão:* para silhueta lisa, desenhe o contorno de frente e de costas com a **Linha** (L) segurando Shift,
de cima até a barra, **antes** de pôr o braço. Depois o braço vai por cima, com o **Lápis**.

## Respiração

Igual à v1: no quadro 6, y25–y48 desce 1 px; y50–y56 não mudam (conferido: 0 px de diferença em y50–y59).
