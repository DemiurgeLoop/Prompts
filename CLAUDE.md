# Regras deste repositório

Biblioteca de prompts de Gustavo. Cada `.md` é um prompt completo. Leia o README para o mapa.

## Quando Gustavo pedir um prompt pelo codinome

Leia o arquivo aqui e siga-o como está escrito, com os modos, a ordem de saída e as marcas de peso. Não use versão antiga, skill nem memória no lugar do arquivo. Abra a resposta com uma linha dizendo qual arquivo e versão você usou. Se o codinome não existir, diga isso, liste os mais próximos e pergunte.

## Ao alterar um prompt

1. **Nome e versão.** `Codename vX.Y.Z - Descrição.md`. MAJOR quando muda o propósito ou a arquitetura, MINOR quando entra ou sai regra, PATCH para ajuste de texto ou de título de embutimento. Renomeie o arquivo para a nova versão e remova a antiga: só a versão atual fica no repositório.
2. **Dentro do arquivo.** Atualize o H1 (`# Nome vX.Y.Z | Descrição`) e acrescente, no topo das notas de versão do rodapé, `*Nome vX.Y.Z: o que mudou. Publicado: AAAA-MM-DD*`. A nota mais recente sempre vem primeiro.
3. **Codenames** em inglês, uma palavra, de origem erudita. Prompt novo entra no registro do Nomenclator, no índice do README e em `docs/Nomes e filosofia dos prompts.md` (o `check` falha se faltar a entrada neste último). Onde o prompt não explica o próprio nome, marque a origem como associação.
4. **Peso das regras.** Toda regra leva [INEGOCIÁVEL], [PREFERÊNCIA] ou [SUGESTÃO], na seção ou na própria regra.
5. **Estilo dentro dos prompts.** Sem travessão, sem emoji e sem parágrafo terminado em dois-pontos. O prompt é escrito do jeito que quer a saída.

## Módulos embutidos

A **Lectern** e a **Vernacular** são as fontes únicas. Gazette, Aion, Pantheon, Herodotus e Hermes embutem cópias, e o Democritus embute a Vernacular em versão fixa própria. **Nunca edite um bloco embutido à mão.**

1. Mude a fonte (e suba a versão dela).
2. Rode `python3 -I tools/sync_modules.py sync`.
3. Suba a versão de cada prompt que mudou e acrescente a nota (o título de embutimento acompanha a versão da fonte, mesmo quando o texto não mudou).
4. Rode `python3 -I tools/sync_modules.py check`. Precisa sair com 0 erros.

Quando um prompt detalha um ponto, vale o prompt naquele detalhe; no princípio, vale a Lectern.

## Antes de subir

- Rode o `check`.
- Alterações grandes vão em branch. Gustavo costuma pedir a subida direto na `main`: siga o pedido dele; sem pedido, abra branch.
- Não ponha chave, senha, token nem dado pessoal de terceiros em prompt nenhum. Número de contato de divulgação da rádio, como o do Hermes, é público e pode ficar.
