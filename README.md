# EFC-02-Padroes-e-Arquitetura-de-Software


Sistema de locadora de carros

Este projeto implementa um sistema simplificado de locadora de carros utilizando quatro padrões de projeto estudados: Factory Method, Decorator, Strategy e Observer. O objetivo é demonstrar, na prática, como esses padrões podem tornar o código mais organizado, flexível, escalável e fácil de manter, aplicando-os dentro do fluxo real de uma locação (criação da reserva, composição do carro, cálculos de preço e notificações).

O sistema permite criar reservas locais ou online, incluir extras opcionais ao veículo (como GPS e seguro adicional), aplicar diferentes estratégias de precificação, registrar eventos e enviar notificações automaticamente conforme o status da reserva é atualizado.

Instruções de Execução
Requisitos:
-Python 3.8+
-Nenhuma biblioteca externa é necessária (uso apenas de módulos nativos)

Executar o programa:
No terminal, dentro da pasta do projeto, digite:
python locadora.py

O programa irá:
-criar reservas locais e online
-mostrar o preço total com base na estratégia aplicada
-exibir notificações simuladas (e-mail, SMS e log)
-atualizar e exibir o status das reservas em tempo real



Padrões de projeto implementados e onde encontra-los

Factory Method:
Responsável por criar reservas locais e online sem expor a lógica interna de construção.

onde está no código:
ReservationFactory
LocalReservationFactory
OnlineReservationFactory
Método: create_reservation(...)

Função no sistema:
Centraliza e organiza a criação de reservas, evitando condicionais e facilitando futuras expansões (novos tipos de reserva).



Decorator:
Usado para adicionar extras ao carro de forma flexível e combinável.

onde está no código:
Car (componente base)
EconomyCar, SuvCar, LuxuryCar (componentes concretos)
CarDecorator (base dos decoradores)
GPSDecorator, ChildSeatDecorator, ExtraInsuranceDecorator

Função no sistema:
Permite montar veículos com GPS, cadeirinha, seguro extra etc. sem criar subclasses infinitas.

Strategy:
Define diferentes políticas de preço da locação.

onde está no código:
PricingStrategy
BasicPricing
PremiumPricing
LongTermPricing
Método chamado dentro de Reservation.summarize()

Função no sistema:
Encapsula os algoritmos de cálculo, permitindo trocar regras sem modificar a classe principal da reserva.

Observer:
Responsável pelas notificações automáticas do sistema.

onde está no código:
ReservationNotifier (Subject)
EmailService, SMSService, AuditLog (Observers)
Métodos: attach(), notify(), update()

Função no sistema:
Envia e-mail, SMS e escreve logs automaticamente quando a reserva é criada, confirmada ou alterada.
