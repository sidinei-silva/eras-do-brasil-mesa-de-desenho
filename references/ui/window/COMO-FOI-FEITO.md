# Kit da janela de teste (UI): como foi feito

Referência de estudo, não arte final. Só cores da P1. Nenhum texto desenhado: todo texto entra como fonte no motor.
A camada `guia` (em `#C070F0`, oculta) marca a área esticável. Cada 9-slice e 3-slice tem também uma **slice** do
Aseprite com o nome da peça.

Cores usadas: contorno `#1A1515` · madeira `#3D261C` `#7C5A3A` (e `#A8703E` só no hover do botão) · dourado `#D8B67A`,
com brilho `#F0E2B6` · miolo `#26262F` · folhas `#223C34` `#3D7A3C` · espada: metal `#DADDD6` `#7F8896`.

## O que o motor precisa saber

Bordas em px, na ordem **esquerda, cima, direita, baixo** (o padrão de 9-patch do Godot e o `border` do Unity, que é
L, B, R, T no Inspector).

| Peça | Tamanho | Bordas fixas (E, C, D, B) | Estica | Observação |
| --- | --- | --- | --- | --- |
| `panel_9slice` | 32×32 | 8, 8, 8, 8 | miolo 16×16 em (8,8); bordas nos 2 eixos | slice `panel` com centro em (8,8,16,16) |
| `title_plate_3slice` | 48×16 | 8, 0, 8, 0 | só na horizontal, colunas 8–39 | altura fixa de 16 |
| `status_bar_3slice` | 48×12 | 8, 0, 8, 0 | só na horizontal, colunas 8–39 | área de texto: y 3–8 (6 px), entre x 5 e 42 |
| `divider_3slice` | 32×5 | ver abaixo | **as pontas**, não o centro | 5 partes |
| `button_3slice` | 48×14 ×3 quadros | 8, 0, 8, 0 | só na horizontal, colunas 8–39 | quadros na folha: x 0 / 48 / 96 |
| `ornament_top` | 32×16 | — | não estica | fica sobre a placa |
| `ornament_corner` | 16×16 | — | não estica | o motor espelha para os outros cantos |
| `icon_sword` | 16×16 | — | não estica | — |

**Divisória (`divider_3slice`), atenção:** ela não é um 3-slice comum. São 5 partes, da esquerda para a direita:

| Colunas | Largura | Parte | Estica? |
| --- | --- | --- | --- |
| 0 | 1 | tampa esquerda | não |
| 1–12 | 12 | linha esquerda | **sim** |
| 13–18 | 6 | losango | **não** |
| 19–30 | 12 | linha direita | **sim** |
| 31 | 1 | tampa direita | não |

As duas linhas esticam por igual, para o losango ficar no centro. Se a largura final for ímpar, sobra 1 px num lado.
No Godot isso vira 3 nós (2 `NinePatchRect` + 1 `TextureRect`); no Unity, 2 sprites 3-slice e 1 sprite simples. Ou
então desenhe a linha como 3-slice simples (1, 0, 1, 0) e ponha o losango por cima, centrado.

**Botão:** `idle` = quadro 1, `hover` = 2, `pressed` = 3 (tags no `.aseprite`; `ui_window_button_3slice_ref.json` traz
os retângulos e as tags). O texto sobe e desce junto: no `idle` e no `hover` a face vai de y 2 a 9; no `pressed`, de y 3 a 10.
O motor desce o rótulo 1 px no `pressed`.

## Como manter as bordas esticáveis

- Toda coluna da área esticável de um 3-slice é **idêntica**. No painel, toda linha da borda de cima é igual à de baixo
  dela ao longo do comprimento, e o mesmo vale para as colunas das bordas laterais. Só faixas paralelas à borda, nada
  atravessado.
- Enfeite (cravo, placa dourada, folha) **só** dentro dos 8 px das pontas ou dos cantos.
- Teste: cole a área esticável repetida 3× ao lado de si mesma. Se aparecer uma emenda, há enfeite no meio.
- À mão: desenhe 1 coluna (ou 1 linha) do perfil, selecione, **Ctrl+C** e cole repetindo, ou estique a seleção com
  **Ctrl+T** em modo *Nearest*. Assim fica garantido que é tudo igual.
- No motor: filtro Point/Nearest e modo de esticar **Stretch** (ou **Tile**, dá no mesmo porque o perfil é igual).

