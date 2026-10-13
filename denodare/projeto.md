# Projeto Denodare 

## Equipe 
Gestor: Eliomar 
Tech Lead: Afonso 
Dev: Eu (Danillo)
GCO: Vitor

## Informações
Gitlab: https://gitlab.com/daurora-fakenews

Eu consigo visualizar 5 projetos, mas existem vários: 
- https://gitlab.com/daurora-fakenews/fakenews-bff 
- https://gitlab.com/daurora-fakenews/fakenews-landing-page 
- https://gitlab.com/daurora-fakenews/fakenews-crawling 
- https://gitlab.com/daurora-fakenews/fakenews-bc 
- https://gitlab.com/daurora-fakenews/fakenews 

Eu sou responsável pelo `fakenews-bff`.
O projeto `fakenews` é o frontend e o projeto `fakenews-bc` é o blockchain, que o Afonso gosta de se referir como o cartório do sistema. 

## Ambiente
O projeto é rico em ambientes, e justamente isso o torna um pouco mais complexo.Possui ambiente de develop, homolog e produção (possuem mais) e são mantidos no portainer. 
Em cada ambiente existente, cada um dos repositórios é um microservice, e cada um possui seus software habilitadores como redis, postgres etc. Aumentando a complexidade, cada microserviço possui uma stack. Para acessar cada ambiente é necessário estar dentro de uma VPN e quem libera o acesso é o Vitor. Meus dados de acesso a vpn estão salvos no google drive (https://drive.google.com/drive/folders/1NcW65ShCR78N4xZiapA1VTKrc-BmMWf7?usp=drive_link).
