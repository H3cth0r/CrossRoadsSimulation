import mesa as ms
from Models import *
from Agents import *
import pandas as pd
import matplotlib.pyplot as plt


params = {"nCars"   :   range(2, 4) }

results = ms.batch_run(
    RoomModel,
    parameters=params,
    iterations=10,
    max_steps=100,
    number_processes=1,
    data_collection_period=1,
    display_progress=True
)


results_df = pd.DataFrame(results)
print(results_df.keys())
results_df