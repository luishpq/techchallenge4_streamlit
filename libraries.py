#Importar library
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

import streamlit as st

#PACF e ACF
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf


#Teste de estacionaridade
from statsmodels.tsa.stattools import adfuller
from pmdarima.arima.utils import ndiffs

#Decompose
from statsmodels.tsa.seasonal import seasonal_decompose

#Modelos
from statsforecast import StatsForecast
from statsforecast.models import Naive
from statsforecast.models import AutoARIMA
from statsforecast.models import ARIMA

from statsforecast.models import SeasonalWindowAverage
from statsforecast.models import HistoricAverage
from statsforecast.models import SimpleExponentialSmoothingOptimized


#Validação
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error, r2_score

#Outros
from statsmodels.tsa.seasonal import STL

#Outros
from PIL import Image