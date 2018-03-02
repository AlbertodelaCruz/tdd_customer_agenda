# -*- coding: utf-8 -*-


from mamba import description, context, it
from doublex import Spy, when
from expects import expect, be, have_key, equal
from doublex_expects import have_been_called_with

import sqlite3


class CustomerService(object):
    def __init__(self, customer_repository):
        self._customer_repository = customer_repository

    def add(self, customer):
        self._customer_repository.put(customer)

    def remove(self, customer):
        self._customer_repository.delete(customer)


class InMemoryRepository(object):
    def __init__(self):
        self._customers = []

    def put(self, customer):
        self._customers.append(customer)

    def delete(self, customer):
        self._customers.remove(customer)

    def find_all(self):
        return self._customers

    def find_by(self, name):
        for customer in self._customers:
            if customer.name==name:
                return customer.__dict__
        return None

class Customer(object):
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname


A_NAME = 'a_name'
A_SURNAME = 'a_surname'


with description('CustomerService'):
    with context('add a customer'):
        with it('calls repository put function'):
            customer = Customer(name=A_NAME, surname=A_SURNAME)
            customer_repository = Spy()
            customer_service = CustomerService(customer_repository)

            customer_service.add(customer)

            expect(customer_repository.put).to(have_been_called_with(customer))

    with context('remove a customer'):
        with it('calls repository delete function'):
            customer = Customer(name=A_NAME, surname=A_SURNAME)
            customer_repository = Spy()
            customer_service = CustomerService(customer_repository)

            customer_service.remove(customer)

            expect(customer_repository.delete).to(have_been_called_with(customer))


with description('InMemoryRepository'):
    with context('put a customer'):
        with it('stores in memory'):
            customer = Customer(name=A_NAME, surname=A_SURNAME)
            customer_repository = InMemoryRepository()

            customer_repository.put(customer)

            result = customer_repository.find_all()
            expect(len(result)).to(be(1))

    with context('find a customer by name'):
        with it('finds it'):
            customer = Customer(name=A_NAME, surname=A_SURNAME)
            customer_repository = InMemoryRepository()
            customer_repository.put(customer)

            result = customer_repository.find_by(A_NAME)

            expect(result).to(have_key('surname', A_SURNAME))

        with context('this customer does not exists'):
            with it('result must be None'):
                customer = Customer(name=A_NAME, surname=A_SURNAME)
                customer_repository = InMemoryRepository()

                result = customer_repository.find_by(A_NAME)

                expect(result).to(be(None))

    with context('remove a customer'):
        with it('deletes from memory'):
            customer = Customer(name=A_NAME, surname=A_SURNAME)
            customer_repository = InMemoryRepository()
            customer_repository.put(customer)

            customer_repository.delete(customer)

            result = customer_repository.find_all()
            expect(result).to(equal([]))

