import math
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np


class Queue:
    def __init__(self, n, m, l, mu, p=1, dt=0.05, n_events=10000, n_total=10000):
        self.n = n
        self.m = m
        self.l = l
        self.mu = mu
        self.p = p
        self.delta_t = dt
        self.n_events = n_events
        self.n_total = n_total

        self.ro = self.l / self.mu
        self.p = [1 / (sum([self.ro ** i / math.factorial(i) for i in range(self.n)]) +
                           sum([self.ro ** (n + i) / (self.n ** i * math.factorial(self.n)) for i in range(1, self.m)]))]
        self.event_time = n_events * self.delta_t
        self.channels = [{'is_taken': False, 'time': None}] * self.n
        self.next_event_time = np.random.exponential(self.l)
        self.queue = 0
        self.state_shots = []

        self._default_chanel = {'is_taken': False, 'time': None}

    def is_request(self, time):
        if self.next_event_time <= time <= self.event_time:
            self.next_event_time += np.random.exponential(self.l)
            return True
        return False

    def run(self):
        for i in range(self.n_total):
            time = round(self.delta_t * i, 6)
            for j in range(len(self.channels)):
                if self.channels[j]['is_taken'] == 1 and time - self.channels[j]['time'] >= 1 / self.mu:
                    self.channels[j] = self._default_chanel
                    print(f'Time {time}. Channel №{j} is done.')
            empty_channels = len([channel for channel in self.channels if channel['is_taken'] is False])
            index = 0
            while index < len(self.channels) and self.queue > 0 and empty_channels > 0:
                if not self.channels[index]['is_taken']:
                    self.channels[index] = {'is_taken': True, 'time': time}
                    print(f'Time {time}. Request goes to Channel №{index} from queue №{self.m - self.queue} until {time + self.mu}.')
                    self.queue -= 1
                    empty_channels -= 1
                index += 1

            is_accepted = False
            is_declined = False
            is_request = self.is_request(time)
            if is_request:
                if empty_channels > 0:
                    free_channel = self.get_free_channel_index()
                    self.channels[free_channel] = {'is_taken': True, 'time': time}
                    print(f'Time {time}. Request goes to Channel №{free_channel} until {time + self.mu}.')
                    empty_channels -= 1
                    is_accepted = True
                elif self.m - self.queue > 0:
                    self.queue += 1
                    print(f'Time {time}. Request goes to queue №{self.queue}.')
                    is_accepted = True
                else:
                    print(f'Time {time}. Request declined.')
                    is_declined = False
            queue_list = [1] * self.queue + [0] * (self.m - self.queue)
            states = self.get_states(empty_channels)
            states_shot = [time, is_request, is_accepted, is_declined] + [channel['is_taken'] for channel in self.channels] + queue_list + states
            self.state_shots.append(states_shot)

    def plot(self):
        plt.plot([self.get_state_index(h) - self.n - self.m - 1 - 4 for h in self.state_shots], 'ro', markersize=0.5, color='green')
        plt.yticks(list(range(self.m + self.n + 1)))
        plt.show()

    def get_state_index(self, shot):
        for i in range(4 + self.n + self.m ,len(shot)):
            if shot[i] == 1:
                return i - 4 + self.n + self.m


    def get_states(self, empty_channels):
        states = []
        for i in range(self.n + self.m + 1):
            if i == self.n + self.queue - empty_channels:
                states.append(1)
            else:
                states.append(0)
        return states

    def get_free_channel_index(self):
        for i in range(len(self.channels)):
            if not self.channels[i]['is_taken']:
                return i

    def get_probabilities_emp(self):
        counter = defaultdict(lambda: 0)
        for state_shot in self.state_shots:
            for i in range(self.n + self.m + 1):
                if state_shot[4 + self.n + self.m + i] == 1:
                    counter[i] += 1
        p = []
        for state, count in counter.items():
            p.append(count / self.n_total)
        return list(map(str, p))

    def get_probabilities_theo(self):
        for i in range(1, self.n + 1):
            self.p.append(self.p[0] * (self.ro ** i) / math.factorial(i))
        for i in range(1, self.m + 1):
            self.p.append(self.p[0] * self.ro ** (self.n + i) / (self.n ** i * math.factorial(self.n)))
        return list(map(str, self.p))

    def get_decline_probability_emp(self):
        count = sum([state_shot[3] for state_shot in self.state_shots])
        p = count / sum([state_shot[1] for state_shot in self.state_shots])
        return p

    def get_decline_probability_theo(self):
        p = self.p[0] * self.ro ** (self.n + self.m) / (self.n ** self.m * math.factorial(self.n))
        return p

    def get_relative_throughput_emp(self):
        requests_count = sum(shot[1] for shot in self.state_shots)
        accepted_count = sum(shot[2] for shot in self.state_shots)
        return accepted_count / requests_count

    def get_relative_throughput_theo(self):
        return 1 - self.get_decline_probability_theo()

    def get_absolute_throughput_emp(self):
        return self.l * self.get_relative_throughput_emp()

    def get_absolute_throughput_theo(self):
        return self.get_relative_throughput_theo() * self.l

    def get_channel_request_avg_emp(self):
        p = np.mean([sum(state_shot[4: 4 + self.n]) for state_shot in self.state_shots])
        return p

    def get_channel_request_avg_theo(self):
        p = self.get_absolute_throughput_theo() / self.mu
        return p

    def get_queue_request_avg_emp(self):
        p = np.mean([sum(state_shot[4 + self.n: 4 + self.n + self.m]) for state_shot in self.state_shots])
        return p

    def get_queue_request_avg_theo(self):
        p = self.p[0] * self.ro ** (self.n + 1) * (1 - (self.ro / self.n) ** self.m * (1 + self.m * (1 - self.ro /
              self.n))) / ((1 - self.ro / self.n) ** 2 * self.n * math.factorial(self.n))
        return p

    def get_smo_request_avg_emp(self):
        return self.get_channel_request_avg_emp() + self.get_queue_request_avg_emp()

    def get_smo_request_avg_theo(self):
        return self.get_channel_request_avg_theo() + self.get_queue_request_avg_theo()

    def get_avg_time_smo_emp(self):
        return self.get_smo_request_avg_emp() / self.l

    def get_avg_time_smo_theo(self):
        return self.get_smo_request_avg_theo() / self.l

    def get_avg_time_queue_emp(self):
        return self.get_queue_request_avg_emp() / self.l

    def get_avg_time_queue_theo(self):
        return self.get_queue_request_avg_theo() / self.l


