from mesa import Model
from mesa import Agent
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation
from random import randrange
from decimal import Decimal
from mesa.batchrunner import BatchRunner
from datetime import datetime

from agent import TreeCell


class ForestFire(Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, width=100, height=100, density=0.65, humidity=0.5):
        """
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(width, height, torus=False)

        self.datacollector = DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
                "low": lambda m: self.count_type(m, "low"),
                "high": lambda m: self.count_type(m, "high")
            }
        )

        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                if self.random.random() < humidity: 
                    new_tree.humidity = "high"
                    new_tree.catchesFire = 0.35
                    if self.random.random() < new_tree.catchesFire:
                        new_tree.pirofita = True
                # Set all trees in the first column on fire.
                if x == 0:
                    new_tree.condition = "On Fire"
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
            if tree.humidity == tree_condition:
                count += 1
        return count

def low(model):
    count = 0
    for tree in model.schedule.agents:
            if tree.humidity == "low":
                count += 1
    return count

def high(model):
    count = 0
    for tree in model.schedule.agents:
        if tree.humidity == "high":
            count += 1
    return count

def onFire(model):
    count = 0
    for tree in model.schedule.agents:
        if tree.condition == "On Fire":
            count += 1
    return count

def fine(model):
    count = 0
    for tree in model.schedule.agents:
        if tree.condition == "Fine":
            count += 1
    return count

def burned(model):
    count = 0
    for tree in model.schedule.agents:
        if tree.condition == "Burned Out":
            count += 1
    return count

def batch_run():
    fix_params={
        "width":100,
        "height":100,
    }
    variable_params={
        "density": [0.25, 0.5, 0.75],
        "humidity": [0.2, 0.3, 0.4]
    }
    batch_run = BatchRunner(
        ForestFire,
        variable_parameters=variable_params,
        fixed_parameters=fix_params,
        iterations=10,
        max_steps=100,
        model_reporters={
            "low": low,
            "high": high,
            "Fine": fine,
            "On Fire": onFire,
            "Burned": burned
        }
    )
    batch_run.run_all()

    run_model_data = batch_run.get_model_vars_dataframe()
    #run_agent_data = batch_run.get_agent_vars_dataframe() 

    now = datetime.now().strftime("%Y-%m-%d")
    file_name_suffix =  ("iter"+str(10)+
                        "steps"+str(100)+"lower_firemans"+now
                        )
    run_model_data.to_csv("model_data"+file_name_suffix+".csv")


batch_run()