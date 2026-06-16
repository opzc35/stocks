// Python engine process management

use std::process::{Child, Command};
use std::sync::Mutex;
use std::time::Duration;
use anyhow::{Result, Context};

pub struct PythonEngine {
    process: Mutex<Option<Child>>,
    base_url: String,
}

impl PythonEngine {
    pub fn new() -> Self {
        Self {
            process: Mutex::new(None),
            base_url: "http://127.0.0.1:8000".to_string(),
        }
    }

    pub fn start(&self) -> Result<()> {
        let mut process = self.process.lock().unwrap();

        // 如果进程已经在运行，返回
        if let Some(ref mut child) = *process {
            if let Ok(None) = child.try_wait() {
                println!("Python engine is already running");
                return Ok(());
            }
        }

        println!("Starting Python engine...");

        // 获取项目根目录
        let exe_dir = std::env::current_exe()
            .context("Failed to get executable path")?
            .parent()
            .context("Failed to get executable directory")?
            .to_path_buf();

        // 开发模式下，使用项目根目录
        let project_root = if cfg!(debug_assertions) {
            std::env::current_dir().context("Failed to get current directory")?
        } else {
            exe_dir.clone()
        };

        let python_engine_path = project_root.join("python-engine");
        let venv_python = if cfg!(target_os = "windows") {
            python_engine_path.join("venv/Scripts/python.exe")
        } else {
            python_engine_path.join("venv/bin/python")
        };

        // 检查虚拟环境是否存在
        if !venv_python.exists() {
            println!("Virtual environment not found at {:?}", venv_python);
            println!("Trying system python...");

            // 尝试使用系统Python
            let child = Command::new("python3")
                .arg(python_engine_path.join("main.py"))
                .current_dir(&python_engine_path)
                .spawn()
                .context("Failed to start Python engine with system python")?;

            *process = Some(child);
            println!("Python engine started with system python");
        } else {
            // 使用虚拟环境Python
            let child = Command::new(&venv_python)
                .arg("main.py")
                .current_dir(&python_engine_path)
                .spawn()
                .context("Failed to start Python engine")?;

            *process = Some(child);
            println!("Python engine started with venv python");
        }

        // 等待一下让服务启动
        std::thread::sleep(Duration::from_secs(2));

        // 检查进程是否还在运行
        if let Some(ref mut child) = *process {
            match child.try_wait() {
                Ok(Some(status)) => {
                    anyhow::bail!("Python engine exited immediately with status: {}", status);
                }
                Ok(None) => {
                    println!("Python engine is running");
                }
                Err(e) => {
                    anyhow::bail!("Error checking Python engine status: {}", e);
                }
            }
        }

        Ok(())
    }

    pub fn stop(&self) -> Result<()> {
        let mut process = self.process.lock().unwrap();

        if let Some(mut child) = process.take() {
            println!("Stopping Python engine...");
            child.kill().context("Failed to kill Python engine")?;
            child.wait().context("Failed to wait for Python engine")?;
            println!("Python engine stopped");
        }

        Ok(())
    }

    pub fn is_running(&self) -> bool {
        let mut process = self.process.lock().unwrap();

        if let Some(ref mut child) = *process {
            if let Ok(None) = child.try_wait() {
                return true;
            }
        }

        false
    }

    pub async fn health_check(&self) -> Result<bool> {
        // 检查Python API是否响应
        let client = reqwest::Client::new();
        match client
            .get(format!("{}/health", self.base_url))
            .timeout(Duration::from_secs(2))
            .send()
            .await
        {
            Ok(response) => Ok(response.status().is_success()),
            Err(_) => Ok(false),
        }
    }

    pub fn get_base_url(&self) -> &str {
        &self.base_url
    }
}

impl Drop for PythonEngine {
    fn drop(&mut self) {
        let _ = self.stop();
    }
}