## Peças, camadas e ferramenta à mão

Ordem das camadas no arquivo, de baixo para cima.

1. **panel_9slice** — `miolo` → `madeira` → `dourado` → `contorno` → `guia`.
   Perfil da borda, de fora para dentro: em cima e à esquerda (lado da luz) `K W W D G D D K`; embaixo e à direita
   (lado da sombra) `K D D D G D W K`. O filete dourado fica sempre a 4 px da borda de fora. A borda interna de baixo e a
   da direita têm 1 px claro, porque recebem a luz que entra pela abertura. Cantos: placa dourada 8×8 com brilho em cima
   à esquerda, sombra embaixo à direita e um cravo preto 2×2 no meio. As 4 placas são iguais, porque a luz é global.
   *À mão:* **Retângulo** de 1 px para cada faixa, **Balde** no miolo, **Lápis** na placa de um canto, e copie a placa
   para os outros 3.
2. **title_plate_3slice** — `madeira` → `dourado` → `contorno` → `guia`. Moldura dourada de 2 px, contorno interno e
   tábua escura `#3D261C` para o título claro (`#F0E2B6`) ler bem. Pontas com cantos cortados, faixa dourada vertical
   (clara à esquerda, `#7C5A3A` à direita) e um cravo 2×2.
3. **status_bar_3slice** — `miolo` → `madeira` → `dourado` → `contorno` → `guia`. Faixa de miolo de 6 px entre 2
   réguas de madeira; pontas em bico, com tampa dourada.
4. **divider_3slice** — `madeira` → `dourado` → `contorno` → `guia`. Linha dourada de 1 px com contorno e um losango
   de 6×5 no centro.
5. **button_3slice** — `madeira` → `dourado` → `contorno` → `guia`; 3 quadros.
   - `idle`: aro dourado em cima e à esquerda, face `#7C5A3A`, sombra de 1 px à direita, base `#3D261C` de 2 px.
   - `hover`: um tom acima em tudo (face `#A8703E`, aro `#F0E2B6`, sombra `#7C5A3A`).
   - `pressed`: tudo 1 px abaixo, face `#3D261C`, aro `#7C5A3A`, base de 1 px. A borda de baixo não se mexe.
   *À mão:* desenhe o `idle`, **Alt+D** para duplicar e use **Shift+R** (trocar cor) para o `hover`. Para o
   `pressed`, duplique, selecione tudo acima da base e mova 1 px para baixo com a seta.
6. **ornament_top** — `folhas` → `dourado` → `contorno`. Meio sol nascendo de trás da placa (as 2 linhas de baixo
   ficam escondidas), 3 raios e uma folha de cada lado. Desenhe a metade esquerda, espelhe com
   **Edit > Flip Horizontal** e repinte o lado direito com a sombra (`#7C5A3A` na beira).
7. **ornament_corner** — `folhas` → `dourado` → `contorno`. Uma folha horizontal e uma vertical (a vertical é a
   horizontal transposta: rode 90° com **Ctrl+Shift+R** e espelhe), e um nó dourado no canto.
8. **icon_sword** — `cabo` → `lamina` → `guarda` → `contorno`. Espada em pé: lâmina de 2 px (clara à esquerda),
   guarda dourada, cabo de madeira e pomo. *À mão:* **Lápis** de 1 px, coluna por coluna.

## Prévia (montagem da cena)

Duas versões, ambas 176×212 e também em ×3. As peças são as mesmas; só muda o miolo do painel:

- `ui_window_mock_ref`: miolo `#26262F`.
- `ui_window_mock_warm_ref`: miolo `#1A1515` (a faixa de estado continua com o miolo `#26262F` dela, porque é a peça).

Foi montada esticando os PNG exportados com os cortes acima, como o motor faria. A camada `guia_texto` (contorno
`#C070F0` de 1 px, visível) marca a caixa de 12 px das linhas da arma e do resultado. A camada `texto_amostra` traz
textos de exemplo na fonte real, só para revisão (no jogo, todo texto é fonte).

### Fonte

**monogram extended**, tamanho 16 (`eras-do-brasil/client/assets/fonts/monogram-extended.ttf`), cor `#F0E2B6`.

