# Entregáveis por etapa

Material submetido a avaliação, uma pasta por etapa. Cada pasta tem um `README.md`
que lista os itens exigidos pelo enunciado e aponta para o ficheiro que responde a cada um.

As cinco etapas do curso são as atividades clássicas do ciclo de vida da
engenharia de software, uma por etapa. As pastas têm o nome da **atividade**, não o
título do enunciado — assim a sequência lê-se de uma vez e não muda se o formador
reformular um título. O título completo de cada etapa está no `README.md` da pasta.

| Etapa | Atividade | Pasta | Estado |
|---|---|---|---|
| 1 — Definição do Problema e Análise de Requisitos | Análise | [`etapa-1-analise/`](etapa-1-analise/) | Entregue |
| 2 — Arquitetura, Tecnologias e Planeamento | Projeto | [`etapa-2-projeto/`](etapa-2-projeto/) | Entrega a 04/09/2026 |
| 3 — Desenvolvimento Colaborativo e Controlo de Versões | Implementação | `etapa-3-implementacao/` | Por abrir |
| 4 — Validação, Testes e Demonstração | Verificação e validação | `etapa-4-validacao/` | Por abrir |
| 5 — Entrega Final e Apresentação | Entrega | `etapa-5-entrega/` | Por abrir |

As pastas das etapas 3 a 5 são criadas quando cada etapa arrancar, com o enunciado respetivo em mãos.

Os enunciados do formador estão em [`../enunciados/`](../enunciados/).

## Documentos vivos

Dois documentos são referidos pelos entregáveis mas não vivem aqui, por serem
atualizados ao longo de todo o projeto:

| Documento | Papel |
|---|---|
| [`../tasks.md`](../tasks.md) | Quadro de tarefas — item 6 do entregável da Etapa 2 |
| [`../decisoes.md`](../decisoes.md) | Registo das decisões técnicas e do motivo de cada uma |

Congelá-los dentro de uma pasta de etapa anulava a função para que existem. O estado
de qualquer um deles numa data passada obtém-se pelo histórico do repositório.

## Estado do repositório numa entrega

Cada entrega é marcada com uma etiqueta Git (`etapa-1`, `etapa-2`, …) no commit submetido:

```bash
git show etapa-2:docs/tasks.md    # ver um ficheiro como estava na entrega
git checkout etapa-2              # ver o repositório inteiro nessa data
```
