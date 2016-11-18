'''
.. py:module:: communication
    :platform: Unix

Simple examples of interaction between agents.

You need to decorate each function used by other agents with '@aiomas.expose'
(remember to import aiomas) **and** they have to be async
(``async def func()``).
'''
import random

from creamas import CreativeAgent, Environment, Simulation

import aiomas

class ServiceAgent(CreativeAgent):
    '''Agent which defines a service for other agents to use.
    '''

    def __init__(self, env):
        super().__init__(env)
        self.number = random.random()

    @aiomas.expose
    async def service(self):
        return self.number

    async def act(self):
        self.number = random.random()
        print("Service defined new number: {}".format(self.number))

class ConsumerAgent(CreativeAgent):
    '''Agent which consumes other agent's service.
    '''

    def __init__(self, env, service_addr):
        super().__init__(env)
        self.service_addr = service_addr

    async def act(self):
        # You have to await the connect and call to service as they are done
        # asynchronously across TCP.
        service_agent = await self.env.connect(self.service_addr)
        ret = await service_agent.service()
        print("Got {} from service.".format(ret))

if __name__ == "__main__":
    env = Environment.create(('localhost', 5555))
    server = ServiceAgent(env)
    consumer = ConsumerAgent(env, server.addr)
    sim = Simulation(env)
    sim.async_steps(10)
    sim.end()