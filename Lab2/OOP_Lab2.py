from abc import ABC, abstractmethod


class TrainTicket(ABC):
    def __init__(self, ticket_id, arrival, destination, price, first_name, last_name, is_child=False):
        self.__ticket_id = ticket_id
        self.__arrival = arrival
        self.__destination = destination
        self.price = price
        self.first_name = first_name
        self.last_name = last_name
        self.is_valid = True
        self.is_child = is_child

    @property
    def ticket_id(self):
        return self.__ticket_id

    @property
    def arrival(self):
        return self.__arrival

    @property
    def destination(self):
        return self.__destination

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def cancel_ticket(self):
        self.is_valid = False
        print(f"\nTicket {self.__ticket_id} for {self.full_name()} has been canceled.\n")

    def change_destination(self, new_destination):
        self.__destination = new_destination
        print(f"Destination changed to: {self.__destination}")

    def change_arrival(self, new_arrival):
        self.__arrival = new_arrival
        print(f"Arrival station changed to: {self.__arrival}")

    @staticmethod
    def check_price_range(ticket):
        if ticket.price > 100:
            return "expensive"
        else:
            return "cheap"

    @abstractmethod
    def apply_discount(self):
        pass


class StudentTicket(TrainTicket):
    def __init__(self, ticket_id, arrival, destination, price, first_name, last_name, student_id):
        super().__init__(ticket_id, arrival, destination, price, first_name, last_name)
        self.student_id = student_id

    def cancel_ticket(self):
        super().cancel_ticket()
        print(f"Student ticket {self.student_id} has been canceled.")

    def apply_discount(self):
        self.price *= 0.8
        print(f"Discount applied. New price: {self.price:.2f}")


class ChildTicket(TrainTicket):
    def __init__(self, ticket_id, arrival, destination, price, first_name, last_name, child_age):
        is_child = child_age <= 14
        super().__init__(ticket_id, arrival, destination, price, first_name, last_name, is_child=is_child)
        self.child_age = child_age

    def apply_discount(self):
        if self.is_child:
            self.price *= 0.5
            print(f"Child discount applied. New price: {self.price:.2f}")


class Insurance:
    def __init__(self, insurance_id, insurance_amount):
        self.insurance_id = insurance_id
        self.insurance_amount = insurance_amount

    def apply_insurance(self):
        print(f"Insurance of {self.insurance_amount} applied.")


class InsuredTicket(TrainTicket, Insurance):
    def __init__(self, ticket_id, arrival, destination, price, first_name, last_name, insurance_id, insurance_amount):
        TrainTicket.__init__(self, ticket_id, arrival, destination, price, first_name, last_name)
        Insurance.__init__(self, insurance_id, insurance_amount)

    def display_insurance(self):
        print(f"Ticket {self.ticket_id} for {self.full_name()} is insured for {self.insurance_amount}")

    def apply_discount(self):
        self.price *= 0.9
        print(f"Discount applied for insured ticket. New price: {self.price:.2f}")


class TicketSystem:
    def __init__(self):
        self.tickets = []

    def add_ticket(self, ticket):
        if TrainTicket.check_price_range(ticket) == "cheap":
            self.tickets.append(ticket)
            print(
                f"Ticket for {ticket.full_name()} added from {ticket.arrival} to {ticket.destination}, price: {ticket.price:.2f}")
            self.print_receipt(ticket)
        else:
            print(f"Ticket price for {ticket.full_name()} is invalid. Exceeds budget.")

    def show_all_tickets(self):
        if not self.tickets:
            print("\nNo available tickets.")
        else:
            print("\nAvailable Tickets:")
            print("-" * 50)
            for ticket in self.tickets:
                print(f"Ticket ID: {ticket.ticket_id}")
                print(f"Passenger: {ticket.full_name()}")
                print(f"Route: {ticket.arrival} to {ticket.destination}")
                print(f"Price: {ticket.price:.2f} USD")
                print("-" * 50)

    def cancel_ticket_by_id(self, ticket_id):
        for ticket in self.tickets:
            if ticket.ticket_id == ticket_id:
                ticket.cancel_ticket()
                self.tickets.remove(ticket)
                return
        print(f"Ticket with ID {ticket_id} not found.")

    @staticmethod
    def print_receipt(ticket):
        print("\nReceipt:")
        print("-" * 30)
        print(f"Ticket ID: {ticket.ticket_id}")
        print(f"Passenger: {ticket.full_name()}")
        print(f"Route: {ticket.arrival} to {ticket.destination}")
        print(f"Price: {ticket.price:.2f} USD")
        print("-" * 30)
        print("Thank you for your purchase!\n")


def test():
    system = TicketSystem()

    student_ticket = StudentTicket(102, "Lviv", "Kyiv", 80, "Maria", "Ivanenko", "ST123")
    child_ticket = ChildTicket(103, "Odesa", "Lviv", 60, "Ivan", "Petrenko", 7)
    insured_ticket = InsuredTicket(105, "Kharkiv", "Kyiv", 200, "Anna", "Kovalenko", "INS789", 50000)

    system.add_ticket(student_ticket)
    system.add_ticket(child_ticket)
    system.add_ticket(insured_ticket)

    system.show_all_tickets()

    student_ticket.apply_discount()
    child_ticket.apply_discount()
    insured_ticket.display_insurance()

    system.cancel_ticket_by_id(102)
    system.show_all_tickets()


test()
