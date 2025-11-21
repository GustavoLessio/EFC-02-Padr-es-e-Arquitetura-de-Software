"""
Sistema de locadora de carros usando padrões de projeto:

"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List



#Decorator
#usado para adicionar extras ao carro (GPS, cadeirinha, seguro) empilhando 
# decoradores sobre o carro base, sem necessidade de criar subclasses para cada
#combinação possível de recursos.

class Car(ABC):
    

    @abstractmethod
    def daily_rate(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass


class EconomyCar(Car):
    def daily_rate(self) -> float:
        return 120.0

    def description(self) -> str:
        return "Carro Econômico"


class SuvCar(Car):
    def daily_rate(self) -> float:
        return 220.0

    def description(self) -> str:
        return "SUV"


class LuxuryCar(Car):
    def daily_rate(self) -> float:
        return 400.0

    def description(self) -> str:
        return "Carro de Luxo"


class CarDecorator(Car):
    

    def __init__(self, car: Car):
        self._car = car


class GPSDecorator(CarDecorator):
    

    def daily_rate(self) -> float:
        return self._car.daily_rate() + 20.0

    def description(self) -> str:
        return self._car.description() + " + GPS"


class ChildSeatDecorator(CarDecorator):
    

    def daily_rate(self) -> float:
        return self._car.daily_rate() + 15.0

    def description(self) -> str:
        return self._car.description() + " + Cadeirinha"


class ExtraInsuranceDecorator(CarDecorator):
    

    def daily_rate(self) -> float:
        return self._car.daily_rate() + 50.0

    def description(self) -> str:
        return self._car.description() + " + Seguro Extra"



#strategy
#Define diferentes formas de calcular o preço total da locação (básico, premium ou longa duração). 
# Cada estratégia encapsula sua própria regra de negócio, evitando condicionais complexas dentro da classe Reservation.


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_total(self, car: Car, days: int) -> float:
        pass


class BasicPricing(PricingStrategy):
    

    def calculate_total(self, car: Car, days: int) -> float:
        return car.daily_rate() * days


class PremiumPricing(PricingStrategy):
    

    def calculate_total(self, car: Car, days: int) -> float:
        return car.daily_rate() * days * 1.15


class LongTermPricing(PricingStrategy):
    

    def calculate_total(self, car: Car, days: int) -> float:
        base = car.daily_rate() * days
        if days >= 10:
            return base * 0.8
        elif days >= 5:
            return base * 0.9
        return base



#Observer
#Permite que serviços externos (e-mail, SMS e log) recebam notificações
#automáticas sempre que o status da reserva muda. Evita acoplamento direto entre
#a reserva e os serviços de notificação.


class Observer(ABC):
    @abstractmethod
    def update(self, message: str) -> None:
        pass


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self, message: str) -> None:
        pass


class ReservationNotifier(Subject):
    

    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, message: str) -> None:
        for obs in self._observers:
            obs.update(message)


class EmailService(Observer):
    

    def update(self, message: str) -> None:
        print(f"[E-mail] {message}")


class SMSService(Observer):
    

    def update(self, message: str) -> None:
        print(f"[SMS] {message}")


class AuditLog(Observer):
    

    def update(self, message: str) -> None:
        print(f"[Log Auditoria] {message}")


#reserva 

class Reservation:
    

    def __init__(
        self,
        customer_name: str,
        car: Car,
        days: int,
        pricing_strategy: PricingStrategy,
        reservation_type: str,
        notifier: ReservationNotifier,
    ) -> None:

        self.customer_name = customer_name
        self.car = car
        self.days = days
        self.pricing_strategy = pricing_strategy
        self.reservation_type = reservation_type
        self.notifier = notifier
        self.status = "criada"

    def summarize(self) -> str:
        total = self.pricing_strategy.calculate_total(self.car, self.days)
        return (
            f"Reserva de {self.customer_name}: "
            f"{self.car.description()} por {self.days} dia(s) "
            f"({self.reservation_type}) - Total: R${total:.2f}"
        )

    def confirm(self) -> None:
        self.status = "confirmada"
        self.notifier.notify(f"{self.summarize()} | Status: {self.status}")

    def set_status(self, new_status: str) -> None:
        self.status = new_status
        self.notifier.notify(
            f"Status alterado: {self.customer_name} → {self.status}"
        )



# Factory Method — Responsável por centralizar a criação das reservas (local ou online) e montar
#os carros com os extras de forma encapsulada. Evita condicionais espalhadas
#pelo código e facilita adicionar novos tipos de reservas futuramente.
#V V V

class ReservationFactory(ABC):
    

    def __init__(self, notifier: ReservationNotifier) -> None:
        self.notifier = notifier

    @abstractmethod
    def create_reservation(
        self,
        customer_name: str,
        car_type: str,
        extras: List[str],
        days: int,
        pricing_strategy: PricingStrategy,
    ) -> Reservation:
        pass

    def _create_car_with_extras(self, car_type: str, extras: List[str]) -> Car:
        

        if car_type == "economy":
            car: Car = EconomyCar()
        elif car_type == "suv":
            car = SuvCar()
        elif car_type == "luxury":
            car = LuxuryCar()
        else:
            raise ValueError("Tipo de carro desconhecido.")

        for extra in extras:
            if extra == "gps":
                car = GPSDecorator(car)
            elif extra == "child_seat":
                car = ChildSeatDecorator(car)
            elif extra == "insurance":
                car = ExtraInsuranceDecorator(car)

        return car


class LocalReservationFactory(ReservationFactory):
    

    def create_reservation(
        self,
        customer_name: str,
        car_type: str,
        extras: List[str],
        days: int,
        pricing_strategy: PricingStrategy,
    ) -> Reservation:
        car = self._create_car_with_extras(car_type, extras)
        reservation = Reservation(
            customer_name, car, days, pricing_strategy, "balcão", self.notifier
        )
        self.notifier.notify(f"Nova reserva local criada: {reservation.summarize()}")
        return reservation


class OnlineReservationFactory(ReservationFactory):
    

    def create_reservation(
        self,
        customer_name: str,
        car_type: str,
        extras: List[str],
        days: int,
        pricing_strategy: PricingStrategy,
    ) -> Reservation:
        car = self._create_car_with_extras(car_type, extras)
        reservation = Reservation(
            customer_name, car, days, pricing_strategy, "online", self.notifier
        )
        self.notifier.notify(f"Nova reserva online criada: {reservation.summarize()}")
        return reservation



#interacao pelo terminal

def escolher_tipo_reserva() -> str:
    while True:
        print("\nTipo de reserva:")
        print("1 - Local (balcão)")
        print("2 - Online")
        opc = input("Escolha uma opção: ").strip()
        if opc == "1":
            return "local"
        elif opc == "2":
            return "online"
        else:
            print("Opção inválida, tente novamente.")


def escolher_tipo_carro() -> str:
    while True:
        print("\nTipos de carro:")
        print("1 - Carro Econômico")
        print("2 - SUV")
        print("3 - Carro de Luxo")
        opc = input("Escolha uma opção: ").strip()
        if opc == "1":
            return "economy"
        elif opc == "2":
            return "suv"
        elif opc == "3":
            return "luxury"
        else:
            print("Opção inválida, tente novamente.")


def escolher_extras() -> List[str]:
    extras: List[str] = []
    while True:
        print("\nExtras disponíveis:")
        print("1 - GPS")
        print("2 - Cadeirinha")
        print("3 - Seguro Extra")
        print("0 - Nenhum / Finalizar seleção")
        opc = input("Escolha um extra (ou 0 para terminar): ").strip()

        if opc == "0":
            break
        elif opc == "1":
            extras.append("gps")
        elif opc == "2":
            extras.append("child_seat")
        elif opc == "3":
            extras.append("insurance")
        else:
            print("Opção inválida, tente novamente.")

    return extras


def escolher_qtd_dias() -> int:
    while True:
        try:
            dias = int(input("\nQuantos dias de locação? "))
            if dias <= 0:
                print("Informe um número positivo de dias.")
                continue
            return dias
        except ValueError:
            print("Digite um número inteiro válido.")


def escolher_estrategia_preco() -> PricingStrategy:
    while True:
        print("\nEstratégia de preço:")
        print("1 - Básico")
        print("2 - Premium")
        print("3 - Longa duração")
        opc = input("Escolha uma opção: ").strip()
        if opc == "1":
            return BasicPricing()
        elif opc == "2":
            return PremiumPricing()
        elif opc == "3":
            return LongTermPricing()
        else:
            print("Opção inválida, tente novamente.")


def atualizar_status_interativamente(reservation: Reservation) -> None:
    print("\nReserva criada e confirmada!")
    print(reservation.summarize())
    print("\nVocê pode atualizar o status da reserva.")
    print("Digite um novo status (ou deixe vazio e pressione ENTER para terminar).")

    while True:
        novo_status = input("Novo status (ENTER para sair): ").strip()
        if novo_status == "":
            break
        reservation.set_status(novo_status)



#interação c/ sistema

def main():
    print("=== Sistema de Locadora de Carros ===")

    #notificador
    notifier = ReservationNotifier()
    notifier.attach(EmailService())
    notifier.attach(SMSService())
    notifier.attach(AuditLog())

    #fabrica
    local_factory = LocalReservationFactory(notifier)
    online_factory = OnlineReservationFactory(notifier)

    while True:
        print("\nMenu principal:")
        print("1 - Criar nova reserva")
        print("2 - Sair")
        opc = input("Escolha uma opção: ").strip()

        if opc == "2":
            print("Encerrando o sistema. Nos vemos em breve!")
            break
        elif opc != "1":
            print("Opção inválida, tente novamente.")
            continue

        
        customer_name = input("\nNome do cliente: ").strip()

        tipo_reserva = escolher_tipo_reserva()
        tipo_carro = escolher_tipo_carro()
        extras = escolher_extras()
        dias = escolher_qtd_dias()
        pricing_strategy = escolher_estrategia_preco()

        
        if tipo_reserva == "local":
            reservation = local_factory.create_reservation(
                customer_name, tipo_carro, extras, dias, pricing_strategy
            )
        else:
            reservation = online_factory.create_reservation(
                customer_name, tipo_carro, extras, dias, pricing_strategy
            )

        
        reservation.confirm()
        atualizar_status_interativamente(reservation)


if __name__ == "__main__":
    main()
