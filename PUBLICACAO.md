# Publicação prevista — ainda não executada

## Destino sugerido

Repositório novo `rotacerta-demo` na conta que o usuário conectar. Não sobrescrever repositório existente sem confirmar. Confirmar a visibilidade antes de publicar.

Para este pacote, o caminho mais simples é **GitHub Pages, branch `main`, pasta `/docs`**. Não é necessário um servidor backend nem GitHub Actions personalizado.

## Configuração

Após confirmar as permissões e a visibilidade:

1. Criar o repositório e enviar todos os arquivos deste projeto, mantendo a estrutura.
2. Configurar **Settings → Pages → Deploy from a branch → main → /docs**.
3. Acompanhar a execução de publicação e verificar o resultado antes de fornecer um link como ativo.
4. Confirmar HTTPS e testar o site pelo endereço efetivamente retornado pelo GitHub. Não presumir o nome do usuário nem inventar uma URL publicada.
5. Validar manifesto, ícones, registro do service worker, instalação em telefone real e fluxo de atendimento até entrega.

O GitHub Free oferece Pages em repositórios públicos. Em planos que permitem repositório privado com Pages, a privacidade do repositório não torna automaticamente a página privada. Restrições organizacionais podem alterar a disponibilidade.

Se o usuário exigir código privado e sua conta não permitir Pages no repositório privado, definir outro destino de hospedagem compatível e conectar esse serviço antes de executar. Não tornar público um repositório privado para contornar a limitação sem autorização.

Fonte: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Checklist antes de entregar o link

- Página publicada retorna HTTP 200 por HTTPS e abre o login.
- Logo Amaro inteiro e as quatro jornadas disponíveis.
- `manifest.webmanifest`, ícones e `sw.js` retornam 200 dentro do caminho do projeto.
- Navegador do celular oferece a instalação compatível; aplicativo abre pelo ícone em modo independente.
- Primeiro carregamento prepara o cache; modo avião permite reabrir a demonstração local.
- É possível retornar ao login e reiniciar os dados de teste por confirmação.
- Leitura da ficha e avisos automáticos continuam claramente simulados.
- Não há promessa de sincronização entre aparelhos ou acesso seguro de produção.
