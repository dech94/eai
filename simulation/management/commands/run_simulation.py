from django.core.management.base import BaseCommand
from simulation.services import run_simulation_step
import time

class Command(BaseCommand):
    help = 'Run the hospital simulation loop'

    def add_arguments(self, parser):
        parser.add_argument('--interval', type=int, default=10, help='Interval in seconds between simulation steps')

    def handle(self, *args, **kwargs):
        interval = kwargs['interval']
        self.stdout.write(f"Starting simulation with interval {interval}s...")
        
        try:
            while True:
                run_simulation_step()
                time.sleep(interval)
        except KeyboardInterrupt:
            self.stdout.write("Simulation stopped.")
