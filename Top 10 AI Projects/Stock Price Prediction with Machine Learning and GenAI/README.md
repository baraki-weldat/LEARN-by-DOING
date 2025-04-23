# Advanced Stock Prediction with GenAI, Monte Carlo, AutoML, and Alert System

## Overview
Predict stock prices with a hybrid AI system combining:
- Machine Learning
- Generative Adversarial Networks (TimeGAN)
- Sentiment Analysis (Transformer models)
- Monte Carlo simulations
- Real-time email alerts for significant price movements.

## Features
- AutoML model selection (AutoKeras)
- Generative AI for future price paths
- News-based sentiment integration
- Monte Carlo risk simulation
- Real-time prediction dashboard (Streamlit)
- Email alerts on threshold crossing

## Technologies
- Python
- TensorFlow / AutoKeras
- Streamlit
- yFinance / NewsAPI
- SMTP Email System

## Setup
```bash
pip install -r requirements.txt
streamlit run app/app.py
