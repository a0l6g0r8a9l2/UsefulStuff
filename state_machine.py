from datetime import datetime, timedelta
from transitions.extensions.asyncio import AsyncMachine
import asyncio


class Notificator:
    states = ['new', 'checking_exchange', 'price_scheduling', 'expired', 'done']

    def __init__(self, name: str, expired_time: datetime):
        self.my_name = name
        self.target_time = expired_time
        self.current_time = datetime.now()
        self.machine = AsyncMachine(model=self, states=Notificator.states, initial='new')
        self.machine.add_transition(trigger='checking_exchange', source='new', dest='checking_exchange')
        self.machine.add_transition(trigger='price_scheduling', source='checking_exchange', dest='price_scheduling')
        self.machine.add_transition(trigger='time_is_over', source='*', dest='expired')
        self.machine.add_transition(trigger='work_is_done', source='price_scheduling', dest='done',
                                    unless='expired_check')

    async def on_enter_price_scheduling(self):
        print(f'{self.my_name} in state {self.state} and scheduling price!')

    async def on_enter_checking_exchange(self):
        print(f'{self.my_name} in state {self.state} and checking exchange!')

    async def on_enter_done(self):
        print(f'{self.my_name} in state {self.state}!')

    async def on_enter_expired(self):
        print(f'{self.my_name} in state {self.state}!')

    # async def do_staff(self):
    #     """
    #     add after_state_change='func' in AsyncMachine if need do something on every change state
    #     :return:
    #     """
    #     print(f'{self.my_name} on state {self.state} and do some staff!')

    async def expired_check(self):
        if self.current_time > self.target_time:
            print(f'{self.my_name} on state {self.state} and return expired check {True}!')
            await self.time_is_over()
            return True
        else:
            print(f'{self.my_name} on state {self.state} and return expired check {False}!')
            return False


target_time1 = datetime.now() + timedelta(seconds=5)
target_time2 = datetime.now() + timedelta(seconds=-5)
notify1 = Notificator('First notification', target_time1)
notify2 = Notificator('Second notification', target_time2)


asyncio.get_event_loop().run_until_complete(notify1.checking_exchange())
asyncio.get_event_loop().run_until_complete(notify1.price_scheduling())
asyncio.get_event_loop().run_until_complete(notify1.work_is_done())

asyncio.get_event_loop().run_until_complete(notify2.checking_exchange())
asyncio.get_event_loop().run_until_complete(notify2.price_scheduling())
asyncio.get_event_loop().run_until_complete(notify2.work_is_done())
