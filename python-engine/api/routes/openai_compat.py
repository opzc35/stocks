"""
OpenAI Chat Completions兼容格式支持
将Claude API包装成OpenAI兼容的接口
"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import time
from core.ai.analyzer import get_analyzer

router = APIRouter()


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "claude-opus-4-8"
    messages: List[ChatMessage]
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = 2000
    stream: Optional[bool] = False


class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: str


class ChatCompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: ChatCompletionUsage


@router.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest):
    """
    OpenAI兼容的Chat Completions API

    将请求转换为Claude API调用
    """
    analyzer = get_analyzer()

    if not analyzer.available:
        raise HTTPException(
            status_code=503,
            detail="Claude API not configured. Set ANTHROPIC_API_KEY environment variable."
        )

    try:
        # 提取最后一条用户消息
        user_messages = [m for m in request.messages if m.role == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="No user message found")

        last_user_message = user_messages[-1].content

        # 调用Claude API
        message = analyzer.client.messages.create(
            model="claude-opus-4-8",
            max_tokens=request.max_tokens or 2000,
            messages=[
                {
                    "role": "user",
                    "content": last_user_message
                }
            ]
        )

        response_text = message.content[0].text

        # 构建OpenAI兼容响应
        response = ChatCompletionResponse(
            id=f"chatcmpl-{int(time.time())}",
            created=int(time.time()),
            model=request.model,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=ChatMessage(
                        role="assistant",
                        content=response_text
                    ),
                    finish_reason="stop"
                )
            ],
            usage=ChatCompletionUsage(
                prompt_tokens=len(last_user_message) // 4,  # 粗略估算
                completion_tokens=len(response_text) // 4,
                total_tokens=(len(last_user_message) + len(response_text)) // 4
            )
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/v1/models")
async def list_models():
    """列出可用的模型（OpenAI兼容格式）"""
    return {
        "object": "list",
        "data": [
            {
                "id": "claude-opus-4-8",
                "object": "model",
                "created": 1677610602,
                "owned_by": "anthropic"
            },
            {
                "id": "claude-sonnet-4-6",
                "object": "model",
                "created": 1677610602,
                "owned_by": "anthropic"
            }
        ]
    }


@router.post("/v1/embeddings")
async def create_embeddings():
    """占位符：嵌入API（暂不支持）"""
    raise HTTPException(
        status_code=501,
        detail="Embeddings API not implemented. Use Claude API directly for text analysis."
    )
