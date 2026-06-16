use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct AnalysisRequest {
    pub symbol: String,
    pub timeframe: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AnalysisResult {
    pub analysis: String,
}

#[tauri::command]
pub async fn analyze_market(request: AnalysisRequest) -> Result<AnalysisResult, String> {
    let client = reqwest::Client::new();
    let response = client
        .post("http://localhost:8000/api/ai/analyze")
        .json(&request)
        .send()
        .await
        .map_err(|e| e.to_string())?;

    response
        .json::<AnalysisResult>()
        .await
        .map_err(|e| e.to_string())
}
