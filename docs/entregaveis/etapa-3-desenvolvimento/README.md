# Etapa 3 — Desenvolvimento Colaborativo e Controlo de Versões

> Atividade do ciclo de vida: **implementação**. O planeamento está na Etapa 2;
> a validação formal começa na Etapa 4.

**Entrega:** a definir (versão intermédia, não a entrega final)

O enunciado lista sete itens no entregável. Onde está cada um:

| # | Item exigido | Onde está |
|:---:|---|---|
| 1 | Estrutura de código organizada | [`src/rememberme/`](../../../src/rememberme/) — 7 módulos conforme [`plano-desenvolvimento.md`](../etapa-2-projeto/plano-desenvolvimento.md) |
| 2 | Funcionalidades principais parcial/totalmente implementadas | [`docs/tasks.md`](../../tasks.md) — RF01–RF08, estado por linha |
| 3 | Histórico de commits envolvendo os três elementos | `git shortlog -sn` — Renato Moraes (36), Felipe Ribeiro (21), Niley (10) |
| 4 | Utilização de branches | README §"Organização do trabalho" — convenção `<tipo>/<nome>-<descrição>` |
| 5 | Pull Requests | [#2](https://github.com/RenatoMoraesDev/RememberME/pull/2), [#3](https://github.com/RenatoMoraesDev/RememberME/pull/3), [#5](https://github.com/RenatoMoraesDev/RememberME/pull/5), [#7](https://github.com/RenatoMoraesDev/RememberME/pull/7) (feature → develop) e [#8](https://github.com/RenatoMoraesDev/RememberME/pull/8) (develop → master) |
| 6 | Revisões de código | ⚠️ ver nota abaixo |
| 7 | Documentação técnica inicial | [`decisoes.md`](../../decisoes.md) — D1 a D9 |

## Nota sobre o item 6 — revisões de código

A decisão [D8](../../decisoes.md#d8--pull-request-apenas-de-develop-para-master)
optou por não exigir revisão cruzada a cada Pull Request, para não introduzir
espera num grupo de três pessoas a trabalhar em ficheiros distintos.

As revisões de código aconteceram, mas presencialmente, em conjunto, durante
as aulas — e resultaram em correções diretas ou em Pull Requests, e não em
comentários/aprovações registados no GitHub. Confirmado via
`gh pr view --json reviews`: nenhum dos PRs #2, #3, #5 ou #7 tem review
registado na plataforma; isso é esperado dado o processo acima, não um
esquecimento.

## Nota sobre a versão desta entrega

O enunciado sugere etiquetar esta entrega como `v0.5 — Protótipo funcional`,
reservando `v1.0 — Versão final` para a Etapa 5. A tag `v1.0_Final`, criada
junto do PR #8, antecipou esse nome antes da hora — sugestão: substituir por
`v0.5` antes da entrega desta etapa.
