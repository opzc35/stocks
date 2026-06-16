use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct BacktestRequest {
    pub strategy_code: String,
    pub symbol: String,
    pub timeframe: String,
    pub start_date: String,
    pub end_date: String,
    pub initial_capital: f64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct BacktestResult {
    pub total_return: f64,
    pub sharpe_ratio: f64,
    pub max_drawdown: f64,
    pub total_trades: u32,
    pub win_rate: f64,
}

#[tauri::command]
pub async fn run_backtest(request: BacktestRequest) -> Result<BacktestResult, String> {
    let client = reqwest::Client::new();
    let response = client
        .post("http://localhost:8000/api/backtest/run")
        .json(&request)
        .send()
        .await
        .map_err(|e| e.to_string())?;

    response
        .json::<BacktestResult>()
        .await
        .map_err(|e| e.to_string())
}