- Letra com ~6 px de avanço; maiúscula com 7 px; descendente de 2 px; acento ocupa até 2 px acima da maiúscula.
- Linha de texto (Label) com **12 px** de altura. Dentro dela: maiúscula nas linhas 3–9, linha de base na 10.
- "Teste de Coleta" (o título mais longo previsto) mede **89 px** de tinta.
- Largura útil em caracteres: arma 76 px ≈ 12; resultado 80 px ≈ 13; faixa 118 px ≈ 19.

**Regra de espaçamento:** 4 px entre cada bloco e 4 px entre o primeiro e o último bloco e a borda interna do painel.
A linha da arma conta como um bloco de 16 px (a altura do ícone), com o texto de 12 px centrado nela.
Área útil do painel (dentro das bordas de 8 px): x 16–159, y 30–182 (144×153).

Coordenadas em px da prévia, origem no canto de cima à esquerda (x, y = canto de cima à esquerda do bloco). Para usar
como filho do painel na Godot, subtraia a origem do painel: **x − 8, y − 22**.

| # | Bloco | Peça / nó | x | y | Larg. | Alt. | Obs. |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | painel | `panel_9slice` (NinePatchRect, bordas 8/8/8/8) | 8 | 22 | 160 | 169 | era 160×157: **+12 de altura**, largura igual |
| — | ornamento | `ornament_top` | 72 | 0 | 32 | 16 | atrás da placa; as 2 linhas de baixo ficam cobertas |
| 1 | placa do título | `title_plate_3slice` (bordas 8/0/8/0) | 35 | 14 | 105 | 16 | era 80: **+25**; 89 do texto + 8 de cada lado |
| 1 | **texto título** | Label | 43 | 16 | 89 | 12 | maiúscula em y 19–25, na tábua escura |
| — | cantos | `ornament_corner` | 8 / 152 | 22 / 175 | 16 | 16 | TR espelhado em H, BL em V, BR nos dois |
| 2 | ícone da arma | `icon_sword` | 40 | 34 | 16 | 16 | define a altura do bloco 2 |
| 2 | **texto arma** | Label | 60 | 36 | 76 | 12 | 4 px depois do ícone; grupo ícone+texto (x 40–135) centrado |
| 3 | d20 | `ui_d20_v2_ref` (tela 64×64) | 56 | 46 | 64 | 64 | dado visível: x 64, y 54, 48×48 |
| 4 | **texto resultado** | Label | 48 | 106 | 80 | 12 | centrado |
| 5 | divisória | `divider_3slice` (5 partes) | 24 | 122 | 128 | 5 | trechos esticados de 60 px cada; losango em x 85–90 |
| 6 | dano 1 | quadrado vazio | 32 | 131 | 32 | 32 | marcação `#4B4A55`, não é peça |
| 6 | dano 2 | quadrado vazio | 72 | 131 | 32 | 32 | 8 px entre quadrados |
| 6 | dano 3 | quadrado vazio | 112 | 131 | 32 | 32 | |
| 7 | faixa de estado | `status_bar_3slice` (bordas 8/0/8/0) | 24 | 167 | 128 | 12 | — |
| 7 | **texto faixa** | Label | 29 | 167 | 118 | 12 | mesma altura da faixa; maiúscula em y 170–176 (ver abaixo) |
| — | botão | `button_3slice` (bordas 8/0/8/0) | 56 | 195 | 64 | 14 | fora do painel, 4 px abaixo dele |

Vertical, de cima para baixo: borda interna 29 → 4 → arma 34–49 → 4 → d20 54–101 → 4 → resultado 106–117 → 4 →
divisória 122–126 → 4 → dano 131–162 → 4 → faixa 167–178 → 4 → borda interna 183.

De onde vêm os +12 de altura: +4 da linha do resultado (8 → 12), +4 da linha da arma (8 → 12) e +4 porque o ícone de
16 px agora conta como o bloco (antes ele encostava na borda interna, sem os 4 px).

**Atenção, faixa de estado:** a área de texto da peça tem 6 px (y 3–8) e a maiúscula da fonte tem 7. A linha de baixo
da letra cai sobre a régua de baixo da faixa (y 176). Acento (Ã, É) sobe 2 px e encosta na régua de cima. Sem mexer na
peça não cabe (até minúscula com haste, como `l` e `d`, tem 7 px); a faixa precisa de uma área de texto de 9 px para
caber maiúscula com acento (peça de 15 px).

`ui_window_kit_sheet_ref_x6.png` mostra todas as peças lado a lado, sobre fundo `#7B7880` só para a revisão.
