# AGENTS.md

Repositório de arte do Eras do Brasil. Regras para qualquer IA aqui.

## Antes de tudo

- A direção de arte é `../eras-do-brasil/docs/direcao-de-arte.md`. Leia antes de qualquer desenho. Se não achar, pare e pergunte.
- Use só as cores da paleta P1 da direção de arte. O arquivo `palettes/eras-35.gpl` deve ter essas mesmas cores; se ele não existir ou estiver diferente da P1, avise antes de desenhar. Cor fora da paleta: pergunte antes.
- **Nenhuma IA roda `git add`, `git commit` ou `git push`.** Quem commita sou eu.

## Autoria (decidir: A, B ou C)

- Até eu decidir a regra de autoria, **tudo que a IA gera vai para `references/`**.
- Só eu movo um arquivo para `source/` e `exports/`. Mover para lá é a minha aprovação.

## MCP do Aseprite

- O MCP está em `.mcp.json` (escopo do projeto). Ele não existe nos outros repos, de propósito.
- Use só as ferramentas de desenho, camada, quadro, paleta e exportação.
- **Nunca use a execução de Lua livre** (ela roda código no meu computador).
- Salve sempre dentro da pasta pedida. Nada fora deste repo.

## Como entregar

- Camadas com nome (por exemplo: `guia`, `sombra`, `pele`, `roupa`, `linhas`, `brilho`). A camada `guia` fica oculta no fim.
- Tags de animação com nome (`idle_down`, `walk_side`, `attack_up`, `spin`).
- Exporte: o `.aseprite`, a sprite sheet `.png` sem ampliar (uma linha por direção), e uma prévia ×8 para eu revisar.
- Junto, um `COMO-FOI-FEITO.md` curto: a ordem das camadas, a ferramenta que eu usaria à mão e o que muda entre os quadros.
- Na resposta: o que ficou ruim e por quê.

## Nomes

- Pastas e arquivos em inglês, minúsculos, com underscore e o tier no fim: `equip_weapon_sword_t2.aseprite`.
- Referência leva `_ref`: `ui_d20_ref.aseprite`.

## Regras de arte (resumo; a fonte é a direção de arte)

- Tiles de 16 px.
- Boneco com ~32 px de altura, cabeça com ~25–30% da altura (proporção adulta, nada de chibi).
- Quadro do boneco de 64×64, pivô nos pés (x=32, y=56), igual em todos os quadros e direções.
- 4 direções (3 desenhadas + espelho). Até 8 cores por personagem.
- Luz de cima à esquerda; quanto mais embaixo e à direita, mais escuro.
- Contorno preto (`#1A1515`) em boneco e item; cenário sem contorno.
- Tier muda cor e acabamento, nunca tamanho nem silhueta.
- Referências: Calamity para mundo e câmera; Mana Seed para o boneco (escala, camadas e troca de paleta).

## Commits

Formato `tipo(escopo): descrição`, em português, imperativo, minúsculo, sem ponto final.
Tipos: `feat`, `fix`, `chore`, `docs`. Escopos: `ui`, `characters`, `equipment`, `environment`, `creatures`, `palettes`, `references`, `repo`.
Exemplo: `feat(ui): adiciona d20 de interface com giro em 3 quadros`