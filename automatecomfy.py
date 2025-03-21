import json
import requests
import os
import time
from datetime import datetime
import uuid
import websocket
from urllib import request, error
import random

'''This class is there to automate comfyui, the standart API Request are fairly simple, but there is a boilerplate observer Patter implemented to extend functionality for future use.'''

class Task:
    def __init__(self, name, timer):
        self.name = name
        self.timer = timer
        self.internalstate = "pending"
    
    def runtask(self):
        self.updateclock()
        self.internalstate = "running"
        self.timer.status()
        time.sleep(5)
        self.internalstate = "done"
        print(f"✅ {self.name} runned")
        self.updateclock()
        self.timer.status()
  
    def updateclock(self):
        self.timer.updatetimer()
        self.timer.updateglobaltimer()
    
    def update(self, message):
        print(f'{self.name} got message "{message}"')
        return self.internalstate, self.name
    

class TimerChecker:
    def __init__(self):
        self.name = "timer"
        self.time = time.time()
        self.globaltime = time.time()
        
    def updatetimer(self):
        self.time = time.time()
    
    def updateglobaltimer(self):
        self.globaltime = self.time
  
    def status(self):
        print('got a message', self.name, self.format_time(self.time), "-> globaltime:", self.format_time(self.globaltime))
       
    def format_time(self, timestamp):
        """Convert Unix timestamp into a human-readable format."""
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


class Publisher:
    def __init__(self, events):
        # Maps event names to subscribers (each event has its own dict of subscribers)
        self.events = { event: dict() for event in events }
    
    def get_subscribers(self, event):
        return self.events[event]
    
    def register(self, event, who, callback=None):
        if callback is None:
            callback = getattr(who, 'update')
        self.get_subscribers(event)[who] = callback
    
    def unregister(self, event, who):
        del self.get_subscribers(event)[who]
    
    def dispatch(self, event, message):
        for subscriber, callback in self.get_subscribers(event).items():
            print(callback(message))
            
def readworkflow(filepath):
    # Read the JSON workflow from file
    with open(filepath, 'r') as f:
        workflow = json.load(f)
        rand=random.randint(3, 1009)
        try:
                # Hole den aktuellen noise_seed aus den widgets_values (Index 0)
                node_25 = next((node for node in workflow.get("nodes", []) if node.get("id") == 25), None)
                if node_25:
                    print(node_25["widgets_values"][0])
                    node_25["widgets_values"][0]=49543990584005-rand
                else:
                    print("Kein Node mit der ID 25 gefunden.")
        except Exception as e:
                print(f"Fehler beim Anpassen des Noise-Seeds: {e}")
                return None
        
       
    # Wrap the workflow data in a dictionary with key "prompt"
    payload = {"prompt": workflow}
    
    # Encode the payload to UTF-8
    encoded_data = json.dumps(payload).encode('utf-8')
 
    return encoded_data


def runprompt(encoded_json):
    # Create the request with a proper header
    req = request.Request(
        "http://127.0.0.1:8188/prompt", 
        data=encoded_json,
        headers={'Content-Type': 'application/json'}
    )
    try:
        response = request.urlopen(req)
        print("Prompt queued successfully!")
    except error.HTTPError as e:
        print(f"HTTPError: {e.code} {e.reason}")
        print(e.read().decode())
    except error.URLError as e:
        print("URLError:", e.reason)

    
  
  

if __name__ == '__main__':
    # Create a TimerChecker instance and two Task instances with names.
    '''
    timer = TimerChecker()
    task_instance = Task("Task A", timer)
    task_instance2 = Task("Task B", timer)
    
    # Create a Publisher with some test events.
    pub = Publisher(['test1', 'test2'])
    
    # Register both tasks as subscribers to event "test1".
    pub.register("test1", task_instance)
    pub.register("test1", task_instance2)
    
    # Run task_instance2.
    task_instance2.runtask()
    if task_instance2.internalstate == "done":
        pub.dispatch("test1", "whatsup?")
  
    '''
    j=0
    workflows=[ r"path",]
    for i in range(2):
        for j in range(1):
            data = readworkflow( workflows[1])
            runprompt(data)
            j+=1
        i+=1