if __name__ == '__main__':
    q = Queue(3, 3, 1, 1, 1)
    q.run()
    q.plot()
    print('=' * 20 + 'Stats' + '=' * 20)

    print(f'Empirical probabilities: {", ".join(q.get_probabilities_emp())}')
    print(f'Theoretical probabilities: {", ".join(q.get_probabilities_theo())}')
    print()
    print(f'Empirical decline probability: {q.get_decline_probability_emp()}')
    print(f'Theoretical decline probability: {q.get_decline_probability_theo()}')
    print()
    print(f'Empirical channel request avg: {q.get_channel_request_avg_emp()}')
    print(f'Theoretical channel request avg: {q.get_channel_request_avg_theo()}')
    print()
    print(f'Empirical relative throughput: {q.get_relative_throughput_emp()}')
    print(f'Theoretical relative throughput: {q.get_relative_throughput_theo()}')
    print()
    print(f'Empirical absolute throughput: {q.get_absolute_throughput_emp()}')
    print(f'Theoretical absolute throughput: {q.get_absolute_throughput_theo()}')
    print()
    print(f'Empirical channel request avg: {q.get_channel_request_avg_emp()}')
    print(f'Theoretical channel request avg: {q.get_channel_request_avg_theo()}')
    print()
    print(f'Empirical queue request avg: {q.get_queue_request_avg_emp()}')
    print(f'Theoretical queue request avg: {q.get_queue_request_avg_theo()}')
    print()
    print(f'Empirical smo request avg: {q.get_smo_request_avg_emp()}')
    print(f'Theoretical smo request avg: {q.get_smo_request_avg_theo()}')
    print()
    print(f'Empirical avg time smo: {q.get_avg_time_smo_emp()}')
    print(f'Theoretical avg time smo: {q.get_avg_time_smo_theo()}')
    print()
    print(f'Empirical avg time queue: {q.get_avg_time_queue_emp()}')
    print(f'Theoretical avg time queue: {q.get_avg_time_queue_theo()}')

