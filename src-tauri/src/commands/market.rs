use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Ticker {
    pub symbol: String,
    pub price: f64,
    pub volume: f64,
    pub timestamp: i64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct OHLCV {
    pub timestamp: i64,
    pub open: f64,
    pub high: f64,
    pub low: f64,
    pub close: f64,
    pub volume: f64,
}

#[tauri::command]
pub async fn get_ticker(symbol: String) -> Result<Ticker, String> {
    // Call Python engine API
    let client = reqwest::Client::new();
    let response = client
        .get(format!("http://localhost:8000/api/market/ticker?symbol={}", symbol))
        .send()
        .await
        .map_err(|e| e.to_string())?;

    response
        .json::<Ticker>()
        .await
        .map_err(|e| e.to_string())
}

#[tauri::command]
pub async fn get_ohlcv(
    symbol: String,
    timeframe: String,
    limit: Option<u32>,
) -> Result<Vec<OHLCV>, String> {
    let client = reqwest::Client::new();
    let url = format!(
        "http://localhost:8000/api/market/ohlcv?symbol={}&timeframe={}&limit={}",
        symbol,
        timeframe,
        limit.unwrap_or(100)
    );

    let response = client
        .get(&url)
        .send()
        .await
        .map_err(|e| e.to_string())?;

    response
        .json::<Vec<OHLCV>>()
        .await
        .map_err(|e| e.to_string())
}
