# RotaCerta — demonstração instalável

PWA de apresentação do gestor de entregas do **Amaro Supermercados**, baseado no protótipo interativo v12 aprovado. Preserva o design system e as jornadas de atendimento, expedição, motorista e gestão.

**Estado da entrega:** projeto preparado no ambiente de trabalho. Este pacote, por si só, **não cria um repositório e não publica um site**. A publicação depende de conexão/autorização com a conta GitHub e definição da visibilidade do repositório.

## Conteúdo

```text
docs/                    Site completo a publicar
  index.html             Protótipo v12 + controles discretos de instalação
  manifest.webmanifest   Nome, ícones e janela standalone
  sw.js                  Cache versionado da demonstração
  pwa.js                 Instalação, modo offline e atualização voluntária
  pwa.css                Estilos somente para a camada PWA
  icons/                 Símbolo RotaCerta nas dimensões de instalação
  .nojekyll              Publicação estática sem Jekyll
README.md
PUBLICACAO.md            Configuração prevista de hospedagem
TESTES.md                Verificações realizadas e pendentes
tests/                   Testes de interface e do service worker
```

Não existe etapa de compilação, `npm install`, banco de dados ou credencial de API para abrir a demonstração. Os modelos impressos e o logo do Amaro continuam incorporados ao HTML original. A pasta pública não inclui o simulador com moldura de smartphone: é o aplicativo responsivo direto.

## Testar localmente

Na pasta do projeto, com Python 3 instalado:

```sh
python -m http.server 8000 --bind 127.0.0.1 --directory docs
```

Abra `http://127.0.0.1:8000/` no mesmo computador. A instalação PWA exige um endereço HTTPS ou o ambiente de desenvolvimento localhost. Abrir `index.html` como arquivo não equivale a instalar o aplicativo.

## Apresentação no celular

Depois da publicação por HTTPS:

1. Abra o link no Chrome do Android ou no Safari do iPhone.
2. Use **Instalar no celular** na tela de login. O botão aciona o convite do navegador quando disponível ou mostra as instruções de instalação.
3. Abra o RotaCerta pelo ícone criado na tela inicial. O manifesto solicita a exibição `standalone`, sem os controles do navegador nos ambientes compatíveis.
4. Use os perfis de demonstração. E-mail e senha são ilustrativos e não são coletados ou validados.
5. Para mostrar uma mesma compra atravessando atendimento, expedição e motorista, troque os perfis **no mesmo aparelho**.

O menu de instalação pode variar conforme o navegador e a versão do sistema. No Safari, a opção **Abrir como App** deve ficar habilitada quando exibida. Não é um APK nem uma publicação na App Store/Google Play.

## O que funciona e o que continua simulado

O cadastro, a associação de cada caixa (inclusive a caixa do frio), a conferência, o romaneio e a execução da rota são interações locais. Fichas e rascunhos usam o armazenamento do navegador quando disponível. Cada instalação tem seu próprio conjunto de dados; não há banco compartilhado entre dispositivos.

**Não há autenticação real, Google Cloud Vision conectado, disparo automático real de WhatsApp, mapas/otimização real nem controle concorrente de motoristas em servidor.** A extração acontece de forma simulada somente no exemplo fornecido. Fotos próprias precisam de revisão/preenchimento manual. O botão de contato manual abre o WhatsApp externo, não envia mensagens sozinho e depende daquele aplicativo/serviço.

A decisão de usar Google Cloud Vision pertence à futura implementação. Nenhuma chave deve ser incluída no HTML, no manifesto ou em um repositório público.

## Funcionamento offline

O service worker prepara os arquivos estáticos da demonstração após o primeiro acesso bem-sucedido. Quando esse preparo é concluído, a seção **Perfil → RotaCerta no celular** informa que a demonstração está disponível offline naquele navegador.

O armazenamento pode ser removido pelo usuário ou pelo navegador. Faça uma abertura online antes da apresentação e teste o modo avião no aparelho real. Recursos externos, como o WhatsApp, continuam dependendo de conexão. Não existe fila de sincronização com backend.

O cache e os dados locais são identificados pelo caminho do projeto para não misturar esta demonstração com outro site do mesmo domínio. O service worker não intercepta URLs do WhatsApp, requisições de escrita ou caminhos fora do aplicativo.

## Atualizações

Ao modificar **qualquer arquivo público**, altere `BUILD` em `docs/sw.js` e `VERSION` em `docs/pwa.js`. Novas versões ficam aguardando e podem ser aplicadas em **Perfil → Atualização disponível**. O aplicativo não recarrega automaticamente um formulário durante a apresentação. Salve o que estiver preenchendo antes de confirmar uma atualização.

## Dados e publicação

Use somente dados fictícios. O login demonstrativo **não protege o site de visitantes**. A diretiva `noindex` reduz descoberta por buscadores compatíveis, mas não é restrição de acesso.

A publicação pública deve ser autorizada pelo proprietário, inclusive o uso do logo do supermercado no material publicado. Não colocar dados reais de clientes, senhas, tokens, planilhas privadas ou configurações de contas no repositório. Este pacote contém apenas os dados fictícios do protótipo, sem alterações feitas pelo usuário em seu navegador.

## Referências técnicas

- MDN — [Making PWAs installable](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable)
- MDN — [Create a standalone app](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/How_to/Create_a_standalone_app)
- GitHub — [Configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- Google — [Usar apps da Web no Android](https://support.google.com/chrome/answer/9658361?co=GENIE.Platform%3DAndroid&hl=pt-BR)

Documentação consultada em 14/10/2026. Condições dos serviços podem mudar.
