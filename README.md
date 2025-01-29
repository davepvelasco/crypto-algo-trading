# crypto-algo-trading

A web application for testing algorithmic trading strategies in the cryptocurrency market. The application enables traders to visualize market data and backtest strategies.
![Screenshot from 2025-01-29 18-12-16](https://github.com/user-attachments/assets/741f6614-edad-4515-97eb-79d174cf632e)

## Features

- 📈 **Live Crypto Data**: Fetch and display real-time cryptocurrency price data from Coingecko.
- 🏛 **Backtesting Framework**: Evaluate trading strategies using historical data.
- 🎯 **Strategy Implementation**: Create and test custom algorithmic strategies.
- ⚡ **Streamlit UI**: Interactive and user-friendly dashboard for analysis and execution.
- 📊 **Performance Metrics**: Track and analyze strategy performance.
- 🔧 **Configurable Parameters**: Customize settings, indicators, and risk management.

## Built With

[![Python][Python.org]][Python-url] [![Streamlit][Streamlit.io]][Streamlit-url] [![Pandas][Pandas.pydata.org]][Pandas-url] [![Docker][Docker.com]][Docker-url]

## Installation

**Clone the Repository**  
   ```bash
   git clone https://github.com/davepvelasco/crypto-algo-trading.git
   cd crypto-algo-trading
   ```

### Standard Installation

**Create a Virtual Environment (Recommended)**
```bash
# On macOS/Linux
source venv/bin/activate  
# On Windows (Command Prompt)
venv\Scripts\activate
# On Windows (PowerShell)
venv\Scripts\Activate.ps1
```

**Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

### Via Docker Compose
```bash
docker-compose up -d
```

## Usage

### Starting the Server
If you installed via Docker Compose, you don't need to run this command manually.

**Standard Installation**
   ```bash
   streamlit run app.py
   ```

**Access the Web Interface**  
   Open your browser and go to:  
   ```
   http://localhost:8501/
   ```

## Contributing

We welcome contributions! To contribute:

1. **Fork** the repository.
2. **Create a branch** (`feature-new-strategy`).
3. **Commit your changes**.
4. **Push to the branch**.
5. **Submit a Pull Request**.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Todos
- [ ] Add more data sources from other platforms
- [ ] More comprehensive metrics (PnL, Sharpe Ratio, Maximum Drawdown, Winrate, etc.)
- [ ] More trading strategies (ex. LSTM)
- [ ] Live trading

[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Streamlit.io]: https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white
[Streamlit-url]: https://streamlit.io/
[Pandas.pydata.org]: https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org/
[Docker.com]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
