// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod commands;
mod services;

use commands::{market, strategy, ai};
use services::python_bridge::PythonEngine;
use tauri::Manager;

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            // 创建Python引擎实例
            let python_engine = PythonEngine::new();

            // 启动Python引擎
            match python_engine.start() {
                Ok(_) => println!("Python engine started successfully"),
                Err(e) => eprintln!("Failed to start Python engine: {}", e),
            }

            // 将Python引擎存储到app state中
            app.manage(python_engine);

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            market::get_ticker,
            market::get_ohlcv,
            strategy::run_backtest,
            ai::analyze_market,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
