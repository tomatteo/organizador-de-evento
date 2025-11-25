# Projeto Programação Orientada a Objetos: Organizador de Eventos
Projeto da disciplina de Programação Orientada a Objetos I do curso de Bacharel em Ciência da Computação.

**Professor:** Alisson Borges Zanetti
**Instituição:** Instituto Federal Catarinense – Campus Concórdia

---

## Tema do Projeto

O sistema escolhido foi o **Organizador de Eventos**, da categoria "Sistemas de Agendamento/Serviço".

Este projeto implementa em Python a estrutura de um sistema para gerenciar eventos, organizadores, participantes e inscrições, aplicando os pilares da Programação Orientada a Objetos.

---

## Integrantes do Grupo

* Filipe José da Costa Nunes
* João Pedro Veloso
* João Vitor Raimundi
* Matteo Dalla Costa Thomé

---

## Como Executar o Projeto

Para testar o sistema e validar as regras de negócio, siga os passos:

1.  Clone este repositório:
    ```bash
    git clone [https://github.com/tomatteo/organizador-de-evento.git](https://github.com/tomatteo/organizador-de-evento.git)
    ```
2.  Navegue até a pasta do projeto.
3.  Execute o arquivo principal de testes (`main.py`):
    ```bash
    python main.py
    ```
4.  A saída dos testes e a demonstração das funcionalidades serão exibidas no console.

---

## Funcionalidades e Conceitos Aplicados

Este projeto foi estruturado de forma modular e aplica os seguintes conceitos de POO:

* **Abstração:** A classe `Usuario` é abstrata (`abc`), definindo um método abstrato (`@abstractmethod`) `autenticar()`.
* **Herança:** As classes `Administrador`, `Organizador` e `Participante` herdam de `Usuario`.
* **Encapsulamento:** Todos os atributos são privados (`_`) e acessados via decoradores `@property` para controle e validação.
* **Polimorfismo:** O método `autenticar()` é sobrescrito em cada subclasse de `Usuario`.
* **Relações:** O sistema implementa Composição (entre `Evento` e `Local`) e Agregação/Associação (entre `Evento`, `Ingresso` e `Participante`).

---

## Diagramas do Sistema

Abaixo estão os diagramas UML desenvolvidos na etapa de modelagem do projeto.

### Diagrama de Casos de Uso 
<div align="center">
  <img src="https://github.com/user-attachments/assets/545a17dc-d682-487d-86a8-194301661519" width="800px" />
</div>

<br>

### Diagrama de Classes
<div align="center">
  <img src="https://github.com/user-attachments/assets/f7010711-f6f4-4eec-90d8-703e6389970d" width="500px" />
</div>
