# Finance
<h3> O projeto Finance é o resultado do penúltimo lab do curso CS50 feito em 2022.</h3>
<h5>Sendo possível ver os requisitos de sua construção <a href="https://cs50.harvard.edu/x/2021/psets/9/finance/">aqui.</a></h5>
<p> <b>Descrição: </b> Site onde os usuários podem criar uma conta, comprar e vender ações imaginárias.</p>
<p> Essa web aplicação foi programada com o Flask, micro framework do python, pelo padrão de arquitetura de software MVC.</p>
 <p>**O site se conecta à API do Yahoo Finance para obter dados. A base de dados utilizada é SQL.<br>
  Sendo necessário rodar o comando <b>abaixo</b> no terminal para que aplicação tenha uma comunicação eficiente com á API.<br>
  <b> export API_KEY=pk_a5595b67022441f2863d3f6faba5642e </b>
</p>

<p><b>Para este projeto, implementei as seguinte funcionalidades pelo python:</b></p>

<ol>
  <li> <i>Register:</i> Permite que um usuário se "registre" no site. O nome do usuário e senha são enviados via Flask e armazenados em um banco de dados sqlite 3 (A senha é amarzenada após passar pelo encriptografamento de uma função hash).
  <li> <i>Quote:</i> permite que um usuário consulte o preço de uma ação usando o símbolo represente de uma determinada empresa.</li>
  <li> <i>Buy:</i> Permite ao usuário comprar uma ação imaginária; As compras são salvas no banco de dados e o saldo de ações é atualizado.</li>
  <li> <i>Index:</i> exibe uma tabela de resumo HTML dos fundos e ações atuais do usuário./li>
  <li> <i>Sell:</i> Permite ao usuário vender ações; As vendidas são projetadas para o banco de dados e o conjunto de ações produzidos.</li>
  <li> <i>History:</i> Exibe uma tabela para o HTML Award o histórico de transações para o usuário.</li>
  </ol>

![Captura de tela 2022-09-08 18 03 40](https://user-images.githubusercontent.com/99035126/189232402-3eeb0695-8947-47f1-993b-842452b8308c.png)


![Captura de tela 2022-09-08 18 03 54](https://user-images.githubusercontent.com/99035126/189232556-19fb8f68-6fc7-4816-bed7-53b5ea1a024a.png)


![Captura de tela 2022-09-08 18 03 58](https://user-images.githubusercontent.com/99035126/189236952-838bb680-a307-4c49-acc6-905c5767b19e.png)


![Captura de tela 2022-09-08 18 04 02](https://user-images.githubusercontent.com/99035126/189237042-f77a68a8-ac05-4302-97c5-067b50264024.png)

![Captura de tela 2022-09-08 18 04 07](https://user-images.githubusercontent.com/99035126/189237062-ad12d9cc-07c9-4d99-8068-d83100aee363.png)


![Captura de tela 2022-09-08 18 04 10](https://user-images.githubusercontent.com/99035126/189237127-749aa562-813a-4483-8b55-4addba3a4b22.png)


