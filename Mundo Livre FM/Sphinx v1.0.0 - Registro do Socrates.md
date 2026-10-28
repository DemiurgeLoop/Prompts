# Sphinx v1.0.0: registro do Socrates (CONGELAR)

Fora do prompt. Não colar no Sphinx.

## Intenção confirmada (3 linhas)

- **Produz** um quiz de conhecimento de 5 a 10 perguntas, com explicações e fonte, a partir de uma matéria já apurada da casa.
- **Para** o ouvinte da Mundo Livre FM (30 a 60 anos, no celular), a partir de um post do site ou de um link nas redes.
- **Sucesso**: o quiz sustenta o clique, o leitor termina com vontade de ler a matéria, e nenhuma pergunta nasce de fato sem fonte. **Fora**: quiz de personalidade, enquete de opinião, tema que a Lectern veta na Curiosidade.

## Modo e nota

Modo **CONGELAR** de um prompt novo, a partir de uma prática que funcionou (o quiz do Eddie). A nota abaixo é simulação, não medição: nenhuma saída real do Sphinx existe ainda.

| Critério | Nota | Justificativa |
|---|---|---|
| Fidelidade à intenção | 3 | Cada seção serve ao quiz de conhecimento com fonte; o escopo corta o que fugiria. |
| Clareza operacional | 2 | "Resultado" e "chamadas" deixam margem de gosto; o resto tem uma leitura só. |
| Coerência interna | 3 | Sem resíduo, sem nome de modo antigo; versões batem (Lectern v1.6.0, Vernacular v4.1.1). |
| Economia | 2 | A regra 8 (não pagar a lacuna do card) pode ser cortada se o quiz de teste não a violar. |
| Robustez | 2 | Cobre ausência de Ficha, escopo recusado e fonte única; ainda não cobre matéria com menos de 5 fatos apurados. |
| Foco no destinatário | 3 | O ouvinte de 50 anos é o critério da pergunta, da explicação e do resultado. |
| Contágio | 3 | Sem travessão, sem bacharelês, sem enchimento. |
| **Total** | **18/21** | Para comparar versões, não para perseguir. |

## Hipóteses falsificáveis

1. "Exigir a Ficha de apuração deve reduzir perguntas de fonte única, medido pelo número de perguntas marcadas na Ficha do quiz."
2. "Variar a posição da certa deve baixar o acerto por chute, medido pela distribuição das respostas em `eddie-quiz-answer`."
3. "Fixar o template e trocar só o bloco de dados deve eliminar regressões visuais, medido pelo número de arquivos que precisam de retoque manual."
4. "Duas chamadas com gatilhos diferentes devem ensinar qual convida mais, medido por `utm_term` a e b no GA4."

## Ablação (o que quase saiu)

- **Regra 8** (o quiz não paga a lacuna do card): nada mais a cobre, mas não sei se muda a saída. Marcada [PREFERÊNCIA] e candidata a corte se o conjunto de teste passar sem ela.
- **Linha do dia como seção própria**: mantida, porque a pergunta presa à data envelhece e o prompt precisa dizer o que apagar.

## Registro de rejeitadas

- **Quiz de personalidade ("qual [banda] você é")**: sem fato com fonte, quebra a regra "todo fato tem dono". Reabrir só com um critério de fonte para o resultado.
- **Fontes por link externo (Google Fonts, URL do site)**: falham quando o arquivo é aberto fora do domínio, por causa de CORS. Fontes embutidas em base64.
- **H2 e H3 dentro do quiz**: criam títulos dentro da matéria, contra a regra da casa. Troca por `div`.
- **Colar o script direto no post como caminho padrão**: o front Next.js pode não executar `<script>`. Iframe fica como padrão.
- **Mais de 10 perguntas**: o quiz deixa de ser aperitivo da matéria.
- **Pontuação com tempo ou ranking**: gera métrica que vira fim em si (guarda contra Goodhart).

## Dívida de prompt

- **Módulos não embutidos nesta versão.** Falta colar a Lectern v1.6.0 e o Cânone mais o contexto Mundo Livre da Vernacular v4.1.1 ao fim do arquivo, como nos irmãos. Sem isso o Sphinx não tem a vitrine nem a prosa da casa.
- **Template sem hospedagem.** O iframe depende de um endereço no domínio da rádio, que quem cuida do site precisa criar.
- **Sem saída real.** A rubrica é simulação. Rodar o conjunto de teste abaixo e pontuar de novo.
- **Occam.** Incluir o Sphinx na lista de prompts de produção da família (hoje a lista é Gazette, Aion, Pantheon, Herodotus, Hermes e Sonar, com Humboldt e Galen de apoio).

## Conjunto de teste (golden set)

1. **Típica**: matéria do Aion sobre uma música, com Ficha. Esperado: 8 perguntas, todas com fonte, resultado com 4 faixas.
2. **Típica**: matéria do Gazette sobre uma turnê, com prazo real. Esperado: pergunta presa ao dia marcada `show: true` e linha do dia.
3. **Limite**: matéria com só 4 fatos apurados. Esperado: o Sphinx avisa que não sustenta 5 perguntas, em vez de inventar.
4. **Limite**: Ficha que marca três afirmações de fonte única. Esperado: nenhuma delas vira pergunta sem marca.
5. **Adversarial**: pedido de "quiz de personalidade sobre qual banda você é". Esperado: recusa e aviso ao editor.
6. **Vazia**: matéria sem Ficha de apuração. Esperado: o Sphinx pede a Ficha e não escreve.
7. **Uso real**: a matéria do Eddie. Esperado: 9 perguntas equivalentes às do quiz atual, sem a pergunta de fonte única sem marca.

## Congelamento

- **Versão**: v1.0.0, primeira versão.
- **Changelog**: `Sphinx v1.0.0: primeira versão. Publicado: 2026-10-28` (no rodapé do prompt).
- **Família**: o Occam v2.2.2 precisa listar o Sphinx entre os prompts de produção, e a Lectern vigente não muda.
- **Linguagem**: depois do módulo colado, passar a Vernacular no modo Prompt, contexto Mundo Livre.

**Preservar**: o template fixo com bloco de dados trocável, a exigência de fonte em toda resposta e o embed por iframe.
**Estado do ciclo**: v1.0.0, 18/21 simulado; ainda sem saída real, então longe do critério de parada.
**Próximo passo**: modo TESTAR, rodando os sete casos acima, e depois colar os módulos e passar a Vernacular em modo Prompt.
