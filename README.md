# Prompts

Biblioteca de prompts de sistema de Gustavo: cada arquivo `.md` é um prompt completo, escrito para ser colado ou lido por um modelo. Os da Mundo Livre FM ficam na pasta `Mundo Livre FM/`; os demais, na raiz.

O nome do arquivo carrega a versão: `Codename vX.Y.Z - Descrição.md`. Só existe uma versão de cada prompt, a atual; o histórico fica no git e na nota de versão no rodapé de cada arquivo.

Para fixar o nome e a ideia de cada prompt, leia `docs/Nomes e filosofia dos prompts.md`.

## Como os prompts se organizam

- **Módulos.** A **Lectern** (leitor, tom, vitrine e busca) e a **Vernacular** (prosa em português do Brasil) são a fonte única do que vale para todo texto da Mundo Livre FM. Os prompts de escrita embutem uma cópia delas, sem editar uma vírgula. Quem muda é a fonte; as cópias são regravadas por `tools/sync_modules.py`.
- **Peso das regras.** Todo prompt marca suas regras como **[INEGOCIÁVEL]**, **[PREFERÊNCIA]** ou **[SUGESTÃO]**.
- **Codenames.** Nomes eruditos em inglês, uma palavra. O registro dos nomes ocupados e dos aposentados está no Nomenclator.

## Índice

### Mundo Livre FM

| Prompt | Para que serve |
|---|---|
| Lectern | Módulo: leitor, tons (Conteúdo e Sóbrio), vitrine, busca e Distribuição com UTM |
| Gazette | Notícia de fato novo |
| Aion | História de obra evergreen |
| Pantheon | Listas, rankings e tier lists |
| Herodotus | Entrevista gravada vira matéria |
| Hermes | Texto promocional (voz da rádio) |
| Sonar | Radar diário de notícias e tendências |
| Humboldt | Preparação e roteiro de entrevistas |
| Galen | Post-mortem de matéria publicada e receita de matéria que foi bem |
| Sphinx | Quiz a partir de uma matéria |
| Laureate | Seção de ganhadores das promoções |
| Occam | Refinador dos prompts da Mundo Livre |

### Escrita, ensaio e vídeo

| Prompt | Para que serve |
|---|---|
| Vernacular | Módulo e editora de texto em português do Brasil |
| Recension | Remaster de ensaios |
| Rhapsode | Ensaio vira roteiro de vídeo-ensaio |
| Aphex | Edição do vídeo-ensaio, da voz ao vídeo renderizado |
| Aristarchus | Análise de ensaios |
| Sherlock | Análise de uma ideia, no método holmesiano |
| Vulgate | Tradução para português brasileiro |

### YouTube e criação de conteúdo

| Prompt | Para que serve |
|---|---|
| Haruspex | Rank de ideia de vídeo, de 0 a 10, contra a régua do canal |
| Exordium | Seis hooks de duas linhas para post ou vídeo |
| Assayer | Nota de 0 a 50 para um rascunho de post |

### Estudo, leitura e acervo

| Prompt | Para que serve |
|---|---|
| Thoth | Guias 101 (Personal Curriculum) |
| Photius | Curador particular: o que vale o seu tempo |
| Vasari | Curadoria de obras-primas |
| Buddhaghosa | Inspeção e resumo de leitura |
| Arrian | Transcrição integral e fiel, com veredito e pathway |
| Callimachus | Bibliotecário do acervo de livros |

### Wizard's Garden (Obsidian)

| Prompt | Para que serve |
|---|---|
| Democritus | Notas atômicas de Zettelkasten |
| Ariadne | Índices e pathways da vault |
| Stobaeus | Clippings do e-reader para notas de leitura |

### Música

| Prompt | Para que serve |
|---|---|
| Orpheus | Acha a playlist certa de cada álbum no YouTube |
| Odysseus | Baixa e organiza a biblioteca musical (yt-dlp) |

### Manutenção

| Prompt | Para que serve |
|---|---|
| Socrates | Auditoria e lapidação de qualquer prompt |
| Nomenclator | Codenames e registro de nomes |
| Lethe | Limpeza de chats antigos do Claude Code |

## Fluxos

- **Notícia:** Sonar, Gazette, publicação, Distribuição da Lectern (links com UTM), Galen.
- **Entrevista:** Humboldt, gravação, Herodotus.
- **Vídeo-ensaio:** Recension, Rhapsode, gravação, Aphex.
- **YouTube:** Haruspex, Exordium, vídeo, Assayer.
- **Estudo:** Photius, Thoth, Callimachus, Buddhaghosa e Arrian, Democritus, Ariadne.
- **Música:** Orpheus, Odysseus.

## Ferramenta

```
python3 -I tools/sync_modules.py check   # confere as cópias embutidas, os nomes e as versões
python3 -I tools/sync_modules.py sync    # regrava as cópias embutidas a partir da Lectern e da Vernacular
```

Depois do `sync`, suba a versão de cada prompt alterado e acrescente a nota de versão.
